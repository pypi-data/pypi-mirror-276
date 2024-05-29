# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import, f-string-without-interpolation, too-many-branches, too-many-statements, unnecessary-pass
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import decimal
import bson


@dataclass
class UnitGetEnumRequest:

    symbol: str = ""

    @staticmethod
    def zero_values() -> 'UnitGetEnumRequest':
        return UnitGetEnumRequest(
            symbol="",
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'UnitGetEnumRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return UnitGetEnumRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        self.validate()
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'symbol': str(self.symbol or ''),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'UnitGetEnumRequest':
        return UnitGetEnumRequest(
            symbol=data.get('symbol'),  # type: ignore
        )

    def validate(self) -> None:
        """" Validates the properties of the instance. """
        if self.symbol is not None:
            if not isinstance(self.symbol, str):
                raise ValueError(f'Property "Symbol" of "UnitGetEnumRequest" is not a string.')
