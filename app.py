import streamlit as st

st.set_page_config(
    page_title="LIM · TP-01",
    page_icon="🔢",
    layout="centered"
)

# ---------------------------------------------------------
# ESTADO
# ---------------------------------------------------------

if "celdas" not in st.session_state:
    st.session_state.celdas = []

if "filas" not in st.session_state:
    st.session_state.filas = []


# ---------------------------------------------------------
# FUNCIONES
# ---------------------------------------------------------

def seleccionar_celda(fila, columna):
    celda = (fila, columna)

    if celda in st.session_state.celdas:
        st.session_state.celdas.remove(celda)
    else:
        # En esta primera versión permitimos hasta dos
        if len(st.session_state.celdas) >= 2:
            st.session_state.celdas.pop(0)

        st.session_state.celdas.append(celda)


def seleccionar_fila(fila):
    if fila in st.session_state.filas:
        st.session_state.filas.remove(fila)
    else:
        # Hasta dos filas simultáneamente
        if len(st.session_state.filas) >= 2:
            st.session_state.filas.pop(0)

        st.session_state.filas.append(fila)


def reiniciar():
    st.session_state.celdas = []
    st.session_state.filas = []


# ---------------------------------------------------------
# ENCABEZADO
# ---------------------------------------------------------

st.caption("Laboratorio de Ideas Matemáticas · TP-01")

st.title("Mirar la tabla de otra manera")

st.write(
    """
La tabla pitagórica reúne muchos productos.

**Tocá algunos números y fijate qué información podés obtener.**
"""
)

st.divider()


# ---------------------------------------------------------
# TABLA PITAGÓRICA
# ---------------------------------------------------------

st.subheader("Explorá la tabla")

# Encabezado
columnas = st.columns(11, gap="small")

with columnas[0]:
    st.markdown("### ×")

for j in range(1, 11):
    with columnas[j]:
        st.markdown(f"### {j}")


# Filas
for i in range(1, 11):

    columnas = st.columns(11, gap="small")

    # Botón de encabezado de fila
    with columnas[0]:

        etiqueta = f"✓ {i}" if i in st.session_state.filas else str(i)

        st.button(
            etiqueta,
            key=f"fila_{i}",
            on_click=seleccionar_fila,
            args=(i,),
            use_container_width=True
        )

    # Productos
    for j in range(1, 11):

        producto = i * j
        seleccionada = (i, j) in st.session_state.celdas

        with columnas[j]:

            etiqueta = f"✓{producto}" if seleccionada else str(producto)

            st.button(
                etiqueta,
                key=f"celda_{i}_{j}",
                on_click=seleccionar_celda,
                args=(i, j),
                use_container_width=True
            )


# ---------------------------------------------------------
# CELDAS SELECCIONADAS
# ---------------------------------------------------------

st.divider()

st.subheader("Productos que elegiste")

if len(st.session_state.celdas) == 0:

    st.write(
        "Todavía no seleccionaste ningún producto. "
        "Tocá un número de la tabla."
    )

else:

    for fila, columna in st.session_state.celdas:

        producto = fila * columna

        st.markdown(
            f"### {fila} × {columna} = {producto}"
        )


# ---------------------------------------------------------
# COMPARACIÓN DE CELDAS
# ---------------------------------------------------------

if len(st.session_state.celdas) == 2:

    (f1, c1), (f2, c2) = st.session_state.celdas

    p1 = f1 * c1
    p2 = f2 * c2

    st.write("**Mirá los dos productos que elegiste.**")

    if p1 == p2 and (f1, c1) != (f2, c2):

        st.info(
            "Los dos productos dan el mismo resultado. "
            "¿Qué cambió? ¿Qué se mantuvo?"
        )

    else:

        st.write(
            "¿Encontrás alguna relación entre ellos?"
        )


# ---------------------------------------------------------
# FILAS SELECCIONADAS
# ---------------------------------------------------------

st.divider()

st.subheader("Compará filas")

st.write(
    """
También podés tocar los números que aparecen al comienzo de cada fila.

**Elegí una o dos filas para mirarlas con más atención.**
"""
)

if len(st.session_state.filas) == 1:

    fila = st.session_state.filas[0]

    productos = [fila * j for j in range(1, 11)]

    st.write(f"Elegiste la fila del **{fila}**.")

    st.write(
        " – ".join(str(x) for x in productos)
    )

    st.write("Ahora elegí otra fila para compararla.")


elif len(st.session_state.filas) == 2:

    fila1, fila2 = st.session_state.filas

    productos1 = [fila1 * j for j in range(1, 11)]
    productos2 = [fila2 * j for j in range(1, 11)]

    st.write(
        f"Estás comparando las filas del **{fila1}** y del **{fila2}**."
    )

    st.markdown(f"**Fila del {fila1}:**")
    st.write(
        " – ".join(str(x) for x in productos1)
    )

    st.markdown(f"**Fila del {fila2}:**")
    st.write(
        " – ".join(str(x) for x in productos2)
    )

    st.info(
        "Mirá los números que ocupan la misma posición "
        "en las dos filas. ¿Encontrás alguna relación?"
    )


# ---------------------------------------------------------
# REINICIAR
# ---------------------------------------------------------

st.divider()

st.button(
    "↺ Empezar de nuevo",
    on_click=reiniciar
)

st.caption(
    "LIM · Laboratorio de Ideas Matemáticas"
)
