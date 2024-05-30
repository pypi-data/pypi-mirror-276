import dataclasses

from roboto.http import (
    HttpClient,
    PATAuthDecoratorV1,
)

from ..profile import RobotoProfile
from .devices import DeviceParams
from .http_delegates import HttpDelegates


@dataclasses.dataclass
class DomainParams:
    """
    This class aggregates all parameters required to instantiate any domain entity from ``roboto.domain``.

    Each entity's factory methods and constructors take a ``*Params`` object as a required parameter, and each of those
    objects is available as a named property of DomainParams.

    The DomainParams object is intended to be constructed once per script for single-threaded usage, and once per
    process or thread for parallel usage.

    It's perfectly safe to instantiate multiple DomainParams objects within the same process or thread, but it could
    result in duplicate creation of some client objects, which incurs a small memory overhead and may negate client
    caching optimizations.

    Example:
        >>> from roboto.domain import DomainParams
        >>> from roboto.domain.devices import Device
        >>> domain_params = DomainParams.from_env()
        >>> device = Device.from_id(device_id="my_device", params=domain_params.devices)

    Attributes:
        delegates: HttpDelegates required to instantiate older classes from ``roboto.domain`` which have not been
            updated to use a single ``*Params`` constructor argument.
        devices: All parameters required to instantiate a :class:`roboto.domain.devices.Device`
    """

    delegates: HttpDelegates
    devices: DeviceParams

    @staticmethod
    def from_client(
        http_client: HttpClient, roboto_service_url: str = "https://api.roboto.ai"
    ) -> "DomainParams":
        """
        Construct a DomainParams object from an HTTP client and an optional service endpoint override.

        Args:
            http_client: An HTTP client set up with Authorization header decoration required to make authenticated
            requests to Roboto.
            roboto_service_url: The base URL of the Roboto service. Defaults to https://api.roboto.ai.

        Returns:
            A DomainParams object usable to instantiate any domain entity from ``roboto.domain``.
        """
        delegates = HttpDelegates.from_client(http_client, roboto_service_url)
        return DomainParams(
            devices=DeviceParams(
                http_client=http_client,
                roboto_service_url=roboto_service_url,
                token_delegate=delegates.tokens,
            ),
            delegates=delegates,
        )

    @staticmethod
    def from_env() -> "DomainParams":
        """
        Construct a DomainParams object from sane default values, based on an inspection of your runtime environment.

        Returns:
            A DomainParams object usable to instantiate any domain entity from ``roboto.domain``.
        """

        entry = RobotoProfile().get_entry()
        auth_decorator = PATAuthDecoratorV1(pat=entry.token)
        http_client = HttpClient(
            default_endpoint=entry.default_endpoint, default_auth=auth_decorator
        )
        return DomainParams.from_client(
            http_client=http_client, roboto_service_url=entry.default_endpoint
        )
