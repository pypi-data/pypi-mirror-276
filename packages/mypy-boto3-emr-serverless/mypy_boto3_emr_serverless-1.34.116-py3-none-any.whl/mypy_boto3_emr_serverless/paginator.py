"""
Type annotations for emr-serverless service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr_serverless/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_emr_serverless.client import EMRServerlessClient
    from mypy_boto3_emr_serverless.paginator import (
        ListApplicationsPaginator,
        ListJobRunAttemptsPaginator,
        ListJobRunsPaginator,
    )

    session = Session()
    client: EMRServerlessClient = session.client("emr-serverless")

    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    list_job_run_attempts_paginator: ListJobRunAttemptsPaginator = client.get_paginator("list_job_run_attempts")
    list_job_runs_paginator: ListJobRunsPaginator = client.get_paginator("list_job_runs")
    ```
"""

from typing import Generic, Iterator, Sequence, TypeVar

from botocore.paginate import PageIterator, Paginator

from .literals import ApplicationStateType, JobRunModeType, JobRunStateType
from .type_defs import (
    ListApplicationsResponseTypeDef,
    ListJobRunAttemptsResponseTypeDef,
    ListJobRunsResponseTypeDef,
    PaginatorConfigTypeDef,
    TimestampTypeDef,
)

__all__ = ("ListApplicationsPaginator", "ListJobRunAttemptsPaginator", "ListJobRunsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListApplicationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless.html#EMRServerless.Paginator.ListApplications)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr_serverless/paginators/#listapplicationspaginator)
    """

    def paginate(
        self,
        *,
        states: Sequence[ApplicationStateType] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless.html#EMRServerless.Paginator.ListApplications.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr_serverless/paginators/#listapplicationspaginator)
        """


class ListJobRunAttemptsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless.html#EMRServerless.Paginator.ListJobRunAttempts)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr_serverless/paginators/#listjobrunattemptspaginator)
    """

    def paginate(
        self, *, applicationId: str, jobRunId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListJobRunAttemptsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless.html#EMRServerless.Paginator.ListJobRunAttempts.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr_serverless/paginators/#listjobrunattemptspaginator)
        """


class ListJobRunsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless.html#EMRServerless.Paginator.ListJobRuns)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr_serverless/paginators/#listjobrunspaginator)
    """

    def paginate(
        self,
        *,
        applicationId: str,
        createdAtAfter: TimestampTypeDef = ...,
        createdAtBefore: TimestampTypeDef = ...,
        states: Sequence[JobRunStateType] = ...,
        mode: JobRunModeType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListJobRunsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless.html#EMRServerless.Paginator.ListJobRuns.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr_serverless/paginators/#listjobrunspaginator)
        """
