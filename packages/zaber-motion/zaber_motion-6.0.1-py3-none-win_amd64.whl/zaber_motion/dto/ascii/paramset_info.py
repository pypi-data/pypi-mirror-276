# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import, f-string-without-interpolation, too-many-branches, too-many-statements, unnecessary-pass
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import decimal
import bson
from .servo_tuning_param import ServoTuningParam


@dataclass
class ParamsetInfo:
    """
    The raw parameters currently saved to a given paramset.
    """

    type: str
    """
    The tuning algorithm used for this axis.
    """

    version: int
    """
    The version of the tuning algorithm used for this axis.
    """

    params: List[ServoTuningParam]
    """
    The raw tuning parameters of this device.
    """

    @staticmethod
    def zero_values() -> 'ParamsetInfo':
        return ParamsetInfo(
            type="",
            version=0,
            params=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'ParamsetInfo':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return ParamsetInfo.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        self.validate()
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': str(self.type or ''),
            'version': int(self.version),
            'params': [item.to_dict() for item in self.params] if self.params is not None else [],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'ParamsetInfo':
        return ParamsetInfo(
            type=data.get('type'),  # type: ignore
            version=data.get('version'),  # type: ignore
            params=[ServoTuningParam.from_dict(item) for item in data.get('params')],  # type: ignore
        )

    def validate(self) -> None:
        """" Validates the properties of the instance. """
        if self.type is not None:
            if not isinstance(self.type, str):
                raise ValueError(f'Property "Type" of "ParamsetInfo" is not a string.')

        if self.version is None:
            raise ValueError(f'Property "Version" of "ParamsetInfo" is None.')

        if not isinstance(self.version, (int, float, decimal.Decimal)):
            raise ValueError(f'Property "Version" of "ParamsetInfo" is not a number.')

        if int(self.version) != self.version:
            raise ValueError(f'Property "Version" of "ParamsetInfo" is not integer value.')

        if self.params is not None:
            if not isinstance(self.params, list):
                raise ValueError('Property "Params" of "ParamsetInfo" is not a list.')

            for i, params_item in enumerate(self.params):
                if params_item is None:
                    raise ValueError(f'Item {i} in property "Params" of "ParamsetInfo" is None.')

                if not isinstance(params_item, ServoTuningParam):
                    raise ValueError(f'Item {i} in property "Params" of "ParamsetInfo" is not an instance of "ServoTuningParam".')

                params_item.validate()
