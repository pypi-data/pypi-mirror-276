import abc
import datetime
from typing import Any, Optional, Tuple

import pydantic

from ...auth import (
    EditAccessRequest,
    GetAccessResponse,
    Permissions,
)
from ...http import PaginatedList
from ...query import QuerySpecification
from ...serde import pydantic_jsonable_dict
from ...time import utcnow
from ...transactions import TransactionRecord
from ...updates import (
    MetadataChangeset,
    UpdateCondition,
)
from ..files import FileRecord, S3Credentials
from .record import (
    Administrator,
    DatasetRecord,
    StorageLocation,
)


class Credentials(pydantic.BaseModel):
    access_key_id: str
    bucket: str
    expiration: datetime.datetime
    secret_access_key: str
    session_token: str
    region: str
    required_prefix: str

    def is_expired(self) -> bool:
        return utcnow() >= self.expiration

    def to_dict(self) -> dict[str, Any]:
        return pydantic_jsonable_dict(self, exclude_none=True)

    def to_s3_credentials(self) -> S3Credentials:
        return {
            "access_key": self.access_key_id,
            "secret_key": self.secret_access_key,
            "token": self.session_token,
            "expiry_time": self.expiration.isoformat(),
            "region": self.region,
        }


class DatasetDelegate(abc.ABC):
    @abc.abstractmethod
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
        raise NotImplementedError("create_dataset")

    @abc.abstractmethod
    def delete_dataset(self, record: DatasetRecord) -> None:
        raise NotImplementedError("delete_dataset")

    @abc.abstractmethod
    def get_dataset_by_id(
        self,
        dataset_id: str,
    ) -> DatasetRecord:
        raise NotImplementedError("get_dataset_by_primary_key")

    @abc.abstractmethod
    def get_temporary_credentials(
        self,
        record: DatasetRecord,
        permissions: Permissions,
        caller: Optional[str] = None,
        transaction_id: Optional[str] = None,
    ) -> Credentials:
        raise NotImplementedError("get_temporary_credentials")

    @abc.abstractmethod
    def list_files(
        self,
        dataset_id: str,
        page_token: Optional[str] = None,
        include_patterns: Optional[list[str]] = None,
        exclude_patterns: Optional[list[str]] = None,
    ) -> PaginatedList[FileRecord]:
        raise NotImplementedError("list_files")

    @abc.abstractmethod
    def query_datasets(
        self,
        query: QuerySpecification,
        org_id: Optional[str] = None,
    ) -> PaginatedList[DatasetRecord]:
        raise NotImplementedError("query_datasets")

    @abc.abstractmethod
    def update(
        self,
        record: DatasetRecord,
        metadata_changeset: Optional[MetadataChangeset] = None,
        conditions: Optional[list[UpdateCondition]] = None,
        description: Optional[str] = None,
        updated_by: Optional[str] = None,
    ) -> DatasetRecord:
        raise NotImplementedError("update")

    @abc.abstractmethod
    def get_access(self, record: DatasetRecord) -> GetAccessResponse:
        raise NotImplementedError("get_access")

    @abc.abstractmethod
    def edit_access(
        self, record: DatasetRecord, edit: EditAccessRequest
    ) -> GetAccessResponse:
        raise NotImplementedError("edit_access")

    @abc.abstractmethod
    def create_manifest_transaction(
        self,
        origination: str,
        dataset_record: DatasetRecord,
        resource_manifest: dict[str, int],
        caller: Optional[str] = None,
    ) -> Tuple[TransactionRecord, dict[str, str]]:
        raise NotImplementedError("create_manifest_transaction")

    @abc.abstractmethod
    def flush_manifest_item_completions(
        self,
        dataset_id: str,
        transaction_id: str,
        manifest_items: list[str],
        org_id: Optional[str] = None,
        caller: Optional[str] = None,
        resource_owner_id: Optional[str] = None,
    ) -> None:
        raise NotImplementedError("flush_manifest_item_completions")

    @abc.abstractmethod
    def complete_manifest_transaction(
        self,
        dataset_id: str,
        transaction_id: str,
        org_id: Optional[str] = None,
    ) -> None:
        raise NotImplementedError("complete_manifest_transaction")

    @abc.abstractmethod
    def on_manifest_item_complete(
        self,
        dataset_id: str,
        transaction_id: str,
        manifest_item_identifier: str,
    ) -> None:
        raise NotImplementedError("on_manifest_item_complete")

    @abc.abstractmethod
    def create_single_file_upload(
        self,
        dataset_record: DatasetRecord,
        file_path: str,
        file_size: int,
        caller: str,
        origination: str,
        org_id: Optional[str] = None,
        resource_owner_id: Optional[str] = None,
    ) -> Tuple[str, str]:
        raise NotImplementedError("create_single_file_upload")

    @abc.abstractmethod
    def complete_single_file_upload(
        self,
        dataset_id: str,
        upload_id: str,
        org_id: Optional[str] = None,
        caller: Optional[str] = None,
        resource_owner_id: Optional[str] = None,
    ) -> None:
        raise NotImplementedError("complete_single_file_upload")
