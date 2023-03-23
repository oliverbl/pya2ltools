from dataclasses import dataclass, field
from typing import Any


@dataclass
class A2LIfData:
    name: str
    content: str


@dataclass
class A2LMemorySegment:
    name: str
    description: str
    program_type: str
    memory_type: str
    location: str
    address: int
    size: int
    offsets: list[int] = field(default_factory=list)
    if_data: list[A2LIfData] = field(default_factory=list)


@dataclass
class A2LModPar:
    description: str
    number_of_interfaces: int
    memory_segments: list[A2LMemorySegment] = field(default_factory=list)  #
    system_constants: dict[str, Any] = field(default_factory=dict)
