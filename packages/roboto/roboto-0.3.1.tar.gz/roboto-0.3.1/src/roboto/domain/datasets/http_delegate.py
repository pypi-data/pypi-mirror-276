from typing import Any, Optional, Tuple
import urllib.parse

from ...auth import (
    EditAccessRequest,
    GetAccessResponse,
    Permissions,
)
from ...exceptions import (
    RobotoHttpExceptionParse,
    RobotoNotFoundException,
)
from ...http import (
    HttpClient,
    PaginatedList,
    roboto_headers,
)
from ...query import QuerySpecification
from ...serde import pydantic_jsonable_dict
from ...transactions import TransactionRecord
from ...updates import (
    MetadataChangeset,
    UpdateCondition,
)
from ..files import FileRecord
from .delegate import Credentials, DatasetDelegate
from .http_resources import (
    BeginManifestTransactionRequest,
    BeginManifestTransactionResponse,
    BeginSingleFileUploadRequest,
    BeginSingleFileUploadResponse,
    CreateDatasetRequest,
    QueryDatasetFilesRequest,
    ReportTransactionProgressRequest,
    UpdateDatasetRequest,
)
from .record import (
    Administrator,
    DatasetRecord,
    StorageLocation,
)


class DatasetHttpDelegate(DatasetDelegate):
    __http_client: HttpClient
    __roboto_service_base_url: str
    __transaction_manifests: dict[str, set[str]]
    __transaction_completed_unreported_items: dict[str, set[str]]
    __manifest_reporting_increments: int = 10
    __manifest_reporting_min_batch_size: int = 10

    def __init__(self, roboto_service_base_url: str, http_client: HttpClient) -> None:
        super().__init__()
        self.__http_client = http_client
        self.__roboto_service_base_url = roboto_service_base_url
        self.__transaction_manifests = {}
        self.__transaction_completed_unreported_items = {}

    def headers(
        self,
        org_id: Optional[str] = None,
        user_id: Optional[str] = None,
        resource_owner_id: Optional[str] = None,
    ) -> dict[str, str]:
        return roboto_headers(
            org_id=org_id,
            user_id=user_id,
            resource_owner_id=resource_owner_id,
            additional_headers={"Content-Type": "application/json"},
        )

    def create_dataset(
        self,
        administrator: Administrator = Administrator.Roboto,
        metadata: Optional[dict[str, Any]] = None,
        storage_location: StorageLocation = StorageLocation.S3,
        tags: Optional[list[str]] = None,
        org_id: Optional[str] = None,
        created_by: Optional[str] = None,
        description: Optional[str] = None,
    ) -> DatasetRecord:
        """
        Create a new dataset.
        """
        url = f"{self.__roboto_service_base_url}/v1/datasets"
        request_body = CreateDatasetRequest(
            metadata=metadata if metadata is not None else {},
            description=description,
            tags=tags if tags is not None else [],
        )

        with RobotoHttpExceptionParse():
            response = self.__http_client.post(
                url,
                data=pydantic_jsonable_dict(request_body),
                headers=self.headers(org_id, created_by),
            )

        return DatasetRecord.model_validate(response.from_json(json_path=["data"]))

    def delete_dataset(self, record: DatasetRecord) -> None:
        """
        Delete a dataset.
        """
        url = f"{self.__roboto_service_base_url}/v1/datasets/{record.dataset_id}"

        with RobotoHttpExceptionParse():
            self.__http_client.delete(
                url,
                headers=self.headers(),
            )

    def get_dataset_by_id(
        self,
        dataset_id: str,
    ) -> DatasetRecord:
        """
        Get a dataset by its primary key (org_id, dataset_id)
        """
        url = f"{self.__roboto_service_base_url}/v1/datasets/{dataset_id}"

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(url, headers=self.headers())

        return DatasetRecord.model_validate(response.from_json(json_path=["data"]))

    def get_temporary_credentials(
        self,
        record: DatasetRecord,
        permissions: Permissions,
        caller: Optional[str] = None,
        transaction_id: Optional[str] = None,
    ) -> Credentials:
        """
        Get temporary credentials to access a dataset.
        """
        query_params = {"mode": permissions.value}
        encoded_qs = urllib.parse.urlencode(query_params)
        url = f"{self.__roboto_service_base_url}/v1/datasets/{record.dataset_id}/credentials?{encoded_qs}"

        if transaction_id:
            url += f"&transaction_id={transaction_id}"

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(url, self.headers(user_id=caller))

        return Credentials.model_validate(response.from_json(json_path=["data"]))

    def list_files(
        self,
        dataset_id: str,
        page_token: Optional[str] = None,
        include_patterns: Optional[list[str]] = None,
        exclude_patterns: Optional[list[str]] = None,
    ) -> PaginatedList[FileRecord]:
        """
        List files associated with dataset.

        Files are associated with datasets in an eventually-consistent manner,
        so there will likely be delay between a file being uploaded and it appearing in this list.
        """
        url = f"{self.__roboto_service_base_url}/v1/datasets/{dataset_id}/files/query"
        if page_token:
            encoded_qs = urllib.parse.urlencode({"page_token": str(page_token)})
            url = f"{url}?{encoded_qs}"

        request_body = QueryDatasetFilesRequest(
            page_token=page_token,
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns,
        )
        with RobotoHttpExceptionParse():
            response = self.__http_client.post(
                url,
                data=pydantic_jsonable_dict(request_body, exclude_none=True),
                headers=self.headers(),
                idempotent=True,
            )

        unmarshalled = response.from_json(json_path=["data"])
        return PaginatedList(
            items=[FileRecord.model_validate(file) for file in unmarshalled["items"]],
            next_token=unmarshalled["next_token"],
        )

    def query_datasets(
        self,
        query: QuerySpecification,
        org_id: Optional[str] = None,
    ) -> PaginatedList[DatasetRecord]:
        url = f"{self.__roboto_service_base_url}/v1/datasets/query"
        post_body = pydantic_jsonable_dict(query, exclude_none=True)
        with RobotoHttpExceptionParse():
            res = self.__http_client.post(
                url,
                data=post_body,
                headers=self.headers(resource_owner_id=org_id),
                idempotent=True,
            )

        unmarshalled = res.from_json(json_path=["data"])
        return PaginatedList(
            items=[
                DatasetRecord.model_validate(dataset)
                for dataset in unmarshalled["items"]
            ],
            next_token=unmarshalled["next_token"],
        )

    def update(
        self,
        record: DatasetRecord,
        metadata_changeset: Optional[MetadataChangeset] = None,
        conditions: Optional[list[UpdateCondition]] = None,
        description: Optional[str] = None,
        updated_by: Optional[str] = None,
    ) -> DatasetRecord:
        url = f"{self.__roboto_service_base_url}/v1/datasets/{record.dataset_id}"
        payload = UpdateDatasetRequest(
            metadata_changeset=metadata_changeset,
            description=description,
            conditions=conditions,
        )
        with RobotoHttpExceptionParse():
            response = self.__http_client.put(
                url,
                data=pydantic_jsonable_dict(payload, exclude_none=True),
                headers=self.headers(user_id=updated_by),
            )

        return DatasetRecord.model_validate(response.from_json(json_path=["data"]))

    def get_access(self, record: DatasetRecord) -> GetAccessResponse:
        url = f"{self.__roboto_service_base_url}/v1/datasets/{record.dataset_id}/access"

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(url, headers=self.headers())

        return GetAccessResponse.model_validate(response.from_json(json_path=["data"]))

    def edit_access(
        self, record: DatasetRecord, edit: EditAccessRequest
    ) -> GetAccessResponse:
        url = f"{self.__roboto_service_base_url}/v1/datasets/{record.dataset_id}/access"

        with RobotoHttpExceptionParse():
            response = self.__http_client.put(
                url, data=edit.model_dump(mode="json"), headers=self.headers()
            )

        return GetAccessResponse.model_validate(response.from_json(json_path=["data"]))

    def create_manifest_transaction(
        self,
        origination: str,
        dataset_record: DatasetRecord,
        resource_manifest: dict[str, int],
        caller: Optional[str] = None,
    ) -> Tuple[TransactionRecord, dict[str, str]]:
        url = f"{self.__roboto_service_base_url}/v2/datasets/{dataset_record.dataset_id}/batch_uploads"
        request_body = BeginManifestTransactionRequest(
            origination=origination,
            resource_manifest=resource_manifest,
        )

        with RobotoHttpExceptionParse():
            response = self.__http_client.post(
                url,
                data=request_body.model_dump_json(exclude_none=True),
                headers=roboto_headers(
                    org_id=dataset_record.org_id,
                    additional_headers={"Content-Type": "application/json"},
                ),
            )

        result = BeginManifestTransactionResponse.model_validate(
            response.from_json(json_path=["data"])
        )

        return (result.record, dict(result.upload_mappings))

    def flush_manifest_item_completions(
        self,
        dataset_id: str,
        transaction_id: str,
        manifest_items: list[str],
        org_id: Optional[str] = None,
        caller: Optional[str] = None,
        resource_owner_id: Optional[str] = None,
    ) -> None:
        url = f"{self.__roboto_service_base_url}/v2/datasets/{dataset_id}/batch_uploads/{transaction_id}/progress"
        request_body = ReportTransactionProgressRequest(
            manifest_items=manifest_items,
        )

        with RobotoHttpExceptionParse():
            self.__http_client.put(
                url,
                data=request_body.model_dump_json(exclude_none=True),
                headers=roboto_headers(
                    org_id=org_id,
                    user_id=caller,
                    resource_owner_id=resource_owner_id,
                    additional_headers={"Content-Type": "application/json"},
                ),
            )

    def complete_manifest_transaction(
        self,
        dataset_id: str,
        transaction_id: str,
        org_id: Optional[str] = None,
    ) -> None:
        """
        Marks a transaction as 'completed', which allows the Roboto Platform to evaluate triggers
        for automatic action on incoming data. This also aids reporting on partial upload failure cases.
        """
        url = f"{self.__roboto_service_base_url}/v2/datasets/{dataset_id}/batch_uploads/{transaction_id}/complete"

        with RobotoHttpExceptionParse():
            self.__http_client.put(
                url=url,
                headers=roboto_headers(
                    org_id=org_id,
                    additional_headers={"Content-Type": "application/json"},
                ),
            )

    def on_manifest_item_complete(
        self,
        dataset_id: str,
        transaction_id: str,
        manifest_item_identifier: str,
    ) -> None:
        if transaction_id not in self.__transaction_manifests:
            raise RobotoNotFoundException(
                f"Transaction {transaction_id} does not have a manifest"
            )

        if transaction_id not in self.__transaction_completed_unreported_items:
            self.__transaction_completed_unreported_items[transaction_id] = set()

        self.__transaction_completed_unreported_items[transaction_id].add(
            manifest_item_identifier
        )

        if self.__unreported_manifest_items_batch_ready_to_report(transaction_id):
            self.flush_manifest_item_completions(
                dataset_id=dataset_id,
                transaction_id=transaction_id,
                manifest_items=list(
                    self.__transaction_completed_unreported_items[transaction_id]
                ),
            )
            self.__transaction_completed_unreported_items[transaction_id] = set()

    def __unreported_manifest_items_batch_ready_to_report(self, transaction_id):
        return (
            len(self.__transaction_completed_unreported_items[transaction_id])
            >= (
                len(self.__transaction_manifests[transaction_id])
                / self.__manifest_reporting_increments
            )
            and len(self.__transaction_completed_unreported_items[transaction_id])
            >= self.__manifest_reporting_min_batch_size
        )

    def create_single_file_upload(
        self,
        dataset_record: DatasetRecord,
        file_path: str,
        file_size: int,
        caller: str,
        origination: Optional[str] = None,
        org_id: Optional[str] = None,
        resource_owner_id: Optional[str] = None,
    ) -> Tuple[str, str]:
        url = f"{self.__roboto_service_base_url}/v2/datasets/{dataset_record.dataset_id}/uploads"
        request_body = BeginSingleFileUploadRequest(
            origination=origination,
            file_path=file_path,
            file_size=file_size,
        )

        with RobotoHttpExceptionParse():
            response = self.__http_client.post(
                url,
                data=request_body.model_dump_json(exclude_none=True),
                headers=roboto_headers(
                    org_id=org_id,
                    user_id=caller,
                    resource_owner_id=resource_owner_id,
                    additional_headers={"Content-Type": "application/json"},
                ),
            )

        parsed_response = BeginSingleFileUploadResponse.model_validate(
            response.from_json(json_path=["data"])
        )
        return parsed_response.upload_id, parsed_response.upload_url

    def complete_single_file_upload(
        self,
        dataset_id: str,
        upload_id: str,
        org_id: Optional[str] = None,
        caller: Optional[str] = None,
        resource_owner_id: Optional[str] = None,
    ) -> None:
        url = f"{self.__roboto_service_base_url}/v2/datasets/{dataset_id}/uploads/{upload_id}/complete"

        with RobotoHttpExceptionParse():
            self.__http_client.put(
                url=url,
                headers=roboto_headers(
                    org_id=org_id,
                    user_id=caller,
                    resource_owner_id=resource_owner_id,
                    additional_headers={"Content-Type": "application/json"},
                ),
            )
