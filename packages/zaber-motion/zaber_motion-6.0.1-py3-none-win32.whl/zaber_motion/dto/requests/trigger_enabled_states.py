# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import, f-string-without-interpolation, too-many-branches, too-many-statements, unnecessary-pass
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import decimal
import bson
from ..ascii.trigger_enabled_state import TriggerEnabledState


@dataclass
class TriggerEnabledStates:

    states: List[TriggerEnabledState] = field(default_factory=list)

    @staticmethod
    def zero_values() -> 'TriggerEnabledStates':
        return TriggerEnabledStates(
            states=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'TriggerEnabledStates':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return TriggerEnabledStates.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        self.validate()
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'states': [item.to_dict() for item in self.states] if self.states is not None else [],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'TriggerEnabledStates':
        return TriggerEnabledStates(
            states=[TriggerEnabledState.from_dict(item) for item in data.get('states')],  # type: ignore
        )

    def validate(self) -> None:
        """" Validates the properties of the instance. """
        if self.states is not None:
            if not isinstance(self.states, list):
                raise ValueError('Property "States" of "TriggerEnabledStates" is not a list.')

            for i, states_item in enumerate(self.states):
                if states_item is None:
                    raise ValueError(f'Item {i} in property "States" of "TriggerEnabledStates" is None.')

                if not isinstance(states_item, TriggerEnabledState):
                    raise ValueError(f'Item {i} in property "States" of "TriggerEnabledStates" is not an instance of "TriggerEnabledState".')

                states_item.validate()
