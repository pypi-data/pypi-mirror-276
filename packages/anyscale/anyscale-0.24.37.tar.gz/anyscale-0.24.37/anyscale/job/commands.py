from typing import Optional, Union

from anyscale._private.sdk import sdk_command
from anyscale.job._private.job_sdk import PrivateJobSDK
from anyscale.job.models import JobConfig, JobState, JobStatus


_JOB_SDK_SINGLETON_KEY = "job_sdk"

_SUBMIT_EXAMPLE = """
import anyscale
from anyscale.job.models import JobConfig

anyscale.job.submit(
    JobConfig(
        name="my-job",
        entrypoint="python main.py",
        working_dir=".",
    ),
)
"""

_SUBMIT_ARG_DOCSTRINGS = {"config": "The config options defining the job."}


@sdk_command(
    _JOB_SDK_SINGLETON_KEY,
    PrivateJobSDK,
    doc_py_example=_SUBMIT_EXAMPLE,
    arg_docstrings=_SUBMIT_ARG_DOCSTRINGS,
)
def submit(config: JobConfig, *, _sdk: PrivateJobSDK) -> str:
    """Submit a job.

    Returns the id of the submitted job.
    """
    return _sdk.submit(config)


_STATUS_EXAMPLE = """
import anyscale
from anyscale.job.models import JobStatus

status: JobStatus = anyscale.job.status(name="my-job")
"""

_STATUS_ARG_DOCSTRINGS = {
    "name": "Name of the job.",
    "job_id": "Unique ID of the job",
    "cloud": "The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the job. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
}


@sdk_command(
    _JOB_SDK_SINGLETON_KEY,
    PrivateJobSDK,
    doc_py_example=_STATUS_EXAMPLE,
    arg_docstrings=_STATUS_ARG_DOCSTRINGS,
)
def status(
    name: Optional[str] = None,
    job_id: Optional[str] = None,
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    *,
    _sdk: PrivateJobSDK
) -> JobStatus:
    """Get the status of a job."""
    return _sdk.status(name=name, job_id=job_id, cloud=cloud, project=project)


_TERMINATE_EXAMPLE = """
import anyscale

anyscale.job.terminate(name="my-job")
"""

_TERMINATE_ARG_DOCSTRINGS = {
    "name": "Name of the job.",
    "job_id": "Unique ID of the job",
    "cloud": "The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the job. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
}


@sdk_command(
    _JOB_SDK_SINGLETON_KEY,
    PrivateJobSDK,
    doc_py_example=_TERMINATE_EXAMPLE,
    arg_docstrings=_TERMINATE_ARG_DOCSTRINGS,
)
def terminate(
    *,
    name: Optional[str] = None,
    job_id: Optional[str] = None,
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    _sdk: PrivateJobSDK
) -> str:
    """Terminate a job.

    This command is asynchronous, so it always returns immediately.

    Returns the id of the terminated job.
    """
    return _sdk.terminate(name=name, job_id=job_id, cloud=cloud, project=project)


_ARCHIVE_EXAMPLE = """
import anyscale

anyscale.job.archive(name="my-job")
"""

_ARCHIVE_ARG_DOCSTRINGS = {
    "name": "Name of the job.",
    "job_id": "Unique ID of the job",
    "cloud": "The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the job . If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
}


@sdk_command(
    _JOB_SDK_SINGLETON_KEY,
    PrivateJobSDK,
    doc_py_example=_ARCHIVE_EXAMPLE,
    arg_docstrings=_ARCHIVE_ARG_DOCSTRINGS,
)
def archive(
    name: Optional[str] = None,
    job_id: Optional[str] = None,
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    *,
    _sdk: PrivateJobSDK
) -> str:
    """Archive a job.

    This command is asynchronous, so it always returns immediately.

    Returns the id of the archived job.
    """
    return _sdk.archive(name=name, job_id=job_id, cloud=cloud, project=project)


_WAIT_EXAMPLE = """\
import anyscale

anyscale.job.wait(name="my-job", timeout_s=180)"""

_WAIT_ARG_DOCSTRINGS = {
    "name": "Name of the job.",
    "job_id": "Unique ID of the job",
    "cloud": "The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the job. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
    "state": "Target state of the job",
    "timeout_s": "Number of seconds to wait before timing out, this timeout will not affect job execution",
}


@sdk_command(
    _JOB_SDK_SINGLETON_KEY,
    PrivateJobSDK,
    doc_py_example=_WAIT_EXAMPLE,
    arg_docstrings=_WAIT_ARG_DOCSTRINGS,
)
def wait(
    *,
    name: Optional[str] = None,
    job_id: Optional[str] = None,
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    state: Union[JobState, str] = JobState.SUCCEEDED,
    timeout_s: float = 1800,
    _sdk: PrivateJobSDK
):
    """"Wait for a job to enter a specific state."""
    _sdk.wait(
        name=name,
        job_id=job_id,
        cloud=cloud,
        project=project,
        state=state,
        timeout_s=timeout_s,
    )


_GET_LOGS_EXAMPLE = """\
import anyscale

anyscale.job.get_logs(name="my-job", run="job-run-name")
"""

_GET_LOGS_ARG_DOCSTRINGS = {
    "name": "Name of the job",
    "job_id": "Unique ID of the job",
    "run": "The name of the run to query. Names can be found in the JobStatus. If not provided, the last job run will be used.",
}


@sdk_command(
    _JOB_SDK_SINGLETON_KEY,
    PrivateJobSDK,
    doc_py_example=_GET_LOGS_EXAMPLE,
    arg_docstrings=_GET_LOGS_ARG_DOCSTRINGS,
)
def get_logs(
    *,
    name: Optional[str] = None,
    job_id: Optional[str] = None,
    run: Optional[str] = None,
    _sdk: PrivateJobSDK
) -> str:
    """"Query the jobs for a job run."""
    return _sdk.get_logs(name=name, job_id=job_id, run=run)
