import streamlit as st
import pandas as pd

# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================

st.set_page_config(
    page_title="LIM · TP-01",
    page_icon="🔢",
    layout="wide"
)

# =========================================================
# ESTADO
# =========================================================

if "celdas_elegidas" not in st.session_state:
    st.session_state.celdas_elegidas = []

if "ultima_celda_evento" not in st.session_state:
    st.session_state.ultima_celda_evento = None

if "filas_comparar" not in st.session_state:
    st.session_state.filas_comparar = []


# =========================================================
# FUNCIONES
# =========================================================

def crear_tabla():
    """
    Construye la tabla pitagórica 1 a 10.
    Filas y columnas conservan directamente los factores.
    """
    datos = {
        str(columna): [fila * columna for fila in range(1, 11)]
        for columna in range(1, 11)
    }

    df = pd.DataFrame(
        datos,
        index=range(1, 11)
    )

    df.index.name = "×"

    return df


def limpiar_celdas():
    st.session_state.celdas_elegidas = []
    st.session_state.ultima_celda_evento = None


def reiniciar():
    st.session_state.celdas_elegidas = []
    st.session_state.ultima_celda_evento = None
    st.session_state.filas_comparar = []


def estilizar_tabla(df, filas, celdas):
    """
    Resalta:
    - filas elegidas para comparar;
    - hasta dos celdas seleccionadas.
    """

    estilos = pd.DataFrame(
        "",
        index=df.index,
        columns=df.columns
    )

    # Filas comparadas
    for fila in filas:
        if fila in estilos.index:
            estilos.loc[fila, :] = (
                "background-color: rgba(59, 130, 246, 0.12);"
                "font-weight: 600;"
            )

    # Celdas seleccionadas
    for fila, columna in celdas:
        columna = str(columna)

        if fila in estilos.index and columna in estilos.columns:
            estilos.loc[fila, columna] = (
                "background-color: #2563eb;"
                "color: white;"
                "font-weight: 800;"
            )

    return df.style.apply(
        lambda _: estilos,
        axis=None
    )


# =========================================================
# DATOS
# =========================================================

tabla = crear_tabla()


# =========================================================
# ENCABEZADO
# =========================================================

st.caption("LIM · Laboratorio de Ideas Matemáticas · TP-01")

st.title("Mirar la tabla de otra manera")

st.write(
    """
La tabla pitagórica reúne muchos productos.

En este laboratorio te proponemos **mirarla como una red de relaciones**.

Podés elegir productos, comparar filas y preguntarte qué cambia y qué permanece.
"""
)

st.divider()


# =========================================================
# 1. EXPLORAR PRODUCTOS
# =========================================================

st.subheader("1. Elegí productos para mirar")

st.write(
    """
Tocá una celda de la tabla.

Podés elegir hasta **dos productos** para compararlos.
"""
)


# ---------------------------------------------------------
# Selector de filas
# ---------------------------------------------------------

filas_comparar = st.multiselect(
    "Si querés, elegí también una o dos filas para compararlas:",
    options=list(range(1, 11)),
    default=st.session_state.filas_comparar,
    max_selections=2,
    placeholder="Elegí una o dos filas"
)

st.session_state.filas_comparar = filas_comparar


# ---------------------------------------------------------
# Estilo actual
# ---------------------------------------------------------

tabla_estilizada = estilizar_tabla(
    tabla,
    st.session_state.filas_comparar,
    st.session_state.celdas_elegidas
)


# ---------------------------------------------------------
# Tabla interactiva
# ---------------------------------------------------------

evento = st.dataframe(
    tabla_estilizada,
    key="tabla_pitagorica",
    width="stretch",
    height=395,
    row_height=34,
    on_select="rerun",
    selection_mode="single-cell",
    lazy=False,
    column_config={
        "_index": st.column_config.NumberColumn(
            "×",
            format="%d",
            width="small"
        ),
        **{
            str(n): st.column_config.NumberColumn(
                str(n),
                format="%d",
                width="small"
            )
            for n in range(1, 11)
        }
    }
)


# =========================================================
# REGISTRAR LA CELDA TOCADA
# =========================================================

celdas_evento = evento.selection.cells

if celdas_evento:

    fila_posicion, columna_nombre = celdas_evento[0]

    # La posición 0 corresponde a la fila del 1
    fila = fila_posicion + 1
    columna = int(columna_nombre)

    celda_actual = (fila, columna)

    # Solo procesamos si es un evento nuevo
    if celda_actual != st.session_state.ultima_celda_evento:

        st.session_state.ultima_celda_evento = celda_actual

        # Si ya estaba elegida, no la repetimos
        if celda_actual not in st.session_state.celdas_elegidas:

            # Conservamos solamente las dos últimas
            if len(st.session_state.celdas_elegidas) >= 2:
                st.session_state.celdas_elegidas.pop(0)

            st.session_state.celdas_elegidas.append(celda_actual)

        # Necesitamos un rerun para que aparezca
        # inmediatamente el resaltado de la celda
        st.rerun()

else:
    st.session_state.ultima_celda_evento = None


# =========================================================
# PRODUCTOS ELEGIDOS
# =========================================================

st.markdown("### Productos que elegiste")

celdas = st.session_state.celdas_elegidas

if len(celdas) == 0:

    st.caption(
        "Todavía no elegiste ningún producto."
    )


else:

    columnas_resultados = st.columns(len(celdas))

    for indice, (fila, columna) in enumerate(celdas):

        producto = fila * columna

        with columnas_resultados[indice]:

            st.markdown(
                f"""
                <div style="
                    border:1px solid rgba(128,128,128,.35);
                    border-radius:12px;
                    padding:14px;
                    text-align:center;
                    margin-bottom:8px;
                ">
                    <div style="font-size:1.35rem;font-weight:700;">
                        {fila} × {columna} = {producto}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


# ---------------------------------------------------------
# Dos productos
# ---------------------------------------------------------

if len(celdas) == 2:

    (f1, c1), (f2, c2) = celdas

    p1 = f1 * c1
    p2 = f2 * c2

    st.markdown("#### Mirá los dos productos")

    if p1 == p2:

        st.info(
            "Los dos productos dan el mismo resultado. "
            "¿Qué cambió entre una multiplicación y la otra? "
            "¿Qué se mantuvo?"
        )

    elif c1 == c2:

        st.info(
            f"Los dos productos están en la misma columna, la del {c1}. "
            "¿Qué relación encontrás entre ellos?"
        )

    elif f1 == f2:

        st.info(
            f"Los dos productos están en la misma fila, la del {f1}. "
            "¿Qué relación encontrás entre ellos?"
        )

    else:

        st.info(
            "¿Encontrás alguna relación entre los productos que elegiste?"
        )


if len(celdas) > 0:

    st.button(
        "Limpiar productos elegidos",
        on_click=limpiar_celdas
    )


# =========================================================
# 2. COMPARAR FILAS
# =========================================================

st.divider()

st.subheader("2. Compará filas")

if len(st.session_state.filas_comparar) == 0:

    st.write(
        """
Elegí una o dos filas en el selector que está arriba de la tabla.

Cuando las selecciones, quedarán destacadas para que puedas mirarlas con más atención.
"""
    )


elif len(st.session_state.filas_comparar) == 1:

    fila = st.session_state.filas_comparar[0]

    st.write(
        f"Elegiste la fila del **{fila}**."
    )

    productos = [
        fila * columna
        for columna in range(1, 11)
    ]

    st.write(
        " · ".join(str(x) for x in productos)
    )

    st.info(
        "Elegí otra fila. ¿Qué te gustaría comparar con esta?"
    )


elif len(st.session_state.filas_comparar) == 2:

    fila1, fila2 = st.session_state.filas_comparar

    st.write(
        f"Estás comparando las filas del **{fila1}** y del **{fila2}**."
    )

    comparacion = pd.DataFrame(
        {
            "Columna": range(1, 11),
            f"Fila del {fila1}": [
                fila1 * n for n in range(1, 11)
            ],
            f"Fila del {fila2}": [
                fila2 * n for n in range(1, 11)
            ]
        }
    )

    st.dataframe(
        comparacion,
        hide_index=True,
        width="stretch"
    )

    st.info(
        "Mirá los números que ocupan la misma columna. "
        "¿Encontrás alguna relación que se repita?"
    )

    st.write(
        "Probá elegir una columna y anticipar qué número debería aparecer "
        "en cada una de las dos filas."
    )


# =========================================================
# CIERRE PROVISORIO
# =========================================================

st.divider()

st.subheader("Antes de seguir")

st.write(
    """
Por ahora no buscamos nombrar propiedades.

Nos interesa encontrar relaciones que aparezcan en la tabla y que podamos explicar.
"""
)

hallazgo = st.text_area(
    "Una relación que encontré...",
    placeholder="Me di cuenta de que...",
    height=90
)

if hallazgo.strip():

    st.success(
        "Guardá esta idea. Más adelante podremos ponerla a prueba "
        "con otros productos."
    )


# =========================================================
# REINICIAR
# =========================================================

st.divider()

st.button(
    "↺ Empezar de nuevo",
    on_click=reiniciar
)

st.caption(
    "TP-01 · Mirar la tabla de otra manera · "
    "LIM – Laboratorio de Ideas Matemáticas"
)
