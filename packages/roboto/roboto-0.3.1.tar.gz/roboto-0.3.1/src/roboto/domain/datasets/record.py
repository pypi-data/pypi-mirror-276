#  Copyright (c) 2023 Roboto Technologies, Inc.

import datetime
import enum
import typing
from typing import Any, Optional

import pydantic


class Administrator(str, enum.Enum):
    # Other supported type would be "Customer"
    Roboto = "Roboto"


class StorageLocation(str, enum.Enum):
    # Other supported locations might be "GCP" or "Azure"
    S3 = "S3"


class S3StorageCtx(pydantic.BaseModel):
    bucket_name: str
    iam_role_arn: str
    key_prefix: str


# https://www.google.com/search?q=pydantic.Field+default_factory+not+evaluated+in+parse_obj&rlz=1C5CHFA_enUS1054US1054&oq=pydantic.Field+default_factory+not+evaluated+in+parse_obj&aqs=chrome..69i57j33i160.6235j0j7&sourceid=chrome&ie=UTF-8
StorageCtxType = typing.Optional[S3StorageCtx]


class DatasetRecord(pydantic.BaseModel):
    # Primary key, defined in CDK
    org_id: str  # partition key
    dataset_id: str  # sort key

    administrator: Administrator
    # Persisted as ISO 8601 string in UTC
    created: datetime.datetime
    created_by: str
    description: Optional[str] = None
    metadata: dict[str, Any] = pydantic.Field(default_factory=dict)
    # Persisted as ISO 8601 string in UTC
    modified: datetime.datetime
    modified_by: str
    storage_location: StorageLocation
    storage_ctx: StorageCtxType = None
    tags: list[str] = pydantic.Field(default_factory=list)
    roboto_record_version: int = 0  # A protected field, incremented on every update

    @staticmethod
    def storage_ctx_from_dict(ctx_dict: dict[str, typing.Any]) -> StorageCtxType:
        """
        Used to cast a dict representation of StorageCtxType into an appropriate pydantic model. Will return None
        if the empty dict (default representation) is provided, and will throw an exception if some fields are set,
        but they don't match a known storage ctx pydantic model.
        """
        if ctx_dict == {}:
            return None

        return S3StorageCtx.model_validate(ctx_dict)
