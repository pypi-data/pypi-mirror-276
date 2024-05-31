from dataclasses import dataclass, field
from functools import total_ordering

from fuel_efficency.entities.node import Node
from fuel_efficency.entities.position import Position


@total_ordering
@dataclass(slots=True)
class DownHill:
    weight: float = float(0.5)
    position: Position = field(default_factory=Position)

    def __eq__(self, other):
        if not isinstance(other, Node):
            raise NotImplementedError(f"Missing `position` or `weight` attribute" )

    def __gt__(self, other):
        if not isinstance(other, Node):
            raise NotImplementedError("Missing `weight` attribute")
