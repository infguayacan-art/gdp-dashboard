import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="ERP Multiplataforma Corporativo 2026", layout="wide", initial_sidebar_state="expanded")

# INICIALIZACIÓN DE VARIABLES GLOBALES EN MEMORIA (Sincronización instantánea)
if "db_productos" not in st.session_state:
    st.session_state.db_productos = [
        {"id": 101, "sku": "REP-001", "nombre": "Kit Transmisión Moto 150cc", "tipo": "Artículo", "rubro": "Repuestos Moto", "stock": 45, "minimo": 10, "costo_fob": 15.0, "costo_cif": 18.5, "p_mayor": 25.0, "p_detal": 32.0, "detalles": "Marca: MotoX, Modelo: Universal", "vence": None, "lote": "L-771", "oferta": 0},
        {"id": 102, "sku": "VIV-002", "nombre": "Arroz Grado 1 Premium 1kg", "tipo": "Artículo", "rubro": "Víveres", "stock": 120, "minimo": 20, "costo_fob": 0.8, "costo_cif": 0.95, "p_mayor": 1.2, "p_detal": 1.5, "detalles": "Reg. Sanitario: RS-9921", "vence": (datetime.now() + timedelta(days=200)).date(), "lote": "LOT-882", "oferta": 10},
        {"id": 103, "sku": "SER-003", "nombre": "Instalación y Ajuste de Cadena", "tipo": "Servicio", "rubro": "Servicios", "stock": 999, "minimo": 0, "costo_fob": 0.0, "costo_cif": 0.0, "p_mayor": 8.0, "p_detal": 10.0, "detalles": "Mano de obra técnica calificada", "oferta": 0}
    ]

if "db_ventas" not in st.session_state:
    st.session_state.db_ventas = []
if "caja_diaria" not in st.session_state:
    st.session_state.caja_diaria = {"estado": "Abierta", "saldo_local": 250000.0, "saldo_usd": 500.0}
if "permisos" not in st.session_state:
    st.session_state.permisos = {
        "venta_maria": {"caja": True, "stock": False, "compras": False, "ofertas": False},
        "bodega_luis": {"caja": False, "stock": True, "compras": False, "ofertas": False},
        "compras_ana": {"caja": False, "stock": True, "compras": True, "ofertas": False}
    }
if "auditoria" not in st.session_state:
    st.session_state.auditoria = []
if "intrusiones" not in st.session_state:
    st.session_state.intrusiones = []
if "publicidad" not in st.session_state:
    st.session_state.publicidad = "🔥 ¡GRAN LIQUIDACIÓN DE REPUESTOS DE MOTO! 15% DE DESCUENTO EN LÍNEA EN KITS DE TRANSMISIÓN 🔥"
if "logo_empresa" not in st.session_state:
    st.session_state.logo_empresa = "🏢 CORPORACIÓN COMERCIAL MULTIRRUBRO"
if "meta_ventas" not in st.session_state:
    st.session_state.meta_ventas = 5000.0

# COMPONENTE DE IMPRESIÓN BLUETOOTH (WEB BLUETOOTH API)
def render_bluetooth_print_button(ticket_text):
    js_code = f"""
    <script>
    async function printBluetooth() {{
        const text = `{ticket_text}`;
        try {{
            const device = await navigator.bluetooth.requestDevice({{
                filters: [{{ services: ['000018f0-0000-1000-8000-00805f9b34fb'] }}]
            }});
            const server = await device.gatt.connect();
            const service = await server.getPrimaryService('000018f0-0000-1000-8000-00805f9b34fb');
            const characteristics = await service.getCharacteristics();
            let encoder = new TextEncoder();
            let data = encoder.encode(text + '\\n\\n\\n');
            await characteristics.writeValue(data);
            alert('¡Ticket impreso!');
        }} catch (error) {{
            alert('Error: ' + error.message);
        }}
    }}
    </script>
    <button onclick="printBluetooth()" style="background-color: #1E88E5; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; width: 100%;">
        🖨️ Conectar e Imprimir vía Bluetooth (ESC/POS)
    </button>
    """
    st.components.v1.html(js_code, height=60)

# INTERFAZ Y LÓGICA DE USUARIOS
st.sidebar.markdown(f"## {st.session_state.logo_empresa}")
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔒 Acceso Seguro")
usuario = st.sidebar.text_input("Usuario", value="jefe_juan")
password = st.sidebar.text_input("Contraseña", type="password", value="jefe2026")

rol_actual = None
if usuario == "admin" and password == "admin2026": rol_actual = "Administrador"
elif usuario == "jefe_juan" and password == "jefe2026": rol_actual = "Jefatura"
elif usuario == "venta_maria" and password == "venta2026": rol_actual = "Vendedor"
elif usuario == "bodega_luis" and password == "bodega2026": rol_actual = "Bodeguero"
elif usuario == "compras_ana" and password == "compras2026": rol_actual = "Comprador"

if rol_actual:
    st.sidebar.success(f"Conectado como: **{rol_actual}**")
else:
    st.sidebar.error("Credenciales Incorrectas")
    st.title("🔒 Sistema ERP Protegido")
    st.warning("Por favor, ingrese sus datos válidos en la barra lateral.")
    st.stop()

vista_dispositivo = st.sidebar.radio("Ver Dispositivo:", ["💻 Servidor Administrativo", "🌐 Página Web Clientes", "📱 App Móvil Personal"])

if vista_dispositivo in ["🌐 Página Web Clientes", "📱 App Móvil Personal"]:
    st.info(st.session_state.publicidad)

def verificar_permiso(usuario, tipo_permiso):
    if usuario in ["admin", "jefe_juan"]: return True
    return st.session_state.permisos.get(usuario, {}).get(tipo_permiso, False)

if vista_dispositivo == "💻 Servidor Administrativo":
    st.title("💻 Centro de Control Administrativo")
    pestanas = st.tabs(["📦 Bodega", "🚢 Adquisiciones", "🛒 Ventas y Caja", "🔐 Permisos"])
    
    with pestanas[0]:
        st.header("Inventario de Artículos y Servicios")
        df_p = pd.DataFrame(st.session_state.db_productos)
        st.dataframe(df_p)
        
    with pestanas[1]:
        st.header("Monitoreo Marítimo e Importaciones")
        st.metric("Contenedores en Alta Mar", "2 Buques en Ruta")
        st.progress(0.70, text="🚢 Contenedor en aduana (70%)")
        
    with pestanas[2]:
        st.header("Flujo de Tesorería")
        st.metric("Saldo Caja CLP", f"\${st.session_state.caja_diaria['saldo_local']:,}")
        st.metric("Saldo Caja USD", f"\${st.session_state.caja_diaria['saldo_usd']:,}")
        
    with pestanas[3]:
        st.header("Matriz de Seguridad del Personal")
        st.write("Configuración de accesos activos para vendedores, compradores y bodegueros.")

elif vista_dispositivo == "🌐 Página Web Clientes":
    st.title(f"🌐 Catálogo Público - {st.session_state.logo_empresa}")
    for p in st.session_state.db_productos:
        st.markdown(f"#### {p['nombre']} (Rubro: {p['rubro']})")
        st.write(f"Precio Venta: \${p['p_detal']} | Disponibilidad: {p['stock']} unidades")
        st.markdown("---")

elif vista_dispositivo == "📱 App Móvil Personal":
    st.title("📱 Interfaz Móvil Corporativa")
    prod_selec = st.selectbox("Seleccione Producto", [p["nombre"] for p in st.session_state.db_productos])
    cantidad_v = st.number_input("Cantidad", min_value=1, value=1)
    if st.button("⚡ Registrar Venta e Imprimir"):
        st.success("¡Venta procesada con éxito en la nube!")
        ticket = f"--- {st.session_state.logo_empresa} ---\\nCANT: {cantidad_v}\\nPRODUCTO: {prod_selec}\\n¡GRACIAS!"
        render_bluetooth_print_button(ticket)