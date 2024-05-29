# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import, f-string-without-interpolation, too-many-branches, too-many-statements, unnecessary-pass
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import decimal
import bson


@dataclass
class AxisAddress:
    """
    Holds device address and axis number.
    """

    device: int
    """
    Device address.
    """

    axis: int
    """
    Axis number.
    """

    @staticmethod
    def zero_values() -> 'AxisAddress':
        return AxisAddress(
            device=0,
            axis=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'AxisAddress':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return AxisAddress.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        self.validate()
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'device': int(self.device),
            'axis': int(self.axis),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'AxisAddress':
        return AxisAddress(
            device=data.get('device'),  # type: ignore
            axis=data.get('axis'),  # type: ignore
        )

    def validate(self) -> None:
        """" Validates the properties of the instance. """
        if self.device is None:
            raise ValueError(f'Property "Device" of "AxisAddress" is None.')

        if not isinstance(self.device, (int, float, decimal.Decimal)):
            raise ValueError(f'Property "Device" of "AxisAddress" is not a number.')

        if int(self.device) != self.device:
            raise ValueError(f'Property "Device" of "AxisAddress" is not integer value.')

        if self.axis is None:
            raise ValueError(f'Property "Axis" of "AxisAddress" is None.')

        if not isinstance(self.axis, (int, float, decimal.Decimal)):
            raise ValueError(f'Property "Axis" of "AxisAddress" is not a number.')

        if int(self.axis) != self.axis:
            raise ValueError(f'Property "Axis" of "AxisAddress" is not integer value.')
