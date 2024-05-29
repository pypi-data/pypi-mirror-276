# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import, f-string-without-interpolation, too-many-branches, too-many-statements, unnecessary-pass
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import decimal
import bson


@dataclass
class DeviceAddressConflictExceptionData:
    """
    Contains additional data for DeviceAddressConflictException.
    """

    device_addresses: List[int]
    """
    The full list of detected device addresses.
    """

    @staticmethod
    def zero_values() -> 'DeviceAddressConflictExceptionData':
        return DeviceAddressConflictExceptionData(
            device_addresses=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'DeviceAddressConflictExceptionData':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return DeviceAddressConflictExceptionData.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        self.validate()
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'deviceAddresses': [int(item) for item in self.device_addresses] if self.device_addresses is not None else [],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'DeviceAddressConflictExceptionData':
        return DeviceAddressConflictExceptionData(
            device_addresses=data.get('deviceAddresses'),  # type: ignore
        )

    def validate(self) -> None:
        """" Validates the properties of the instance. """
        if self.device_addresses is not None:
            if not isinstance(self.device_addresses, list):
                raise ValueError('Property "DeviceAddresses" of "DeviceAddressConflictExceptionData" is not a list.')

            for i, device_addresses_item in enumerate(self.device_addresses):
                if device_addresses_item is None:
                    raise ValueError(f'Item {i} in property "DeviceAddresses" of "DeviceAddressConflictExceptionData" is None.')

                if not isinstance(device_addresses_item, (int, float, decimal.Decimal)):
                    raise ValueError(f'Item {i} in property "DeviceAddresses" of "DeviceAddressConflictExceptionData" is not a number.')

                if int(device_addresses_item) != device_addresses_item:
                    raise ValueError(f'Item {i} in property "DeviceAddresses" of "DeviceAddressConflictExceptionData" is not integer value.')
