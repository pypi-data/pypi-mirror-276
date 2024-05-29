# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import, f-string-without-interpolation, too-many-branches, too-many-statements, unnecessary-pass
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import decimal
import bson
from .process_controller_source_sensor import ProcessControllerSourceSensor


@dataclass
class ProcessControllerSource:
    """
    The source used by a process in a closed-loop mode.
    """

    sensor: ProcessControllerSourceSensor
    """
    The type of input sensor.
    """

    port: int
    """
    The specific input to use.
    """

    @staticmethod
    def zero_values() -> 'ProcessControllerSource':
        return ProcessControllerSource(
            sensor=next(first for first in ProcessControllerSourceSensor),
            port=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'ProcessControllerSource':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return ProcessControllerSource.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        self.validate()
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'sensor': self.sensor.value,
            'port': int(self.port),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'ProcessControllerSource':
        return ProcessControllerSource(
            sensor=ProcessControllerSourceSensor(data.get('sensor')),  # type: ignore
            port=data.get('port'),  # type: ignore
        )

    def validate(self) -> None:
        """" Validates the properties of the instance. """
        if self.sensor is None:
            raise ValueError(f'Property "Sensor" of "ProcessControllerSource" is None.')

        if not isinstance(self.sensor, ProcessControllerSourceSensor):
            raise ValueError(f'Property "Sensor" of "ProcessControllerSource" is not an instance of "ProcessControllerSourceSensor".')

        if self.port is None:
            raise ValueError(f'Property "Port" of "ProcessControllerSource" is None.')

        if not isinstance(self.port, (int, float, decimal.Decimal)):
            raise ValueError(f'Property "Port" of "ProcessControllerSource" is not a number.')

        if int(self.port) != self.port:
            raise ValueError(f'Property "Port" of "ProcessControllerSource" is not integer value.')
