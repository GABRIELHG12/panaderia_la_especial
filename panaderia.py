import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd
from datetime import datetime
import uuid
from pathlib import Path


# ==========================================================
# CONFIGURACIÓN
# ==========================================================

st.set_page_config(
    page_title="La Especial",
    page_icon="🥖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# PALETA DE COLORES - LA ESPECIAL
# ==========================================================
st.markdown("""
<style>
    /* Fondo general crema */
    .stApp {
        background-color: #FFF8E7;
        color: #3B2418;
    }

    /* Barra lateral */
    [data-testid="stSidebar"] {
        background-color: #5A1E22;
    }

    [data-testid="stSidebar"] * {
        color: #FFF8E7 !important;
    }

    /* Títulos */
    h1, h2, h3 {
        color: #6B2026 !important;
    }

    /* Texto */
    p, label, .stMarkdown {
        color: #3B2418;
    }

    /* Tarjetas y contenedores */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFDF5;
        border: 1px solid #D4A72C;
        border-radius: 14px;
    }

    /* Botones */
    .stButton > button {
        background-color: #7A2630;
        color: white;
        border: 1px solid #D4A72C;
        border-radius: 10px;
        font-weight: 600;
    }

    .stButton > button:hover {
        background-color: #D4A72C;
        color: #3B2418;
        border-color: #7A2630;
    }

    /* Botón principal */
    .stButton > button[kind="primary"] {
        background-color: #D4A72C;
        color: #3B2418;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #7A2630;
        color: white;
    }

    /* Mensajes */
    [data-testid="stAlert"] {
        border-radius: 10px;
    }

    /* Precio */
    .price-box {
        background-color: #F3E1A6;
        color: #6B2026;
        padding: 12px;
        border-radius: 10px;
        font-weight: bold;
    }

    /* Separadores */
    hr {
        border-color: #D4A72C;
    }

    /* Inputs */
    input, textarea, select {
        border-radius: 8px !important;
    }

    /* Pie de página */
    footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)


DB_NAME = "pan_sabor.db"

# Logo de la panadería
LOGO_PATH = "logo_la_especial.png"
NOMBRE_PANADERIA = 'Panadería y Pastelería "La Especial"'


# ==========================================================
# BASE DE DATOS
# ==========================================================

def conectar():
    return sqlite3.connect(DB_NAME)


def crear_base_datos():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE,
            categoria TEXT,
            descripcion TEXT,
            precio REAL,
            stock INTEGER,
            icono TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_compra TEXT,
            fecha TEXT,
            proveedor TEXT,
            producto TEXT,
            cantidad INTEGER,
            precio REAL,
            total REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_venta TEXT,
            fecha TEXT,
            cliente TEXT,
            producto TEXT,
            cantidad INTEGER,
            precio REAL,
            total REAL,
            pago TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alertas_stock (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            producto TEXT,
            stock INTEGER,
            minimo INTEGER,
            estado TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_pedido TEXT,
            fecha TEXT,
            cliente TEXT,
            telefono TEXT,
            direccion TEXT,
            producto TEXT,
            cantidad INTEGER,
            precio REAL,
            total REAL,
            pago TEXT,
            estado TEXT
        )
    """)

    conn.commit()
    conn.close()


crear_base_datos()


# ==========================================================
# 108 TIPOS DE PAN
# ==========================================================

def cargar_productos():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM productos"
    )

    cantidad = cursor.fetchone()[0]

    if True:

        productos = [

            # ------------------------------------------------
            # PAN DULCE
            # ------------------------------------------------

            (
                "Concha de vainilla",
                "Pan dulce",
                "Pan suave con cubierta de vainilla",
                9, 50, "🍞"
            ),

            (
                "Concha de chocolate",
                "Pan dulce",
                "Pan suave con cubierta de chocolate",
                10, 50, "🍫"
            ),

            (
                "Concha de fresa",
                "Pan dulce",
                "Concha con deliciosa cubierta de fresa",
                10, 40, "🍓"
            ),

            (
                "Concha de café",
                "Pan dulce",
                "Concha con cubierta sabor café",
                11, 40, "☕"
            ),

            (
                "Oreja",
                "Pan dulce",
                "Hojaldre crujiente con azúcar",
                12, 35, "🥐"
            ),

            (
                "Garibaldi",
                "Pan dulce",
                "Pan cubierto con pequeñas grageas",
                13, 30, "🧁"
            ),

            (
                "Chocolatín",
                "Pan dulce",
                "Pan relleno de chocolate",
                15, 30, "🍫"
            ),

            (
                "Besos de nuez",
                "Pan dulce",
                "Pan dulce relleno y cubierto de nuez",
                16, 25, "🥜"
            ),

            (
                "Polvorón",
                "Pan dulce",
                "Galleta suave que se deshace en la boca",
                10, 40, "🍪"
            ),

            (
                "Piedra",
                "Pan dulce",
                "Pan tradicional crujiente y dulce",
                9, 30, "🥖"
            ),

            (
                "Pan de muerto",
                "Pan dulce",
                "Pan tradicional mexicano",
                25, 30, "💀"
            ),

            (
                "Rosca de azúcar",
                "Pan dulce",
                "Rosca suave cubierta de azúcar",
                18, 25, "🍩"
            ),

            (
                "Pan de canela",
                "Pan dulce",
                "Pan suave con canela y azúcar",
                14, 30, "🍥"
            ),

            (
                "Pan de nuez",
                "Pan dulce",
                "Pan dulce con trozos de nuez",
                17, 25, "🥜"
            ),

            (
                "Pan de naranja",
                "Pan dulce",
                "Pan aromático con sabor a naranja",
                15, 25, "🍊"
            ),

            (
                "Pan de limón",
                "Pan dulce",
                "Pan dulce con un toque de limón",
                15, 25, "🍋"
            ),

            # ------------------------------------------------
            # BOLLERÍA
            # ------------------------------------------------

            (
                "Cuernito",
                "Bollería",
                "Cuernito de hojaldre recién horneado",
                12, 30, "🥐"
            ),

            (
                "Cuernito de chocolate",
                "Bollería",
                "Cuernito relleno de chocolate",
                18, 25, "🥐"
            ),

            (
                "Cuernito de queso",
                "Bollería",
                "Cuernito relleno de queso",
                18, 25, "🧀"
            ),

            (
                "Croissant",
                "Bollería",
                "Croissant francés de mantequilla",
                25, 20, "🥐"
            ),

            (
                "Croissant de chocolate",
                "Bollería",
                "Croissant relleno de chocolate",
                30, 20, "🍫"
            ),

            (
                "Brioche",
                "Bollería",
                "Pan francés suave y mantequilloso",
                25, 20, "🍞"
            ),

            (
                "Brioche de chocolate",
                "Bollería",
                "Brioche relleno de chocolate",
                30, 20, "🍫"
            ),

            (
                "Rol de canela",
                "Bollería",
                "Rol suave con canela y azúcar",
                25, 25, "🍥"
            ),

            (
                "Rol de nuez",
                "Bollería",
                "Rol de canela con nueces",
                28, 20, "🥜"
            ),

            (
                "Danés de manzana",
                "Bollería",
                "Pan danés con relleno de manzana",
                22, 20, "🍎"
            ),

            # ------------------------------------------------
            # DONAS
            # ------------------------------------------------

            (
                "Dona glaseada",
                "Donas",
                "Dona cubierta con glaseado",
                10, 40, "🍩"
            ),

            (
                "Dona de chocolate",
                "Donas",
                "Dona cubierta de chocolate",
                15, 35, "🍫"
            ),

            (
                "Dona de fresa",
                "Donas",
                "Dona cubierta con fresa",
                15, 35, "🍓"
            ),

            (
                "Dona de vainilla",
                "Donas",
                "Dona con cubierta de vainilla",
                14, 35, "🍩"
            ),

            (
                "Dona rellena de crema",
                "Donas",
                "Dona rellena de crema pastelera",
                18, 30, "🍮"
            ),

            (
                "Dona rellena de chocolate",
                "Donas",
                "Dona rellena de chocolate",
                20, 30, "🍫"
            ),

            (
                "Dona de azúcar",
                "Donas",
                "Dona tradicional con azúcar",
                10, 40, "🍩"
            ),

            (
                "Dona de cajeta",
                "Donas",
                "Dona rellena de cajeta",
                20, 25, "🍯"
            ),

            # ------------------------------------------------
            # PAN BLANCO
            # ------------------------------------------------

            (
                "Bolillo",
                "Pan blanco",
                "Crujiente por fuera y suave por dentro",
                4, 100, "🥖"
            ),

            (
                "Telera",
                "Pan blanco",
                "Pan tradicional para tortas",
                5, 80, "🥖"
            ),

            (
                "Baguette",
                "Pan blanco",
                "Baguette crujiente estilo francés",
                25, 30, "🥖"
            ),

            (
                "Pan de caja blanco",
                "Pan blanco",
                "Pan de caja suave para sandwiches",
                45, 20, "🍞"
            ),

            (
                "Pan integral",
                "Pan blanco",
                "Pan elaborado con harina integral",
                50, 20, "🍞"
            ),

            (
                "Pan multigrano",
                "Pan blanco",
                "Pan con semillas y diferentes cereales",
                55, 20, "🌾"
            ),

            (
                "Pan de avena",
                "Pan blanco",
                "Pan suave elaborado con avena",
                50, 20, "🌾"
            ),

            (
                "Pan campesino",
                "Pan blanco",
                "Pan rústico de corteza crujiente",
                35, 20, "🍞"
            ),

            # ------------------------------------------------
            # GALLETAS
            # ------------------------------------------------

            (
                "Galletas de mantequilla",
                "Galletas",
                "Galletas caseras de mantequilla",
                18, 25, "🍪"
            ),

            (
                "Galletas de chocolate",
                "Galletas",
                "Galletas con chispas de chocolate",
                20, 25, "🍪"
            ),

            (
                "Galletas de avena",
                "Galletas",
                "Galletas caseras de avena",
                18, 25, "🍪"
            ),

            (
                "Galletas con chispas",
                "Galletas",
                "Galletas con abundantes chispas de chocolate",
                22, 25, "🍪"
            ),

            (
                "Galletas de nuez",
                "Galletas",
                "Galletas con trozos de nuez",
                22, 20, "🥜"
            ),

            (
                "Galletas de canela",
                "Galletas",
                "Galletas con azúcar y canela",
                18, 25, "🍪"
            ),

            # ------------------------------------------------
            # EMPANADAS
            # ------------------------------------------------

            (
                "Empanada de piña",
                "Empanadas",
                "Empanada rellena de dulce de piña",
                15, 30, "🥧"
            ),

            (
                "Empanada de fresa",
                "Empanadas",
                "Empanada rellena de fresa",
                15, 30, "🍓"
            ),

            (
                "Empanada de manzana",
                "Empanadas",
                "Empanada rellena de manzana con canela",
                17, 25, "🍎"
            ),

            (
                "Empanada de cajeta",
                "Empanadas",
                "Empanada rellena de cajeta",
                18, 25, "🍯"
            ),

            (
                "Empanada de chocolate",
                "Empanadas",
                "Empanada rellena de chocolate",
                18, 25, "🍫"
            ),

            # ------------------------------------------------
            # PASTELES Y POSTRES
            # ------------------------------------------------

            (
                "Pastel de chocolate",
                "Pasteles",
                "Pastel de chocolate para celebraciones",
                280, 5, "🎂"
            ),

            (
                "Pastel de vainilla",
                "Pasteles",
                "Pastel clásico de vainilla",
                260, 5, "🎂"
            ),

            (
                "Pastel de fresa",
                "Pasteles",
                "Pastel con crema y fresas",
                300, 5, "🍓"
            ),

            (
                "Pastel de tres leches",
                "Pasteles",
                "Pastel suave bañado en tres leches",
                320, 5, "🎂"
            ),

            (
                "Cheesecake",
                "Pasteles",
                "Pastel de queso cremoso",
                300, 5, "🍰"
            ),

            (
                "Rebanada de pastel",
                "Postres",
                "Rebanada individual de pastel",
                45, 20, "🍰"
            ),

            (
                "Flan napolitano",
                "Postres",
                "Flan casero con caramelo",
                35, 20, "🍮"
            ),

            (
                "Pan de elote",
                "Pan dulce",
                "Pan suave preparado con elote dulce",
                20, 30, "🌽"
            ),

            (
                "Pan de plátano",
                "Pan dulce",
                "Pan casero con sabor a plátano",
                22, 25, "🍌"
            ),

            (
                "Pan de coco",
                "Pan dulce",
                "Pan dulce con coco rallado",
                20, 25, "🥥"
            ),

            (
                "Pan de almendra",
                "Pan dulce",
                "Pan suave con almendras",
                24, 20, "🌰"
            ),

            (
                "Pan de miel",
                "Pan dulce",
                "Pan dulce endulzado con miel",
                18, 30, "🍯"
            ),

            (
                "Pan de pasas",
                "Pan dulce",
                "Pan suave con pasas",
                17, 30, "🍇"
            ),

            (
                "Pan de anís",
                "Pan dulce",
                "Pan tradicional con aroma de anís",
                15, 30, "🌿"
            ),

            (
                "Pan de vainilla",
                "Pan dulce",
                "Pan esponjoso con sabor a vainilla",
                16, 30, "🍞"
            ),

            (
                "Pan de chocolate",
                "Pan dulce",
                "Pan suave con sabor intenso a chocolate",
                20, 30, "🍫"
            ),

            (
                "Pan de cajeta",
                "Pan dulce",
                "Pan relleno de dulce de leche y cajeta",
                22, 25, "🍯"
            ),

            (
                "Concha de fresa",
                "Pan dulce",
                "Concha con cubierta de fresa",
                10, 40, "🍓"
            ),

            (
                "Concha de café",
                "Pan dulce",
                "Concha con cubierta sabor café",
                11, 40, "☕"
            ),

            (
                "Concha de nuez",
                "Pan dulce",
                "Concha con cubierta y nuez",
                13, 30, "🥜"
            ),

            (
                "Concha de coco",
                "Pan dulce",
                "Concha con cubierta de coco",
                12, 30, "🥥"
            ),

            (
                "Concha de canela",
                "Pan dulce",
                "Concha con cubierta de canela",
                11, 35, "🍥"
            ),

            (
                "Mantecada",
                "Pan dulce",
                "Pan esponjoso tradicional de vainilla",
                12, 35, "🧁"
            ),

            (
                "Muffin de chocolate",
                "Pan dulce",
                "Muffin suave con chocolate",
                22, 25, "🧁"
            ),

            (
                "Muffin de vainilla",
                "Pan dulce",
                "Muffin esponjoso de vainilla",
                20, 25, "🧁"
            ),

            (
                "Muffin de arándanos",
                "Pan dulce",
                "Muffin con arándanos",
                24, 20, "🫐"
            ),

            (
                "Panqué de limón",
                "Pan dulce",
                "Panqué suave con sabor a limón",
                25, 20, "🍋"
            ),

            (
                "Panqué de naranja",
                "Pan dulce",
                "Panqué casero con naranja",
                25, 20, "🍊"
            ),

            (
                "Panqué de chocolate",
                "Pan dulce",
                "Panqué esponjoso de chocolate",
                28, 20, "🍫"
            ),

            (
                "Panqué de nuez",
                "Pan dulce",
                "Panqué con trozos de nuez",
                30, 20, "🥜"
            ),

            (
                "Panqué de plátano",
                "Pan dulce",
                "Panqué casero de plátano",
                26, 20, "🍌"
            ),

            (
                "Rosca de canela",
                "Pan dulce",
                "Rosca suave con canela y azúcar",
                20, 25, "🍥"
            ),

            (
                "Rosca de nuez",
                "Pan dulce",
                "Rosca dulce con nueces",
                24, 20, "🥜"
            ),

            (
                "Rosca de chocolate",
                "Pan dulce",
                "Rosca cubierta con chocolate",
                25, 20, "🍫"
            ),

            (
                "Rosca de naranja",
                "Pan dulce",
                "Rosca aromática con naranja",
                22, 20, "🍊"
            ),

            (
                "Rosca de reyes",
                "Pan dulce",
                "Rosca tradicional para compartir",
                280, 8, "👑"
            ),

            (
                "Pan de feria",
                "Pan dulce",
                "Pan tradicional de feria con azúcar",
                18, 30, "🍞"
            ),

            (
                "Churro",
                "Bollería",
                "Masa frita crujiente con azúcar y canela",
                12, 50, "🥨"
            ),

            (
                "Churro relleno de cajeta",
                "Bollería",
                "Churro relleno de cajeta",
                18, 35, "🍯"
            ),

            (
                "Churro relleno de chocolate",
                "Bollería",
                "Churro relleno de chocolate",
                18, 35, "🍫"
            ),

            (
                "Palmera",
                "Bollería",
                "Hojaldre caramelizado y crujiente",
                15, 30, "🥐"
            ),

            (
                "Napolitana de chocolate",
                "Bollería",
                "Hojaldre relleno de chocolate",
                22, 25, "🍫"
            ),

            (
                "Napolitana de crema",
                "Bollería",
                "Hojaldre relleno de crema pastelera",
                22, 25, "🥐"
            ),

            (
                "Strudel de manzana",
                "Bollería",
                "Hojaldre relleno de manzana y canela",
                28, 20, "🍎"
            ),

            (
                "Bollo de leche",
                "Bollería",
                "Bollo suave y ligeramente dulce",
                15, 30, "🍞"
            ),

            (
                "Bollo de mantequilla",
                "Bollería",
                "Bollo suave con mantequilla",
                18, 25, "🧈"
            ),

            (
                "Babka de chocolate",
                "Bollería",
                "Pan trenzado suave con chocolate",
                35, 15, "🍫"
            ),

            (
                "Dona de canela",
                "Donas",
                "Dona cubierta con azúcar y canela",
                14, 35, "🍩"
            ),

            (
                "Dona de nuez",
                "Donas",
                "Dona con cubierta y trozos de nuez",
                18, 30, "🥜"
            ),

            (
                "Dona de cajeta y nuez",
                "Donas",
                "Dona rellena de cajeta con nuez",
                22, 25, "🍯"
            ),

            (
                "Dona de maple",
                "Donas",
                "Dona cubierta con glaseado de maple",
                18, 30, "🍩"
            ),

            (
                "Dona de limón",
                "Donas",
                "Dona con glaseado de limón",
                16, 30, "🍋"
            ),

            (
                "Pan de ajo",
                "Pan blanco",
                "Pan suave con mantequilla y ajo",
                18, 30, "🧄"
            ),

            (
                "Pan de cebolla",
                "Pan blanco",
                "Pan suave con cebolla horneada",
                20, 25, "🧅"
            ),

            (
                "Pan rústico",
                "Pan blanco",
                "Pan artesanal de corteza crujiente",
                35, 20, "🥖"
            ),

            (
                "Pan de centeno",
                "Pan blanco",
                "Pan elaborado con harina de centeno",
                45, 20, "🍞"
            ),

            (
                "Pan de semillas",
                "Pan blanco",
                "Pan artesanal con mezcla de semillas",
                50, 20, "🌾"
            ),

        ]

        cursor.executemany("""
            INSERT OR IGNORE INTO productos
            (
                nombre,
                categoria,
                descripcion,
                precio,
                stock,
                icono
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, productos)

        conn.commit()

    conn.close()


cargar_productos()


# ==========================================================
# SESSION STATE
# ==========================================================

if "carrito" not in st.session_state:
    st.session_state.carrito = []

if "pagina" not in st.session_state:
    st.session_state.pagina = "Inicio"

if "pedido_realizado" not in st.session_state:
    st.session_state.pedido_realizado = None

if "pagina_ticket" not in st.session_state:
    st.session_state.pagina_ticket = None

if "ticket_compra" not in st.session_state:
    st.session_state.ticket_compra = None



# ==========================================================
# FUNCIONES
# ==========================================================

def obtener_productos():

    conn = conectar()

    df = pd.read_sql_query(
        """
        SELECT *
        FROM productos
        WHERE stock > 0
        ORDER BY nombre
        """,
        conn
    )

    conn.close()

    return df


def agregar_carrito(producto):

    for item in st.session_state.carrito:

        if item["nombre"] == producto["nombre"]:

            if item["cantidad"] < producto["stock"]:

                item["cantidad"] += 1

                item["total"] = (
                    item["cantidad"]
                    * item["precio"]
                )

            return

    st.session_state.carrito.append({

        "nombre": producto["nombre"],

        "precio": float(producto["precio"]),

        "cantidad": 1,

        "total": float(producto["precio"])

    })


def quitar_carrito(indice):

    producto = st.session_state.carrito[indice]

    producto["cantidad"] -= 1

    if producto["cantidad"] <= 0:

        st.session_state.carrito.pop(indice)

    else:

        producto["total"] = (
            producto["cantidad"]
            * producto["precio"]
        )


def eliminar_carrito(indice):

    st.session_state.carrito.pop(indice)


def total_carrito():

    return sum(
        producto["total"]
        for producto in st.session_state.carrito
    )



# ==========================================================
# TICKETS Y ALERTAS


def imprimir_ticket(ticket, titulo="Ticket"):
    """Muestra un ticket listo para imprimir desde el navegador."""
    import html

    contenido = html.escape(str(ticket)).replace("\n", "<br>")

    pagina = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{html.escape(titulo)}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: white;
                margin: 0;
                padding: 12px;
            }}
            .ticket {{
                width: 72mm;
                margin: auto;
                font-family: "Courier New", monospace;
                font-size: 12px;
                line-height: 1.35;
                white-space: normal;
                color: #000;
            }}
            .acciones {{
                text-align: center;
                margin-bottom: 12px;
            }}
            button {{
                padding: 9px 18px;
                border: 0;
                border-radius: 6px;
                background: #7A2630;
                color: white;
                font-weight: bold;
                cursor: pointer;
            }}
            @media print {{
                .acciones {{
                    display: none;
                }}
                @page {{
                    size: 80mm auto;
                    margin: 4mm;
                }}
                body {{
                    padding: 0;
                }}
                .ticket {{
                    width: 72mm;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="acciones">
            <button onclick="window.print()">🖨️ Imprimir ticket</button>
        </div>
        <div class="ticket">{contenido}</div>
    </body>
    </html>
    """

    components.html(pagina, height=330, scrolling=True)


# ==========================================================

STOCK_MINIMO = 10


def generar_ticket_venta(numero, cliente, pago, productos, total):
    lineas = [
        "========================================",
        '       PANADERÍA Y PASTELERÍA',
        '               "LA ESPECIAL"',
        "========================================",
        f"Ticket de venta: {numero}",
        f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        f"Cliente: {cliente or 'Público general'}",
        f"Forma de pago: {pago}",
        "----------------------------------------",
    ]

    for producto in productos:
        lineas.append(
            f"{producto['cantidad']} x {producto['nombre']}"
        )
        lineas.append(
            f"   ${producto['precio']:,.2f} c/u   "
            f"${producto['total']:,.2f}"
        )

    lineas.extend([
        "----------------------------------------",
        f"TOTAL: ${total:,.2f}",
        "========================================",
        "     Gracias por su compra",
        "========================================",
    ])
    return "\n".join(lineas)


def generar_ticket_compra(numero, proveedor, producto, cantidad, precio):
    total = cantidad * precio
    return "\n".join([
        "========================================",
        '       PANADERÍA Y PASTELERÍA',
        '               "LA ESPECIAL"',
        "========================================",
        f"Ticket de compra: {numero}",
        f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        f"Proveedor: {proveedor}",
        "----------------------------------------",
        f"Producto: {producto}",
        f"Cantidad: {cantidad}",
        f"Precio unitario: ${precio:,.2f}",
        f"TOTAL: ${total:,.2f}",
        "========================================",
        "       Compra registrada",
        "========================================",
    ])


def obtener_alertas_stock():
    conn = conectar()
    alertas = pd.read_sql_query(
        """
        SELECT nombre AS producto, stock
        FROM productos
        WHERE stock <= ?
        ORDER BY stock ASC, nombre
        """,
        conn,
        params=(STOCK_MINIMO,)
    )
    conn.close()
    if not alertas.empty:
        alertas["mínimo"] = STOCK_MINIMO
        alertas["estado"] = alertas["stock"].apply(
            lambda x: "AGOTADO" if x == 0 else "STOCK BAJO"
        )
    return alertas


# ==========================================================
# BARRA LATERAL
# ==========================================================

with st.sidebar:

    st.title("🥖 LA ESPECIAL")

    st.success(
        "✨ Pan recién horneado"
    )

    st.write(
        "Elige tus panes favoritos y realiza tu pedido."
    )

    st.divider()

    st.subheader("📋 Navegación")

    if st.button(
        "🏠 Inicio",
        use_container_width=True
    ):

        st.session_state.pagina = "Inicio"
        st.rerun()

    if st.button(
        "🥖 Ver menú",
        use_container_width=True
    ):

        st.session_state.pagina = "Menu"
        st.rerun()

    if st.button(
        "🔥 Promociones",
        use_container_width=True
    ):

        st.session_state.pagina = "Promociones"
        st.rerun()

    cantidad_carrito = sum(
        producto["cantidad"]
        for producto in st.session_state.carrito
    )

    if st.button(
        f"🛒 Carrito ({cantidad_carrito})",
        use_container_width=True
    ):

        st.session_state.pagina = "Carrito"
        st.rerun()

    if st.button(
        "🔐 Administración",
        use_container_width=True
    ):

        st.session_state.pagina = "Admin"
        st.rerun()


    if st.button(
        "🧾 Tickets y alertas",
        use_container_width=True
    ):

        st.session_state.pagina = "Tickets"
        st.rerun()

    st.divider()

    st.info(
        "📞 Pedidos: 55 1234 5678"
    )

    st.warning(
        "🕐 Lunes a domingo\n8:00 AM - 8:00 PM"
    )


# ==========================================================
# DATOS
# ==========================================================

df = obtener_productos()


# ==========================================================
# ENCABEZADO
# ==========================================================

# ==========================================================
# LOGO Y NOMBRE DE LA PANADERÍA
# ==========================================================

logo_archivo = Path(LOGO_PATH)

if logo_archivo.exists():
    # Mostrar el logo más pequeño, con un tamaño máximo de 500 × 500 px
    _, columna_logo, _ = st.columns([1, 2, 1])
    with columna_logo:
        st.image(str(logo_archivo), width=500)

st.title('🥖 Panadería y Pastelería "La Especial"')

st.subheader(
    "🍞 El sabor de un pan recién horneado"
)

st.write(
    "Pan tradicional, bollería, donas, galletas y pasteles."
)

st.divider()


# ==========================================================
# INICIO
# ==========================================================

if st.session_state.pagina == "Inicio":

    st.header(
        "🌞 Buenos días, bienvenido a La Especial"
    )

    st.success(
        "🔥 PROMOCIÓN DEL DÍA: 6 piezas de pan dulce por solo $50"
    )

    st.info(
        "🥐 Tenemos más de 100 variedades de pan para ti."
    )

    st.warning(
        "🎂 También elaboramos pasteles para cumpleaños y celebraciones."
    )

    st.divider()

    st.header(
        "⭐ Los favoritos de nuestros clientes"
    )

    favoritos = df.head(8)

    columnas = st.columns(4)

    for i, (_, producto) in enumerate(
        favoritos.iterrows()
    ):

        with columnas[i % 4]:

            with st.container(border=True):

                st.markdown(
                    f"# {producto['icono']}"
                )

                st.subheader(
                    producto["nombre"]
                )

                st.write(
                    producto["descripcion"]
                )

                st.success(
                    f"${producto['precio']:,.2f}"
                )

                st.caption(
                    f"📦 Disponibles: {producto['stock']}"
                )

                if st.button(
                    "🛒 Agregar",
                    key=f"inicio_{producto['id']}",
                    use_container_width=True
                ):

                    agregar_carrito(producto)

                    st.toast(
                        f"{producto['nombre']} agregado 🛒"
                    )

    st.divider()

    st.header(
        "🍞 Nuestras categorías"
    )

    categorias = [
        ("🥐", "Pan dulce"),
        ("🥖", "Pan blanco"),
        ("🍩", "Donas"),
        ("🍪", "Galletas"),
        ("🥧", "Empanadas"),
        ("🎂", "Pasteles"),
        ("🍰", "Postres")
    ]

    columnas = st.columns(4)

    for i, (icono, nombre) in enumerate(categorias):

        with columnas[i % 4]:

            with st.container(border=True):

                st.subheader(
                    f"{icono} {nombre}"
                )


# ==========================================================
# MENÚ
# ==========================================================

elif st.session_state.pagina == "Menu":

    st.header(
        "🥖 Nuestro menú"
    )

    st.write(
        f"Tenemos {len(df)} productos disponibles."
    )

    buscar = st.text_input(
        "🔎 Buscar un pan",
        placeholder="Ejemplo: concha, dona, chocolate..."
    )

    categorias = [
        "Todos"
    ]

    categorias += sorted(
        df["categoria"].unique().tolist()
    )

    categoria = st.selectbox(
        "🏷️ Selecciona una categoría",
        categorias
    )

    productos = df.copy()

    if buscar:

        productos = productos[
            productos["nombre"].str.contains(
                buscar,
                case=False,
                na=False
            )
        ]

    if categoria != "Todos":

        productos = productos[
            productos["categoria"]
            == categoria
        ]

    st.divider()

    if productos.empty:

        st.error(
            "😔 No encontramos ese producto."
        )

    else:

        for inicio in range(
            0,
            len(productos),
            4
        ):

            columnas = st.columns(4)

            grupo = productos.iloc[
                inicio:inicio + 4
            ]

            for posicion, (_, producto) in enumerate(
                grupo.iterrows()
            ):

                with columnas[posicion]:

                    with st.container(border=True):

                        st.markdown(
                            f"# {producto['icono']}"
                        )

                        st.subheader(
                            producto["nombre"]
                        )

                        st.caption(
                            producto["categoria"]
                        )

                        st.write(
                            producto["descripcion"]
                        )

                        st.success(
                            f"${producto['precio']:,.2f}"
                        )

                        st.caption(
                            f"📦 Stock: {producto['stock']}"
                        )

                        if st.button(
                            "🛒 Agregar al carrito",
                            key=f"menu_{producto['id']}",
                            use_container_width=True
                        ):

                            agregar_carrito(producto)

                            st.toast(
                                "Producto agregado 🛒"
                            )


# ==========================================================
# PROMOCIONES
# ==========================================================

elif st.session_state.pagina == "Promociones":

    st.header(
        "🔥 Promociones de La Especial"
    )

    st.success(
        "🥐 6 piezas de pan dulce por $50"
    )

    st.info(
        "☕ Combo mañanero: café + pan dulce"
    )

    st.warning(
        "🎂 Pasteles personalizados para tus eventos"
    )

    st.success(
        "🍩 Compra 5 donas y recibe la sexta con descuento"
    )

    st.info(
        "🥖 Descuento especial en compras grandes de bolillo"
    )


# ==========================================================
# CARRITO
# ==========================================================

elif st.session_state.pagina == "Carrito":

    st.header(
        "🛒 Mi carrito"
    )

    if not st.session_state.carrito:

        st.warning(
            "Tu carrito está vacío."
        )

        st.info(
            "Agrega algunos panes deliciosos desde nuestro menú."
        )

    else:

        for i, producto in enumerate(
            st.session_state.carrito
        ):

            with st.container(border=True):

                st.subheader(
                    producto["nombre"]
                )

                col1, col2, col3, col4 = st.columns(4)

                with col1:

                    st.write(
                        f"Precio: ${producto['precio']:,.2f}"
                    )

                with col2:

                    st.write(
                        f"Cantidad: {producto['cantidad']}"
                    )

                with col3:

                    st.write(
                        f"Subtotal: ${producto['total']:,.2f}"
                    )

                with col4:

                    if st.button(
                        "❌ Eliminar",
                        key=f"eliminar_{i}"
                    ):

                        eliminar_carrito(i)
                        st.rerun()

                a, b = st.columns(2)

                with a:

                    if st.button(
                        "➖ Quitar uno",
                        key=f"menos_{i}"
                    ):

                        quitar_carrito(i)
                        st.rerun()

                with b:

                    if st.button(
                        "➕ Agregar uno",
                        key=f"mas_{i}"
                    ):

                        datos = df[
                            df["nombre"]
                            == producto["nombre"]
                        ]

                        if not datos.empty:

                            agregar_carrito(
                                datos.iloc[0]
                            )

                        st.rerun()

        st.divider()

        total = total_carrito()

        st.header(
            f"💰 Total: ${total:,.2f}"
        )

        if st.button(
            "✅ Continuar con mi pedido",
            type="primary",
            use_container_width=True
        ):

            st.session_state.pagina = "Checkout"
            st.rerun()


# ==========================================================
# CHECKOUT
# ==========================================================

elif st.session_state.pagina == "Checkout":

    st.header(
        "📦 Completar pedido"
    )

    if not st.session_state.carrito:

        st.warning(
            "Tu carrito está vacío."
        )

    else:

        st.subheader(
            "👤 Datos del cliente"
        )

        nombre = st.text_input(
            "Nombre completo"
        )

        telefono = st.text_input(
            "📞 Teléfono"
        )

        direccion = st.text_area(
            "📍 Dirección de entrega"
        )

        pago = st.selectbox(
            "💳 Forma de pago",
            [
                "💵 Efectivo",
                "💳 Tarjeta",
                "📱 Transferencia"
            ]
        )

        st.divider()

        st.subheader(
            "🛒 Resumen"
        )

        for producto in st.session_state.carrito:

            st.write(
                f"{producto['cantidad']} x "
                f"{producto['nombre']} = "
                f"${producto['total']:,.2f}"
            )

        total = total_carrito()

        st.success(
            f"💰 TOTAL A PAGAR: ${total:,.2f}"
        )

        if st.button(
            "🟢 CONFIRMAR PEDIDO",
            type="primary",
            use_container_width=True
        ):

            if not nombre:

                st.error(
                    "❌ Escribe tu nombre."
                )

            elif not telefono:

                st.error(
                    "❌ Escribe tu teléfono."
                )

            elif not direccion:

                st.error(
                    "❌ Escribe tu dirección."
                )

            else:

                numero = (
                    "PED-"
                    + str(uuid.uuid4())[:6].upper()
                )

                fecha = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                conn = conectar()
                cursor = conn.cursor()

                for producto in st.session_state.carrito:

                    cursor.execute(
                        """
                        INSERT INTO pedidos
                        (
                            numero_pedido,
                            fecha,
                            cliente,
                            telefono,
                            direccion,
                            producto,
                            cantidad,
                            precio,
                            total,
                            pago,
                            estado
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            numero,
                            fecha,
                            nombre,
                            telefono,
                            direccion,
                            producto["nombre"],
                            producto["cantidad"],
                            producto["precio"],
                            producto["total"],
                            pago,
                            "PENDIENTE"
                        )
                    )

                    cursor.execute(
                        """
                        UPDATE productos
                        SET stock = stock - ?
                        WHERE nombre = ?
                        """,
                        (
                            producto["cantidad"],
                            producto["nombre"]
                        )
                    )

                conn.commit()
                conn.close()

                st.session_state.carrito = []

                st.session_state.pedido_realizado = numero

                st.session_state.pagina = "Confirmado"

                st.rerun()


# ==========================================================
# PEDIDO CONFIRMADO
# ==========================================================

elif st.session_state.pagina == "Confirmado":

    st.balloons()

    st.success(
        "🎉 ¡Pedido realizado correctamente!"
    )

    st.header(
        "🥖 ¡Gracias por comprar en La Especial!"
    )

    st.write(
        "Tu número de pedido es:"
    )

    st.title(
        st.session_state.pedido_realizado
    )

    st.info(
        "📦 Conserva este número para consultar tu pedido."
    )

    st.success(
        "🧑‍🍳 Nuestro equipo comenzará a preparar tu pedido."
    )

    if st.button(
        "🥐 Seguir comprando",
        use_container_width=True
    ):

        st.session_state.pagina = "Menu"

        st.session_state.pedido_realizado = None

        st.rerun()



# ==========================================================
# TICKETS Y ALERTAS
# ==========================================================

elif st.session_state.pagina == "Tickets":

    st.header('🧾 Tickets y control de inventario')

    pestaña = st.radio(
        "Selecciona una opción:",
        ["🧾 Ticket de venta", "📦 Ticket de compra", "🚨 Alertas de stock"],
        horizontal=True
    )

    # ------------------------------------------------------
    # TICKET DE VENTA
    # ------------------------------------------------------
    if pestaña == "🧾 Ticket de venta":

        st.subheader("🧾 Generar ticket de venta")

        conn = conectar()
        ventas = pd.read_sql_query(
            """
            SELECT *
            FROM pedidos
            ORDER BY id DESC
            """,
            conn
        )
        conn.close()

        if ventas.empty:
            st.info("Todavía no hay ventas registradas.")
        else:
            numeros = ventas["numero_pedido"].dropna().unique().tolist()
            numero = st.selectbox("Selecciona el número de pedido", numeros)

            pedido = ventas[ventas["numero_pedido"] == numero]

            cliente = pedido.iloc[0]["cliente"]
            pago = pedido.iloc[0]["pago"]

            productos_ticket = []
            for _, fila in pedido.iterrows():
                productos_ticket.append({
                    "nombre": fila["producto"],
                    "cantidad": int(fila["cantidad"]),
                    "precio": float(fila["precio"]),
                    "total": float(fila["total"])
                })

            total = sum(x["total"] for x in productos_ticket)

            ticket = generar_ticket_venta(
                numero,
                cliente,
                pago,
                productos_ticket,
                total
            )

            st.code(ticket, language="text")

            imprimir_ticket(
                ticket,
                f"Ticket de venta {numero}"
            )

    # ------------------------------------------------------
    # TICKET DE COMPRA
    # ------------------------------------------------------
    elif pestaña == "📦 Ticket de compra":

        st.subheader("📦 Registrar y generar ticket de compra")

        proveedor = st.text_input("Proveedor")
        producto_compra = st.text_input("Producto comprado")
        cantidad_compra = st.number_input(
            "Cantidad",
            min_value=1,
            value=1,
            step=1
        )
        precio_compra = st.number_input(
            "Precio unitario",
            min_value=0.01,
            value=1.0,
            step=1.0
        )

        if st.button(
            "💾 Registrar compra",
            type="primary",
            use_container_width=True
        ):

            if not proveedor or not producto_compra:
                st.error("Escribe el proveedor y el producto.")
            else:
                numero = "COM-" + str(uuid.uuid4())[:6].upper()
                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                total = cantidad_compra * precio_compra

                conn = conectar()
                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO compras
                    (numero_compra, fecha, proveedor, producto, cantidad, precio, total)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        numero,
                        fecha,
                        proveedor,
                        producto_compra,
                        cantidad_compra,
                        precio_compra,
                        total
                    )
                )

                # Si el producto existe, aumenta el inventario.
                cursor.execute(
                    """
                    UPDATE productos
                    SET stock = stock + ?
                    WHERE nombre = ?
                    """,
                    (cantidad_compra, producto_compra)
                )

                conn.commit()
                conn.close()

                st.session_state.ticket_compra = generar_ticket_compra(
                    numero,
                    proveedor,
                    producto_compra,
                    cantidad_compra,
                    precio_compra
                )

                st.success(f"Compra registrada: {numero}")

        if st.session_state.get("ticket_compra"):
            ticket_compra = str(st.session_state.ticket_compra)

            st.code(ticket_compra, language="text")

            imprimir_ticket(
                ticket_compra,
                "Ticket de compra"
            )

    # ------------------------------------------------------
    # ALERTAS DE STOCK
    # ------------------------------------------------------
    else:

        st.subheader("🚨 Alertas de stock")

        alertas = obtener_alertas_stock()

        if alertas.empty:
            st.success(
                f"✅ No hay productos con stock igual o menor a {STOCK_MINIMO}."
            )
        else:
            agotados = int((alertas["stock"] == 0).sum())
            bajos = len(alertas) - agotados

            col1, col2 = st.columns(2)
            with col1:
                st.error(f"🔴 Agotados: {agotados}")
            with col2:
                st.warning(f"🟠 Stock bajo: {bajos}")

            st.dataframe(
                alertas,
                use_container_width=True,
                hide_index=True
            )

            st.warning(
                f"⚠️ Se considera stock bajo cuando quedan {STOCK_MINIMO} "
                "piezas o menos."
            )


# ==========================================================
# ADMINISTRACIÓN
# ==========================================================

elif st.session_state.pagina == "Admin":

    st.header(
        "🔐 Administración"
    )

    st.warning(
        "Área exclusiva para el administrador."
    )

    password = st.text_input(
        "🔑 Contraseña",
        type="password"
    )

    if password == "1234":

        st.success(
            "✅ Acceso autorizado"
        )

        opcion = st.radio(
            "Selecciona una sección:",
            [
                "📦 Inventario",
                "📊 Pedidos",
                "➕ Agregar producto"
            ],
            horizontal=True
        )


        # ==================================================
        # INVENTARIO
        # ==================================================

        if opcion == "📦 Inventario":

            st.subheader(
                "📦 Inventario de la panadería"
            )

            conn = conectar()

            inventario = pd.read_sql_query(
                """
                SELECT *
                FROM productos
                ORDER BY categoria, nombre
                """,
                conn
            )

            conn.close()

            st.dataframe(
                inventario,
                use_container_width=True,
                hide_index=True
            )


        # ==================================================
        # PEDIDOS
        # ==================================================

        elif opcion == "📊 Pedidos":

            st.subheader(
                "📊 Pedidos realizados"
            )

            conn = conectar()

            pedidos = pd.read_sql_query(
                """
                SELECT *
                FROM pedidos
                ORDER BY id DESC
                """,
                conn
            )

            conn.close()

            if pedidos.empty:

                st.info(
                    "Todavía no hay pedidos."
                )

            else:

                st.dataframe(
                    pedidos,
                    use_container_width=True,
                    hide_index=True
                )


        # ==================================================
        # AGREGAR PRODUCTO
        # ==================================================

        elif opcion == "➕ Agregar producto":

            st.subheader(
                "➕ Agregar un nuevo pan"
            )

            nombre = st.text_input(
                "Nombre del producto"
            )

            categoria = st.selectbox(
                "Categoría",
                [
                    "Pan dulce",
                    "Bollería",
                    "Donas",
                    "Pan blanco",
                    "Galletas",
                    "Empanadas",
                    "Pasteles",
                    "Postres"
                ]
            )

            descripcion = st.text_area(
                "Descripción"
            )

            precio = st.number_input(
                "Precio",
                min_value=0.0,
                step=1.0
            )

            stock = st.number_input(
                "Cantidad en stock",
                min_value=0,
                step=1
            )

            icono = st.selectbox(
                "Icono",
                [
                    "🥖",
                    "🍞",
                    "🥐",
                    "🍩",
                    "🍪",
                    "🥧",
                    "🎂",
                    "🍰",
                    "🍫",
                    "🍓",
                    "🍎",
                    "🥜",
                    "☕"
                ]
            )

            if st.button(
                "💾 Guardar producto",
                type="primary"
            ):

                if not nombre:

                    st.error(
                        "Escribe el nombre del producto."
                    )

                elif precio <= 0:

                    st.error(
                        "El precio debe ser mayor que 0."
                    )

                else:

                    try:

                        conn = conectar()
                        cursor = conn.cursor()

                        cursor.execute(
                            """
                            INSERT OR IGNORE INTO productos
                            (
                                nombre,
                                categoria,
                                descripcion,
                                precio,
                                stock,
                                icono
                            )
                            VALUES (?, ?, ?, ?, ?, ?)
                            """,
                            (
                                nombre,
                                categoria,
                                descripcion,
                                precio,
                                stock,
                                icono
                            )
                        )

                        conn.commit()
                        conn.close()

                        st.success(
                            "🎉 Producto agregado correctamente."
                        )

                        st.rerun()

                    except sqlite3.IntegrityError:

                        st.error(
                            "❌ Ese producto ya existe."
                        )

    elif password:

        st.error(
            "❌ Contraseña incorrecta."
        )



# ==========================================================
# ALERTA RÁPIDA DE STOCK
# ==========================================================

alertas_rapidas = obtener_alertas_stock()

if not alertas_rapidas.empty:
    st.warning(
        f"🚨 Atención: hay {len(alertas_rapidas)} productos "
        "con stock bajo o agotado. Revisa 'Tickets y alertas'."
    )

# ==========================================================
# PIE DE PÁGINA
# ==========================================================

st.divider()

st.info(
    "🥖 Panadería y Pastelería \"La Especial\" | Pan recién horneado todos los días | "
    "📞 55 1234 5678 | 🕐 8:00 AM - 8:00 PM"
)
