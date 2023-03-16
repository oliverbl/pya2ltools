from dataclasses import dataclass, field
from typing import Tuple


@dataclass
class A2LAnnotation:
    label: str
    origin: str
    text: str


@dataclass
class A2LCompuMethod:
    name: str
    description: str
    format: str = ""
    conversion_type: str = ""
    compu_tab_ref: str = None


@dataclass
class A2LAxisPts:
    size: int
    datatype: str
    index_increment: str
    annotations: list[A2LAnnotation] = field(default_factory=list)


@dataclass
class A2lNoAxisPts:
    size: int
    datatype: str


@dataclass
class A2lFncValues:
    size: int
    datatype: str
    index_mode: str
    direct_or_indirect: str


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
    monotony : str = None

@dataclass
class A2LAxisDescriptionComAxis(A2LAxisDescription):
    axis_pts_ref: str = ""


@dataclass
class A2LAxisDescriptionFixAxis(A2LAxisDescription):
    par_dist: list[int] = field(default_factory=list)
    par_list : list[str] = field(default_factory=list)

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
    conversion_type: str = None


@dataclass
class A2LCompuVTab:
    name: str
    description: str
    fields: dict[int, str] = field(default_factory=dict)


@dataclass
class A2LCompuVTabRange:
    name: str
    description: str
    fields: dict[Tuple[int, int], str] = field(default_factory=dict)


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
