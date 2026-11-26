from dataclasses import dataclass


class ASA:
    """Clase base para los nodos del árbol de sintaxis abstracta."""
    pass


@dataclass(frozen=True)
class NUM(ASA):
    valor: int


@dataclass(frozen=True)
class LOC(ASA):
    nombre: str


@dataclass(frozen=True)
class BOOL(ASA):
    valor: bool


@dataclass(frozen=True)
class PLUS(ASA):
    izquierda: ASA
    derecha: ASA


@dataclass(frozen=True)
class MINUS(ASA):
    izquierda: ASA
    derecha: ASA


@dataclass(frozen=True)
class TIMES(ASA):
    izquierda: ASA
    derecha: ASA


@dataclass(frozen=True)
class EQ(ASA):
    izquierda: ASA
    derecha: ASA


@dataclass(frozen=True)
class LE(ASA):
    izquierda: ASA
    derecha: ASA


@dataclass(frozen=True)
class NOT(ASA):
    expresion: ASA


@dataclass(frozen=True)
class AND(ASA):
    izquierda: ASA
    derecha: ASA


@dataclass(frozen=True)
class OR(ASA):
    izquierda: ASA
    derecha: ASA


@dataclass(frozen=True)
class SKIP(ASA):
    pass


@dataclass(frozen=True)
class ASIG(ASA):
    variable: LOC
    expresion: ASA


@dataclass(frozen=True)
class SEQ(ASA):
    primero: ASA
    segundo: ASA


@dataclass(frozen=True)
class IF(ASA):
    condicion: ASA
    entonces: ASA
    si_no: ASA


@dataclass(frozen=True)
class WHILE(ASA):
    condicion: ASA
    cuerpo: ASA


@dataclass(frozen=True)
class PROGRAMA(ASA):
    elementos: list[ASA]


@dataclass(frozen=True)
class BLOQUE(ASA):
    elementos: list[ASA]


@dataclass(frozen=True)
class TIPO(ASA):
    nombre: str


@dataclass(frozen=True)
class DECL(ASA):
    tipo_declarado: TIPO
    variable: LOC
    expresion: ASA


@dataclass(frozen=True)
class PRINT(ASA):
    expresion: ASA


@dataclass(frozen=True)
class NEG(ASA):
    expresion: ASA


@dataclass(frozen=True)
class INC(ASA):
    variable: LOC


@dataclass(frozen=True)
class DEC(ASA):
    variable: LOC


@dataclass(frozen=True)
class FOR(ASA):
    inicio: ASA
    condicion: ASA
    actualizacion: ASA
    cuerpo: ASA