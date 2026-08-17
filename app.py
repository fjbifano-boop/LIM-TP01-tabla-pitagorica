import streamlit as st
import pandas as pd

# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="LIM · TP-01",
    page_icon="🔢",
    layout="wide"
)

# =========================================================
# ESTADO
# =========================================================

defaults = {
    "producto_inicial": None,
    "ultima_celda_evento": None,
    "relacion": None,
    "factor_a": None,
    "factor_b": None,
    "anticipacion_guardada": False,
    "comprobacion": None,
    "registro": []
}

for clave, valor in defaults.items():
    if clave not in st.session_state:
        st.session_state[clave] = valor


# =========================================================
# FUNCIONES
# =========================================================

def crear_tabla():
    datos = {
        str(columna): [fila * columna for fila in range(1, 11)]
        for columna in range(1, 11)
    }
    df = pd.DataFrame(datos, index=range(1, 11))
    df.index.name = "×"
    return df


def nueva_exploracion():
    st.session_state.producto_inicial = None
    st.session_state.ultima_celda_evento = None
    st.session_state.relacion = None
    st.session_state.factor_a = None
    st.session_state.factor_b = None
    st.session_state.anticipacion_guardada = False
    st.session_state.comprobacion = None


def cambiar_producto():
    nueva_exploracion()


def guardar_anticipacion():
    if (
        st.session_state.factor_a is not None
        and st.session_state.factor_b is not None
    ):
        st.session_state.anticipacion_guardada = True
        st.session_state.comprobacion = None
        st.session_state.ultima_celda_evento = None


def guardar_resultado():
    inicial = st.session_state.producto_inicial

    registro = {
        "inicial": inicial,
        "relacion": st.session_state.relacion,
        "anticipacion": (
            st.session_state.factor_a,
            st.session_state.factor_b
        ),
        "comprobacion": st.session_state.comprobacion
    }

    st.session_state.registro.append(registro)
    nueva_exploracion()


def reiniciar():
    st.session_state.registro = []
    nueva_exploracion()


def estilizar_tabla(df, celdas):
    estilos = pd.DataFrame(
        "",
        index=df.index,
        columns=df.columns
    )

    for fila, columna, tipo in celdas:
        columna = str(columna)

        if fila in estilos.index and columna in estilos.columns:

            if tipo == "inicial":
                estilos.loc[fila, columna] = (
                    "background-color:#2563eb;"
                    "color:white;"
                    "font-weight:800;"
                )

            elif tipo == "comprobacion":
                estilos.loc[fila, columna] = (
                    "background-color:#16a34a;"
                    "color:white;"
                    "font-weight:800;"
                )

    return df.style.apply(lambda _: estilos, axis=None)


# =========================================================
# TABLA
# =========================================================

tabla = crear_tabla()


# =========================================================
# ENCABEZADO
# =========================================================

st.caption("LIM · Laboratorio de Ideas Matemáticas · TP-01")

st.title("Buscando relaciones entre productos")

st.write(
    """
Elegí un producto de la tabla y usalo como punto de partida
para anticipar otros productos relacionados.
"""
)

st.divider()


# =========================================================
# DETERMINAR CELDAS A DESTACAR
# =========================================================

celdas_destacadas = []

if st.session_state.producto_inicial:
    f, c = st.session_state.producto_inicial
    celdas_destacadas.append((f, c, "inicial"))

if st.session_state.comprobacion:
    f, c = st.session_state.comprobacion
    celdas_destacadas.append((f, c, "comprobacion"))


tabla_estilizada = estilizar_tabla(
    tabla,
    celdas_destacadas
)


# =========================================================
# ETAPA 1 · ELEGIR PRODUCTO
# =========================================================

if st.session_state.producto_inicial is None:

    st.subheader("1. Elegí un producto")

    st.write(
        "Tocá cualquier producto de la tabla para comenzar."
    )

else:

    f, c = st.session_state.producto_inicial
    p = f * c

    st.subheader("Tu producto de partida")

    st.markdown(f"## {f} × {c} = {p}")


# =========================================================
# TABLA INTERACTIVA
# =========================================================

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
# PROCESAR SELECCIÓN EN LA TABLA
# =========================================================

celdas_evento = evento.selection.cells

if celdas_evento:

    fila_posicion, columna_nombre = celdas_evento[0]

    fila = fila_posicion + 1
    columna = int(columna_nombre)

    celda_actual = (fila, columna)

    if celda_actual != st.session_state.ultima_celda_evento:

        st.session_state.ultima_celda_evento = celda_actual

        # Primera etapa: elegir producto inicial
        if st.session_state.producto_inicial is None:

            st.session_state.producto_inicial = celda_actual
            st.rerun()

        # Etapa de comprobación
        elif st.session_state.anticipacion_guardada:

            st.session_state.comprobacion = celda_actual
            st.rerun()

else:
    st.session_state.ultima_celda_evento = None


# =========================================================
# ETAPA 2 · ELEGIR RELACIÓN
# =========================================================

if (
    st.session_state.producto_inicial is not None
    and not st.session_state.anticipacion_guardada
):

    f, c = st.session_state.producto_inicial
    producto = f * c

    st.divider()

    st.subheader("2. Elegí qué querés buscar")

    relacion = st.radio(
        "A partir de este producto, quiero encontrar...",
        [
            "otro producto que dé lo mismo",
            "un producto que dé el doble"
        ],
        index=None,
        key="relacion"
    )

    if relacion:

        if relacion == "otro producto que dé lo mismo":
            objetivo = producto

            st.info(
                f"Buscamos otra multiplicación cuyo resultado sea "
                f"**{objetivo}**."
            )

        else:
            objetivo = producto * 2

            st.info(
                f"El doble de {producto} es **{objetivo}**."
            )

        # =================================================
        # ANTICIPACIÓN
        # =================================================

        st.subheader("3. Antes de buscar en la tabla...")

        st.write(
            f"¿Qué multiplicación pensás que podría dar **{objetivo}**?"
        )

        col1, colx, col2 = st.columns([2, 1, 2])

        with col1:
            st.number_input(
                "Primer número",
                min_value=1,
                max_value=10,
                value=None,
                step=1,
                key="factor_a"
            )

        with colx:
            st.markdown(
                "<div style='text-align:center;"
                "padding-top:35px;font-size:1.5rem;'>×</div>",
                unsafe_allow_html=True
            )

        with col2:
            st.number_input(
                "Segundo número",
                min_value=1,
                max_value=10,
                value=None,
                step=1,
                key="factor_b"
            )

        if (
            st.session_state.factor_a is not None
            and st.session_state.factor_b is not None
        ):

            anticipado = (
                st.session_state.factor_a
                * st.session_state.factor_b
            )

            st.write(
                f"Tu anticipación es: "
                f"**{st.session_state.factor_a} × "
                f"{st.session_state.factor_b} = {anticipado}**"
            )

            st.button(
                "Ahora quiero comprobarlo",
                on_click=guardar_anticipacion,
                use_container_width=True
            )

    st.button(
        "Elegir otro producto de partida",
        on_click=cambiar_producto
    )


# =========================================================
# ETAPA 4 · COMPROBAR
# =========================================================

if st.session_state.anticipacion_guardada:

    f0, c0 = st.session_state.producto_inicial
    producto0 = f0 * c0

    a = st.session_state.factor_a
    b = st.session_state.factor_b

    anticipado = a * b

    if st.session_state.relacion == "otro producto que dé lo mismo":
        objetivo = producto0
        nombre_relacion = "el mismo resultado"
    else:
        objetivo = producto0 * 2
        nombre_relacion = "el doble"

    st.divider()

    st.subheader("4. Comprobá tu anticipación")

    st.write(
        f"Anticipaste **{a} × {b} = {anticipado}**."
    )

    st.write(
        "Ahora buscá esa multiplicación en la tabla y tocala."
    )

    if st.session_state.comprobacion:

        fc, cc = st.session_state.comprobacion
        resultado_comprobado = fc * cc

        st.markdown(
            f"### Elegiste {fc} × {cc} = {resultado_comprobado}"
        )

        if (
            fc == a and cc == b
        ):

            st.success(
                "Encontraste en la tabla la multiplicación "
                "que habías anticipado."
            )

            if resultado_comprobado == objetivo:

                st.write(
                    f"El resultado es **{objetivo}**: "
                    f"encontraste {nombre_relacion} que buscabas."
                )

            else:

                st.write(
                    f"Esta multiplicación da **{resultado_comprobado}**, "
                    f"pero buscábamos **{objetivo}**."
                )

                st.write(
                    "Podés volver a pensar tu anticipación "
                    "y probar con otros números."
                )

        else:

            st.info(
                f"Habías anticipado **{a} × {b}**. "
                f"En la tabla elegiste **{fc} × {cc}**."
            )

            st.write(
                "Podés buscar la multiplicación que anticipaste "
                "o explorar si esta nueva elección también sirve."
            )

        st.button(
            "Guardar esta exploración",
            on_click=guardar_resultado,
            use_container_width=True
        )


# =========================================================
# CUADERNO
# =========================================================

if st.session_state.registro:

    st.divider()

    st.subheader("Mis exploraciones")

    for numero, registro in enumerate(
        st.session_state.registro,
        start=1
    ):

        f0, c0 = registro["inicial"]
        producto0 = f0 * c0

        a, b = registro["anticipacion"]

        fc, cc = registro["comprobacion"]

        with st.container(border=True):

            st.caption(f"Exploración {numero}")

            st.write(
                f"**Partí de:** "
                f"{f0} × {c0} = {producto0}"
            )

            st.write(
                f"**Busqué:** {registro['relacion']}"
            )

            st.write(
                f"**Anticipé:** {a} × {b} = {a*b}"
            )

            st.write(
                f"**Comprobé en la tabla:** "
                f"{fc} × {cc} = {fc*cc}"
            )


# =========================================================
# REINICIO
# =========================================================

st.divider()

st.button(
    "↺ Reiniciar el laboratorio",
    on_click=reiniciar
)

st.caption(
    "TP-01 · Buscando relaciones entre productos · "
    "LIM – Laboratorio de Ideas Matemáticas · v0.6"
)
