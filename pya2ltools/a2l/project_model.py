from dataclasses import dataclass, field
from typing import Optional

from .characteristic_model import A2LCharacteristic, A2LMeasurement
from .model import (
    A2LAxisPts,
    A2LCompuMethod,
    A2LCompuTab,
    A2LCompuVTab,
    A2LCompuVTabRange,
    A2LGroup,
    A2LModCommon,
    A2LModPar,
    A2LRecordLayout,
)


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
    compu_vtab_ranges: list[A2LCompuVTabRange] = field(default_factory=list)
    groups: list[A2LGroup] = field(default_factory=list)
    mod_common: list[A2LModCommon] = field(default_factory=list)
    mod_par: list[A2LModPar] = field(default_factory=list)
    record_layouts: list[A2LRecordLayout] = field(default_factory=list)


@dataclass
class A2LHeader:
    pass


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
