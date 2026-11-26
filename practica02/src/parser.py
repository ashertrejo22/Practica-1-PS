"""Completar los casos de IMP++ en construye_nodo y la función desugar."""

from pathlib import Path
from lark import Lark, Token, Tree
if __package__:
    from .asa import (
        ASA, NUM, LOC, BOOL, PLUS, MINUS, TIMES, EQ, LE, NOT, AND, OR,
        SKIP, ASIG, SEQ, IF, WHILE, PROGRAMA, BLOQUE, TIPO, DECL,
        PRINT, NEG, INC, DEC, FOR
    )
else:
    from asa import (
        ASA, NUM, LOC, BOOL, PLUS, MINUS, TIMES, EQ, LE, NOT, AND, OR,
        SKIP, ASIG, SEQ, IF, WHILE, PROGRAMA, BLOQUE, TIPO, DECL,
        PRINT, NEG, INC, DEC, FOR
    )


def analiza(tokens: list[Token]) -> ASA:
    """Recibe una lista de tokens y devuelve el ASA desendulzado."""

    # 1. Obtener la ruta del módulo del analizador sintáctico
    archivo_actual = Path(__file__)

    # 2. Obtener la ruta del archivo con la gramática
    archivo_gramatica = archivo_actual.with_name("grammars.lark")

    # 3. Leer la gramática
    gramatica = archivo_gramatica.read_text(encoding="utf-8")

    # 4. Construir el analizador sintáctico
    analizador = Lark(
        gramatica,
        parser="lalr", # Análisis ascendente usando LALR(1)
        lexer="basic",
        start="programa", # Indicamos el símbolo inicial
        propagate_positions=True
    )

    # 5. Crear una sesión de análisis sintáctico interactivo
    sesion = analizador.parse_interactive()

    # 6. Entregar los tokens al parser uno por uno
    # La sesión recibe los tokens que ya produjo el analizador léxico.
    for token in tokens:
        sesion.feed_token(token)

    # 7. Indicar que ya no hay más tokens
    arbol_sintactico = sesion.feed_eof()

    # 8. Convertir el árbol de análisis sintáctico de Lark en un ASA
    asa = construye_asa(arbol_sintactico)

    # 9. Devolver el ASA
    return asa


# Estos tokens contienen los datos que se guardan en las hojas del ASA.
DATOS = {"NUM", "LOC", "TRUE", "FALSE"}


def construye_asa(arbol: Tree | Token) -> ASA:
    """Construye los nodos y devuelve el ASA desendulzado."""

    # 1. Construir los nodos del ASA a partir del árbol de Lark.
    asa = construye_nodo(arbol)

    # 2. Eliminar el azúcar sintáctica antes de devolver el ASA.
    return desugar(asa)


def construye_nodo(arbol: Tree | Token) -> ASA:
    """Convierte recursivamente un Tree de Lark en un ASA."""

    # 1. Caso base de la recursión:
    #    convertir los tokens que contienen datos en hojas del ASA.
    if isinstance(arbol, Token):

        if arbol.type == "NUM":
            return NUM(int(arbol.value))

        if arbol.type == "LOC":
            return LOC(str(arbol.value))

        if arbol.type == "TRUE":
            return BOOL(True)

        if arbol.type == "FALSE":
            return BOOL(False)

        raise ValueError(f"Token inesperado: {arbol.type}")

    # 2. Obtener el nombre de la regla de producción
    #    utilizada por Lark para construir este nodo.
    regla = str(arbol.data)

    # 3. Eliminar los tokens que pertenecen únicamente
    #    a la sintaxis concreta. El nombre de la regla
    #    ya indica qué operación o comando se debe construir.
    hijos = [
        hijo
        for hijo in arbol.children
        if not isinstance(hijo, Token) or hijo.type in DATOS
    ]

    # 4. Los paréntesis no forman parte del ASA.
    if regla == "parentesis":
        return construye_nodo(hijos[0])

    # 5. Si una producción sólo envuelve un dato o comando,
    #    continuar recursivamente con ese contenido.
    if regla in {"numero", "variable", "verdadero", "falso", "sentencia", "actualizacion"}:
        return construye_nodo(hijos[0])

    # 6. Construir recursivamente los hijos.
    hijos_asa = [
        construye_nodo(hijo)
        for hijo in hijos
    ]

    # 7. Construir el nodo del ASA correspondiente.
    if regla == "programa":
        return PROGRAMA(hijos_asa)

    if regla == "bloque":
        return BLOQUE(hijos_asa)

    if regla == "suma":
        return PLUS(
            hijos_asa[0],
            hijos_asa[1]
        )

    if regla == "resta":
        return MINUS(
            hijos_asa[0],
            hijos_asa[1]
        )

    if regla == "multiplicacion":
        return TIMES(
            hijos_asa[0],
            hijos_asa[1]
        )

    if regla == "igualdad":
        return EQ(
            hijos_asa[0],
            hijos_asa[1]
        )

    if regla == "menor_igual":
        return LE(
            hijos_asa[0],
            hijos_asa[1]
        )

    if regla == "negacion":
        return NOT(
            hijos_asa[0]
        )

    if regla == "conjuncion":
        return AND(
            hijos_asa[0],
            hijos_asa[1]
        )

    if regla == "disyuncion":
        return OR(
            hijos_asa[0],
            hijos_asa[1]
        )

    if regla == "omitir":
        return SKIP()

    if regla == "asignacion":
        return ASIG(
            hijos_asa[0],
            hijos_asa[1]
        )

    if regla == "secuencia":
        return SEQ(
            hijos_asa[0],
            hijos_asa[1]
        )

    if regla == "condicional":
        return IF(
            hijos_asa[0],
            hijos_asa[1],
            hijos_asa[2]
        )

    if regla == "mientras":
        return WHILE(
            hijos_asa[0],
            hijos_asa[1]
        )

    if regla == "tipo_int":
        return TIPO("int")

    if regla == "tipo_bool":
        return TIPO("bool")

    if regla == "declaracion":
        return DECL(
            hijos_asa[0],
            hijos_asa[1],
            hijos_asa[2]
        )

    if regla == "impresion":
        return PRINT(
            hijos_asa[0]
        )

    if regla == "negativo":
        return NEG(
            hijos_asa[0]
        )

    if regla == "incremento":
        return INC(
            hijos_asa[0]
        )

    if regla == "decremento":
        return DEC(
            hijos_asa[0]
        )

    if regla == "ciclo_for":
        return FOR(
            hijos_asa[0],
            hijos_asa[1],
            hijos_asa[2],
            hijos_asa[3]
        )

    # 8. Detectar producciones que todavía no tienen
    #    una representación definida en el ASA.
    raise ValueError(f"Producción no reconocida: {regla}")


def desugar(arbol: ASA) -> ASA:
    """Devuelve un ASA equivalente sin incrementos, decrementos ni for."""

    if isinstance(arbol, INC):
        return ASIG(arbol.variable, PLUS(arbol.variable, NUM(1)))

    if isinstance(arbol, DEC):
        return ASIG(arbol.variable, MINUS(arbol.variable, NUM(1)))

    if isinstance(arbol, FOR):
        inicio = desugar(arbol.inicio)
        condicion = desugar(arbol.condicion)
        cuerpo = desugar(arbol.cuerpo)
        actualizacion = desugar(arbol.actualizacion)
        return SEQ(inicio, WHILE(condicion, SEQ(cuerpo, actualizacion)))

    if isinstance(arbol, PROGRAMA):
        return PROGRAMA([desugar(e) for e in arbol.elementos])

    if isinstance(arbol, BLOQUE):
        return BLOQUE([desugar(e) for e in arbol.elementos])

    if isinstance(arbol, DECL):
        return DECL(arbol.tipo_declarado, arbol.variable, desugar(arbol.expresion))

    if isinstance(arbol, ASIG):
        return ASIG(arbol.variable, desugar(arbol.expresion))

    if isinstance(arbol, SEQ):
        return SEQ(desugar(arbol.primero), desugar(arbol.segundo))

    if isinstance(arbol, IF):
        return IF(desugar(arbol.condicion), desugar(arbol.entonces), desugar(arbol.si_no))

    if isinstance(arbol, WHILE):
        return WHILE(desugar(arbol.condicion), desugar(arbol.cuerpo))

    if isinstance(arbol, (PRINT, NOT, NEG)):
        return type(arbol)(desugar(arbol.expresion))

    if isinstance(arbol, (PLUS, MINUS, TIMES, EQ, LE, AND, OR)):
        return type(arbol)(desugar(arbol.izquierda), desugar(arbol.derecha))

    return arbol
