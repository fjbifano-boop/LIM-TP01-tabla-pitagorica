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

if "registro_exploracion" not in st.session_state:
    st.session_state.registro_exploracion = []

if "observacion_actual" not in st.session_state:
    st.session_state.observacion_actual = ""


# =========================================================
# FUNCIONES
# =========================================================

def crear_tabla():
    """
    Construye la tabla pitagórica de 1 a 10.
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
    """
    Limpia los productos elegidos para iniciar
    una nueva exploración.
    """
    st.session_state.celdas_elegidas = []
    st.session_state.ultima_celda_evento = None
    st.session_state.observacion_actual = ""


def guardar_observacion():
    """
    Guarda el par de productos elegido junto con
    la observación escrita por el estudiante.
    """
    texto = st.session_state.observacion_actual.strip()

    if len(st.session_state.celdas_elegidas) == 2 and texto:

        (f1, c1), (f2, c2) = st.session_state.celdas_elegidas

        st.session_state.registro_exploracion.append(
            {
                "celda1": (f1, c1),
                "celda2": (f2, c2),
                "producto1": f1 * c1,
                "producto2": f2 * c2,
                "observacion": texto
            }
        )

        # Dejamos lista la tabla para buscar otro caso
        st.session_state.celdas_elegidas = []
        st.session_state.ultima_celda_evento = None
        st.session_state.observacion_actual = ""


def reiniciar():
    """
    Reinicia completamente el laboratorio.
    """
    st.session_state.celdas_elegidas = []
    st.session_state.ultima_celda_evento = None
    st.session_state.filas_comparar = []
    st.session_state.registro_exploracion = []
    st.session_state.observacion_actual = ""


def estilizar_tabla(df, filas, celdas):
    """
    Resalta filas elegidas y productos seleccionados.
    """

    estilos = pd.DataFrame(
        "",
        index=df.index,
        columns=df.columns
    )

    # Filas seleccionadas para comparar
    for fila in filas:
        if fila in estilos.index:
            estilos.loc[fila, :] = (
                "background-color: rgba(59, 130, 246, 0.12);"
                "font-weight: 600;"
            )

    # Productos seleccionados
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

Elegí productos, comparalos y registrá las relaciones que vayas encontrando.
"""
)

st.divider()


# =========================================================
# 1. EXPLORAR PRODUCTOS
# =========================================================

st.subheader("1. Elegí dos productos para mirar")

st.write(
    """
Tocá dos celdas de la tabla.

No tienen que cumplir ninguna condición especial:
**elegí dos productos que te interese comparar.**
"""
)


# =========================================================
# SELECTOR DE FILAS
# =========================================================

filas_comparar = st.multiselect(
    "Si querés, también podés destacar una o dos filas:",
    options=list(range(1, 11)),
    default=st.session_state.filas_comparar,
    max_selections=2,
    placeholder="Elegí una o dos filas"
)

st.session_state.filas_comparar = filas_comparar


# =========================================================
# TABLA INTERACTIVA
# =========================================================

tabla_estilizada = estilizar_tabla(
    tabla,
    st.session_state.filas_comparar,
    st.session_state.celdas_elegidas
)

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
# REGISTRAR CELDA TOCADA
# =========================================================

celdas_evento = evento.selection.cells

if celdas_evento:

    fila_posicion, columna_nombre = celdas_evento[0]

    fila = fila_posicion + 1
    columna = int(columna_nombre)

    celda_actual = (fila, columna)

    if celda_actual != st.session_state.ultima_celda_evento:

        st.session_state.ultima_celda_evento = celda_actual

        if celda_actual not in st.session_state.celdas_elegidas:

            if len(st.session_state.celdas_elegidas) >= 2:
                st.session_state.celdas_elegidas.pop(0)

            st.session_state.celdas_elegidas.append(celda_actual)

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
                    <div style="
                        font-size:1.35rem;
                        font-weight:700;
                    ">
                        {fila} × {columna} = {producto}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# OBSERVAR Y REGISTRAR UNA RELACIÓN
# =========================================================

if len(celdas) == 2:

    (f1, c1), (f2, c2) = celdas

    p1 = f1 * c1
    p2 = f2 * c2

    st.markdown("### Mirá los dos productos")

    # -----------------------------------------------------
    # Pregunta contextual
    # -----------------------------------------------------

    if p1 == p2:

        st.info(
            "Los dos productos dan el mismo resultado. "
            "**¿Qué cambió entre una multiplicación y la otra? "
            "¿Qué se mantuvo?**"
        )

    elif c1 == c2:

        st.info(
            f"Los dos productos están en la columna del **{c1}**. "
            "**¿Qué relación encontrás entre ellos?**"
        )

    elif f1 == f2:

        st.info(
            f"Los dos productos están en la fila del **{f1}**. "
            "**¿Qué relación encontrás entre ellos?**"
        )

    else:

        st.info(
            "**¿Encontrás alguna relación entre los productos "
            "que elegiste?**"
        )

    # -----------------------------------------------------
    # Respuesta abierta
    # -----------------------------------------------------

    st.text_area(
        "Escribí qué observás:",
        key="observacion_actual",
        placeholder=(
            "Podés escribir una relación que encontraste, "
            "algo que te llamó la atención o que no encontrás "
            "una relación todavía..."
        ),
        height=100
    )

    col_guardar, col_probar = st.columns(2)

    with col_guardar:

        st.button(
            "Guardar mi observación",
            on_click=guardar_observacion,
            use_container_width=True,
            disabled=not bool(
                st.session_state.observacion_actual.strip()
            )
        )

    with col_probar:

        st.button(
            "Probar con otros productos",
            on_click=limpiar_celdas,
            use_container_width=True
        )


elif len(celdas) == 1:

    st.info(
        "Elegí otro producto para poder compararlos."
    )

    st.button(
        "Cambiar el producto elegido",
        on_click=limpiar_celdas
    )


# =========================================================
# 2. MI EXPLORACIÓN
# =========================================================

if st.session_state.registro_exploracion:

    st.divider()

    st.subheader("2. Mi exploración")

    st.write(
        """
Estas son algunas de las relaciones que fuiste encontrando.
"""
    )

    for numero, registro in enumerate(
        st.session_state.registro_exploracion,
        start=1
    ):

        f1, c1 = registro["celda1"]
        f2, c2 = registro["celda2"]

        p1 = registro["producto1"]
        p2 = registro["producto2"]

        observacion = registro["observacion"]

        st.markdown(
            f"""
            <div style="
                border:1px solid rgba(128,128,128,.30);
                border-radius:12px;
                padding:16px;
                margin-bottom:12px;
            ">
                <div style="
                    font-size:.9rem;
                    opacity:.7;
                    margin-bottom:6px;
                ">
                    Observación {numero}
                </div>

                <div style="
                    font-size:1.1rem;
                    font-weight:700;
                    margin-bottom:8px;
                ">
                    {f1} × {c1} = {p1}
                    &nbsp;&nbsp; ↔ &nbsp;&nbsp;
                    {f2} × {c2} = {p2}
                </div>

                <div style="font-size:1rem;">
                    “{observacion}”
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # -----------------------------------------------------
    # Pregunta después de varias exploraciones
    # -----------------------------------------------------

    if len(st.session_state.registro_exploracion) >= 2:

        st.info(
            "Mirá las observaciones que guardaste. "
            "**¿Hay alguna relación que te gustaría probar "
            "con otros productos de la tabla?**"
        )


# =========================================================
# 3. COMPARAR FILAS
# =========================================================

st.divider()

st.subheader("3. Compará filas")

if len(st.session_state.filas_comparar) == 0:

    st.write(
        """
También podés mirar relaciones entre filas completas.

Elegí una o dos filas en el selector que está arriba de la tabla.
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
        "Elegí otra fila. "
        "**¿Qué te gustaría comparar con esta?**"
    )


elif len(st.session_state.filas_comparar) == 2:

    fila1, fila2 = st.session_state.filas_comparar

    st.write(
        f"Estás comparando las filas del "
        f"**{fila1}** y del **{fila2}**."
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
        "**¿Encontrás alguna relación que se repita?**"
    )


# =========================================================
# CIERRE
# =========================================================

if st.session_state.registro_exploracion:

    st.divider()

    st.subheader("Antes de terminar")

    st.write(
        """
Encontrar una relación en algunos productos puede ser el comienzo.

La pregunta ahora es:
"""
    )

    st.markdown(
        "### ¿Esa relación funcionará también con otros productos?"
    )

    st.write(
        """
Podés volver a la tabla y buscar nuevos casos para ponerla a prueba.
"""
    )


# =========================================================
# REINICIAR
# =========================================================

st.divider()

st.button(
    "↺ Reiniciar toda la exploración",
    on_click=reiniciar
)

st.caption(
    "TP-01 · Mirar la tabla de otra manera · "
    "LIM – Laboratorio de Ideas Matemáticas"
)