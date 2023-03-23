from dataclasses import dataclass, field


@dataclass
class A2LCompuMethod:
    name: str
    description: str
    format: str = ""
    unit: str = ""


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
    formula_inv: str = ""


@dataclass
class A2LCompuMethodTableInterpolation(A2LCompuMethod):
    compu_tab_ref: str = ""
    values: dict[int, int] = field(default_factory=dict)
    default_value: float = None


@dataclass
class A2LCompuMethodTableNoInterpolation(A2LCompuMethod):
    compu_tab_ref: str = ""
    values: dict[int, int] = field(default_factory=dict)


@dataclass
class A2LCompuMethodVerbalTable(A2LCompuMethod):
    compu_tab_ref: str = ""
    values: dict[int, str] = field(default_factory=dict)
