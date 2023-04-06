from dataclasses import dataclass, field
from typing import Any, Optional, Self

from .compu_methods import A2LCompuMethod

from .mod_par_model import A2LModPar, A2LIfData

from .characteristic_model import (
    A2LAxisPts,
    A2LCharacteristic,
    A2LMeasurement,
    A2LCharacteristicTypedef,
    A2LTypedefAxis,
)
from .model import (
    A2LBlob,
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
    version: str | None = None

    def resolve_references(self, references: dict[str, Any]):
        self.ref_characteristics = [references[c] for c in self.ref_characteristics]
        self.def_characteristics = [references[c] for c in self.def_characteristics]
        self.in_measurements = [references[m] for m in self.in_measurements]
        self.out_measurements = [references[m] for m in self.out_measurements]
        self.loc_measurements = [references[m] for m in self.loc_measurements]
        self.sub_functions = [references[f] for f in self.sub_functions]


@dataclass
class A2LGroup:
    name: str
    description: str = ""
    root: bool = False
    characteristics: list[A2LCharacteristic] = field(default_factory=list)
    measurements: list[A2LMeasurement] = field(default_factory=list)
    sub_groups: list[Self] = field(default_factory=list)
    function_lists: list[A2LFunction] = field(default_factory=list)

    def resolve_references(self, references: dict[str, Any]):
        self.characteristics = [references[c] for c in self.characteristics]
        self.measurements = [references[m] for m in self.measurements]
        self.sub_groups = [references[g] for g in self.sub_groups]
        self.function_lists = [references[f] for f in self.function_lists]


@dataclass
class A2ML:
    content: str


@dataclass
class A2LModule:
    name: str = ""
    description: str = ""
    a2ml: list[A2ML] = field(default_factory=list)
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
    typedef_axes: list[A2LTypedefAxis] = field(default_factory=list)
    instances: list[A2LInstance] = field(default_factory=list)
    transformers: list[A2LTransformer] = field(default_factory=list)
    blobs: list[A2LBlob] = field(default_factory=list)
    if_data: list[A2LIfData] = field(default_factory=list)
    global_list: list[Any] = field(default_factory=list)
    _reference_dict: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self._reference_dict = {"NO_COMPU_METHOD": None}
        for item in self.global_list:
            if hasattr(item, "name"):
                self._reference_dict[item.name] = item
        for item in self.global_list:
            if hasattr(item, "resolve_references"):
                item.resolve_references(self._reference_dict)

    def get_addressable_objects(self):
        return self.characteristics + self.measurements + self.axis_pts

    def __add__(self, other):
        if isinstance(other, A2LModule):
            self.characteristics += other.characteristics
            self.measurements += other.measurements
            self.compu_methods += other.compu_methods
            self.axis_pts += other.axis_pts
            self.compu_tabs += other.compu_tabs
            self.compu_vtabs += other.compu_vtabs
            self.compu_vtab_ranges += other.compu_vtab_ranges
            self.groups += other.groups
            self.functions += other.functions
            self.mod_common += other.mod_common
            self.mod_par += other.mod_par
            self.record_layouts += other.record_layouts
            self.typedef_characteristics += other.typedef_characteristics
            self.typedef_structures += other.typedef_structures
            self.typedef_axes += other.typedef_axes
            self.instances += other.instances
            self.transformers += other.transformers
            self.blobs += other.blobs
            self.if_data += other.if_data
            self.global_list += other.global_list
            self._reference_dict.update(other._reference_dict)
        return self


@dataclass
class A2LHeader:
    description: str
    project_number: str
    version: str


@dataclass
class A2LProject:
    name: str = ""
    description: str = ""
    modules: list[A2LModule] = field(default_factory=list)
    header: Optional[A2LHeader] = None


@dataclass
class A2lFile:
    project: A2LProject
    asap2_version: str = ""
    a2ml_version: str = ""

    def __add__(self, other):
        if isinstance(other, A2lFile):
            self.project.modules[0] += other.project.modules[0]
        return self
