# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import, f-string-without-interpolation, too-many-branches, too-many-statements, unnecessary-pass
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import decimal
import bson
from ...units import Units, UnitsAndLiterals, units_from_literals


@dataclass
class GetAxisSetting:
    """
    Specifies a setting to get with one of the multi-get commands.
    """

    setting: str
    """
    The setting to read.
    """

    unit: Optional[UnitsAndLiterals] = None
    """
    The unit to convert the read setting to.
    """

    @staticmethod
    def zero_values() -> 'GetAxisSetting':
        return GetAxisSetting(
            setting="",
            unit=None,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'GetAxisSetting':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return GetAxisSetting.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        self.validate()
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'setting': str(self.setting or ''),
            'unit': units_from_literals(self.unit).value if self.unit is not None else None,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'GetAxisSetting':
        return GetAxisSetting(
            setting=data.get('setting'),  # type: ignore
            unit=Units(data.get('unit')) if data.get('unit') is not None else None,  # type: ignore
        )

    def validate(self) -> None:
        """" Validates the properties of the instance. """
        if self.setting is not None:
            if not isinstance(self.setting, str):
                raise ValueError(f'Property "Setting" of "GetAxisSetting" is not a string.')
