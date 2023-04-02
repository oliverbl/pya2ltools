from dataclasses import dataclass, field
from typing import Any

from .model import A2LCompuTab


@dataclass
class A2LCompuMethod:
    name: str
    description: str
    format: str
    unit: str


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
