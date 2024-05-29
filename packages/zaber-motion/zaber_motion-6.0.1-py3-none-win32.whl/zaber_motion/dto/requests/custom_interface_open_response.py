# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import, f-string-without-interpolation, too-many-branches, too-many-statements, unnecessary-pass
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import decimal
import bson


@dataclass
class CustomInterfaceOpenResponse:

    transport_id: int = 0

    @staticmethod
    def zero_values() -> 'CustomInterfaceOpenResponse':
        return CustomInterfaceOpenResponse(
            transport_id=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'CustomInterfaceOpenResponse':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return CustomInterfaceOpenResponse.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        self.validate()
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'transportId': int(self.transport_id),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'CustomInterfaceOpenResponse':
        return CustomInterfaceOpenResponse(
            transport_id=data.get('transportId'),  # type: ignore
        )

    def validate(self) -> None:
        """" Validates the properties of the instance. """
        if self.transport_id is None:
            raise ValueError(f'Property "TransportId" of "CustomInterfaceOpenResponse" is None.')

        if not isinstance(self.transport_id, (int, float, decimal.Decimal)):
            raise ValueError(f'Property "TransportId" of "CustomInterfaceOpenResponse" is not a number.')

        if int(self.transport_id) != self.transport_id:
            raise ValueError(f'Property "TransportId" of "CustomInterfaceOpenResponse" is not integer value.')
