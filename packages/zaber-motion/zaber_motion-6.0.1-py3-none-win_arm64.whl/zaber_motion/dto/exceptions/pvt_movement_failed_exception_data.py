# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import, f-string-without-interpolation, too-many-branches, too-many-statements, unnecessary-pass
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import decimal
import bson


@dataclass
class PvtMovementFailedExceptionData:
    """
    Contains additional data for PvtMovementFailedException.
    """

    warnings: List[str]
    """
    The full list of warnings.
    """

    reason: str
    """
    The reason for the Exception.
    """

    @staticmethod
    def zero_values() -> 'PvtMovementFailedExceptionData':
        return PvtMovementFailedExceptionData(
            warnings=[],
            reason="",
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'PvtMovementFailedExceptionData':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return PvtMovementFailedExceptionData.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        self.validate()
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'warnings': [str(item or '') for item in self.warnings] if self.warnings is not None else [],
            'reason': str(self.reason or ''),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'PvtMovementFailedExceptionData':
        return PvtMovementFailedExceptionData(
            warnings=data.get('warnings'),  # type: ignore
            reason=data.get('reason'),  # type: ignore
        )

    def validate(self) -> None:
        """" Validates the properties of the instance. """
        if self.warnings is not None:
            if not isinstance(self.warnings, list):
                raise ValueError('Property "Warnings" of "PvtMovementFailedExceptionData" is not a list.')

            for i, warnings_item in enumerate(self.warnings):
                if warnings_item is not None:
                    if not isinstance(warnings_item, str):
                        raise ValueError(f'Item {i} in property "Warnings" of "PvtMovementFailedExceptionData" is not a string.')

        if self.reason is not None:
            if not isinstance(self.reason, str):
                raise ValueError(f'Property "Reason" of "PvtMovementFailedExceptionData" is not a string.')
