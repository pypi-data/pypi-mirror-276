import collections.abc
import dataclasses
import typing
import urllib.parse

from roboto.exceptions import (
    RobotoHttpExceptionParse,
    RobotoNotImplementedException,
)
from roboto.http import (
    HttpClient,
    PaginatedList,
    roboto_headers,
)

from ..tokens import Token, TokenDelegate
from .device_models import (
    CreateDeviceRequest,
    DeviceRecord,
)


@dataclasses.dataclass
class DeviceParams:
    http_client: HttpClient
    roboto_service_url: str
    token_delegate: TokenDelegate


class Device:
    """
    A device is a non-human entity which can interact with Roboto on behalf of a specific organization.
    Each device is identified by a device_id, which is unique among all devices in the organization to which it belongs.

    The most typical device is a robot which uploads its log data to Roboto, either directly from its on-board software
    stack, or indirectly through an automatic upload station or human-in-the-loop upload process. Its device ID
    may be a string that represents its serial number in a scheme native to its organization.

    A dedicated uploader station which connects to many different robots and uploads data on their behalf could also
    be modeled as a device.

    API access tokens can be allocated for devices, and these tokens can be used to authenticate Roboto requests made
    on behalf of a device.
    """

    __params: DeviceParams
    __record: DeviceRecord

    # Class methods + Constructor

    @classmethod
    def create(cls, request: CreateDeviceRequest, params: DeviceParams) -> "Device":
        """
        Registers a device with Roboto.

        Args:
            request: User-specified fields for the to-be-created device record
            params: Common parameters required to construct any Device object

        Returns:
            A Device object representing the newly-created device
        """
        with RobotoHttpExceptionParse():
            response = params.http_client.post(
                url=f"{params.roboto_service_url}/v1/devices/create",
                headers=roboto_headers(resource_owner_id=request.org_id),
                data=request.model_dump(),
            )

        record = DeviceRecord.model_validate(response.from_json(json_path=["data"]))
        return cls(record=record, params=params)

    @classmethod
    def for_org(
        cls, org_id: str, params: DeviceParams
    ) -> collections.abc.Generator["Device", None, None]:
        """
        List all devices registered for a given org.

        Args:
            org_id: The org to list devices for
            params: Common parameters required to construct any Device object

        Returns:
            A generator of Device objects. For orgs with a large number of devices, this may involve multiple service
            calls, and the generator will yield results as they become available.
        """
        next_token: typing.Optional[str] = None
        while True:
            url = f"{params.roboto_service_url}/v1/devices/org/{org_id}"
            if next_token:
                encoded_qs = urllib.parse.urlencode({"page_token": str(next_token)})
                url = f"{url}?{encoded_qs}"

            with RobotoHttpExceptionParse():
                response = params.http_client.get(url=url)

            unmarshalled = response.from_json(json_path=["data"])

            results = PaginatedList(
                next_token=unmarshalled.get("next_token"),
                items=[
                    DeviceRecord.model_validate(item)
                    for item in unmarshalled.get("items", [])
                ],
            )

            for item in results.items:
                yield cls(record=item, params=params)

            next_token = results.next_token
            if not next_token:
                break

    @classmethod
    def from_id(
        cls, device_id: str, params: DeviceParams, org_id: typing.Optional[str] = None
    ) -> "Device":
        """
        Args:
            device_id: The device ID to look up. See :func:`Device.device_id` for more details.
            params: Common parameters required to construct any Device object
            org_id: The org to which the device belongs.
                If not specified by a caller who only belongs to one org, will default to the org_id of that org.
                If not specified by a caller who belongs to multiple orgs, will raise an exception.

        Returns:
            A Device object representing the specified device

        Raises:
            RobotoNotFoundException: If the specified device is not registered with Roboto
        """
        with RobotoHttpExceptionParse():
            response = params.http_client.get(
                url=f"{params.roboto_service_url}/v1/devices/id/{device_id}",
                headers=roboto_headers(resource_owner_id=org_id),
            )

        record = DeviceRecord.model_validate(response.from_json(json_path=["data"]))
        return cls(record=record, params=params)

    def __init__(self, record: DeviceRecord, params: DeviceParams):
        self.__params = params
        self.__record = record

    # Public properties

    @property
    def device_id(self) -> str:
        """
        This device's ID. Device ID is a user-provided identifier for a device, which is unique within the
        device's org.
        """
        return self.__record.device_id

    @property
    def org_id(self) -> str:
        """
        The ID of the org to which this device belongs.
        """
        return self.__record.org_id

    # Public methods

    def create_token(self) -> Token:
        """
        Stub API - Not Yet Implemented

        Raises:
            RobotoNotImplementedException: Always, because it's not implemented
        """
        raise RobotoNotImplementedException("Cannot create tokens for device.")

    def delete(self) -> None:
        """
        Deletes this device.
        """
        with RobotoHttpExceptionParse():
            self.__params.http_client.delete(
                url=f"{self.__params.roboto_service_url}/v1/devices/id/{self.device_id}",
                headers=roboto_headers(resource_owner_id=self.org_id),
            )

    def tokens(self) -> collections.abc.Generator[Token, None, None]:
        """
        Stub API - Not Yet Implemented

        Raises:
            RobotoNotImplementedException: Always, because it's not implemented
        """
        raise RobotoNotImplementedException("Cannot get tokens for device.")

    # Protected methods

    @property
    def _record(self) -> DeviceRecord:
        """
        The underlying DeviceRecord object which represents this device. This is often used as the wire representation
        of a device during API requests, and is subject to evolve over time. You should not program against this
        if avoidable.
        """
        return self.__record
