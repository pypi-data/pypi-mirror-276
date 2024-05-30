import dataclasses
from typing import Any

from tqbus_sdk.tqsystem import TqSystem, TqSystemEnums


@dataclasses.dataclass
class GenericIndV1Service:
    """
    A generic service class for individual life  system.

    This class provides methods to make HTTP requests to the individual life  system.

    Attributes:
        system (TqSystem): The TqSystem instance representing the individual life  system.

    Methods:
        request: Makes an HTTP request to the individual life  system.

    """

    system: TqSystem = dataclasses.field(
        default_factory=lambda: TqSystem(tq_system_enum=TqSystemEnums.IND_V1)
    )

    def request(self, method: str, url: str, **kwargs) -> Any:
        """
        Makes an HTTP request to the individual life  system.

        Args:
            method (str): The HTTP method to use for the request.
            url (str): The URL to send the request to.
            **kwargs: Additional keyword arguments to be passed to the underlying request method.

        Returns:
            Any: The response from the individual life  system.

        """
        url = self.system.base_url + url
        return self.system.request(method=method, url=url, **kwargs)


@dataclasses.dataclass
class GenericIndV2Service:
    system: TqSystem = dataclasses.field(
        default_factory=lambda: TqSystem(tq_system_enum=TqSystemEnums.IND_V2)
    )

    def request(self, method: str, url: str, **kwargs) -> Any:
        url = self.system.base_url + url
        return self.system.request(method=method, url=url, **kwargs)
