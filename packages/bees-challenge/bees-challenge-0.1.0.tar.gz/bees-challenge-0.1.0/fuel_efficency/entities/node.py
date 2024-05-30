from dataclasses import dataclass
from typing import Protocol

from fuel_efficency.entities.position import Position


@dataclass(slots=True)
class Node(Protocol):
    weight: float
    position: 'Position' = Position()
