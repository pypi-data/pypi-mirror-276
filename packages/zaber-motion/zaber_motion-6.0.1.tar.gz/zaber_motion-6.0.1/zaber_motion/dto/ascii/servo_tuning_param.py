# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import, f-string-without-interpolation, too-many-branches, too-many-statements, unnecessary-pass
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import decimal
import bson


@dataclass
class ServoTuningParam:
    """
    A parameter used to establish the servo tuning of an axis.
    """

    name: str
    """
    The name of the parameter to set.
    """

    value: float
    """
    The value to use for this parameter.
    """

    @staticmethod
    def zero_values() -> 'ServoTuningParam':
        return ServoTuningParam(
            name="",
            value=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'ServoTuningParam':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return ServoTuningParam.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        self.validate()
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': str(self.name or ''),
            'value': float(self.value),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'ServoTuningParam':
        return ServoTuningParam(
            name=data.get('name'),  # type: ignore
            value=data.get('value'),  # type: ignore
        )

    def validate(self) -> None:
        """" Validates the properties of the instance. """
        if self.name is not None:
            if not isinstance(self.name, str):
                raise ValueError(f'Property "Name" of "ServoTuningParam" is not a string.')

        if self.value is None:
            raise ValueError(f'Property "Value" of "ServoTuningParam" is None.')

        if not isinstance(self.value, (int, float, decimal.Decimal)):
            raise ValueError(f'Property "Value" of "ServoTuningParam" is not a number.')
