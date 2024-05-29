# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import, f-string-without-interpolation, too-many-branches, too-many-statements, unnecessary-pass
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import decimal
import bson
from ..ascii.get_axis_setting_result import GetAxisSettingResult


@dataclass
class GetAxisSettingResults:

    results: List[GetAxisSettingResult] = field(default_factory=list)

    @staticmethod
    def zero_values() -> 'GetAxisSettingResults':
        return GetAxisSettingResults(
            results=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'GetAxisSettingResults':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return GetAxisSettingResults.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        self.validate()
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'results': [item.to_dict() for item in self.results] if self.results is not None else [],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'GetAxisSettingResults':
        return GetAxisSettingResults(
            results=[GetAxisSettingResult.from_dict(item) for item in data.get('results')],  # type: ignore
        )

    def validate(self) -> None:
        """" Validates the properties of the instance. """
        if self.results is not None:
            if not isinstance(self.results, list):
                raise ValueError('Property "Results" of "GetAxisSettingResults" is not a list.')

            for i, results_item in enumerate(self.results):
                if results_item is None:
                    raise ValueError(f'Item {i} in property "Results" of "GetAxisSettingResults" is None.')

                if not isinstance(results_item, GetAxisSettingResult):
                    raise ValueError(f'Item {i} in property "Results" of "GetAxisSettingResults" is not an instance of "GetAxisSettingResult".')

                results_item.validate()
