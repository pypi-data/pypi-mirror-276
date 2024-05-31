from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

from fuel_efficency.entities.position import Position


@runtime_checkable
@dataclass(slots=True)
class Node(Protocol):
    weight: float
    position: Position =  field(default_factory=Position)

    def __eq__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return self.position == other.position
