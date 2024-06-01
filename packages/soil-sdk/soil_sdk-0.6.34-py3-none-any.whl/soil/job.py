"""Job module"""

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import TypedDict, cast, overload

from soil import data, errors
from soil.api import create_experiment, get_experiment, get_state, set_state
from soil.data_structure import DataStructure
from soil.data_structure import DataStructure as InternalDataStructure
from soil.types import ExperimentStatuses as Statuses
from soil.types import Job

_DEFAULT_JOB_COLLECTION = "__default_job_collection"


class _JobDict(TypedDict):
    """Represents a Job."""

    experiment_id: str
    result_id: str
    created_at: str


class _JobGroup(TypedDict):
    """Represents a Job Group."""

    jobs: list[_JobDict]
    id: str
    created_at: str
    updated_at: str
    total_jobs: int | None


class _Collection(TypedDict):
    job_groups: list[_JobGroup]


@dataclass(kw_only=True, slots=True)
class _Job(Job):
    """Represents a Job."""

    experiment_id: str
    result_id: str
    _created_at: str
    _group: str
    _group_created_at: str
    _total_jobs: int | None = None

    @property
    def group(self) -> str:
        """Get the group of the job"""
        return self._group

    @property
    def created_at(self) -> str:
        """Get the created at of the job"""
        return self._created_at

    @property
    def group_created_at(self) -> str:
        """Get the created at of the job group"""
        return self._group_created_at

    @property
    def total_jobs(self) -> int | None:
        """Get the total jobs of the job group"""
        return self._total_jobs

    @property
    def status(self) -> Statuses:
        """Get the status of the job"""
        experiment = get_experiment(self.experiment_id)
        output_key = next(
            output_key
            for (output_key, output_id) in experiment["outputs"].items()
            if output_id == self.result_id
        )
        return experiment["status"][output_key]

    @property
    def data(self) -> DataStructure:  # type:ignore[reportIncompatibleMethodOverride]
        """Get the data of the job"""
        return data(self.result_id)


@overload
def job(
    *,
    group: str | None = None,
    collection: str = _DEFAULT_JOB_COLLECTION,
    total_jobs: int | None = None,
) -> list[Job]:
    ...


@overload
def job(
    data_object: DataStructure,
    *,
    group: str,
    collection: str = _DEFAULT_JOB_COLLECTION,
    total_jobs: int | None = None,
) -> Job:
    ...


def _new_job(
    data_structure: InternalDataStructure,
    group: str,
    collection: str,
    total_jobs: int | None = None,
) -> Job:
    if data_structure.pipeline is None:
        raise ValueError("Pipeline plan is required")
    experiment = create_experiment(data_structure.pipeline.plan)
    state_id = None
    try:
        (state, state_id) = cast(tuple[_Collection, str], get_state(collection))
    except errors.ObjectNotFound:
        state: _Collection = {"job_groups": []}
    now = datetime.now(tz=UTC).isoformat()
    try:
        selected_group = next(
            (
                job_group
                for job_group in state["job_groups"]
                if job_group["id"] == group
            ),
        )
        if (total_jobs is not None) & (selected_group.get("total_jobs") is None):
            selected_group["total_jobs"] = total_jobs
    except StopIteration:
        selected_group: _JobGroup = {
            "jobs": [],
            "id": group,
            "created_at": now,
            "updated_at": now,
            "total_jobs": total_jobs,
        }
        state["job_groups"].append(selected_group)
    if data_structure.sym_id is None:
        raise ValueError("sym_id is required")
    selected_group["jobs"].append(
        {
            "experiment_id": experiment["_id"],
            "result_id": experiment["outputs"][data_structure.sym_id],
            "created_at": now,
        }
    )
    selected_group["updated_at"] = now
    set_state(collection, state, state_id=state_id)
    if data_structure.sym_id is None:
        raise ValueError("sym_id is required")
    return _Job(
        experiment_id=experiment["_id"],
        result_id=experiment["outputs"][data_structure.sym_id],
        _created_at=datetime.fromtimestamp(
            experiment["created_at"] / 1000, tz=UTC
        ).isoformat(),
        _group=group,
        _group_created_at=selected_group["created_at"],
        _total_jobs=total_jobs,
    )


def job(
    data_object: DataStructure | None = None,
    *,
    group: str | None = None,
    collection: str = _DEFAULT_JOB_COLLECTION,
    total_jobs: int | None = None,
) -> Job | list[Job] | list[list[Job]]:
    """Creates a non-blocking job at soil."""
    if data_object is not None:
        if group is None:
            raise ValueError("Group is required when creating a job with a data object")
        new_job = _new_job(
            data_object, group=group, collection=collection, total_jobs=total_jobs
        )
        return new_job
    try:
        state, _ = cast(tuple[_Collection, str], get_state(collection))
    except errors.ObjectNotFound as e:
        raise errors.JobCollectionNotFound(
            f"Job collection {collection} not found."
        ) from e
    if group is not None:
        raw_jobs = next(
            (
                job_group["jobs"]
                for job_group in state["job_groups"]
                if job_group["id"] == group
            ),
            [],
        )
        job_created_at = next(
            job_group["created_at"]
            for job_group in state["job_groups"]
            if job_group["id"] == group
        )
        group_total_jobs = next(
            job_group.get("total_jobs")
            for job_group in state["job_groups"]
            if job_group["id"] == group
        )
        return [
            _Job(
                experiment_id=job["experiment_id"],
                result_id=job["result_id"],
                _created_at=job["created_at"],
                _group=group,
                _group_created_at=job_created_at,
                _total_jobs=group_total_jobs,
            )
            for job in raw_jobs
        ]

    jobs: list[Job] = []
    for job_group in state["job_groups"]:
        for job in job_group["jobs"]:
            jobs.append(
                _Job(
                    experiment_id=job["experiment_id"],
                    result_id=job["result_id"],
                    _created_at=job["created_at"],
                    _group=job_group["id"],
                    _group_created_at=job_group["created_at"],
                    _total_jobs=job_group.get("total_jobs"),
                )
            )
    return jobs
