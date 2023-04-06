from dataclasses import dataclass, field
from symtable import Symbol
from typing import Any

from .compu_methods import A2LCompuMethod

from .mod_par_model import A2LIfData

from .model import A2LAnnotation, A2LRecordLayout


@dataclass
class SymbolLink:
    symbol_name: str
    offset: int


@dataclass
class VirtualMeasurement:
    variables: list[str] = field(default_factory=list)


@dataclass
class A2LMeasurement:
    name: str
    description: str
    datatype: str
    compu_method: A2LCompuMethod
    display_identifier: str = None
    offset_1: int = 0
    offset_2: int = 0
    min: int = 0
    max: int = 0
    ecu_address: int = 0
    bitmask: int | None = None
    format: str = None
    matrix_dim: list[int] = None
    annotations: list[A2LAnnotation] = field(default_factory=list)
    discrete: bool = False
    virtual: VirtualMeasurement | None = None
    if_data: list[A2LIfData] = field(default_factory=list)
    symbol_link: SymbolLink | None = None

    def resolve_references(self, references: dict[str, Any]):
        self.compu_method = references[self.compu_method]


@dataclass
class A2LAxisDescription:
    measurement: A2LMeasurement
    compu_method: A2LCompuMethod
    size: int
    min: int
    max: int
    annotations: list[A2LAnnotation] = field(default_factory=list)
    monotony: str | None = None

    def resolve_references(self, references: dict[str, Any]):
        self.compu_method = references[self.compu_method]
        if self.measurement == "NO_INPUT_QUANTITY":
            self.measurement = None
        else:
            self.measurement = references[self.measurement]


@dataclass
class A2LAxisDescriptionComAxis(A2LAxisDescription):
    axis_pts_ref: str = None

    def resolve_references(self, references: dict[str, Any]):
        self.axis_pts_ref = references[self.axis_pts_ref]
        return super().resolve_references(references)


@dataclass
class A2LAxisDescriptionFixAxis(A2LAxisDescription):
    par_dist: list[int] = field(default_factory=list)
    par_list: list[str] = field(default_factory=list)


@dataclass
class A2LAxisDescriptionCurveAxis(A2LAxisDescription):
    curve_axis_ref: str = ""

    def resolve_references(self, references: dict[str, Any]):
        super().resolve_references(references)
        self.curve_axis_ref = references[self.curve_axis_ref]


@dataclass
class A2LAxisDescriptionResAxis(A2LAxisDescriptionComAxis):
    pass


A2LCharacteristic = "Placeholder"


@dataclass
class DependentCharacteristic:
    formula: str
    variables: list[A2LCharacteristic] = field(default_factory=list)

    def resolve_references(self, references: dict[str, Any]):
        self.variables = [references[variable] for variable in self.variables]


@dataclass
class VirtualCharacteristic(DependentCharacteristic):
    pass


@dataclass
class A2LCharacteristicTypedefInternal:
    record_layout: A2LRecordLayout
    maxdiff: int  # TODO find out what this is
    compu_method: A2LCompuMethod
    min: int
    max: int
    extended_min: int | None = None
    extended_max: int | None = None
    format: str | None = None
    bitmask: int | None = None
    phys_unit: str | None = None
    discrete: bool = False

    def resolve_references(self, references: dict[str, Any]):
        self.compu_method = references[self.compu_method]
        self.record_layout = references[self.record_layout]


@dataclass
class A2LCharacteristicValue(A2LCharacteristicTypedefInternal):
    pass


@dataclass
class A2LCharacteristicArray(A2LCharacteristicTypedefInternal):
    matrix_dim: list[int] = field(default_factory=list)


@dataclass
class A2LCharacteristicAscii(A2LCharacteristicTypedefInternal):
    size: int | None = None


@dataclass
class A2LCharacteristicCurve(A2LCharacteristicTypedefInternal):
    axis_descriptions: list[A2LAxisDescription] = field(default_factory=list)

    def resolve_references(self, references: dict[str, Any]):
        super().resolve_references(references)
        for axis_description in self.axis_descriptions:
            axis_description.resolve_references(references)


@dataclass
class A2LCharacteristicMap(A2LCharacteristicCurve):
    pass


@dataclass
class A2LCharacteristicCuboid(A2LCharacteristicCurve):
    pass


@dataclass
class A2LCharacteristicCube4(A2LCharacteristicCurve):
    pass


@dataclass
class A2LCharacteristic:
    typedef: A2LCharacteristicTypedefInternal
    name: str
    description: str
    ecu_address: int
    display_identifier: str | None = None
    annotations: list[A2LAnnotation] = field(default_factory=list)
    dependent_characteristic: DependentCharacteristic | None = None
    virtual_characteristic: VirtualCharacteristic | None = None
    model_link: str | None = None
    symbol_link: SymbolLink | None = None

    def resolve_references(self, references: dict[str, Any]):
        self.typedef.resolve_references(references)
        if self.dependent_characteristic is not None:
            self.dependent_characteristic.resolve_references(references)
        if self.virtual_characteristic is not None:
            self.virtual_characteristic.resolve_references(references)


@dataclass
class A2LCharacteristicTypedef:
    typedef: A2LCharacteristicTypedefInternal
    name: str
    description: str

    def resolve_references(self, references: dict[str, Any]):
        self.typedef.resolve_references(references)


@dataclass
class A2LAxisPts:
    name: str
    description: str
    ecu_address: int
    measurement: A2LMeasurement
    record_layout: A2LRecordLayout
    offset: int
    compu_method: A2LCompuMethod
    max_number_sample_points: int
    min: int
    max: int
    display_identifier: str | None = None
    symbol_link: SymbolLink | None = None

    def resolve_references(self, references: dict[str, Any]):
        self.record_layout = references[self.record_layout]
        self.compu_method = references[self.compu_method]
        self.measurement = references[self.measurement]


@dataclass
class A2LTypedefAxis:
    name: str
    description: str
    measurement: str
    record_layout: str
    max_diff: float
    compu_method: str
    max_number_of_axis_points: int
    lower_limit: int
    upper_limit: int

    def resolve_references(self, references: dict[str, Any]):
        self.record_layout = references[self.record_layout]
        self.compu_method = references[self.compu_method]
        self.measurement = references[self.measurement]
