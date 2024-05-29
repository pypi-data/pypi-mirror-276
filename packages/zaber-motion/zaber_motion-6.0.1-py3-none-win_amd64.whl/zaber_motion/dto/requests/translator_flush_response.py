# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import, f-string-without-interpolation, too-many-branches, too-many-statements, unnecessary-pass
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import decimal
import bson


@dataclass
class TranslatorFlushResponse:

    commands: List[str] = field(default_factory=list)

    @staticmethod
    def zero_values() -> 'TranslatorFlushResponse':
        return TranslatorFlushResponse(
            commands=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'TranslatorFlushResponse':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return TranslatorFlushResponse.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        self.validate()
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'commands': [str(item or '') for item in self.commands] if self.commands is not None else [],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'TranslatorFlushResponse':
        return TranslatorFlushResponse(
            commands=data.get('commands'),  # type: ignore
        )

    def validate(self) -> None:
        """" Validates the properties of the instance. """
        if self.commands is not None:
            if not isinstance(self.commands, list):
                raise ValueError('Property "Commands" of "TranslatorFlushResponse" is not a list.')

            for i, commands_item in enumerate(self.commands):
                if commands_item is not None:
                    if not isinstance(commands_item, str):
                        raise ValueError(f'Item {i} in property "Commands" of "TranslatorFlushResponse" is not a string.')
