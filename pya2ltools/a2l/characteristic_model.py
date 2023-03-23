from dataclasses import dataclass, field

from .mod_par_model import A2LIfData

from .model import A2LAnnotation, A2LAxisDescription, A2LCompuMethod, A2LRecordLayout


@dataclass
class VirtualMeasurement:
    variables: list[str] = field(default_factory=list)


@dataclass
class A2LMeasurement:
    name: str = ""
    description: str = ""
    datatype: str = ""
    compu_method: str = ""
    display_identifier: str = ""
    min: int = 0
    max: int = 0
    ecu_address: int = 0
    bitmask: int | None = None
    format: str = ""
    matrix_dim: list[int] = field(default_factory=list)
    annotations: list[A2LAnnotation] = field(default_factory=list)
    discrete: bool = False
    virtual: VirtualMeasurement | None = None
    if_data: list[A2LIfData] = field(default_factory=list)


@dataclass
class DependentCharacteristic:
    formula: str
    variables: list[str] = field(default_factory=list)


@dataclass
class VirtualCharacteristic:
    formula: str
    variables: list[str] = field(default_factory=list)


@dataclass
class A2LCharacteristicTypedefInternal:
    record_layout: A2LRecordLayout
    maxdiff: int  # TODO find out what this is
    compu_method: str | A2LCompuMethod
    min: int
    max: int
    extended_min: int | None = None
    extended_max: int | None = None
    format: str | None = None
    bitmask: int | None = None
    phys_unit: str | None = None
    discrete: bool = False


@dataclass
class A2LCharacteristicValue(A2LCharacteristicTypedefInternal):
    pass


@dataclass
class A2LCharacteristicArray(A2LCharacteristicTypedefInternal):
    matrix_dim: list[int] = field(default_factory=list)


@dataclass
class A2LCharactersiticAscii(A2LCharacteristicTypedefInternal):
    size: int | None = None


@dataclass
class A2LCharacteristicCurve(A2LCharacteristicTypedefInternal):
    axis_descriptions: list[A2LAxisDescription] = field(default_factory=list)


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
    matrix_dim: list[int] | None = None


@dataclass
class A2LCharacteristicTypedef:
    typedef: A2LCharacteristicTypedefInternal
    name: str
    description: str
