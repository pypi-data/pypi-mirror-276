# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import, f-string-without-interpolation, too-many-branches, too-many-statements, unnecessary-pass
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import decimal
import bson


@dataclass
class FindDeviceResponse:

    address: int = 0

    @staticmethod
    def zero_values() -> 'FindDeviceResponse':
        return FindDeviceResponse(
            address=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'FindDeviceResponse':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return FindDeviceResponse.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        self.validate()
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'address': int(self.address),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'FindDeviceResponse':
        return FindDeviceResponse(
            address=data.get('address'),  # type: ignore
        )

    def validate(self) -> None:
        """" Validates the properties of the instance. """
        if self.address is None:
            raise ValueError(f'Property "Address" of "FindDeviceResponse" is None.')

        if not isinstance(self.address, (int, float, decimal.Decimal)):
            raise ValueError(f'Property "Address" of "FindDeviceResponse" is not a number.')

        if int(self.address) != self.address:
            raise ValueError(f'Property "Address" of "FindDeviceResponse" is not integer value.')
