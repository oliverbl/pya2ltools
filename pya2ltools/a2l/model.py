from dataclasses import dataclass, field
from typing import Optional, Tuple


@dataclass
class A2LHeader:
    pass


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
    pass


@dataclass
class A2LModCommon:
    pass


@dataclass
class A2LModPar:
    pass


@dataclass
class A2LMeasurement:
    name: str = ""
    description: str = ""
    datatype: str = ""
    symbol_name: str = ""
    min: int = 0
    max: int = 0
    ecu_address: int = 0
    format: str = ""
    matrix_dim: list[int] = field(default_factory=list)


@dataclass
class A2LCharacteristic:
    name: str
    description: str
    record_layout: A2LRecordLayout = None


@dataclass
class A2LModule:
    name: str = ""
    description: str = ""
    characteristics: list[A2LCharacteristic] = field(default_factory=list)
    measurements: list[A2LMeasurement] = field(default_factory=list)
    compu_methods: list[A2LCompuMethod] = field(default_factory=list)
    axis_pts: list[A2LAxisPts] = field(default_factory=list)
    compu_tabs: list[A2LCompuTab] = field(default_factory=list)
    compu_vtabs: list[A2LCompuVTab] = field(default_factory=list)
    groups: list[A2LGroup] = field(default_factory=list)
    mod_common: list[A2LModCommon] = field(default_factory=list)
    mod_par: list[A2LModPar] = field(default_factory=list)


@dataclass
class A2LProject:
    name: str = ""
    description: str = ""
    modules: list[A2LModule] = field(default_factory=list)
    header: Optional[A2LHeader] = None


@dataclass
class A2lFile:
    project: A2LProject = None
    asap2_version: str = ""
    a2ml_version: str = ""
