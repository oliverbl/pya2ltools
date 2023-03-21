from dataclasses import dataclass, field
from typing import Tuple

from .compu_methods import A2LCompuMethod


@dataclass
class A2LAnnotation:
    label: str
    origin: str
    text: str


@dataclass
class A2LAxisPts:
    axis: str
    position: int
    datatype: str
    index_mode: str
    addressing_mode: str
    annotations: list[A2LAnnotation] = field(default_factory=list)


@dataclass
class A2lNoAxisPts:
    axis: str
    position: int
    datatype: str


@dataclass
class A2lLRescaleAxis:
    axis: str
    position: int
    datatype: str
    map_position: int
    index_mode: str
    addressing_mode: str
    annotations: list[A2LAnnotation] = field(default_factory=list)


@dataclass
class A2lFncValues:
    position: int
    datatype: str
    index_mode: str
    addressing_mode: str


@dataclass
class A2LRecordLayout:
    name: str = ""
    fields: list[A2lNoAxisPts | A2LAxisPts | A2lFncValues] = field(default_factory=list)


@dataclass
class A2LAxisDescription:
    measurement: str  # or characteristic?
    compu_method: str | A2LCompuMethod
    size: int
    min: int
    max: int
    annotations: list[A2LAnnotation] = field(default_factory=list)
    monotony: str = None


@dataclass
class A2LAxisDescriptionComAxis(A2LAxisDescription):
    axis_pts_ref: str = ""


@dataclass
class A2LAxisDescriptionFixAxis(A2LAxisDescription):
    par_dist: list[int] = field(default_factory=list)
    par_list: list[str] = field(default_factory=list)


@dataclass
class A2LAxisDescriptionCurveAxis(A2LAxisDescription):
    curve_axis_ref: str = ""


@dataclass
class A2LAxisDescriptionResAxis(A2LAxisDescriptionComAxis):
    pass


@dataclass
class A2LCompuTab:
    name: str
    description: str
    table_type: str = None
    values: dict[int, int] = field(default_factory=dict)
    default_value: float = None


@dataclass
class A2LCompuVTab:
    name: str
    description: str
    values: dict[int, str] = field(default_factory=dict)
    default_value: str = None


@dataclass
class A2LCompuVTabRange:
    name: str
    description: str
    values: dict[Tuple[int, int], str] = field(default_factory=dict)
    default_value: str = None


@dataclass
class A2LGroup:
    members: list[str] = field(default_factory=list)
    annotations: list[A2LAnnotation] = field(default_factory=list)


@dataclass
class A2LModCommon:
    pass


@dataclass
class A2LModPar:
    pass
