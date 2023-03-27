from dataclasses import dataclass, field
import enum
from typing import Any, Self, Tuple


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
    fields: list[
        A2LRecordLayoutNoAxisPts | A2LRecordLayoutAxisPts | A2lFncValues
    ] = field(default_factory=list)


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
