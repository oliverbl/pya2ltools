from dataclasses import dataclass, field
import enum
from typing import Self, Tuple

from .compu_methods import A2LCompuMethod


@dataclass
class A2LAnnotation:
    label: str
    origin: str
    text: str


@dataclass
class A2LRecordLayoutAxisPts:
    axis: str
    position: int
    datatype: str
    index_mode: str
    addressing_mode: str
    annotations: list[A2LAnnotation] = field(default_factory=list)


@dataclass
class A2LRecordLayoutNoAxisPts:
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
    fields: list[A2LRecordLayoutNoAxisPts | A2LRecordLayoutAxisPts | A2lFncValues] = field(default_factory=list)


@dataclass
class A2LAxisDescription:
    measurement: str  # or characteristic?
    compu_method: str | A2LCompuMethod
    size: int
    min: int
    max: int
    annotations: list[A2LAnnotation] = field(default_factory=list)
    monotony: str | None = None


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
    table_type: str | None = None
    values: dict[int, int] = field(default_factory=dict)
    default_value: float | None = None


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
    description : str
    deposit : str
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
    in_objects: list[str] = field(default_factory=list)
    out_objects: list[str] = field(default_factory=list)


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
    matrix_dim : list[int] | None = None


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
    reference: str
    ecu_address: int
    matrix_dim : list[int] | None = None
    display_identifier: str | None = None

@dataclass
class A2LAxisPts:
    name: str
    description: str
    ecu_address: int
    measurement: str
    record_layout: str
    offset: int
    compu_method: str
    max_number_sample_points : int
    min: int
    max: int
    display_identifier: str | None = None

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