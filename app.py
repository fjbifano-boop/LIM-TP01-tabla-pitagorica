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
    "observacion_elegida": None,
    "conjetura": "",
    "modo_prueba": False,
    "resultado_prueba": None,
    "comentario_prueba": ""
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
            "observacion": texto
        })

        limpiar_seleccion()


def elegir_observacion(indice):
    st.session_state.observacion_elegida = indice
    st.session_state.conjetura = ""
    st.session_state.modo_prueba = False
    st.session_state.resultado_prueba = None
    st.session_state.comentario_prueba = ""
    st.session_state.celdas_elegidas = []
    st.session_state.ultima_celda_evento = None


def comenzar_prueba():
    if st.session_state.conjetura.strip():
        st.session_state.modo_prueba = True
        st.session_state.celdas_elegidas = []
        st.session_state.ultima_celda_evento = None


def terminar_prueba():
    st.session_state.observacion_elegida = None
    st.session_state.conjetura = ""
    st.session_state.modo_prueba = False
    st.session_state.resultado_prueba = None
    st.session_state.comentario_prueba = ""
    st.session_state.celdas_elegidas = []
    st.session_state.ultima_celda_evento = None


def reiniciar():
    st.session_state.celdas_elegidas = []
    st.session_state.ultima_celda_evento = None
    st.session_state.registro_exploracion = []
    st.session_state.observacion_actual = ""
    st.session_state.observacion_elegida = None
    st.session_state.conjetura = ""
    st.session_state.modo_prueba = False
    st.session_state.resultado_prueba = None
    st.session_state.comentario_prueba = ""


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

st.title("Mirar la tabla de otra manera")

st.write(
    """
La tabla pitagórica reúne muchos productos.

En este laboratorio vamos a usarla para **buscar relaciones,
formular ideas y ponerlas a prueba**.
"""
)

st.divider()


# =========================================================
# FUNCIÓN PARA MOSTRAR LA TABLA
# =========================================================

def mostrar_tabla(clave):

    tabla_estilizada = estilizar_tabla(
        tabla,
        st.session_state.celdas_elegidas
    )

    evento = st.dataframe(
        tabla_estilizada,
        key=clave,
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
# FUNCIÓN PARA MOSTRAR LOS DOS PRODUCTOS
# =========================================================

def mostrar_productos():

    celdas = st.session_state.celdas_elegidas

    if not celdas:
        return

    columnas = st.columns(len(celdas))

    for indice, (fila, columna) in enumerate(celdas):

        producto = fila * columna

        with columnas[indice]:
            with st.container(border=True):
                st.markdown(
                    f"### {fila} × {columna} = {producto}"
                )


# =========================================================
# ETAPA 1 · EXPLORACIÓN LIBRE
# =========================================================

if st.session_state.observacion_elegida is None:

    st.subheader("1. Elegí dos productos")

    st.write(
        """
Elegí dos productos de la tabla que te interese comparar.
No tienen que cumplir ninguna condición especial.
"""
    )

    mostrar_tabla("tabla_exploracion")

    mostrar_productos()

    celdas = st.session_state.celdas_elegidas

    if len(celdas) == 1:

        st.info(
            "Elegí un segundo producto para compararlo con el primero."
        )

    elif len(celdas) == 2:

        (f1, c1), (f2, c2) = celdas

        p1 = f1 * c1
        p2 = f2 * c2

        st.markdown("### 2. Escribí qué observás")

        if p1 == p2:

            st.write(
                "Los dos productos dan el mismo resultado. "
                "¿Qué cambió y qué se mantuvo?"
            )

        elif c1 == c2:

            st.write(
                f"Los dos productos están en la columna del {c1}. "
                "¿Qué relación encontrás entre ellos?"
            )

        elif f1 == f2:

            st.write(
                f"Los dos productos están en la fila del {f1}. "
                "¿Qué relación encontrás entre ellos?"
            )

        else:

            st.write(
                "¿Encontrás alguna relación entre los productos "
                "que elegiste?"
            )

        st.text_area(
            "Tu observación:",
            key="observacion_actual",
            placeholder=(
                "Escribí algo que hayas notado al comparar "
                "los dos productos..."
            ),
            height=100
        )

        col1, col2 = st.columns(2)

        with col1:
            st.button(
                "Guardar mi observación",
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


    # =====================================================
    # REGISTRO
    # =====================================================

    if st.session_state.registro_exploracion:

        st.divider()

        st.subheader("3. Mis observaciones")

        st.write(
            "Estas son las relaciones que fuiste registrando."
        )

        for numero, registro in enumerate(
            st.session_state.registro_exploracion
        ):

            f1, c1 = registro["celda1"]
            f2, c2 = registro["celda2"]

            p1 = registro["producto1"]
            p2 = registro["producto2"]

            with st.container(border=True):

                st.caption(f"Observación {numero + 1}")

                st.markdown(
                    f"### {f1} × {c1} = {p1}  ↔  "
                    f"{f2} × {c2} = {p2}"
                )

                st.write(registro["observacion"])

                st.button(
                    "Seguir explorando esta idea",
                    key=f"seguir_{numero}",
                    on_click=elegir_observacion,
                    args=(numero,)
                )


# =========================================================
# ETAPA 2 · TRANSFORMAR UNA OBSERVACIÓN EN UNA IDEA
# =========================================================

else:

    indice = st.session_state.observacion_elegida
    registro = st.session_state.registro_exploracion[indice]

    f1, c1 = registro["celda1"]
    f2, c2 = registro["celda2"]

    p1 = registro["producto1"]
    p2 = registro["producto2"]

    st.subheader("1. Una idea para seguir investigando")

    with st.container(border=True):

        st.caption("Elegiste esta observación")

        st.markdown(
            f"### {f1} × {c1} = {p1}  ↔  "
            f"{f2} × {c2} = {p2}"
        )

        st.write(
            f'Vos escribiste: “{registro["observacion"]}”'
        )

    if not st.session_state.modo_prueba:

        st.markdown("### 2. ¿Qué idea podrías poner a prueba?")

        st.write(
            """
Intentá expresar qué pensás que podría ocurrir
con otros productos de la tabla.
"""
        )

        st.text_area(
            "Mi idea es que...",
            key="conjetura",
            placeholder=(
                "Por ejemplo: pienso que esto también podría "
                "ocurrir cuando..."
            ),
            height=100
        )

        st.button(
            "Poner mi idea a prueba",
            on_click=comenzar_prueba,
            disabled=not bool(
                st.session_state.conjetura.strip()
            ),
            use_container_width=True
        )

        st.button(
            "Volver a mis observaciones",
            on_click=terminar_prueba
        )


# =========================================================
# ETAPA 3 · BUSCAR OTRO CASO
# =========================================================

if (
    st.session_state.observacion_elegida is not None
    and st.session_state.modo_prueba
):

    st.divider()

    st.subheader("3. Buscá otro caso")

    st.write("La idea que querés poner a prueba es:")

    st.info(
        st.session_state.conjetura
    )

    st.write(
        """
Elegí dos productos de la tabla que te sirvan
para poner esa idea a prueba.
"""
    )

    mostrar_tabla("tabla_prueba")

    mostrar_productos()

    if len(st.session_state.celdas_elegidas) == 2:

        st.markdown("### 4. ¿Qué pasó con tu idea?")

        resultado = st.radio(
            "Después de mirar este nuevo caso:",
            [
                "Parece funcionar",
                "Encontré un caso en el que no funciona",
                "Todavía no estoy seguro"
            ],
            index=None,
            key="resultado_prueba"
        )

        st.text_area(
            "Contá qué observaste:",
            key="comentario_prueba",
            placeholder=(
                "Explicá qué pasó cuando probaste tu idea "
                "con estos productos..."
            ),
            height=100
        )

        if (
            resultado is not None
            and st.session_state.comentario_prueba.strip()
        ):

            st.success(
                "Probaste tu idea con un nuevo caso. "
                "Podés volver a la tabla y seguir investigándola."
            )

            col1, col2 = st.columns(2)

            with col1:
                st.button(
                    "Probar con otro caso",
                    on_click=limpiar_seleccion,
                    use_container_width=True
                )

            with col2:
                st.button(
                    "Terminar esta investigación",
                    on_click=terminar_prueba,
                    use_container_width=True
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
    "TP-01 · Mirar la tabla de otra manera · "
    "LIM – Laboratorio de Ideas Matemáticas"
)
