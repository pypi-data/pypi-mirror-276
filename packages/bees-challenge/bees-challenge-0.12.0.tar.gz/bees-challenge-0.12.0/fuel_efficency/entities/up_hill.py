from dataclasses import dataclass

from fuel_efficency.entities.node import Node
from fuel_efficency.entities.position import Position


@dataclass(slots=True)
class UpHill:
    weight: float = float(2)
    position: 'Position' = Position()
