"""Provides functions to create adaptive learners for a pipeline."""

from __future__ import annotations

import functools
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Tuple, Union

import adaptive

from pipefunc._utils import at_least_tuple, prod
from pipefunc.map._mapspec import MapSpec
from pipefunc.map._run import (
    RunInfo,
    _execute_single,
    _func_kwargs,
    _maybe_load_single_output,
    _MockPipeline,
    _run_iteration_and_process,
    run,
)

if TYPE_CHECKING:
    import sys

    from pipefunc import PipeFunc, Pipeline, Sweep
    from pipefunc.map._storage_base import StorageBase

    if sys.version_info < (3, 10):  # pragma: no cover
        from typing_extensions import TypeAlias
    else:
        from typing import TypeAlias


_OUTPUT_TYPE: TypeAlias = Union[str, Tuple[str, ...]]


def create_learners(
    pipeline: Pipeline,
    inputs: dict[str, Any],
    run_folder: str | Path,
    internal_shapes: dict[str, int | tuple[int, ...]] | None = None,
    *,
    storage: str = "file_array",
    return_output: bool = False,
    cleanup: bool = True,
) -> list[dict[_OUTPUT_TYPE, adaptive.SequenceLearner]]:
    """Create adaptive learners for a single `Pipeline.map` call.

    Creates a learner for each function node in the graph. Which means that
    the returned lists of learners have to be executed in order.
    If a single list contains multiple learners, they can be executed in
    parallel.

    Parameters
    ----------
    pipeline
        The pipeline to create learners for.
    inputs
        The inputs to the pipeline, the same as passed to `pipeline.map`.
    run_folder
        The folder to store the run information.
    internal_shapes
        The internal shapes to use for the run.
    storage
        The storage class to use for the file arrays. The default is `file_array`.
        Can use any registered storage class. See `pipefunc.map.storage_registry`.
    return_output
        Whether to return the output of the function in the learner.
    cleanup
        Whether to clean up the `run_folder`.

    Returns
    -------
    A list of dictionaries where the keys are the output names of the
    functions and the values are the corresponding adaptive learners. As noted
    above, the learners have to be executed in order.

    """
    run_folder = Path(run_folder)
    run_info = RunInfo.create(
        run_folder,
        pipeline,
        inputs,
        internal_shapes,
        storage=storage,
        cleanup=cleanup,
    )
    run_info.dump(run_folder)
    store = run_info.init_store()
    learners = []
    for gen in pipeline.topological_generations[1]:
        _learners = {}
        for func in gen:
            if func.mapspec and func.mapspec.inputs:
                f = functools.partial(
                    _execute_iteration_in_map_spec,
                    func=func,
                    run_info=run_info,
                    run_folder=run_folder,
                    store=store,
                    return_output=return_output,
                )
                sequence = list(range(prod(run_info.shapes[func.output_name])))
            else:
                f = functools.partial(
                    _execute_iteration_in_single,
                    func=func,
                    run_info=run_info,
                    run_folder=run_folder,
                    store=store,
                    return_output=return_output,
                )
                sequence = [None]  # type: ignore[list-item]
            learner = adaptive.SequenceLearner(f, sequence)
            _learners[func.output_name] = learner
        learners.append(_learners)
    return learners


def flatten_learners(
    learners_dicts: list[dict[_OUTPUT_TYPE, adaptive.SequenceLearner]],
) -> dict[_OUTPUT_TYPE, adaptive.SequenceLearner]:
    """Flatten the list of dictionaries of learners into a single dictionary."""
    return {k: v for learner_dict in learners_dicts for k, v in learner_dict.items()}


def _execute_iteration_in_single(
    _: Any,
    func: PipeFunc,
    run_info: RunInfo,
    run_folder: Path,
    store: dict[str, StorageBase],
    *,
    return_output: bool = False,
) -> Any | None:
    """Execute a single iteration of a single function.

    Meets the requirements of `adaptive.SequenceLearner`.
    """
    output, exists = _maybe_load_single_output(func, run_folder, return_output=return_output)
    if exists:
        return output
    kwargs = _func_kwargs(
        func,
        run_info.input_paths,
        run_info.shapes,
        run_info.shape_masks,
        store,
        run_folder,
    )
    result = _execute_single(func, kwargs, run_folder)
    return result if return_output else None


def _execute_iteration_in_map_spec(
    index: int,
    func: PipeFunc,
    run_info: RunInfo,
    run_folder: Path,
    store: dict[str, StorageBase],
    *,
    return_output: bool = False,
) -> list[Any] | None:
    """Execute a single iteration of a map spec.

    Performs a single iteration of the code in `_execute_map_spec`, however,
    it does not keep and return the output. This is meant to be used in the
    parallel execution of the map spec.

    Meets the requirements of `adaptive.SequenceLearner`.
    """
    shape = run_info.shapes[func.output_name]
    mask = run_info.shape_masks[func.output_name]
    file_arrays = [store[o] for o in at_least_tuple(func.output_name)]
    # Load the data if it exists
    if all(arr.has_index(index) for arr in file_arrays):
        if not return_output:
            return None
        return [arr.get_from_index(index) for arr in file_arrays]
    # Otherwise, run the function
    assert isinstance(func.mapspec, MapSpec)
    kwargs = _func_kwargs(
        func,
        run_info.input_paths,
        run_info.shapes,
        run_info.shape_masks,
        store,
        run_folder,
    )
    outputs = _run_iteration_and_process(index, func, kwargs, shape, mask, file_arrays)
    return outputs if return_output else None


@dataclass
class _MapWrapper:
    """Wraps the `pipefunc.map.run` function and makes it a callable with a single unused argument.

    Uses a `_MockPipeline` that contains all the required information to run the pipeline but is
    cheaper to serialize and pass around.
    """

    mock_pipeline: _MockPipeline
    inputs: dict[str, Any]
    run_folder: Path
    internal_shapes: dict[str, int | tuple[int, ...]] | None
    parallel: bool
    cleanup: bool

    def __call__(self, _: Any) -> None:
        """Run the pipeline."""
        run(
            self.mock_pipeline,  # type: ignore[arg-type]
            self.inputs,
            self.run_folder,
            self.internal_shapes,
            parallel=self.parallel,
            cleanup=self.cleanup,
        )


def create_learners_from_sweep(
    pipeline: Pipeline,
    sweep: Sweep,
    run_folder: str | Path,
    internal_shapes: dict[str, int | tuple[int, ...]] | None = None,
    *,
    parallel: bool = True,
    cleanup: bool = True,
) -> tuple[list[adaptive.SequenceLearner], list[Path]]:
    """Create adaptive learners for a sweep.

    Creates an `adaptive.SequenceLearner` for each sweep run. These learners
    have a single iteration that executes the map in parallel. This means
    that here we rely on the internal parallelization of the pipeline. Each
    learner is fully independent of the others, and they can be executed in
    parallel.

    Note that this only parallelizes the nodes with a `MapSpec`, the rest of
    the nodes are executed in order. Only use this if the sequential execution
    of the nodes is not a bottleneck.

    Parameters
    ----------
    pipeline
        The pipeline to create learners for.
    sweep
        The sweep to create learners for, must generate `input` dictionaries as
        expected by `pipeline.map`.
    run_folder
        The folder to store the run information. Each sweep run will be stored in
        a subfolder of this folder.
    internal_shapes
        The internal shapes to use for the run, as expected by `pipeline.map`.
    parallel
        Whether to run the map in parallel.
    cleanup
        Whether to clean up the `run_folder`.

    Returns
    -------
    A tuple of lists where the first list contains the learners and the second
    list contains the run folders for each sweep run.

    """
    run_folder = Path(run_folder)
    learners = []
    folders = []
    max_digits = len(str(len(sweep) - 1))
    for i, inputs in enumerate(sweep):
        sweep_run = run_folder / f"sweep_{str(i).zfill(max_digits)}"
        mock_pipeline = _MockPipeline.from_pipeline(pipeline)
        f = _MapWrapper(mock_pipeline, inputs, sweep_run, internal_shapes, parallel, cleanup)
        learner = adaptive.SequenceLearner(f, sequence=[None])
        learners.append(learner)
        folders.append(sweep_run)
    return learners, folders
