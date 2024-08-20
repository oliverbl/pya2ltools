from dataclasses import dataclass, field
import enum
from typing import Any, Self, Tuple

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


@dataclass
class A2LAnnotation:
    label: str
    origin: str
    text: str


@dataclass
class A2LBaseType:
    name: str
    signed: bool
    size: int

    @staticmethod
    def from_string(s):
        if s in base_types:
            return s
        raise ValueError(f"{s} not a valid base type")

@dataclass
class A2LCompuMethod:
    name: str
    description: str
    format: str
    unit: str

@dataclass
class A2LRecordLayoutAxisPts:
    axis: str
    position: int
    datatype: A2LBaseType
    index_mode: str
    addressing_mode: str
    annotations: list[A2LAnnotation] = field(default_factory=list)

    def __post__init__(self):
        self.datatype = A2LBaseType.from_string(self.datatype)

@dataclass
class A2LRecordLayoutNoAxisPts:
    axis: str
    position: int
    datatype: A2LBaseType

    def __post__init__(self):
        self.datatype = A2LBaseType.from_string(self.datatype)

@dataclass
class A2lLRescaleAxis:
    axis: str
    position: int
    datatype: A2LBaseType
    map_position: int
    index_mode: str
    addressing_mode: str
    annotations: list[A2LAnnotation] = field(default_factory=list)

    def __post__init__(self):
        self.datatype = A2LBaseType.from_string(self.datatype)

@dataclass
class A2lFncValues:
    position: int
    datatype: A2LBaseType
    index_mode: str
    addressing_mode: str

    def __post__init__(self):
        self.datatype = A2LBaseType.from_string(self.datatype)


@dataclass
class A2LRecordLayout:
    name: str = ""
    fields: list[
        A2LRecordLayoutNoAxisPts | A2LRecordLayoutAxisPts | A2lFncValues
    ] = field(default_factory=list)




@dataclass
class A2LCompuVTab:
    name: str
    description: str
    values: dict[int, str] = field(default_factory=dict)
    default_value: str | None = None


@dataclass
class A2LCompuVTabRange:
    name: str
    description: str
    values: dict[Tuple[int, int], str] = field(default_factory=dict)
    default_value: str | None = None


class ByteOrder(enum.Enum):
    MSB_LAST = "MSB_LAST"
    MSB_FIRST = "MSB_FIRST"


@dataclass
class A2LModCommon:
    description: str
    deposit: str
    byte_order: ByteOrder | None = None
    alignment_byte: int | None = None
    alignment_word: int | None = None
    alignment_long: int | None = None
    alignment_int64: int | None = None
    alignment_float32_ieee: int | None = None
    alignment_float64_ieee: int | None = None


@dataclass
class A2LTransformer:
    name: str
    version: str
    name_32bit_dll: str
    name_64bit_dll: str
    timeout_in_ms: int
    event: str
    reverse_transformer: str | Self
    in_objects: list[Any] = field(default_factory=list)
    out_objects: list[Any] = field(default_factory=list)

    def resolve_references(self, references: dict[str, Any]):
        self.reverse_transformer = references[self.reverse_transformer]
        self.in_objects = [references[obj] for obj in self.in_objects]
        self.out_objects = [references[obj] for obj in self.out_objects]


@dataclass
class A2LBlob:
    name: str
    description: str
    ecu_address: int
    number_of_bytes: int
    calibration_access: str


@dataclass
class A2LStructureComponent:
    name: str
    datatype: str
    offset: int
    matrix_dim: list[int] | None = None


@dataclass
class A2LStructure:
    name: str
    size: int
    description: str
    components: list[A2LStructureComponent] = field(default_factory=list)


@dataclass
class A2LInstance:
    name: str
    description: str
    reference: Any
    ecu_address: int
    matrix_dim: list[int] | None = None
    display_identifier: str | None = None

    def resolve_references(self, references: dict[str, Any]):
        self.reference = references[self.reference]




base_types = {
    "UBYTE": A2LBaseType(name="UBYTE", signed=False, size=1),
    "SBYTE": A2LBaseType(name="SBYTE", signed=True, size=1),
    "UWORD": A2LBaseType(name="UWORD", signed=False, size=2),
    "SWORD": A2LBaseType(name="SWORD", signed=True, size=2),
    "ULONG": A2LBaseType(name="ULONG", signed=False, size=4),
    "SLONG": A2LBaseType(name="SLONG", signed=True, size=4),
    "FLOAT32_IEEE": A2LBaseType(name="FLOAT32_IEEE", signed=True, size=4),
    "FLOAT64_IEEE": A2LBaseType(name="FLOATT64_IEEE", signed=True, size=8),
}


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
    datatype: A2LBaseType
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

@dataclass
class A2LCompuTab:
    name: str
    description: str
    table_type: str | None = None
    values: dict[int, int] = field(default_factory=dict)
    default_value: float | None = None





@dataclass
class A2LCompuMethodRational(A2LCompuMethod):
    coeffs: list[int] = field(default_factory=list)
    status_string_ref: str = None


@dataclass
class A2LCompuMethodLinear(A2LCompuMethod):
    coeffs: list[int] = field(default_factory=list)
    status_string_ref: str = None


@dataclass
class A2LCompuMethodFormula(A2LCompuMethod):
    formula: str = ""
    formula_inv: str = None


@dataclass
class A2LCompuMethodTableInterpolation(A2LCompuMethod):
    compu_tab_ref: A2LCompuTab
    values: dict[int, int] = field(default_factory=dict)
    default_value: float = None

    def resolve_references(self, references: dict[str, Any]):
        self.compu_tab_ref = references[self.compu_tab_ref]


@dataclass
class A2LCompuMethodTableNoInterpolation(A2LCompuMethod):
    compu_tab_ref: A2LCompuTab
    values: dict[int, int] = field(default_factory=dict)

    def resolve_references(self, references: dict[str, Any]):
        self.compu_tab_ref = references[self.compu_tab_ref]


@dataclass
class A2LCompuMethodVerbalTable(A2LCompuMethod):
    compu_tab_ref: A2LCompuTab
    values: dict[int, str] = field(default_factory=dict)

    def resolve_references(self, references: dict[str, Any]):
        self.compu_tab_ref = references[self.compu_tab_ref]
