from dataclasses import dataclass, field

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
    bitmask: int = None
    format: str = ""
    matrix_dim: list[int] = field(default_factory=list)
    annotations: list[A2LAnnotation] = field(default_factory=list)
    discrete: bool = False
    virtual: VirtualMeasurement = None


@dataclass
class DependentCharacteristic:
    formula: str
    variables: list[str] = field(default_factory=list)


@dataclass
class VirtualCharacteristic:
    formula: str
    variables: list[str] = field(default_factory=list)


@dataclass
class A2LCharacteristic:
    name: str
    description: str
    ecu_address: int
    record_layout: A2LRecordLayout
    unknown: int  # TODO find out what this is
    compu_method: str | A2LCompuMethod
    min: int
    max: int
    extended_min: int = None
    extended_max: int = None
    display_identifier: str = None
    format: str = None
    bitmask: int = None
    phys_unit: str = None
    annotations: list[A2LAnnotation] = field(default_factory=list)
    discrete: bool = False
    dependent_characteristic: DependentCharacteristic = None
    virtual_characteristic: VirtualCharacteristic = None
    model_link: str = None


@dataclass
class A2LCharacteristicValue(A2LCharacteristic):
    pass


@dataclass
class A2LCharacteristicArray(A2LCharacteristic):
    matrix_dim: list[int] = field(default_factory=list)


@dataclass
class A2LCharactersiticAscii(A2LCharacteristic):
    size: int = None


@dataclass
class A2LCharacteristicCurve(A2LCharacteristic):
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
