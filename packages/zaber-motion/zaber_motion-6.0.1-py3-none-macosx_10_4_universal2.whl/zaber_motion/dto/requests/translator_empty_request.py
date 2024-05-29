# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import, f-string-without-interpolation, too-many-branches, too-many-statements, unnecessary-pass
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import decimal
import bson


@dataclass
class TranslatorEmptyRequest:

    translator_id: int = 0

    @staticmethod
    def zero_values() -> 'TranslatorEmptyRequest':
        return TranslatorEmptyRequest(
            translator_id=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'TranslatorEmptyRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return TranslatorEmptyRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        self.validate()
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'translatorId': int(self.translator_id),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'TranslatorEmptyRequest':
        return TranslatorEmptyRequest(
            translator_id=data.get('translatorId'),  # type: ignore
        )

    def validate(self) -> None:
        """" Validates the properties of the instance. """
        if self.translator_id is None:
            raise ValueError(f'Property "TranslatorId" of "TranslatorEmptyRequest" is None.')

        if not isinstance(self.translator_id, (int, float, decimal.Decimal)):
            raise ValueError(f'Property "TranslatorId" of "TranslatorEmptyRequest" is not a number.')

        if int(self.translator_id) != self.translator_id:
            raise ValueError(f'Property "TranslatorId" of "TranslatorEmptyRequest" is not integer value.')
