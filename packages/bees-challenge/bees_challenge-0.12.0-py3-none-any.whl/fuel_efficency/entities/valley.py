from dataclasses import dataclass

from fuel_efficency.entities.node import Node
from fuel_efficency.entities.position import Position


@dataclass(slots=True)
class Valley:
   weight: float = float(1)
   position: 'Position' = Position()
