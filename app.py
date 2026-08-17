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
    "celdas_elegidas": [],
    "ultima_celda_evento": None,
    "registro_exploracion": [],
    "observacion_actual": "",
    "orientacion": "Exploración libre",
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


def limpiar_seleccion():
    st.session_state.celdas_elegidas = []
    st.session_state.ultima_celda_evento = None
    st.session_state.observacion_actual = ""


def guardar_observacion():
    texto = st.session_state.observacion_actual.strip()

    if len(st.session_state.celdas_elegidas) == 2 and texto:
        (f1, c1), (f2, c2) = st.session_state.celdas_elegidas

        st.session_state.registro_exploracion.append({
            "celda1": (f1, c1),
            "celda2": (f2, c2),
            "producto1": f1 * c1,
            "producto2": f2 * c2,
            "observacion": texto,
            "orientacion": st.session_state.orientacion
        })

        limpiar_seleccion()


def volver_a_caso(indice):
    registro = st.session_state.registro_exploracion[indice]

    st.session_state.celdas_elegidas = [
        registro["celda1"],
        registro["celda2"]
    ]

    st.session_state.observacion_actual = registro["observacion"]
    st.session_state.ultima_celda_evento = None


def borrar_registro(indice):
    st.session_state.registro_exploracion.pop(indice)
    limpiar_seleccion()


def reiniciar():
    st.session_state.celdas_elegidas = []
    st.session_state.ultima_celda_evento = None
    st.session_state.registro_exploracion = []
    st.session_state.observacion_actual = ""
    st.session_state.orientacion = "Exploración libre"


def estilizar_tabla(df, celdas):
    estilos = pd.DataFrame(
        "",
        index=df.index,
        columns=df.columns
    )

    for fila, columna in celdas:
        columna = str(columna)

        if fila in estilos.index and columna in estilos.columns:
            estilos.loc[fila, columna] = (
                "background-color:#2563eb;"
                "color:white;"
                "font-weight:800;"
            )

    return df.style.apply(lambda _: estilos, axis=None)


# =========================================================
# DATOS
# =========================================================

tabla = crear_tabla()


# =========================================================
# ENCABEZADO
# =========================================================

st.caption("LIM · Laboratorio de Ideas Matemáticas · TP-01")

st.title("Explorando la tabla pitagórica")

st.write(
    """
En la tabla pitagórica hay muchas relaciones que podemos descubrir.

Elegí productos, comparalos y registrá lo que vas observando.
"""
)

st.divider()


# =========================================================
# 1. ELEGIR UNA FORMA DE EXPLORAR
# =========================================================

st.subheader("1. Elegí dos productos para comparar")

st.write(
    """
Podés elegir libremente dos productos que te interese mirar.
Si necesitás una idea para empezar, también podés elegir
una propuesta de exploración.
"""
)

with st.expander("Ideas para explorar", expanded=False):

    st.radio(
        "Elegí una propuesta:",
        [
            "Exploración libre",
            "Buscá dos productos que den el mismo resultado",
            "Buscá dos productos que tengan un número en común",
            "Buscá dos productos donde los números aparezcan cambiados de lugar"
        ],
        key="orientacion"
    )

    if st.session_state.orientacion == "Exploración libre":
        st.caption(
            "Elegí dos productos que, por alguna razón, "
            "te interese comparar."
        )
    else:
        st.info(st.session_state.orientacion)


# =========================================================
# 2. TABLA INTERACTIVA
# =========================================================

tabla_estilizada = estilizar_tabla(
    tabla,
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
# DETECTAR CELDA SELECCIONADA
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
# 3. PRODUCTOS ELEGIDOS
# =========================================================

celdas = st.session_state.celdas_elegidas

st.markdown("### Productos que elegiste")

if len(celdas) == 0:

    st.caption("Todavía no elegiste ningún producto.")

else:

    columnas = st.columns(len(celdas))

    for indice, (fila, columna) in enumerate(celdas):

        producto = fila * columna

        with columnas[indice]:
            with st.container(border=True):
                st.markdown(
                    f"### {fila} × {columna} = {producto}"
                )


# =========================================================
# 4. REGISTRAR LO OBSERVADO
# =========================================================

if len(celdas) == 1:

    st.info("Elegí otro producto para compararlos.")


elif len(celdas) == 2:

    st.subheader("2. ¿Qué observás?")

    st.write(
        """
Mirá los dos productos que elegiste.
¿Qué relación encontrás entre ellos?
"""
    )

    st.text_area(
        "Escribí lo que observás:",
        key="observacion_actual",
        placeholder=(
            "Podés escribir algo que tengan en común, "
            "algo que cambie o cualquier relación que hayas encontrado..."
        ),
        height=100
    )

    col1, col2 = st.columns(2)

    with col1:
        st.button(
            "Guardar en mi cuaderno",
            on_click=guardar_observacion,
            use_container_width=True,
            disabled=not bool(
                st.session_state.observacion_actual.strip()
            )
        )

    with col2:
        st.button(
            "Elegir otros productos",
            on_click=limpiar_seleccion,
            use_container_width=True
        )


# =========================================================
# 5. CUADERNO DE EXPLORACIÓN
# =========================================================

if st.session_state.registro_exploracion:

    st.divider()

    st.subheader("3. Mi cuaderno de exploración")

    st.write(
        """
Acá quedan guardados los productos que comparaste
y lo que observaste en cada caso.
"""
    )

    for numero, registro in enumerate(
        st.session_state.registro_exploracion
    ):

        f1, c1 = registro["celda1"]
        f2, c2 = registro["celda2"]

        p1 = registro["producto1"]
        p2 = registro["producto2"]

        with st.container(border=True):

            st.caption(f"Exploración {numero + 1}")

            st.markdown(
                f"### {f1} × {c1} = {p1}  ↔  "
                f"{f2} × {c2} = {p2}"
            )

            st.write(registro["observacion"])

            if registro["orientacion"] != "Exploración libre":
                st.caption(
                    "Propuesta usada: "
                    + registro["orientacion"]
                )

            col_ver, col_borrar = st.columns([3, 1])

            with col_ver:
                st.button(
                    "Volver a mirar estos productos",
                    key=f"volver_{numero}",
                    on_click=volver_a_caso,
                    args=(numero,),
                    use_container_width=True
                )

            with col_borrar:
                st.button(
                    "Borrar",
                    key=f"borrar_{numero}",
                    on_click=borrar_registro,
                    args=(numero,),
                    use_container_width=True
                )


# =========================================================
# CIERRE ABIERTO
# =========================================================

if len(st.session_state.registro_exploracion) >= 2:

    st.divider()

    st.subheader("Para seguir mirando")

    st.write(
        """
Tu cuaderno ya tiene varias exploraciones.

Podés volver a cualquiera de ellas, comparar lo que observaste
o elegir nuevos productos de la tabla.
"""
    )


# =========================================================
# REINICIAR
# =========================================================

st.divider()

st.button(
    "↺ Reiniciar el laboratorio",
    on_click=reiniciar
)

st.caption(
    "TP-01 · Explorando la tabla pitagórica · "
    "LIM – Laboratorio de Ideas Matemáticas · v0.5"
)
st.caption(
    "TP-01 · Mirar la tabla de otra manera · "
    "LIM – Laboratorio de Ideas Matemáticas"
)
