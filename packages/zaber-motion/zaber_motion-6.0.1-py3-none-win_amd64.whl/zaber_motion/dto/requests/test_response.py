# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import, f-string-without-interpolation, too-many-branches, too-many-statements, unnecessary-pass
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import decimal
import bson


@dataclass
class TestResponse:

    data_pong: str = ""

    @staticmethod
    def zero_values() -> 'TestResponse':
        return TestResponse(
            data_pong="",
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'TestResponse':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return TestResponse.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        self.validate()
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'dataPong': str(self.data_pong or ''),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'TestResponse':
        return TestResponse(
            data_pong=data.get('dataPong'),  # type: ignore
        )

    def validate(self) -> None:
        """" Validates the properties of the instance. """
        if self.data_pong is not None:
            if not isinstance(self.data_pong, str):
                raise ValueError(f'Property "DataPong" of "TestResponse" is not a string.')
