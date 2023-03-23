from dataclasses import dataclass, field
from typing import Optional, Self

from .mod_par_model import A2LModPar

from .characteristic_model import (
    A2LCharacteristic,
    A2LMeasurement,
    A2LCharacteristicTypedef,
)
from .model import (
    A2LAxisPts,
    A2LBlob,
    A2LCompuMethod,
    A2LCompuTab,
    A2LCompuVTab,
    A2LCompuVTabRange,
    A2LInstance,
    A2LModCommon,
    A2LRecordLayout,
    A2LStructure,
    A2LTransformer,
)


@dataclass
class A2LFunction:
    name: str
    description: str = ""
    ref_characteristics: list[A2LCharacteristic] = field(default_factory=list)
    def_characteristics: list[A2LCharacteristic] = field(default_factory=list)
    in_measurements: list[A2LMeasurement] = field(default_factory=list)
    out_measurements: list[A2LMeasurement] = field(default_factory=list)
    loc_measurements: list[A2LMeasurement] = field(default_factory=list)
    sub_functions: list[Self] = field(default_factory=list)
    version: str = None


@dataclass
class A2LGroup:
    name: str
    description: str = ""
    characteristics: list[A2LCharacteristic] = field(default_factory=list)
    measurements: list[A2LMeasurement] = field(default_factory=list)
    sub_groups: list[Self] = field(default_factory=list)
    function_lists: list[A2LFunction] = field(default_factory=list)


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
    functions: list[A2LFunction] = field(default_factory=list)
    mod_common: list[A2LModCommon] = field(default_factory=list)
    mod_par: list[A2LModPar] = field(default_factory=list)
    record_layouts: list[A2LRecordLayout] = field(default_factory=list)
    typedef_characteristics: list[A2LCharacteristicTypedef] = field(
        default_factory=list
    )
    typedef_structures: list[A2LStructure] = field(default_factory=list)
    instances: list[A2LInstance] = field(default_factory=list)
    transformers: list[A2LTransformer] = field(default_factory=list)
    blobs: list[A2LBlob] = field(default_factory=list)


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
