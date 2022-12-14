from __future__ import annotations

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List, Union


@dataclass_json
@dataclass
class Tick:
    currentTick: int
    totalTicks: int
    map: Map
    currentLocation: Union[Position, None]
    spawnLocation: Union[Position, None]
    visitedPortIndices: List[int]
    tideSchedule: List[int]
    isOver: bool

@dataclass_json
@dataclass
class Map:
    topology: List[List[int]]
    ports: List[Position]
    tideLevels: TideLevels

@dataclass_json
@dataclass
class TideLevels:
    max: int
    min: int

@dataclass_json
@dataclass
class Position:
    row: int
    column: int

@dataclass_json
@dataclass
class Action():
    pass

@dataclass_json
@dataclass
class Sail(Action):
    direction: str
    kind: str = "sail"

@dataclass_json
@dataclass
class Spawn(Action):
    position: Position
    kind: str = "spawn"

@dataclass_json
@dataclass
class Anchor(Action):
    kind: str = "anchor"

@dataclass_json
@dataclass
class Dock(Action):
    kind: str = "dock"

directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
