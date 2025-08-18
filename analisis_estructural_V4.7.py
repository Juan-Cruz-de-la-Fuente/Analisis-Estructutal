import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle
import math
from datetime import datetime
import io
import plotly.graph_objects as go
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import base64
import tempfile
import os

# Configuración de la página con tema moderno
st.set_page_config(
    page_title="Análisis Estructural - Método de Matrices",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado mejorado para estilo web moderno
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary-black: #000000;
        --primary-white: #ffffff;
        --gray-100: #f8f9fa;
        --gray-200: #e9ecef;
        --gray-300: #dee2e6;
        --gray-400: #ced4da;
        --gray-500: #adb5bd;
        --gray-600: #6c757d;
        --gray-700: #495057;
        --gray-800: #343a40;
        --gray-900: #212529;
        --blue-500: #495057;
        --blue-600: #343a40;
        --green-500: #28a745;
        --green-600: #218838;
    }
    
    .css-1d391kg {
        display: none;
    }
    
    .show-sidebar .css-1d391kg {
        display: block !important;
        background: linear-gradient(135deg, var(--gray-100) 0%, var(--gray-200) 100%);
        border-right: 2px solid var(--gray-300);
        box-shadow: 2px 0 10px rgba(0,0,0,0.1);
    }
    
    .main {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        color: var(--primary-black);
        min-height: 100vh;
    }
    
    .landing-container {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: -1rem;
        padding: 2rem;
    }
    
    .mode-card {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 2rem;
        margin: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    }
    
    .mode-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 40px rgba(31, 38, 135, 0.5);
        background: rgba(255, 255, 255, 0.35);
    }
    
    .progress-bar {
        background: var(--primary-white);
        border-bottom: 3px solid var(--gray-300);
        padding: 1.5rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        position: sticky;
        top: 0;
        z-index: 100;
    }
    
    .progress-steps {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .progress-step {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .step-circle {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s ease;
    }
    
    .step-circle.completed {
        background: var(--green-500);
        color: white;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
    
    .step-circle.current {
        background: var(--blue-500);
        color: white;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        animation: pulse 2s infinite;
    }
    
    .step-circle.pending {
        background: var(--gray-300);
        color: var(--gray-600);
    }
    
    .step-line {
        width: 60px;
        height: 3px;
        background: var(--gray-300);
        transition: all 0.3s ease;
    }
    
    .step-line.completed {
        background: var(--green-500);
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3); }
        50% { box-shadow: 0 4px 20px rgba(59, 130, 246, 0.6); }
        100% { box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3); }
    }
    
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        color: var(--primary-black);
        letter-spacing: -0.02em;
    }
    
    h1 {
        font-size: 3rem;
        margin-bottom: 2rem;
        text-align: center;
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h2 {
        font-size: 2rem;
        margin-bottom: 1.5rem;
        border-bottom: 3px solid var(--gray-700);
        padding-bottom: 0.5rem;
        display: inline-block;
    }
    
    h3 {
        font-size: 1.5rem;
        margin-bottom: 1rem;
        color: var(--gray-800);
    }
    
    .stButton > button {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        border-radius: 12px;
        border: none;
        background: linear-gradient(135deg, var(--blue-500) 0%, var(--blue-600) 100%);
        color: var(--primary-white);
        transition: all 0.3s ease;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
        background: linear-gradient(135deg, var(--blue-600) 0%, var(--blue-500) 100%);
    }
    
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        font-family: 'Inter', sans-serif;
        border: 2px solid var(--gray-300);
        border-radius: 10px;
        background-color: var(--primary-white);
        color: var(--primary-black);
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: var(--blue-500);
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    .metric-container {
        background: linear-gradient(135deg, var(--primary-white) 0%, var(--gray-100) 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid var(--gray-200);
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .metric-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .dataframe {
        font-family: 'Inter', sans-serif;
        border: none;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .streamlit-expanderHeader {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        background: linear-gradient(135deg, var(--gray-100) 0%, var(--gray-200) 100%);
        border: 1px solid var(--gray-300);
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, var(--gray-200) 0%, var(--gray-300) 100%);
    }
    
    .stInfo {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border-left: 4px solid var(--blue-500);
        color: var(--primary-black);
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.1);
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-left: 4px solid var(--green-500);
        color: var(--primary-black);
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.1);
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 4px solid #f59e0b;
        color: var(--primary-black);
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.1);
    }
    
    .stError {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-left: 4px solid #ef4444;
        color: var(--primary-black);
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.1);
    }
    
    .footer-section {
        background: linear-gradient(135deg, var(--gray-900) 0%, var(--gray-800) 100%);
        color: var(--primary-white);
        padding: 3rem 0;
        margin-top: 4rem;
        border-radius: 20px 20px 0 0;
    }
    
    .footer-content {
        text-align: center;
        max-width: 800px;
        margin: 0 auto;
        padding: 0 2rem;
    }
    
    .footer-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .footer-survey {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# Base de datos de materiales aeroespaciales
MATERIALES_AEROESPACIALES = {
    "Aluminio 6061-T6": {
        "modulo_young": 68.9e9,  # Pa
        "densidad": 2700,  # kg/m³
        "descripcion": "Aleación de aluminio estructural común"
    },
    "Aluminio 7075-T6": {
        "modulo_young": 71.7e9,  # Pa
        "densidad": 2810,  # kg/m³
        "descripcion": "Aleación de aluminio de alta resistencia"
    },
    "Aluminio 2024-T3": {
        "modulo_young": 73.1e9,  # Pa
        "densidad": 2780,  # kg/m³
        "descripcion": "Aleación de aluminio para fuselajes"
    },
    "Titanio Ti-6Al-4V": {
        "modulo_young": 113.8e9,  # Pa
        "densidad": 4430,  # kg/m³
        "descripcion": "Aleación de titanio aeroespacial"
    },
    "Acero 4130": {
        "modulo_young": 205e9,  # Pa
        "densidad": 7850,  # kg/m³
        "descripcion": "Acero aleado para estructuras"
    },
    "Fibra de Carbono T300": {
        "modulo_young": 230e9,  # Pa
        "densidad": 1760,  # kg/m³
        "descripcion": "Compuesto de fibra de carbono"
    },
    "Magnesio AZ31B": {
        "modulo_young": 45e9,  # Pa
        "densidad": 1770,  # kg/m³
        "descripcion": "Aleación de magnesio ligera"
    }
}

# Inicializar estado de la sesión
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'tipo_elemento' not in st.session_state:
    st.session_state.tipo_elemento = None
if 'modo' not in st.session_state:
    st.session_state.modo = None
if 'usuario_nombre' not in st.session_state:
    st.session_state.usuario_nombre = ""
if 'nodos' not in st.session_state:
    st.session_state.nodos = []
if 'elementos' not in st.session_state:
    st.session_state.elementos = []
if 'matrices_elementos' not in st.session_state:
    st.session_state.matrices_elementos = {}
if 'grados_libertad_info' not in st.session_state:
    st.session_state.grados_libertad_info = []
if 'nombres_fuerzas' not in st.session_state:
    st.session_state.nombres_fuerzas = {}
if 'resultados' not in st.session_state:
    st.session_state.resultados = None
if 'materiales_personalizados' not in st.session_state:
    st.session_state.materiales_personalizados = {}
if 'auto_calcular' not in st.session_state:
    st.session_state.auto_calcular = True
if 'nodo_seleccionado_interactivo' not in st.session_state:
    st.session_state.nodo_seleccionado_interactivo = None
if 'nodos_interactivos' not in st.session_state:
    st.session_state.nodos_interactivos = []
if 'elementos_interactivos' not in st.session_state:
    st.session_state.elementos_interactivos = []
if 'num_nodos' not in st.session_state:
    st.session_state.num_nodos = 2
if 'num_fijos' not in st.session_state:
    st.session_state.num_fijos = 1
if 'num_elementos' not in st.session_state:
    st.session_state.num_elementos = 1
if 'grupos_elementos' not in st.session_state:
    st.session_state.grupos_elementos = {}

def formatear_unidades(valor, tipo="presion"):
    """Formatear valores con prefijos apropiados"""
    abs_valor = abs(valor)

    if tipo == "presion":
        if abs_valor == 0:
            return "0 Pa"
        elif abs_valor < 10:
            return f"{valor:.3f} Pa"
        elif abs_valor < 1000:
            return f"{valor:.1f} Pa"
        elif abs_valor < 1e6:
            return f"{valor/1e3:.3f} kPa"
        elif abs_valor < 1e9:
            return f"{valor/1e6:.3f} MPa"
        else:
            return f"{valor/1e9:.3f} GPa"

    elif tipo == "fuerza":
        if abs_valor == 0:
            return "0 N"
        elif abs_valor < 1000:
            return f"{valor:.3f} N"
        elif abs_valor < 1e6:
            return f"{valor/1e3:.3f} kN"
        else:
            return f"{valor/1e6:.3f} MN"

    elif tipo == "desplazamiento":
        if abs_valor == 0:
            return "0 m"
        elif abs_valor < 1e-6:
            return f"{valor*1e9:.3f} nm"
        elif abs_valor < 1e-3:
            return f"{valor*1e6:.3f} μm"
        elif abs_valor < 1:
            return f"{valor*1e3:.3f} mm"
        else:
            return f"{valor:.6f} m"

    elif tipo == "rigidez":
        if abs_valor == 0:
            return "0 N/m"
        elif abs_valor < 1e-6:
            return f"{valor*1e9:.3f} nN/m"
        elif abs_valor < 1e-3:
            return f"{valor*1e6:.3f} μN/m"
        elif abs_valor < 1:
            return f"{valor*1e3:.3f} mN/m"
        elif abs_valor < 1e3:
            return f"{valor:.3f} N/m"
        elif abs_valor < 1e6:
            return f"{valor/1e3:.3f} kN/m"
        elif abs_valor < 1e9:
            return f"{valor/1e6:.3f} MN/m"
        else:
            return f"{valor/1e9:.3f} GN/m"

    return f"{valor:.6e}" 

def reset_app():
    """Reiniciar la aplicación"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def set_tipo_elemento(tipo):
    """Establecer el tipo de elemento"""
    st.session_state.tipo_elemento = tipo
    st.session_state.step = 1
    st.rerun()

def set_modo(modo):
    """Establecer el modo de análisis"""
    st.session_state.modo = modo
    st.session_state.step = 3  # Saltar al paso 3 después de seleccionar modo
    st.rerun()

def next_step():
    """Avanzar al siguiente paso"""
    st.session_state.step += 1
    st.rerun()

def prev_step():
    """Retroceder al paso anterior"""
    if st.session_state.step > 1:
        st.session_state.step -= 1
        st.rerun()

def calcular_grados_libertad_globales(nodo_id):
    """Calcular grados de libertad globales para un nodo según el tipo de elemento"""
    if st.session_state.tipo_elemento == "barra":
        # Barra: 2 GL por nodo (X, Y)
        gl_por_nodo = 2
        return [(nodo_id - 1) * gl_por_nodo + 1, (nodo_id - 1) * gl_por_nodo + 2]
    elif st.session_state.tipo_elemento == "viga":
        # Viga: 2 GL por nodo (Y, θ) 
        gl_por_nodo = 2
        return [(nodo_id - 1) * gl_por_nodo + 1, (nodo_id - 1) * gl_por_nodo + 2]
    elif st.session_state.tipo_elemento == "viga_portico":
        # Viga Pórtico: 3 GL por nodo (X, Y, θ)
        gl_por_nodo = 3
        return [(nodo_id - 1) * gl_por_nodo + 1, (nodo_id - 1) * gl_por_nodo + 2, (nodo_id - 1) * gl_por_nodo + 3]
    else:
        # Por defecto, barra
        gl_por_nodo = 2
        return [(nodo_id - 1) * gl_por_nodo + 1, (nodo_id - 1) * gl_por_nodo + 2]

def calcular_longitud_elemento(nodo_inicio, nodo_fin):
    """Calcular la longitud del elemento"""
    dx = nodo_fin['x'] - nodo_inicio['x']
    dy = nodo_fin['y'] - nodo_inicio['y']
    return math.sqrt(dx**2 + dy**2)

def calcular_angulo_beta(nodo_inicio, nodo_fin):
    """Calcular el ángulo β entre la horizontal y la barra"""
    dx = nodo_fin['x'] - nodo_inicio['x']
    dy = nodo_fin['y'] - nodo_inicio['y']
    return math.atan2(dy, dx)

def calcular_area_seccion(tipo_seccion, parametros):
    """Calcular el área de la sección según su tipo"""
    if tipo_seccion == "circular_solida":
        radio = parametros.get("radio", 0)
        return math.pi * radio**2
    elif tipo_seccion == "circular_hueca":
        radio_ext = parametros.get("radio_ext", 0)
        radio_int = parametros.get("radio_int", 0)
        return math.pi * (radio_ext**2 - radio_int**2)
    elif tipo_seccion == "rectangular":
        lado1 = parametros.get("lado1", 0)
        lado2 = parametros.get("lado2", 0)
        return lado1 * lado2
    elif tipo_seccion == "cuadrada":
        lado = parametros.get("lado", 0)
        return lado**2
    else:
        return parametros.get("area", 0.01)

def calcular_momento_inercia(tipo_seccion, parametros):
    """Calcular el momento de inercia según el tipo de sección"""
    if tipo_seccion == "circular_solida":
        radio = parametros.get("radio", 0)
        return (math.pi * radio**4) / 4
    elif tipo_seccion == "circular_hueca":
        radio_ext = parametros.get("radio_ext", 0)
        radio_int = parametros.get("radio_int", 0)
        return (math.pi * (radio_ext**4 - radio_int**4)) / 4
    elif tipo_seccion == "rectangular":
        lado1 = parametros.get("lado1", 0)  # base
        lado2 = parametros.get("lado2", 0)  # altura
        return (lado1 * lado2**3) / 12
    elif tipo_seccion == "cuadrada":
        lado = parametros.get("lado", 0)
        return (lado**4) / 12
    else:
        return parametros.get("inercia", 1e-6)

def generar_matriz_rigidez_barra(E, A, L, beta):
    """Generar matriz de rigidez para barra (4x4)"""
    c = math.cos(beta)
    s = math.sin(beta)
    factor = (E * A) / L
    
    matriz_global = factor * np.array([
        [c**2,      c*s,       -c**2,     -c*s],
        [c*s,       s**2,      -c*s,      -s**2],
        [-c**2,     -c*s,      c**2,      c*s],
        [-c*s,      -s**2,     c*s,       s**2]
    ])

    k_local = factor * np.array([
        [1, 0, -1, 0],
        [0, 0,  0, 0],
        [-1,0,  1, 0],
        [0, 0,  0, 0]
    ])

    return matriz_global, k_local

def generar_matriz_rigidez_viga(E, I, L):
    """Generar matriz de rigidez para viga pura (4x4) - solo flexión"""
    matriz = np.array([
        [12*E*I/L**3,  6*E*I/L**2,   -12*E*I/L**3,  6*E*I/L**2],
        [6*E*I/L**2,   4*E*I/L,      -6*E*I/L**2,   2*E*I/L],
        [-12*E*I/L**3, -6*E*I/L**2,  12*E*I/L**3,   -6*E*I/L**2],
        [6*E*I/L**2,   2*E*I/L,      -6*E*I/L**2,   4*E*I/L]
    ])
    return matriz, matriz

def generar_matriz_rigidez_viga_portico(E, A, I, L, beta):
    """Generar matriz de rigidez para viga pórtico (6x6)"""
    c = math.cos(beta)
    s = math.sin(beta)
    
    # Matriz de rigidez local de viga pórtico
    k_local = np.array([
        [E*A/L,     0,           0,        -E*A/L,    0,           0],
        [0,         12*E*I/L**3, 6*E*I/L**2, 0,       -12*E*I/L**3, 6*E*I/L**2],
        [0,         6*E*I/L**2,  4*E*I/L,   0,        -6*E*I/L**2,  2*E*I/L],
        [-E*A/L,    0,           0,         E*A/L,    0,           0],
        [0,         -12*E*I/L**3, -6*E*I/L**2, 0,      12*E*I/L**3, -6*E*I/L**2],
        [0,         6*E*I/L**2,  2*E*I/L,   0,        -6*E*I/L**2,  4*E*I/L]
    ])
    
    # Matriz de transformación
    T = np.array([
        [c,  s,  0,  0,  0,  0],
        [-s, c,  0,  0,  0,  0],
        [0,  0,  1,  0,  0,  0],
        [0,  0,  0,  c,  s,  0],
        [0,  0,  0, -s,  c,  0],
        [0,  0,  0,  0,  0,  1]
    ])
    
    # Transformar a coordenadas globales
    k_global = T.T @ k_local @ T

    return k_global, k_local

def generar_matriz_transformacion_viga_portico(beta):
    """Generar matriz de transformación de coordenadas para viga pórtico"""
    c = math.cos(beta)
    s = math.sin(beta)
    
    T = np.array([
        [c,  s,  0,  0,  0,  0],
        [-s, c,  0,  0,  0,  0],
        [0,  0,  1,  0,  0,  0],
        [0,  0,  0,  c,  s,  0],
        [0,  0,  0, -s,  c,  0],
        [0,  0,  0,  0,  0,  1]
    ])
    return T
def hermite_interpolation(v1, theta1, v2, theta2, L, num_points=50):
    """
    Calcula la forma de la deflexión de una viga usando polinomios de Hermite.
    Retorna las coordenadas locales (x, v) de la curva.
    """
    x_local = np.linspace(0, L, num_points)
    s = x_local / L  # Coordenada normalizada

    # Funciones de forma cúbicas de Hermite
    H1 = 2*s**3 - 3*s**2 + 1
    H2 = (s**3 - 2*s**2 + s) * L
    H3 = -2*s**3 + 3*s**2
    H4 = (s**3 - s**2) * L

    # Deflexión transversal v(x) en coordenadas locales
    v_local = H1*v1 + H2*theta1 + H3*v2 + H4*theta2
    
    return x_local, v_local

def crear_grafico_interactivo_moderno():
    """Crear un gráfico interactivo con estilo moderno"""
    fig = go.Figure()

    # Configurar aspecto moderno del gráfico
    fig.update_layout(
        title=dict(
            text="Editor Interactivo de Estructura",
            font=dict(family="Inter, sans-serif", size=20, color="#111827", weight=700),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title=dict(text="X [m]", font=dict(family="Inter, sans-serif", size=14, color="#374151", weight=600)),
            showgrid=True,
            gridcolor="#E5E7EB",
            gridwidth=1,
            zeroline=True,
            zerolinecolor="#9CA3AF",
            zerolinewidth=2,
            range=[-10, 10],
            tickfont=dict(family="Inter, sans-serif", size=12, color="#6B7280"),
            linecolor="#E5E7EB",
            mirror=True
        ),
        yaxis=dict(
            title=dict(text="Y [m]", font=dict(family="Inter, sans-serif", size=14, color="#374151", weight=600)),
            showgrid=True,
            gridcolor="#E5E7EB",
            gridwidth=1,
            zeroline=True,
            zerolinecolor="#9CA3AF",
            zerolinewidth=2,
            range=[-10, 10],
            scaleanchor="x",
            scaleratio=1,
            tickfont=dict(family="Inter, sans-serif", size=12, color="#6B7280"),
            linecolor="#E5E7EB",
            mirror=True
        ),
        showlegend=True,
        legend=dict(
            font=dict(family="Inter, sans-serif", size=12, color="#374151", weight=500),
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='#E5E7EB',
            borderwidth=1,
            x=1,
            y=1,
            xanchor='right',
            yanchor='top'
        ),
        height=600,
        margin=dict(l=60, r=60, t=80, b=60),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Inter, sans-serif")
    )

    # Añadir nodos existentes con estilo moderno
    nodos_fijos_x = []
    nodos_fijos_y = []
    nodos_fijos_text = []

    nodos_libres_x = []
    nodos_libres_y = []
    nodos_libres_text = []

    for nodo in st.session_state.nodos_interactivos:
        if nodo['tipo'] == 'fijo':
            nodos_fijos_x.append(nodo['x'])
            nodos_fijos_y.append(nodo['y'])
            nodos_fijos_text.append(f"Nodo {nodo['id']}<br>({nodo['x']:.1f}, {nodo['y']:.1f})<br>Tipo: Fijo")
        else:
            nodos_libres_x.append(nodo['x'])
            nodos_libres_y.append(nodo['y'])
            nodos_libres_text.append(f"Nodo {nodo['id']}<br>({nodo['x']:.1f}, {nodo['y']:.1f})<br>Tipo: Libre")

    # Añadir nodos fijos con estilo moderno
    if nodos_fijos_x:
        fig.add_trace(go.Scatter(
            x=nodos_fijos_x,
            y=nodos_fijos_y,
            mode='markers+text',
            marker=dict(
                size=12,
                color='#DC2626',
                line=dict(width=2, color='#991B1B'),
                symbol='circle'
            ),
            text=[f"{nodo['id']}" for nodo in st.session_state.nodos_interactivos if nodo['tipo'] == 'fijo'],
            textposition="middle center",
            textfont=dict(size=10, color='white', family="Inter, sans-serif", weight=700),
            hoverinfo='text',
            hovertext=nodos_fijos_text,
            name='Nodos Fijos',
            hovertemplate='<b>%{hovertext}</b><extra></extra>'
        ))

    # Añadir nodos libres con estilo moderno
    if nodos_libres_x:
        fig.add_trace(go.Scatter(
            x=nodos_libres_x,
            y=nodos_libres_y,
            mode='markers+text',
            marker=dict(
                size=12,
                color='#2563EB',
                line=dict(width=2, color='#1D4ED8'),
                symbol='circle'
            ),
            text=[f"{nodo['id']}" for nodo in st.session_state.nodos_interactivos if nodo['tipo'] == 'libre'],
            textposition="middle center",
            textfont=dict(size=10, color='white', family="Inter, sans-serif", weight=700),
            hoverinfo='text',
            hovertext=nodos_libres_text,
            name='Nodos Libres',
            hovertemplate='<b>%{hovertext}</b><extra></extra>'
        ))

    # Añadir elementos con estilo moderno
    for elemento in st.session_state.elementos_interactivos:
        nodo_inicio = next((n for n in st.session_state.nodos_interactivos if n['id'] == elemento['nodo_inicio']), None)
        nodo_fin = next((n for n in st.session_state.nodos_interactivos if n['id'] == elemento['nodo_fin']), None)

        if nodo_inicio and nodo_fin:
            # Calcular punto medio para etiqueta
            mid_x = (nodo_inicio['x'] + nodo_fin['x']) / 2
            mid_y = (nodo_inicio['y'] + nodo_fin['y']) / 2
            longitud = calcular_longitud_elemento(nodo_inicio, nodo_fin)

            # Añadir etiqueta de elemento con estilo moderno
            fig.add_trace(go.Scatter(
                x=[mid_x],
                y=[mid_y],
                mode='text',
                text=[f"E{elemento['id']}"],
                textposition="middle center",
                textfont=dict(size=10, color='#111827', family="Inter, sans-serif", weight=600),
                hoverinfo='skip',
                showlegend=False
            ))

            # Añadir elemento con estilo moderno
            fig.add_trace(go.Scatter(
                x=[nodo_inicio['x'], nodo_fin['x']],
                y=[nodo_inicio['y'], nodo_fin['y']],
                mode='lines',
                line=dict(width=4, color='#000000'),
                name=f"{st.session_state.tipo_elemento.title()} {elemento['id']}",
                hoverinfo='text',
                hovertext=f"<b>{st.session_state.tipo_elemento.title()} {elemento['id']}</b><br>Nodo {nodo_inicio['id']} → Nodo {nodo_fin['id']}<br>Longitud: {longitud:.3f} m",
                showlegend=True,
                hovertemplate='%{hovertext}<extra></extra>'
            ))

    # Configurar interactividad
    fig.update_layout(
        dragmode='pan',
        clickmode='event+select',
        hovermode='closest'
    )

    return fig

def agregar_nodo_interactivo(x, y, tipo='libre'):
    nodo_id = len(st.session_state.nodos_interactivos) + 1
    gl_globales = calcular_grados_libertad_globales(nodo_id)
    
    nuevo_nodo = {
        'id': nodo_id,
        'x': x,
        'y': y,
        'tipo': tipo,
        'grados_libertad_globales': gl_globales
    }
    
    st.session_state.nodos_interactivos.append(nuevo_nodo)
    return nodo_id

def agregar_elemento_interactivo(nodo_inicio_id, nodo_fin_id):
    if nodo_inicio_id == nodo_fin_id:
        return None
    
    for elem in st.session_state.elementos_interactivos:
        if (elem['nodo_inicio'] == nodo_inicio_id and elem['nodo_fin'] == nodo_fin_id) or \
            (elem['nodo_inicio'] == nodo_fin_id and elem['nodo_fin'] == nodo_inicio_id):
            return None
    
    elemento_id = len(st.session_state.elementos_interactivos) + 1
    
    nodo_inicio = next((n for n in st.session_state.nodos_interactivos if n['id'] == nodo_inicio_id), None)
    nodo_fin = next((n for n in st.session_state.nodos_interactivos if n['id'] == nodo_fin_id), None)
    
    if not nodo_inicio or not nodo_fin:
        return None
    
    gl_globales = nodo_inicio['grados_libertad_globales'] + nodo_fin['grados_libertad_globales']
    
    nuevo_elemento = {
        'id': elemento_id,
        'nodo_inicio': nodo_inicio_id,
        'nodo_fin': nodo_fin_id,
        'grados_libertad_global': gl_globales,
        'tipo': st.session_state.tipo_elemento.title(),
        'material': None,
        'tipo_seccion': None,
        'parametros_seccion': {}
    }
    
    st.session_state.elementos_interactivos.append(nuevo_elemento)
    return elemento_id

def eliminar_nodo_interactivo(nodo_id):
    st.session_state.nodos_interactivos = [n for n in st.session_state.nodos_interactivos if n['id'] != nodo_id]
    for i, nodo in enumerate(st.session_state.nodos_interactivos):
        nodo['id'] = i + 1
        nodo['grados_libertad_globales'] = calcular_grados_libertad_globales(i + 1)
    st.session_state.elementos_interactivos = [e for e in st.session_state.elementos_interactivos 
                                        if e['nodo_inicio'] != nodo_id and e['nodo_fin'] != nodo_id]
    st.rerun()

def eliminar_elemento_interactivo(elemento_id):
    st.session_state.elementos_interactivos = [e for e in st.session_state.elementos_interactivos if e['id'] != elemento_id]
    for i, elemento in enumerate(st.session_state.elementos_interactivos):
        elemento['id'] = i + 1
    st.rerun()

def transferir_datos_interactivos():
    st.session_state.nodos = st.session_state.nodos_interactivos.copy()
    st.session_state.num_nodos = len(st.session_state.nodos)
    st.session_state.num_fijos = sum(1 for n in st.session_state.nodos if n['tipo'] == 'fijo')
    st.session_state.num_libres = st.session_state.num_nodos - st.session_state.num_fijos
    st.session_state.elementos = []
    st.session_state.matrices_elementos = {}
    st.session_state.num_elementos = len(st.session_state.elementos_interactivos)
    
    # Pre-poblar st.session_state.elementos desde interactivos para que grupos funcione
    for elem_interactivo in st.session_state.elementos_interactivos:
        st.session_state.elementos.append(elem_interactivo.copy())

    st.session_state.step = 7  # Ir directamente a definición de elementos
    st.rerun()

def visualizar_estructura_moderna(mostrar_deformada=False, factor_escala=10):
    """Visualizar la estructura con estilo moderno minimalista - VERSIÓN CORREGIDA"""
    if not st.session_state.nodos:
        st.warning("No hay nodos para visualizar")
        return None
    
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(14, 10), facecolor='white')
    ax.set_facecolor('white')

    nodos_deformados = []
    all_x = [nodo['x'] for nodo in st.session_state.nodos]
    all_y = [nodo['y'] for nodo in st.session_state.nodos]

    if mostrar_deformada and st.session_state.resultados:
        for nodo in st.session_state.nodos:
            nodo_deformado = nodo.copy()
            dx, dy = 0, 0
            
            if nodo['tipo'] != 'fijo':
                gl_indices = [gl - 1 for gl in nodo['grados_libertad_globales']]
                desplazamientos_res = st.session_state.resultados['desplazamientos']
                
                if st.session_state.tipo_elemento == "barra":
                    dx = desplazamientos_res[gl_indices[0]] if len(gl_indices) > 0 else 0
                    dy = desplazamientos_res[gl_indices[1]] if len(gl_indices) > 1 else 0
                elif st.session_state.tipo_elemento == "viga":
                    dy = desplazamientos_res[gl_indices[0]] if len(gl_indices) > 0 else 0
                elif st.session_state.tipo_elemento == "viga_portico":
                    dx = desplazamientos_res[gl_indices[0]] if len(gl_indices) > 0 else 0
                    dy = desplazamientos_res[gl_indices[1]] if len(gl_indices) > 1 else 0

            nodo_deformado['x'] += dx * factor_escala
            nodo_deformado['y'] += dy * factor_escala
            nodos_deformados.append(nodo_deformado)
            
            all_x.append(nodo_deformado['x'])
            all_y.append(nodo_deformado['y'])

    x_min, x_max = min(all_x), max(all_x)
    y_min, y_max = min(all_y), max(all_y)
    x_range = x_max - x_min if x_max > x_min else 2
    y_range = y_max - y_min if y_max > y_min else 2
    padding = 0.15 * max(x_range, y_range, 1)
    
    ax.set_xlim(x_min - padding, x_max + padding)
    ax.set_ylim(y_min - padding, y_max + padding)

    if mostrar_deformada:
        for elemento in st.session_state.elementos:
            nodo_inicio = next((n for n in st.session_state.nodos if n['id'] == elemento['nodo_inicio']), None)
            nodo_fin = next((n for n in st.session_state.nodos if n['id'] == elemento['nodo_fin']), None)
            if nodo_inicio and nodo_fin:
                ax.plot([nodo_inicio['x'], nodo_fin['x']], 
                        [nodo_inicio['y'], nodo_fin['y']], 
                        color='#ced4da', linewidth=2, alpha=0.8, linestyle='--', 
                        label='Estructura Original' if 'Estructura Original' not in ax.get_legend_handles_labels()[1] else "")

    for elemento in st.session_state.elementos:
        nodo_inicio = next((n for n in st.session_state.nodos if n['id'] == elemento['nodo_inicio']), None)
        nodo_fin = next((n for n in st.session_state.nodos if n['id'] == elemento['nodo_fin']), None)
        
        if not (nodo_inicio and nodo_fin):
            continue

        if mostrar_deformada and nodos_deformados:
            nodo_inicio_def = next((n for n in nodos_deformados if n['id'] == elemento['nodo_inicio']), None)
            nodo_fin_def = next((n for n in nodos_deformados if n['id'] == elemento['nodo_fin']), None)

            if nodo_inicio_def and nodo_fin_def and st.session_state.tipo_elemento in ["viga", "viga_portico"]:
                U_global_vec = st.session_state.resultados['desplazamientos']
                
                if st.session_state.tipo_elemento == "viga":
                    gl_i, gl_j = nodo_inicio['grados_libertad_globales'], nodo_fin['grados_libertad_globales']
                    u_local = [0, U_global_vec[gl_i[0]-1], U_global_vec[gl_i[1]-1], 0, U_global_vec[gl_j[0]-1], U_global_vec[gl_j[1]-1]]
                else:
                    gl_i, gl_j = nodo_inicio['grados_libertad_globales'], nodo_fin['grados_libertad_globales']
                    T = generar_matriz_transformacion_viga_portico(elemento['beta'])
                    U_global_elem = np.array([U_global_vec[i-1] for i in elemento['grados_libertad_global']])
                    u_local = T @ U_global_elem
                
                theta1_local, theta2_local = u_local[2], u_local[5]
                
                p_start_def = np.array([nodo_inicio_def['x'], nodo_inicio_def['y']])
                p_end_def = np.array([nodo_fin_def['x'], nodo_fin_def['y']])
                vec_deformed = p_end_def - p_start_def
                len_deformed = np.linalg.norm(vec_deformed)

                if len_deformed > 1e-9:
                    t_vec = vec_deformed / len_deformed
                    n_vec = np.array([-t_vec[1], t_vec[0]])
                    
                    x_local, v_local = hermite_interpolation(
                        v1=U_global_vec[gl_i[0]-1],
                        theta1=U_global_vec[gl_i[1]-1],
                        v2=U_global_vec[gl_j[0]-1],
                        theta2=U_global_vec[gl_j[1]-1],
                        L=elemento['longitud'],
                        num_points=50
                    )

                    baseline_points = p_start_def + np.outer(x_local * (len_deformed / elemento['longitud']), t_vec)
                    final_curve_points = baseline_points + np.outer(v_local * factor_escala, n_vec)

                    ax.plot(final_curve_points[:, 0], final_curve_points[:, 1],
                            color='#000000', linewidth=3, alpha=0.9,
                            label='Estructura Deformada' if 'Estructura Deformada' not in ax.get_legend_handles_labels()[1] else "")

            
            elif nodo_inicio_def and nodo_fin_def:
                ax.plot([nodo_inicio_def['x'], nodo_fin_def['x']], [nodo_inicio_def['y'], nodo_fin_def['y']], 
                        color='#000000', linewidth=3, alpha=0.9,
                        label='Estructura Deformada' if 'Estructura Deformada' not in ax.get_legend_handles_labels()[1] else "")
        else:
            ax.plot([nodo_inicio['x'], nodo_fin['x']], [nodo_inicio['y'], nodo_fin['y']], color='#000000', linewidth=3, alpha=0.9)

        mid_x, mid_y = (nodo_inicio['x'] + nodo_fin['x']) / 2, (nodo_inicio['y'] + nodo_fin['y']) / 2
        ax.text(mid_x, mid_y, f'E{elemento["id"]}', ha='center', va='center', fontsize=9, fontweight='600',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="black", linewidth=1.5, alpha=0.95), zorder=20)

    for i, nodo in enumerate(st.session_state.nodos):
        color_orig = '#DC2626' if nodo['tipo'] == 'fijo' else '#6c757d'
        ax.add_patch(plt.Circle((nodo['x'], nodo['y']), 0.025 * max(x_range, y_range, 1), color=color_orig, zorder=10))
        
        if mostrar_deformada and nodos_deformados:
            nodo_def = nodos_deformados[i]
            color_def = '#DC2626' if nodo['tipo'] == 'fijo' else '#28a745'
            ax.add_patch(plt.Circle((nodo_def['x'], nodo_def['y']), 0.025 * max(x_range, y_range, 1), color=color_def, zorder=11))
            ax.plot([nodo['x'], nodo_def['x']], [nodo['y'], nodo_def['y']], color='#6c757d', linestyle=':', linewidth=1.5)
        
        ax.text(nodo['x'], nodo['y'], str(nodo['id']), ha='center', va='center', fontsize=9, fontweight='700', color='white', zorder=12)

    ax.set_xlabel('X [m]', fontsize=12, fontweight='600')
    ax.set_ylabel('Y [m]', fontsize=12, fontweight='600')
    ax.set_title(f'Estructura Deformada (x{factor_escala})' if mostrar_deformada else 'Estructura Original', fontsize=16, fontweight='700', pad=20)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='#adb5bd')
    ax.set_aspect('equal', adjustable='box')
    
    handles, labels = ax.get_legend_handles_labels()
    if handles:
        unique_labels = dict(zip(labels, handles))
        ax.legend(unique_labels.values(), unique_labels.keys(), loc='upper right', frameon=True, fancybox=True, shadow=True, fontsize=10)
    
    plt.tight_layout()
    return fig

def crear_tabla_nodos():
    """Crear tabla de nodos con coordenadas y grados de libertad"""
    if not st.session_state.nodos:
        return pd.DataFrame()

    nodos_data = []
    for nodo in st.session_state.nodos:
        gl_str = ", ".join([f"GL{gl}" for gl in nodo['grados_libertad_globales']])
        nodos_data.append({
            'ID': nodo['id'],
            'Tipo': nodo['tipo'].title(),
            'X [m]': f"{nodo['x']:.3f}",
            'Y [m]': f"{nodo['y']:.3f}",
            'Grados de Libertad': gl_str,
            'Coordenadas': f"({nodo['x']:.3f}, {nodo['y']:.3f})"
        })

    return pd.DataFrame(nodos_data)

def crear_tabla_conectividad():
    """Crear tabla de conectividad de elementos"""
    if not st.session_state.elementos:
        return pd.DataFrame()

    conectividad_data = []
    for elem in st.session_state.elementos:
        tipo_seccion_val = elem.get('tipo_seccion')
        if tipo_seccion_val:
            seccion_str = tipo_seccion_val.replace('_', ' ').title()
        else:
            seccion_str = "No Definida"
        if 'inercia' not in elem:
            elem['inercia'] = calcular_momento_inercia(elem.get('tipo_seccion'), elem.get('parametros_seccion', {}))

        conectividad_data.append({
            'Elemento': elem.get('id', 'N/A'),
            'Tipo': elem.get('tipo', st.session_state.tipo_elemento.title()),
            'Nodo Inicio': elem.get('nodo_inicio', 'N/A'),
            'Nodo Fin': elem.get('nodo_fin', 'N/A'),
            'Material': elem.get('material', 'No Definido'),
            'Sección': seccion_str,
            'Área [m²]': f"{elem.get('area', 0.0):.6f}",
            'Inercia [m⁴]': f"{elem.get('inercia', 0.0):.6e}",
            'Longitud [m]': f"{elem.get('longitud', 0.0):.3f}",
            'Ángulo β [rad]': f"{elem.get('beta', 0.0):.4f}",
            'GL Globales': str(elem.get('grados_libertad_global', '[]'))
        })

    return pd.DataFrame(conectividad_data)



def resolver_sistema():
    """Resolver el sistema de ecuaciones automáticamente"""
    if not st.session_state.elementos or not st.session_state.grados_libertad_info:
        return None
    
    try:
        # Ensamblar matriz K global numérica
        max_gl = len(st.session_state.grados_libertad_info)
        K_global = np.zeros((max_gl, max_gl))
        
        # Ensamblar usando las matrices numéricas de cada elemento
        for elemento in st.session_state.elementos:
            if elemento['id'] in st.session_state.matrices_elementos:
                matriz_num = np.array(st.session_state.matrices_elementos[elemento['id']]['numerica'])
                
                for i, gl_i in enumerate(elemento['grados_libertad_global']):
                    for j, gl_j in enumerate(elemento['grados_libertad_global']):
                        K_global[gl_i-1, gl_j-1] += matriz_num[i][j]
        
        # Vectores de fuerzas y desplazamientos
        F = np.zeros(max_gl)
        U = np.zeros(max_gl)
        
        for i, info in enumerate(st.session_state.grados_libertad_info):
            if info['fuerza_conocida']:
                F[i] = info['valor_fuerza']
            if info['desplazamiento_conocido']:
                U[i] = info['valor_desplazamiento']
        
        # Identificar incógnitas
        incognitas_u = [i for i, info in enumerate(st.session_state.grados_libertad_info) 
                        if not info['desplazamiento_conocido']]
        conocidos_u = [i for i, info in enumerate(st.session_state.grados_libertad_info) 
                        if info['desplazamiento_conocido']]
        
        # Resolver para desplazamientos desconocidos
        if incognitas_u:
            K_uu = K_global[np.ix_(incognitas_u, incognitas_u)]
            K_uk = K_global[np.ix_(incognitas_u, conocidos_u)] if conocidos_u else np.zeros((len(incognitas_u), 0))
            
            F_u = F[incognitas_u]
            U_k = U[conocidos_u] if conocidos_u else np.array([])
            
            
            F_efectivo = F_u - (K_uk @ U_k if conocidos_u else 0)
            
            if np.linalg.det(K_uu) != 0:
                U_u = np.linalg.solve(K_uu, F_efectivo)
                
                for i, idx in enumerate(incognitas_u):
                    U[idx] = U_u[i]
            else:
                return None
        
        # Calcular fuerzas resultantes
        F_calculado = K_global @ U
        
        # Corregir el problema con fuerzas conocidas
        for i, info in enumerate(st.session_state.grados_libertad_info):
            if info['fuerza_conocida']:
                F_calculado[i] = info['valor_fuerza']
        
        return {
            'K_global': K_global,
            'desplazamientos': U,
            'fuerzas': F_calculado,
            'determinante': np.linalg.det(K_global),
            'exito': True
        }
        
    except Exception as e:
        return None

def generar_pdf_reporte():
    """
    Genera un reporte PDF completo del análisis.
    Cada tabla y gráfico principal se coloca en una página horizontal separada.
    Incluye la matriz de rigidez global, las matrices de transformación locales
    y el gráfico de la estructura deformada.
    """
    buffer = io.BytesIO()
    # Usar pagesize horizontal para todas las páginas y ajustar márgenes
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4),
                            rightMargin=inch/2, leftMargin=inch/2,
                            topMargin=inch/2, bottomMargin=inch/2)
    styles = getSampleStyleSheet()
    story = []

    # Estilo para títulos de sección (centrado)
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.black,
        alignment=1 # 1 = Center
    )
    
    # Estilo para texto justificado
    normal_justified_style = ParagraphStyle(
        'NormalJustified',
        parent=styles['Normal'],
        alignment=4 # 4 = Justify
    )
    
    # --- PÁGINA 1: TÍTULO E INFORMACIÓN GENERAL ---
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=22,
        spaceAfter=20,
        alignment=1,
        textColor=colors.darkblue
    )
    story.append(Paragraph("Reporte de Análisis Estructural - Método Matricial", title_style))
    story.append(Spacer(1, 10))

    info_style = ParagraphStyle('InfoStyle', parent=styles['Normal'], fontSize=11, spaceAfter=5)
    story.append(Paragraph(f"<b>Usuario:</b> {st.session_state.get('usuario_nombre', 'N/A')}", info_style))
    story.append(Paragraph(f"<b>Tipo de Elemento:</b> {st.session_state.get('tipo_elemento', 'N/A').replace('_', ' ').title()}", info_style))
    story.append(Paragraph(f"<b>Modo de Análisis:</b> {st.session_state.get('modo', 'N/A').capitalize()}", info_style))
    story.append(Paragraph(f"<b>Fecha de Generación:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", info_style))
    story.append(PageBreak())

    # --- PÁGINA: TABLA DE NODOS ---
    story.append(Paragraph("Tabla de Nodos", section_title_style))
    df_nodos = crear_tabla_nodos()
    if not df_nodos.empty:
        nodos_data = [df_nodos.columns.tolist()] + df_nodos.values.tolist()
        nodos_table = Table(nodos_data, hAlign='CENTER')
        nodos_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(nodos_table)
    else:
        story.append(Paragraph("No hay datos de nodos disponibles.", normal_justified_style))
    story.append(PageBreak())

    # --- PÁGINA: TABLA DE CONECTIVIDAD ---
    story.append(Paragraph("Tabla de Conectividad de Elementos", section_title_style))
    df_conectividad = crear_tabla_conectividad()
    if not df_conectividad.empty:
        conectividad_data = [df_conectividad.columns.tolist()] + df_conectividad.values.tolist()
        conectividad_table = Table(conectividad_data, hAlign='CENTER')
        conectividad_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 7), # Tamaño de fuente reducido para tabla ancha
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(conectividad_table)
    else:
        story.append(Paragraph("No hay datos de conectividad disponibles.", normal_justified_style))
    story.append(PageBreak())

    # --- PÁGINAS DE RESULTADOS (SI EXISTEN) ---
    if st.session_state.get('resultados'):
        resultados = st.session_state.resultados

        # --- PÁGINA: TABLA DE RESULTADOS GLOBALES ---
        story.append(Paragraph("Resultados Globales (Fuerzas y Desplazamientos)", section_title_style))
        resultados_data = []
        headers = ['GL', 'Nodo', 'Dirección', 'Fuerza/Momento', 'Desplazamiento/Rotación']
        for i, (info, fuerza, desplazamiento) in enumerate(zip(
            st.session_state.grados_libertad_info,
            resultados['fuerzas'],
            resultados['desplazamientos']
        )):
            if info['direccion'] == 'θ':
                fuerza_formateada = f"{fuerza:.4f} N·m"
                desplaz_formateado = f"{desplazamiento:.6f} rad"
            else:
                fuerza_formateada = formatear_unidades(fuerza, "fuerza")
                desplaz_formateado = formatear_unidades(desplazamiento, "desplazamiento")
            
            resultados_data.append([
                f"GL{i+1}", f"N{info['nodo']}", info['direccion'],
                fuerza_formateada, desplaz_formateado
            ])
        
        resultados_table_data = [headers] + resultados_data
        resultados_table = Table(resultados_table_data, hAlign='CENTER')
        resultados_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(resultados_table)
        story.append(PageBreak())
        # --- PÁGINAS: MATRICES DE RIGIDEZ LOCALES (k') ---
        story.append(Paragraph("Matrices de Rigidez Locales por Elemento (k')", section_title_style))
        story.append(Paragraph(
            "Cada una de las siguientes páginas muestra la matriz de rigidez para un elemento en su propio "
            "sistema de coordenadas locales (antes de la rotación al sistema global).",
            normal_justified_style
        ))
        story.append(PageBreak())

        for elemento in st.session_state.get('elementos', []):
            matriz_local_list = st.session_state.matrices_elementos.get(elemento['id'], {}).get('local')
            
            if matriz_local_list:
                story.append(Paragraph(f"Matriz de Rigidez Local (k') - Elemento {elemento['id']}", section_title_style))
                
                # Definir etiquetas para los ejes de la matriz local
                if st.session_state.tipo_elemento == "barra":
                    labels = ["u1", "v1", "u2", "v2"]
                elif st.session_state.tipo_elemento == "viga":
                    labels = ["v1", "θ1", "v2", "θ2"]
                else:  # viga_portico
                    labels = ["u1", "v1", "θ1", "u2", "v2", "θ2"]

                # Preparar datos para la tabla
                header_k_local = [''] + labels
                data_k_local = [header_k_local]
                for i, row in enumerate(matriz_local_list):
                    formatted_row = [labels[i]] + [f'{val:.3e}' for val in row]
                    data_k_local.append(formatted_row)

                # Crear y estilizar la tabla
                num_cols = len(header_k_local)
                col_width = (doc.width) / num_cols
                
                k_local_table = Table(data_k_local, colWidths=[col_width]*num_cols, hAlign='CENTER')
                k_local_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.darkslateblue),
                    ('BACKGROUND', (0, 1), (0, -1), colors.darkslateblue),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('TEXTCOLOR', (0, 1), (0, -1), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('INNERGRID', (1, 1), (-1, -1), 0.25, colors.black),
                    ('BOX', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(k_local_table)
                story.append(PageBreak())

        # --- PÁGINA: MATRIZ DE RIGIDEZ GLOBAL (K) ---
        story.append(Paragraph("Matriz de Rigidez Global (K)", section_title_style))
        K_global = resultados.get('K_global')
        if K_global is not None:
            header_k = [''] + [f'GL {j+1}' for j in range(K_global.shape[1])]
            data_k = [header_k]
            for i, row in enumerate(K_global):
                formatted_row = [f'GL {i+1}'] + [f'{val:.3e}' for val in row]
                data_k.append(formatted_row)
            
            num_cols = len(header_k)
            col_width = (doc.width) / num_cols
            
            k_table = Table(data_k, colWidths=[col_width]*num_cols, hAlign='CENTER')
            k_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('BACKGROUND', (0, 1), (0, -1), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('TEXTCOLOR', (0, 1), (0, -1), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 6), # Tamaño de fuente muy pequeño para que quepa
                ('INNERGRID', (1, 1), (-1, -1), 0.25, colors.black),
                ('BOX', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(k_table)
        else:
            story.append(Paragraph("Matriz de rigidez global no disponible.", normal_justified_style))
        story.append(PageBreak())

        # --- PÁGINAS: MATRICES DE TRANSFORMACIÓN (Solo Viga Pórtico) ---
        if st.session_state.get('tipo_elemento') == "viga_portico":
            story.append(Paragraph("Matrices de Transformación Locales por Elemento (T)", section_title_style))
            story.append(Paragraph("Cada una de las siguientes páginas muestra la matriz de transformación para un elemento. Esta matriz convierte los desplazamientos y fuerzas del sistema de coordenadas locales (a lo largo del elemento) al sistema global (X, Y).", normal_justified_style))
            story.append(PageBreak())

            for elemento in st.session_state.get('elementos', []):
                story.append(Paragraph(f"Matriz de Transformación (T) - Elemento {elemento['id']}", section_title_style))
                story.append(Paragraph(f"<i>Ángulo del elemento β = {elemento.get('beta', 0):.4f} rad ({math.degrees(elemento.get('beta', 0)):.2f}°)</i>", styles['Italic']))

                T = generar_matriz_transformacion_viga_portico(elemento.get('beta', 0))
                data_t = [[f'{val:.4f}' for val in row] for row in T]

                t_table = Table(data_t, hAlign='CENTER')
                t_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('BOX', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 0), (2, 2), colors.lightcyan),
                    ('BACKGROUND', (3, 3), (5, 5), colors.lightcyan),
                ]))
                story.append(t_table)
                story.append(PageBreak())

        # --- PÁGINA: GRÁFICO DE ESTRUCTURA DEFORMADA ---
        story.append(Paragraph("Visualización de la Estructura Deformada", section_title_style))
        factor_escala = 100 # Se puede tomar del slider si se desea
        story.append(Paragraph(f"<i>Nota: La deformación se ha escalado por un factor de <b>{factor_escala}</b> para una mejor visualización. La estructura original se muestra en líneas discontinuas.</i>", styles['Italic']))
        
        try:
            fig_deformada = visualizar_estructura_moderna(mostrar_deformada=True, factor_escala=factor_escala)
            if fig_deformada:
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                    fig_deformada.savefig(tmp_file.name, dpi=300, bbox_inches='tight', facecolor='white')
                    plt.close(fig_deformada)
                    
                    img_deformada = Image(tmp_file.name, width=10*inch, height=6.5*inch, hAlign='CENTER')
                    story.append(img_deformada)
                    
                    os.unlink(tmp_file.name)
            else:
                story.append(Paragraph("No se pudo generar el gráfico de la estructura deformada.", normal_justified_style))
        except Exception as e:
            story.append(Paragraph(f"Error al generar el gráfico de la estructura deformada: {e}", normal_justified_style))

    else:
        story.append(Paragraph("No hay resultados de análisis disponibles para mostrar en el reporte.", section_title_style))

    doc.build(story)
    buffer.seek(0)
    return buffer

def mostrar_barra_progreso():
    """Mostrar barra de progreso estilo web moderno"""
    if st.session_state.step == 0:
        return
    
    pasos = [
        "Selección de Tipo",
        "Información del Usuario",
        "Selección de Modo",
        "Número de Nodos", 
        "Clasificación de Nodos",
        "Coordenadas de Nodos",
        "Número de Elementos",
        "Definición de Elementos", 
        "Configuración de Incógnitas",
        "Resultados"
    ]
    
    st.markdown("""
    <div class='progress-bar'>
        <div style='max-width: 1200px; margin: 0 auto; padding: 0 2rem;'>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;'>
                <h1 style='margin: 0; font-size: 1.8rem;'>Análisis Estructural - Método de Matrices</h1>
                <div style='display: flex; gap: 1rem;'>
    """, unsafe_allow_html=True)
    
    # Botones de control en la barra
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔄 Reiniciar", key="reset_top"):
            reset_app()
    with col2:
        if st.session_state.step > 1:
            if st.button("← Anterior", key="prev_top"):
                prev_step()
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Mostrar pasos con círculos
    progress_html = "<div class='progress-steps'>"
    
    for i, paso in enumerate(pasos, 1):
        if i < st.session_state.step:
            circle_class = "completed"
        elif i == st.session_state.step:
            circle_class = "current"
        else:
            circle_class = "pending"
        
        progress_html += f"""
        <div class='progress-step'>
            <div class='step-circle {circle_class}'>
                {'✓' if i < st.session_state.step else i}
            </div>
        """
        
        if i < len(pasos):
            line_class = "completed" if i < st.session_state.step else ""
            progress_html += f"<div class='step-line {line_class}'></div>"
        
        progress_html += "</div>"
    
    progress_html += "</div>"
    
    # Mostrar paso actual
    progress_html += f"""
        <div style='text-align: center; margin-top: 1rem;'>
            <div style='font-size: 1.1rem; font-weight: 600; color: var(--gray-800);'>
                Paso {st.session_state.step}: {pasos[st.session_state.step - 1]}
            </div>
        </div>
    </div>
    """
    
    st.markdown(progress_html, unsafe_allow_html=True)

def mostrar_sidebar_mejorado():
    """Mostrar sidebar mejorado solo cuando hay tipo seleccionado"""
    if st.session_state.tipo_elemento is None:
        return
    
    # Agregar clase CSS para mostrar sidebar
    st.markdown('<div class="show-sidebar">', unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("### Progreso del Análisis")
        
        # Indicador de paso actual
        pasos = [
            "0. Selección de Tipo",
            "1. Información del Usuario",
            "2. Selección de Modo",
            "3. Número de Nodos",
            "4. Clasificación de Nodos", 
            "5. Coordenadas de Nodos",
            "6. Número de Elementos",
            "7. Definición de Elementos",
            "8. Configuración de Incógnitas",
            "9. Resultados"
        ]
        
        for i, paso in enumerate(pasos):
            if i == st.session_state.step:
                st.markdown(f"**→ {paso}**")
            elif i < st.session_state.step:
                st.markdown(f"✓ {paso}")
            else:
                st.markdown(f"⏳ {paso}")
        
        st.divider()
        
        # Información del proyecto
        st.markdown("### Información del Proyecto")
        
        if st.session_state.usuario_nombre:
            st.markdown(f"**Usuario:** {st.session_state.usuario_nombre}")
        
        if st.session_state.tipo_elemento:
            st.markdown(f"**Tipo:** {st.session_state.tipo_elemento.replace('_', ' ').title()}")
        
        if st.session_state.modo:
            st.markdown(f"**Modo:** {st.session_state.modo.capitalize()}")
        
        if st.session_state.step >= 5 and st.session_state.nodos:
            st.markdown(f"**Nodos:** {len(st.session_state.nodos)}")
        
        if st.session_state.step >= 7 and st.session_state.elementos:
            st.markdown(f"**Elementos:** {len(st.session_state.elementos)}")
        
        if st.session_state.step >= 8 and st.session_state.grados_libertad_info:
            st.markdown(f"**Grados de Libertad:** {len(st.session_state.grados_libertad_info)}")
        
        st.markdown(f"**Fecha:** {datetime.now().strftime('%d/%m/%Y')}")
        st.markdown(f"**Hora:** {datetime.now().strftime('%H:%M:%S')}")

def mostrar_matriz_formateada_moderna(matriz, titulo="Matriz", es_simbolica=True):
    """Mostrar matriz en formato tabla con estilo moderno"""
    if matriz is None or len(matriz) == 0:
        st.warning(f"⚠️ Matriz '{titulo}' vacía o no disponible.")
        return

    st.markdown(f"##### {titulo}")

    if es_simbolica:
        df = pd.DataFrame(matriz)
    else:
        # Formatear números para legibilidad
        matriz_formateada = []
        for fila in matriz:
            fila_formateada = [f"{valor:.3e}" for valor in fila]
            matriz_formateada.append(fila_formateada)
        
        df = pd.DataFrame(matriz_formateada)
        if len(matriz) > 0:
            df.index = [f"GL {i+1}" for i in range(len(matriz))]
            df.columns = [f"GL {j+1}" for j in range(len(matriz[0]))]

    st.dataframe(df, use_container_width=True)

    # Botón de descarga
    csv_data = df.to_csv(sep=';').encode('utf-8')
    st.download_button(
        label=f"📋 Descargar Tabla '{titulo}'",
        data=csv_data,
        file_name=f"{titulo.replace(' ', '_')}.csv",
        mime="text/csv",
        key=f"download_{titulo.replace(' ', '_')}" # Clave única para el botón
    )

# Mostrar barra de progreso si no estamos en step 0
mostrar_barra_progreso()

# Mostrar sidebar solo si hay tipo seleccionado
mostrar_sidebar_mejorado()

# Contenido principal según el paso
if st.session_state.step == 0:
    # Página de selección de tipo de elemento
    st.markdown("""
    <div style='background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%); 
                min-height: 80vh; display: flex; align-items: center; justify-content: center; 
                margin: -1rem; padding: 2rem; border-radius: 15px;'>
        <div style='max-width: 1200px; text-align: center;'>
            <h1 style='font-size: 4rem; margin-bottom: 1rem; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
                Análisis Estructural
            </h1>
            <p style='font-size: 1.5rem; color: rgba(255,255,255,0.9); margin-bottom: 3rem; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);'>
                Método de Matrices • Seleccione el Tipo de Elemento
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tarjetas de tipo de elemento
    st.markdown("## Seleccione el Tipo de Elemento Estructural")
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown("""
        <div style='background: white; padding: 2rem; border-radius: 15px; border: 2px solid #e2e8f0; 
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 1rem 0;'>
            <h3 style='color: #1a202c; font-size: 1.8rem; margin-bottom: 1rem; text-align: center;'>🔗 Modo Barra</h3>
            <p style='color: #4a5568; line-height: 1.6; margin-bottom: 1.5rem; text-align: center;'>
                Elementos que solo resisten fuerzas axiales.<br><br>
                • 2 grados de libertad por nodo (X, Y)<br>
                • Matriz de rigidez 4×4<br>
                • Solo esfuerzos de tracción/compresión
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("SELECCIONAR BARRA", key="barra_mode", type="primary", use_container_width=True):
            set_tipo_elemento("barra")
    
    with col2:
        st.markdown("""
        <div style='background: white; padding: 2rem; border-radius: 15px; border: 2px solid #e2e8f0; 
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 1rem 0;'>
            <h3 style='color: #1a202c; font-size: 1.8rem; margin-bottom: 1rem; text-align: center;'>📏 Modo Viga</h3>
            <p style='color: #4a5568; line-height: 1.6; margin-bottom: 1.5rem; text-align: center;'>
                Elementos que resisten flexión pura.<br><br>
                • 2 grados de libertad por nodo (Y, θ)<br>
                • Matriz de rigidez 4×4<br>
                • Solo esfuerzos de flexión y cortante
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("SELECCIONAR VIGA", key="viga_mode", type="primary", use_container_width=True):
            set_tipo_elemento("viga")
    
    with col3:
        st.markdown("""
        <div style='background: white; padding: 2rem; border-radius: 15px; border: 2px solid #e2e8f0; 
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 1rem 0;'>
            <h3 style='color: #1a202c; font-size: 1.8rem; margin-bottom: 1rem; text-align: center;'>🏗️ Modo Viga Pórtico</h3>
            <p style='color: #4a5568; line-height: 1.6; margin-bottom: 1.5rem; text-align: center;'>
                Elementos que combinan barra y viga.<br><br>
                • 3 grados de libertad por nodo (X, Y, θ)<br>
                • Matriz de rigidez 6×6<br>
                • Esfuerzos axiales y de flexión
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("SELECCIONAR VIGA PÓRTICO", key="viga_portico_mode", type="primary", use_container_width=True):
            set_tipo_elemento("viga_portico")
    
    # Información adicional
    st.markdown("""
    <div style='background: white; padding: 2rem; border-radius: 15px; border: 2px solid #e2e8f0; 
                box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 2rem 0;'>
        <h3 style='color: #1a202c; font-size: 1.5rem; margin-bottom: 1.5rem; text-align: center;'>
            🎯 Características del Sistema Avanzado
        </h3>
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; color: #4a5568;'>
            <div style='text-align: left;'>
                <p>✓ <strong>Múltiples tipos de elementos</strong> estructurales</p>
                <p>✓ <strong>Matrices de transformación</strong> automáticas</p>
                <p>✓ <strong>Cálculo de desplazamientos nodales</strong></p>
                <p>✓ <strong>Base de datos de materiales</strong> aeroespaciales</p>
                <p>✓ <strong>Exportación PDF y Excel</strong> completa</p>
            </div>
            <div style='text-align: left;'>
                <p>✓ <strong>Visualización gráfica</strong> optimizada</p>
                <p>✓ <strong>Formateo inteligente de unidades</strong></p>
                <p>✓ <strong>Cálculo automático</strong> en tiempo real</p>
                <p>✓ <strong>Edición y eliminación</strong> de elementos</p>
                <p>✓ <strong>Secciones personalizables</strong> avanzadas</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.step == 1:
    st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)
    st.markdown("## Información del Usuario")
    st.markdown(f"Bienvenido al sistema de análisis estructural con elementos tipo **{st.session_state.tipo_elemento.replace('_', ' ').title()}**.")
    
    usuario_nombre = st.text_input("👤 Nombre completo:", 
                                    value=st.session_state.usuario_nombre,
                                    placeholder="Ej: Juan Pérez")
    
    if usuario_nombre:
        st.session_state.usuario_nombre = usuario_nombre
        
        # Mostrar información específica del tipo de elemento seleccionado - CORREGIDO
        if st.session_state.tipo_elemento == "barra":
            st.markdown("""
            <div style='background: white; padding: 2rem; border-radius: 15px; border: 2px solid #e2e8f0; 
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 2rem 0; text-align: center;'>
                <h4 style='color: #1a202c; font-size: 1.5rem; margin-bottom: 1.5rem;'>
                    🔗 Análisis de Barras
                </h4>
                <div style='color: #4a5568; line-height: 1.8;'>
                    <p>• <strong>2 grados de libertad por nodo:</strong> desplazamientos X e Y</p>
                    <p>• <strong>Matriz de rigidez:</strong> 4×4 por elemento</p>
                    <p>• <strong>Esfuerzos:</strong> solo axiales (tracción/compresión)</p>
                    <p>• <strong>Aplicaciones:</strong> cerchas, estructuras reticuladas</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif st.session_state.tipo_elemento == "viga":
            st.markdown("""
            <div style='background: white; padding: 2rem; border-radius: 15px; border: 2px solid #e2e8f0; 
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 2rem 0; text-align: center;'>
                <h4 style='color: #1a202c; font-size: 1.5rem; margin-bottom: 1.5rem;'>
                    📏 Análisis de Vigas
                </h4>
                <div style='color: #4a5568; line-height: 1.8;'>
                    <p>• <strong>2 grados de libertad por nodo:</strong> desplazamiento Y y rotación θ</p>
                    <p>• <strong>Matriz de rigidez:</strong> 4×4 por elemento</p>
                    <p>• <strong>Esfuerzos:</strong> flexión y cortante</p>
                    <p>• <strong>Aplicaciones:</strong> vigas continuas, marcos simples</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:  # viga_portico
            st.markdown("""
            <div style='background: white; padding: 2rem; border-radius: 15px; border: 2px solid #e2e8f0; 
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 2rem 0; text-align: center;'>
                <h4 style='color: #1a202c; font-size: 1.5rem; margin-bottom: 1.5rem;'>
                    🏗️ Análisis de Vigas Pórtico
                </h4>
                <div style='color: #4a5568; line-height: 1.8;'>
                    <p>• <strong>3 grados de libertad por nodo:</strong> desplazamientos X, Y y rotación θ</p>
                    <p>• <strong>Matriz de rigidez:</strong> 6×6 por elemento</p>
                    <p>• <strong>Esfuerzos:</strong> axiales, flexión y cortante</p>
                    <p>• <strong>Aplicaciones:</strong> pórticos, marcos rígidos, estructuras complejas</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: white; padding: 2rem; border-radius: 15px; border: 2px solid #e2e8f0; 
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 2rem 0; text-align: center;'>
            <h4 style='color: #1a202c; font-size: 1.5rem; margin-bottom: 1.5rem;'>
                🧪 Materiales Aeroespaciales Incluidos
            </h4>
            <div style='color: #4a5568; line-height: 1.8;'>
                <p>Aluminio 6061-T6, 7075-T6, 2024-T3 • Titanio Ti-6Al-4V • Acero 4130 •</p>
                <p>Fibra de Carbono T300 • Magnesio AZ31B • + Materiales personalizados</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Continuar →", type="primary", use_container_width=True):
            next_step()
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.step == 2:
    st.markdown("## Selección de Modo")
    st.markdown(f"Seleccione el modo de trabajo para el análisis con elementos tipo **{st.session_state.tipo_elemento.replace('_', ' ').title()}**")
    
    # Tarjetas de modo con Streamlit nativo
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div style='background: white; padding: 2rem; border-radius: 15px; border: 2px solid #e2e8f0; 
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 1rem 0;'>
            <h3 style='color: #1a202c; font-size: 1.8rem; margin-bottom: 1rem; text-align: center;'>📝 Modo Manual</h3>
            <p style='color: #4a5568; line-height: 1.6; margin-bottom: 1.5rem; text-align: center;'>
                Control preciso con coordenadas exactas.<br><br>
                • Coordenadas exactas de cada nodo<br>
                • Conexiones entre nodos para formar elementos<br>
                • Propiedades de materiales y secciones
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("SELECCIONAR MANUAL", key="manual_mode", type="primary", use_container_width=True):
            set_modo("manual")
    
    with col2:
        st.markdown("""
        <div style='background: white; padding: 2rem; border-radius: 15px; border: 2px solid #e2e8f0; 
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 1rem 0;'>
            <h3 style='color: #1a202c; font-size: 1.8rem; margin-bottom: 1rem; text-align: center;'>🎨 Modo Interactivo</h3>
            <p style='color: #4a5568; line-height: 1.6; margin-bottom: 1.5rem; text-align: center;'>
                Diseño visual rápido e intuitivo.<br><br>
                • Colocar nodos haciendo clic en un gráfico<br>
                • Conectar nodos visualmente para crear elementos<br>
                • Definir propiedades mediante formularios simples
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("SELECCIONAR INTERACTIVO", key="interactive_mode", type="primary", use_container_width=True):
            set_modo("interactivo")

elif st.session_state.step == 3 and st.session_state.modo == "manual":
    st.markdown("## Número de Nodos")
    st.markdown(f"Ingrese el número total de nodos para el análisis con elementos tipo **{st.session_state.tipo_elemento.replace('_', ' ').title()}**")
    
    num_nodos = st.number_input("Número de Nodos", min_value=2, max_value=20, 
                                value=st.session_state.num_nodos)
    
    # Mostrar información sobre grados de libertad - 
    if st.session_state.tipo_elemento == "barra":
        gl_info = "2 grados de libertad por nodo (X, Y)"
        total_gl = num_nodos * 2
    elif st.session_state.tipo_elemento == "viga":
        gl_info = "2 grados de libertad por nodo (Y, θ)" 
        total_gl = num_nodos * 2
    else:  # viga_portico
        gl_info = "3 grados de libertad por nodo (X, Y, θ)"
        total_gl = num_nodos * 3
    
    st.info(f"ℹ️ **{gl_info}** → Total: {total_gl} grados de libertad")
    
    if st.button("Continuar →", type="primary"):
        st.session_state.num_nodos = num_nodos
        next_step()

elif st.session_state.step == 3 and st.session_state.modo == "interactivo":
    st.markdown("## Editor Interactivo de Estructura")
    st.markdown(f"Utilice el gráfico para crear su estructura con elementos tipo **{st.session_state.tipo_elemento.replace('_', ' ').title()}**. Haga clic para añadir nodos y conectarlos para formar elementos.")
    
    # Columnas para controles
    col1, col2, col3 = st.columns(3)
    
    with col1:
        tipo_nodo = st.radio("Tipo de nodo a añadir:", ["libre", "fijo"])
    
    with col2:
        if st.button("🗑️ Limpiar Todo", type="secondary"):
            st.session_state.nodos_interactivos = []
            st.session_state.elementos_interactivos = []
            st.session_state.nodo_seleccionado_interactivo = None
            st.rerun()
    
    with col3:
        if st.button("✅ Finalizar Diseño", type="primary"):
            if len(st.session_state.nodos_interactivos) >= 2 and len(st.session_state.elementos_interactivos) >= 1:
                transferir_datos_interactivos()
            else:
                st.error("Necesita al menos 2 nodos y 1 elemento para continuar")
    
    # Crear gráfico interactivo moderno
    fig = crear_grafico_interactivo_moderno()
    st.plotly_chart(fig, use_container_width=True)

    # Controles para añadir nodos manualmente
    st.markdown("### Añadir Nodos Manualmente")
    col1, col2, col3 = st.columns(3)

    with col1:
        x_nuevo = st.number_input("Coordenada X", value=0.0, format="%.2f", key="x_nuevo")

    with col2:
        y_nuevo = st.number_input("Coordenada Y", value=0.0, format="%.2f", key="y_nuevo")

    with col3:
        if st.button("➕ Añadir Nodo", type="primary"):
            nodo_id = agregar_nodo_interactivo(x_nuevo, y_nuevo, tipo_nodo)
            st.success(f"Nodo {nodo_id} ({tipo_nodo}) añadido en ({x_nuevo:.2f}, {y_nuevo:.2f})")
            st.rerun()

    # Controles para crear elementos
    if len(st.session_state.nodos_interactivos) >= 2:
        st.markdown(f"### Crear {st.session_state.tipo_elemento.replace('_', ' ').title()}s")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            nodos_disponibles = [n['id'] for n in st.session_state.nodos_interactivos]
            nodo_inicio_sel = st.selectbox("Nodo Inicio", nodos_disponibles, key="nodo_inicio_sel")
        
        with col2:
            nodos_fin_disponibles = [n for n in nodos_disponibles if n != nodo_inicio_sel]
            nodo_fin_sel = st.selectbox("Nodo Fin", nodos_fin_disponibles, key="nodo_fin_sel")
        
        with col3:
            if st.button(f"🔗 Crear {st.session_state.tipo_elemento.title()}", type="primary"):
                elemento_id = agregar_elemento_interactivo(nodo_inicio_sel, nodo_fin_sel)
                if elemento_id:
                    st.success(f"{st.session_state.tipo_elemento.title()} {elemento_id} creado entre nodos {nodo_inicio_sel} y {nodo_fin_sel}")
                    st.rerun()
                else:
                    st.warning("No se pudo crear el elemento (puede que ya exista)")
    
    # Mostrar nodos y elementos en tablas
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Nodos")
        if st.session_state.nodos_interactivos:
            for nodo in st.session_state.nodos_interactivos:
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.markdown(f"Nodo {nodo['id']} ({nodo['tipo']}): ({nodo['x']:.2f}, {nodo['y']:.2f})")
                with col_b:
                    if st.button(f"🗑️", key=f"del_nodo_{nodo['id']}"):
                        eliminar_nodo_interactivo(nodo['id'])
    
    with col2:
        st.markdown(f"### {st.session_state.tipo_elemento.replace('_', ' ').title()}s")
        if st.session_state.elementos_interactivos:
            for elem in st.session_state.elementos_interactivos:
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.markdown(f"{st.session_state.tipo_elemento.title()} {elem['id']}: Nodo {elem['nodo_inicio']} → Nodo {elem['nodo_fin']}")
                with col_b:
                    if st.button(f"🗑️", key=f"del_elem_{elem['id']}"):
                        eliminar_elemento_interactivo(elem['id'])

elif st.session_state.step == 4:
    st.markdown("## Clasificación de Nodos")
    st.markdown("Defina cuántos nodos son fijos y cuántos son libres")
    
    col1, col2 = st.columns(2)
    
    with col1:
        num_fijos = st.number_input("Nodos Fijos", min_value=1, max_value=st.session_state.num_nodos, 
                                    value=st.session_state.num_fijos)
    
    with col2:
        num_libres = st.session_state.num_nodos - num_fijos
        st.metric("Nodos Libres", num_libres)
    
    if st.button("Continuar →", type="primary"):
        st.session_state.num_fijos = num_fijos
        st.session_state.num_libres = num_libres
        next_step()

elif st.session_state.step == 5:
    st.markdown("## Coordenadas de Nodos")
    st.markdown("Ingrese las coordenadas para cada nodo")
    
    # Botones de control
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Limpiar Todos los Nodos", type="secondary"):
            st.session_state.nodos = []
            st.rerun()
    
    with col2:
        if st.button("🔄 Cambiar Número de Nodos", type="secondary"):
            st.session_state.step = 3
            st.rerun()
    
    # Determinar tipos de nodos
    tipos_nodos = ['fijo'] * st.session_state.num_fijos + ['libre'] * st.session_state.num_libres
    
    # Mostrar formulario para todos los nodos
    with st.form("coordenadas_nodos"):
        st.markdown("### Coordenadas de Todos los Nodos")
        
        nodos_temp = []
        
        for i in range(st.session_state.num_nodos):
            nodo_id = i + 1
            tipo_actual = tipos_nodos[i]
            
            # Buscar nodo existente o usar valores por defecto
            nodo_existente = next((n for n in st.session_state.nodos if n['id'] == nodo_id), None)
            x_default = nodo_existente['x'] if nodo_existente else 0.0
            y_default = nodo_existente['y'] if nodo_existente else 0.0
            
            st.markdown(f"**Nodo {nodo_id} ({tipo_actual.title()})**")
            
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                x = st.number_input(f"X{nodo_id}", value=x_default, format="%.2f", key=f"x_{nodo_id}")
            
            with col2:
                y = st.number_input(f"Y{nodo_id}", value=y_default, format="%.2f", key=f"y_{nodo_id}")
            
            with col3:
                gl_globales = calcular_grados_libertad_globales(nodo_id)
                st.markdown(f"GL Globales: {gl_globales}")
                
                # Mostrar descripción de grados de libertad según el tipo - CORREGIDO
                if st.session_state.tipo_elemento == "barra":
                    st.markdown(f"GL{gl_globales[0]} → X, GL{gl_globales[1]} → Y")
                elif st.session_state.tipo_elemento == "viga":
                    st.markdown(f"GL{gl_globales[0]} → Y, GL{gl_globales[1]} → θ")  # CORREGIDO
                else:  # viga_portico
                    st.markdown(f"GL{gl_globales[0]} → X, GL{gl_globales[1]} → Y, GL{gl_globales[2]} → θ")
            
            nodos_temp.append({
                'id': nodo_id,
                'x': x,
                'y': y,
                'tipo': tipo_actual,
                'grados_libertad_globales': gl_globales
            })
        
        if st.form_submit_button("💾 Guardar Todos los Nodos", type="primary"):
            st.session_state.nodos = nodos_temp
            st.success(f"✅ Se guardaron {len(nodos_temp)} nodos correctamente")
    
    # Mostrar nodos guardados
    if st.session_state.nodos:
        st.markdown("### 📋 Nodos Configurados")
        df_nodos = crear_tabla_nodos()
        st.dataframe(df_nodos, use_container_width=True)
        
        if len(st.session_state.nodos) == st.session_state.num_nodos:
            if st.button("Continuar →", type="primary"):
                next_step()

elif st.session_state.step == 6:
    st.markdown("## Número de Elementos")
    st.markdown(f"Ingrese el número total de elementos tipo **{st.session_state.tipo_elemento.replace('_', ' ').title()}** en el sistema")
    
    num_elementos = st.number_input("Número de Elementos", min_value=1, max_value=50, 
                                    value=st.session_state.num_elementos)
    
    if st.button("Continuar →", type="primary"):
        st.session_state.num_elementos = num_elementos
        next_step()

elif st.session_state.step == 7:
    st.markdown("## Definición de Elementos")
    st.markdown(f"Configure cada elemento tipo **{st.session_state.tipo_elemento.replace('_', ' ').title()}** del sistema")
    
    # Mostrar información específica según el tipo de elemento
    if st.session_state.tipo_elemento == "barra":
        st.info("🔗 **Elementos Barra:** Solo requieren área de sección transversal y material")
    elif st.session_state.tipo_elemento == "viga":
        st.info("📏 **Elementos Viga:** Requieren momento de inercia y material")
    else:  # viga_portico
        st.info("🏗️ **Elementos Viga Pórtico:** Requieren área, momento de inercia y material")
    
    # Botones de control
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Limpiar Todos los Elementos", type="secondary"):
            st.session_state.elementos = []
            st.session_state.matrices_elementos = {}
            st.rerun()
    with col2:
        if st.button("🔄 Cambiar Número de Elementos", type="secondary"):
            st.session_state.step = 6
            st.rerun()
    
    with st.expander("📚 Base de Datos de Materiales"):
        for nombre, props in MATERIALES_AEROESPACIALES.items():
            st.markdown(f"**{nombre}**: E = {formatear_unidades(props['modulo_young'], 'presion')}, ρ = {props['densidad']} kg/m³")
            st.caption(props['descripcion'])
    
    with st.expander("➕ Agregar Material Personalizado"):
        with st.form("material_personalizado"):
            col1, col2, col3 = st.columns(3)
            with col1:
                nombre_material = st.text_input("Nombre del Material")
            with col2:
                modulo_young = st.number_input("Módulo de Young (Pa)", value=200e9, format="%.2e")
            with col3:
                densidad = st.number_input("Densidad (kg/m³)", value=7850.0)
            descripcion = st.text_area("Descripción")
            if st.form_submit_button("Agregar Material"):
                if nombre_material:
                    st.session_state.materiales_personalizados[nombre_material] = {
                        'modulo_young': modulo_young, 
                        'densidad': densidad, 
                        'descripcion': descripcion
                    }
                    st.success(f"Material '{nombre_material}' agregado exitosamente")
    
    st.markdown("### 🔧 Configuración Individual de Elementos")
    
    # Funcionalidad de agrupación de elementos -
    with st.expander("👥 Agrupación de Elementos", expanded=True):
        st.markdown("Agrupe elementos con propiedades similares para configuración masiva")
        
        # Crear grupo
        col1, col2, col3 = st.columns(3)
        with col1:
            nombre_grupo = st.text_input("Nombre del grupo:", placeholder="Ej: Columnas, Vigas principales")
        with col2:
            elementos_disponibles = [f"Elemento {i+1}" for i in range(st.session_state.num_elementos)]
            elementos_seleccionados = st.multiselect("Seleccionar elementos:", elementos_disponibles)
        with col3:
            if st.button("➕ Crear Grupo") and nombre_grupo and elementos_seleccionados:
                if nombre_grupo not in st.session_state.grupos_elementos:
                    st.session_state.grupos_elementos[nombre_grupo] = {
                        'elementos': [int(elem.split()[-1]) for elem in elementos_seleccionados],
                        'material': None,
                        'tipo_seccion': None,
                        'parametros_seccion': {}
                    }
                    st.success(f"Grupo '{nombre_grupo}' creado con {len(elementos_seleccionados)} elementos")
                    st.rerun()
                else:
                    st.warning("Ya existe un grupo con ese nombre")
        
        # Mostrar grupos existentes
        if st.session_state.grupos_elementos:
            st.markdown("#### Grupos Existentes")
            for nombre_grupo, info_grupo in st.session_state.grupos_elementos.items():
                with st.container():
                    col1, col2, col3 = st.columns([2, 2, 1])
                    with col1:
                        st.markdown(f"**{nombre_grupo}**")
                        st.caption(f"Elementos: {info_grupo['elementos']}")
                    with col2:
                        # Configuración automática expandida
                        pass
                    with col3:
                        if st.button(f"🗑️", key=f"del_grupo_{nombre_grupo}"):
                            del st.session_state.grupos_elementos[nombre_grupo]
                            st.rerun()
                    
                    # Configuración del grupo - SIEMPRE EXPANDIDA
                    st.markdown(f"##### Configuración para grupo '{nombre_grupo}'")
                    
                    # Material del grupo
                    todos_materiales = {**MATERIALES_AEROESPACIALES, **st.session_state.materiales_personalizados}
                    nombres_materiales = list(todos_materiales.keys())
                    material_grupo = st.selectbox("Material del grupo:", nombres_materiales, key=f"mat_grupo_{nombre_grupo}")
                    
                    # Tipo de sección del grupo
                    tipo_seccion_grupo = st.radio("Tipo de sección:", 
                                                ["circular_solida", "circular_hueca", "rectangular", "cuadrada"], 
                                                format_func=lambda x: {
                                                    "circular_solida": "Circular Sólida", 
                                                    "circular_hueca": "Circular Hueca", 
                                                    "rectangular": "Rectangular", 
                                                    "cuadrada": "Cuadrada"
                                                }[x], 
                                                key=f"seccion_grupo_{nombre_grupo}")
                    
                    # Parámetros de sección según el tipo - DINÁMICOS
                    parametros_grupo = {}
                    if tipo_seccion_grupo == "circular_solida":
                        radio_grupo = st.number_input("Radio (m):", value=0.01, min_value=0.001, format="%.4f", key=f"radio_grupo_{nombre_grupo}")
                        parametros_grupo['radio'] = radio_grupo
                        area_calc = math.pi * radio_grupo**2
                        st.info(f"Área calculada: {area_calc:.6f} m²")
                        if st.session_state.tipo_elemento in ["viga", "viga_portico"]:
                            inercia_calc = (math.pi * radio_grupo**4) / 4
                            st.info(f"Momento de Inercia: {inercia_calc:.8e} m⁴")
                    elif tipo_seccion_grupo == "circular_hueca":
                        col_a, col_b = st.columns(2)
                        with col_a:
                            radio_ext_grupo = st.number_input("Radio Exterior (m):", value=0.02, min_value=0.001, format="%.4f", key=f"radio_ext_grupo_{nombre_grupo}")
                        with col_b:
                            radio_int_grupo = st.number_input("Radio Interior (m):", value=0.01, min_value=0.0, max_value=radio_ext_grupo*0.99, format="%.4f", key=f"radio_int_grupo_{nombre_grupo}")
                        parametros_grupo['radio_ext'] = radio_ext_grupo
                        parametros_grupo['radio_int'] = radio_int_grupo
                        area_calc = math.pi * (radio_ext_grupo**2 - radio_int_grupo**2)
                        st.info(f"Área calculada: {area_calc:.6f} m²")
                        if st.session_state.tipo_elemento in ["viga", "viga_portico"]:
                            inercia_calc = (math.pi * (radio_ext_grupo**4 - radio_int_grupo**4)) / 4
                            st.info(f"Momento de Inercia: {inercia_calc:.8e} m⁴")
                    elif tipo_seccion_grupo == "rectangular":
                        col_a, col_b = st.columns(2)
                        with col_a:
                            lado1_grupo = st.number_input("Base (m):", value=0.02, min_value=0.001, format="%.4f", key=f"lado1_grupo_{nombre_grupo}")
                        with col_b:
                            lado2_grupo = st.number_input("Altura (m):", value=0.01, min_value=0.001, format="%.4f", key=f"lado2_grupo_{nombre_grupo}")
                        parametros_grupo['lado1'] = lado1_grupo
                        parametros_grupo['lado2'] = lado2_grupo
                        area_calc = lado1_grupo * lado2_grupo
                        st.info(f"Área calculada: {area_calc:.6f} m²")
                        if st.session_state.tipo_elemento in ["viga", "viga_portico"]:
                            inercia_calc = (lado1_grupo * lado2_grupo**3) / 12
                            st.info(f"Momento de Inercia: {inercia_calc:.8e} m⁴")
                    elif tipo_seccion_grupo == "cuadrada":
                        lado_grupo = st.number_input("Lado (m):", value=0.02, min_value=0.001, format="%.4f", key=f"lado_grupo_{nombre_grupo}")
                        parametros_grupo['lado'] = lado_grupo
                        area_calc = lado_grupo**2
                        st.info(f"Área calculada: {area_calc:.6f} m²")
                        if st.session_state.tipo_elemento in ["viga", "viga_portico"]:
                            inercia_calc = (lado_grupo**4) / 12
                            st.info(f"Momento de Inercia: {inercia_calc:.8e} m⁴")
                    
                    if st.button(f"💾 Aplicar a Grupo '{nombre_grupo}'", key=f"aplicar_grupo_{nombre_grupo}"):
                        # Aplicar configuración a todos los elementos del grupo
                        elementos_grupo = info_grupo['elementos']
                        props_material = todos_materiales[material_grupo]
                        
                        for elemento_id in elementos_grupo:
                            # Buscar el elemento real para obtener sus nodos de inicio y fin
                            elemento_real = next((e for e in st.session_state.elementos if e['id'] == elemento_id), None)
                            if elemento_real:
                                nodo_inicio_obj = next((n for n in st.session_state.nodos if n['id'] == elemento_real['nodo_inicio']), None)
                                nodo_fin_obj = next((n for n in st.session_state.nodos if n['id'] == elemento_real['nodo_fin']), None)
                            else:
                                # Si no existe el elemento, usar nodos por defecto basados en el elemento_id
                                nodo_inicio_obj = st.session_state.nodos[0] if st.session_state.nodos else None
                                nodo_fin_obj = st.session_state.nodos[-1] if len(st.session_state.nodos) > 1 else st.session_state.nodos[0] if st.session_state.nodos else None

                            if not nodo_inicio_obj or not nodo_fin_obj:
                                continue  # Saltar este elemento si no se pueden encontrar los nodos
                            
                            longitud = calcular_longitud_elemento(nodo_inicio_obj, nodo_fin_obj)
                            beta = calcular_angulo_beta(nodo_inicio_obj, nodo_fin_obj)
                            gl_globales = nodo_inicio_obj['grados_libertad_globales'] + nodo_fin_obj['grados_libertad_globales']
                            
                            area_final = calcular_area_seccion(tipo_seccion_grupo, parametros_grupo)
                            inercia_final = calcular_momento_inercia(tipo_seccion_grupo, parametros_grupo) if st.session_state.tipo_elemento in ["viga", "viga_portico"] else 0
                            
                            nuevo_elemento = {
                                'id': elemento_id,
                                'nodo_inicio': nodo_inicio_obj['id'],
                                'nodo_fin': nodo_fin_obj['id'],
                                'tipo': st.session_state.tipo_elemento.replace('_', ' ').title(),
                                'material': material_grupo,
                                'tipo_seccion': tipo_seccion_grupo,
                                'parametros_seccion': parametros_grupo,
                                'area': area_final,
                                'inercia': inercia_final,
                                'longitud': longitud,
                                'beta': beta,
                                'grados_libertad_global': gl_globales
                            }
                            
                            # Actualizar o agregar elemento
                            elemento_idx = next((i for i, e in enumerate(st.session_state.elementos) if e['id'] == elemento_id), None)
                            if elemento_idx is not None:
                                st.session_state.elementos[elemento_idx] = nuevo_elemento
                            else:
                                st.session_state.elementos.append(nuevo_elemento)
                            
                            # Generar matriz de rigidez
                            E = props_material['modulo_young']
                            A = area_final
                            I = inercia_final
                            L = longitud
                            
                            if st.session_state.tipo_elemento == "barra":
                                matriz_global, matriz_local = generar_matriz_rigidez_barra(E, A, L, beta)
                            elif st.session_state.tipo_elemento == "viga":
                                matriz_global, matriz_local = generar_matriz_rigidez_viga(E, I, L)
                            else:  # viga_portico
                                matriz_global, matriz_local = generar_matriz_rigidez_viga_portico(E, A, I, L, beta)

                            st.session_state.matrices_elementos[elemento_id] = {
                                'simbolica': [],
                                'numerica': matriz_global.tolist(),
                                'local': matriz_local.tolist()  # <-- Aquí se guarda la matriz local
                            }
                        
                        st.success(f"✅ Configuración aplicada a {len(elementos_grupo)} elementos del grupo '{nombre_grupo}'")
                        st.rerun()
                    
                    st.divider()

    elementos_base = [{'id': i+1} for i in range(st.session_state.num_elementos)]
    
    for i, elem_base in enumerate(elementos_base):
        elemento_id = elem_base['id']
        with st.expander(f"🔧 Elemento {elemento_id} ({st.session_state.tipo_elemento.replace('_', ' ').title()})", expanded=False):
            elemento_existente = next((e for e in st.session_state.elementos if e['id'] == elemento_id), None)
            
            col1, col2 = st.columns(2)
            with col1:
                nodos_disponibles = [n['id'] for n in st.session_state.nodos]
                nodo_inicio_default = elemento_existente['nodo_inicio'] if elemento_existente else nodos_disponibles[0]
                nodo_fin_default = elemento_existente['nodo_fin'] if elemento_existente else nodos_disponibles[-1]
                nodo_inicio = st.selectbox(f"Nodo Inicio", nodos_disponibles, 
                                        index=nodos_disponibles.index(nodo_inicio_default) if nodo_inicio_default in nodos_disponibles else 0, 
                                        key=f"inicio_{elemento_id}")
                nodo_fin = st.selectbox(f"Nodo Fin", nodos_disponibles, 
                                        index=nodos_disponibles.index(nodo_fin_default) if nodo_fin_default in nodos_disponibles else -1, 
                                        key=f"fin_{elemento_id}")
            
            with col2:
                todos_materiales = {**MATERIALES_AEROESPACIALES, **st.session_state.materiales_personalizados}
                nombres_materiales = list(todos_materiales.keys())
                material_default = elemento_existente['material'] if elemento_existente and elemento_existente.get('material') else nombres_materiales[0]
                material_idx = nombres_materiales.index(material_default) if material_default in nombres_materiales else 0
                material_seleccionado = st.selectbox(f"Material", nombres_materiales, index=material_idx, key=f"material_{elemento_id}")
                props_material = todos_materiales[material_seleccionado]
                st.markdown(f"E = {formatear_unidades(props_material['modulo_young'], 'presion')}")
                st.markdown(f"ρ = {props_material['densidad']} kg/m³")
            
            st.markdown("#### Tipo de Sección")
            tipo_seccion_default = elemento_existente.get('tipo_seccion', 'circular_solida') if elemento_existente else 'circular_solida'
            tipo_seccion = st.radio("Seleccione el tipo de sección:", 
                                    ["circular_solida", "circular_hueca", "rectangular", "cuadrada"], 
                                    format_func=lambda x: {
                                        "circular_solida": "Circular Sólida", 
                                        "circular_hueca": "Circular Hueca (Cilindro)", 
                                        "rectangular": "Rectangular", 
                                        "cuadrada": "Cuadrada"
                                    }[x], 
                                    index=["circular_solida", "circular_hueca", "rectangular", "cuadrada"].index(tipo_seccion_default) if tipo_seccion_default in ["circular_solida", "circular_hueca", "rectangular", "cuadrada"] else 0, 
                                    key=f"tipo_seccion_{elemento_id}")
            
            parametros_seccion = {}
            if tipo_seccion == "circular_solida":
                col1, col2, col3 = st.columns(3)
                with col1:
                    radio_default = elemento_existente.get('parametros_seccion', {}).get('radio', 0.01) if elemento_existente else 0.01
                    radio = st.number_input(f"Radio (m)", value=radio_default, min_value=0.001, format="%.4f", key=f"radio_{elemento_id}")
                    parametros_seccion['radio'] = radio
                with col2:
                    area = math.pi * radio**2
                    st.metric("Área calculada", f"{area:.6f} m²")
                with col3:
                    if st.session_state.tipo_elemento in ["viga", "viga_portico"]:
                        inercia = (math.pi * radio**4) / 4
                        st.metric("Momento de Inercia", f"{inercia:.8e} m⁴")
            
            elif tipo_seccion == "circular_hueca":
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    radio_ext_default = elemento_existente.get('parametros_seccion', {}).get('radio_ext', 0.02) if elemento_existente else 0.02
                    radio_ext = st.number_input(f"Radio Exterior (m)", value=radio_ext_default, min_value=0.001, format="%.4f", key=f"radio_ext_{elemento_id}")
                    parametros_seccion['radio_ext'] = radio_ext
                with col2:
                    radio_int_default = elemento_existente.get('parametros_seccion', {}).get('radio_int', 0.01) if elemento_existente else 0.01
                    radio_int = st.number_input(f"Radio Interior (m)", value=radio_int_default, min_value=0.0, max_value=radio_ext*0.99, format="%.4f", key=f"radio_int_{elemento_id}")
                    parametros_seccion['radio_int'] = radio_int
                with col3:
                    area = math.pi * (radio_ext**2 - radio_int**2)
                    st.metric("Área calculada", f"{area:.6f} m²")
                with col4:
                    if st.session_state.tipo_elemento in ["viga", "viga_portico"]:
                        inercia = (math.pi * (radio_ext**4 - radio_int**4)) / 4
                        st.metric("Momento de Inercia", f"{inercia:.8e} m⁴")
            
            elif tipo_seccion == "rectangular":
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    lado1_default = elemento_existente.get('parametros_seccion', {}).get('lado1', 0.02) if elemento_existente else 0.02
                    lado1 = st.number_input(f"Base (m)", value=lado1_default, min_value=0.001, format="%.4f", key=f"lado1_{elemento_id}")
                    parametros_seccion['lado1'] = lado1
                with col2:
                    lado2_default = elemento_existente.get('parametros_seccion', {}).get('lado2', 0.01) if elemento_existente else 0.01
                    lado2 = st.number_input(f"Altura (m)", value=lado2_default, min_value=0.001, format="%.4f", key=f"lado2_{elemento_id}")
                    parametros_seccion['lado2'] = lado2
                with col3:
                    area = lado1 * lado2
                    st.metric("Área calculada", f"{area:.6f} m²")
                with col4:
                    if st.session_state.tipo_elemento in ["viga", "viga_portico"]:
                        inercia = (lado1 * lado2**3) / 12
                        st.metric("Momento de Inercia", f"{inercia:.8e} m⁴")
            
            elif tipo_seccion == "cuadrada":
                col1, col2, col3 = st.columns(3)
                with col1:
                    lado_default = elemento_existente.get('parametros_seccion', {}).get('lado', 0.02) if elemento_existente else 0.02
                    lado = st.number_input(f"Lado (m)", value=lado_default, min_value=0.001, format="%.4f", key=f"lado_{elemento_id}")
                    parametros_seccion['lado'] = lado
                with col2:
                    area = lado**2
                    st.metric("Área calculada", f"{area:.6f} m²")
                with col3:
                    if st.session_state.tipo_elemento in ["viga", "viga_portico"]:
                        inercia = (lado**4) / 12
                        st.metric("Momento de Inercia", f"{inercia:.8e} m⁴")
            
            area_final = calcular_area_seccion(tipo_seccion, parametros_seccion)
            inercia_final = calcular_momento_inercia(tipo_seccion, parametros_seccion) if st.session_state.tipo_elemento in ["viga", "viga_portico"] else 0
            
            if st.button(f"💾 Guardar Elemento {elemento_id}", key=f"guardar_{elemento_id}"):
                nodo_inicio_obj = next((n for n in st.session_state.nodos if n['id'] == nodo_inicio), None)
                nodo_fin_obj = next((n for n in st.session_state.nodos if n['id'] == nodo_fin), None)
                
                if nodo_inicio_obj and nodo_fin_obj:
                    longitud = calcular_longitud_elemento(nodo_inicio_obj, nodo_fin_obj)
                    beta = calcular_angulo_beta(nodo_inicio_obj, nodo_fin_obj)
                    gl_globales = nodo_inicio_obj['grados_libertad_globales'] + nodo_fin_obj['grados_libertad_globales']
                    
                    nuevo_elemento = {
                        'id': elemento_id,
                        'nodo_inicio': nodo_inicio,
                        'nodo_fin': nodo_fin,
                        'tipo': st.session_state.tipo_elemento.replace('_', ' ').title(),
                        'material': material_seleccionado,
                        'tipo_seccion': tipo_seccion,
                        'parametros_seccion': parametros_seccion,
                        'area': area_final,
                        'inercia': inercia_final,
                        'longitud': longitud,
                        'beta': beta,
                        'grados_libertad_global': gl_globales
                    }
                    
                    elemento_idx = next((i for i, e in enumerate(st.session_state.elementos) if e['id'] == elemento_id), None)
                    if elemento_idx is not None:
                        st.session_state.elementos[elemento_idx] = nuevo_elemento
                    else:
                        st.session_state.elementos.append(nuevo_elemento)
                    
                    # Generar matriz de rigidez según el tipo de elemento
                    E = props_material['modulo_young']
                    A = area_final
                    I = inercia_final
                    L = longitud
                    
                    if st.session_state.tipo_elemento == "barra":
                        matriz_global, matriz_local = generar_matriz_rigidez_barra(E, A, L, beta)
                    elif st.session_state.tipo_elemento == "viga":
                        matriz_global, matriz_local = generar_matriz_rigidez_viga(E, I, L)
                    else:  # viga_portico
                        matriz_global, matriz_local = generar_matriz_rigidez_viga_portico(E, A, I, L, beta)

                    st.session_state.matrices_elementos[elemento_id] = {
                        'simbolica': [],
                        'numerica': matriz_global.tolist(),
                        'local': matriz_local.tolist() 
                    }
                    
                    st.success(f"✅ Elemento {elemento_id} guardado correctamente")
                    st.rerun()
    
    if st.session_state.elementos:
        st.markdown("### 📋 Elementos Configurados")
        df_elementos = crear_tabla_conectividad()
        st.dataframe(df_elementos, use_container_width=True)
        
        if len(st.session_state.elementos) >= st.session_state.num_elementos:
            if st.button("Continuar →", type="primary"):
                # Configurar grados de libertad automáticamente
                max_gl = max([max(nodo['grados_libertad_globales']) for nodo in st.session_state.nodos])
                st.session_state.grados_libertad_info = []
                
                for i in range(max_gl):
                    gl_num = i + 1
                    nodo_propietario = None
                    direccion = None
                    
                    for nodo in st.session_state.nodos:
                        if gl_num in nodo['grados_libertad_globales']:
                            nodo_propietario = nodo
                            gl_index = nodo['grados_libertad_globales'].index(gl_num)
                            
                            if st.session_state.tipo_elemento == "barra":
                                direccion = 'X' if gl_index == 0 else 'Y'
                            elif st.session_state.tipo_elemento == "viga":
                                direccion = 'Y' if gl_index == 0 else 'θ'  
                            else:  # viga_portico
                                direccion = ['X', 'Y', 'θ'][gl_index]
                            break
                    
                    es_fijo = nodo_propietario['tipo'] == 'fijo' if nodo_propietario else False
                    
                    info_gl = {
                        'numero': gl_num,
                        'nodo': nodo_propietario['id'] if nodo_propietario else None,
                        'direccion': direccion,
                        'desplazamiento_conocido': es_fijo,
                        'valor_desplazamiento': 0.0 if es_fijo else None,
                        'fuerza_conocida': not es_fijo,
                        'valor_fuerza': 0.0 if not es_fijo else None
                    }
                    st.session_state.grados_libertad_info.append(info_gl)
                
                next_step()

elif st.session_state.step == 8:
    st.markdown("## Configuración de Incógnitas y Datos")
    st.markdown("Defina qué fuerzas y desplazamientos son conocidos (datos) o desconocidos (incógnitas)")
    st.info("💡 **Cálculo Automático:** Los resultados se calculan automáticamente cuando complete esta configuración.")
    
    st.markdown("### ⚙️ Configuración de Grados de Libertad")
    
    for i, info in enumerate(st.session_state.grados_libertad_info):
        with st.container():
            st.markdown(f"#### Grado de Libertad {info['numero']} (Nodo {info['nodo']}, Dirección {info['direccion']})")
            
            # Determinar la opción por defecto para el selector
            # Si el desplazamiento es conocido por defecto (nodo fijo), la opción es 'Desplazamiento'
            default_choice_index = 0 if info['desplazamiento_conocido'] else 1

            # Selector para definir la condición de contorno
            condicion_conocida = st.radio(
                "¿Qué valor es conocido para este Grado de Libertad?",
                ("Desplazamiento / Rotación", "Fuerza / Momento"),
                index=default_choice_index,
                key=f"condicion_{info['numero']}",
                horizontal=True
            )

            # Actualizar el estado basado en la selección del usuario
            es_desplazamiento_conocido = (condicion_conocida == "Desplazamiento / Rotación")
            st.session_state.grados_libertad_info[i]['desplazamiento_conocido'] = es_desplazamiento_conocido
            st.session_state.grados_libertad_info[i]['fuerza_conocida'] = not es_desplazamiento_conocido
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### Desplazamiento")
                if es_desplazamiento_conocido:
                    st.markdown("📝 **DATO** (Debe especificar)")
                    if info['valor_desplazamiento'] is None:
                        info['valor_desplazamiento'] = 0.0
                    
                    valor_desplazamiento = st.number_input("Valor:",
                                                        value=info['valor_desplazamiento'],
                                                        format="%.6f",
                                                        key=f"desp_{info['numero']}")
                    st.session_state.grados_libertad_info[i]['valor_desplazamiento'] = valor_desplazamiento
                    st.session_state.grados_libertad_info[i]['valor_fuerza'] = None
                else:
                    st.markdown("❓ **INCÓGNITA** (Se calculará)")

            with col2:
                st.markdown("##### Fuerza / Momento")
                if not es_desplazamiento_conocido:
                    st.markdown("📝 **DATO** (Debe especificar)")
                    if info['valor_fuerza'] is None:
                        info['valor_fuerza'] = 0.0

                    label_fuerza = "Momento [N·m]:" if info['direccion'] == 'θ' else "Fuerza [N]:"
                    valor_fuerza = st.number_input(label_fuerza,
                                                value=info['valor_fuerza'],
                                                format="%.3f",
                                                key=f"fuerza_{info['numero']}")

                    # --- LÍNEA QUE DEBES AÑADIR AQUÍ ---
                    if info['direccion'] != 'θ':
                        st.markdown(f"Valor: **{formatear_unidades(valor_fuerza, 'fuerza')}**")
                    # ------------------------------------

                    st.session_state.grados_libertad_info[i]['valor_fuerza'] = valor_fuerza
                    st.session_state.grados_libertad_info[i]['valor_desplazamiento'] = None
                else:
                    st.markdown("❓ **INCÓGNITA** (Se calculará)")
            
            st.divider()
    
    if st.button("🧮 Calcular Sistema", type="primary", use_container_width=True):
        resultado = resolver_sistema()
        if resultado and resultado['exito']:
            st.session_state.resultados = resultado
            st.success("✅ Sistema resuelto exitosamente")
            next_step()
        else:
            st.error("❌ Error al resolver el sistema. Verifique los datos ingresados.")

elif st.session_state.step == 9:
    st.markdown("## 🎉 Resultados del Análisis")
    st.markdown(f"El análisis estructural con elementos tipo **{st.session_state.tipo_elemento.replace('_', ' ').title()}** se ha completado exitosamente.")

    if st.session_state.resultados:
        resultado = st.session_state.resultados
        
        # Métricas principales
        st.markdown("### 📈 Métricas Principales")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Nodos", len(st.session_state.nodos))
        with col2:
            st.metric("Elementos", len(st.session_state.elementos))
        with col3:
            st.metric("Grados de Libertad", len(st.session_state.grados_libertad_info))
        with col4:
            det_K = resultado.get('determinante', 0)
            st.metric("Det(K)", f"{det_K:.2e}")
        
        st.divider()

        # Tablas de resultados
        st.markdown("### 📋 Tablas de Resultados y Análisis")

        st.markdown("#### Resultados Globales")
        resultados_data = []
        for i, (info, fuerza, desplazamiento) in enumerate(zip(
            st.session_state.grados_libertad_info, 
            resultado['fuerzas'], 
            resultado['desplazamientos']
        )):
            nombre = st.session_state.nombres_fuerzas.get(i+1, f"F{i+1}")
            detalle_fuerza = "Dato (Entrada)" if info['fuerza_conocida'] else "Incógnita (Calculado)"
            detalle_desplazamiento = "Dato (Entrada)" if info['desplazamiento_conocido'] else "Incógnita (Calculado)"
            
            # Formatear según el tipo de dirección
            if info['direccion'] == 'θ':
                fuerza_formateada = f"{fuerza:.3f} N·m"
                desplaz_formateado = f"{desplazamiento:.6f} rad"
            else:
                fuerza_formateada = formatear_unidades(fuerza, "fuerza")
                desplaz_formateado = formatear_unidades(desplazamiento, "desplazamiento")
            
            resultados_data.append({
                'GL': f"GL{i+1}",
                'Nodo': f"N{info['nodo']}",
                'Dirección': info['direccion'],
                'Fuerza/Momento': fuerza_formateada,
                'Detalle Fuerza': detalle_fuerza,
                'Desplazamiento/Rotación': desplaz_formateado,
                'Detalle Desplazamiento': detalle_desplazamiento
            })
        
        df_resultados = pd.DataFrame(resultados_data)
        st.dataframe(df_resultados, use_container_width=True)

        st.markdown("#### 📍 Tabla de Nodos")
        df_nodos = crear_tabla_nodos()
        if not df_nodos.empty:
            st.dataframe(df_nodos, use_container_width=True)

        st.markdown("#### 🔗 Tabla de Conectividad")
        df_conectividad = crear_tabla_conectividad()
        if not df_conectividad.empty:
            st.dataframe(df_conectividad, use_container_width=True)

        st.markdown("#### ⚙️ Matrices de Rigidez Locales por Elemento (k')")
        st.info("Estas matrices representan la rigidez de cada elemento en su propio sistema de coordenadas, antes de ser rotadas al sistema global.")

        for elemento in st.session_state.elementos:
            with st.expander(f"Elemento {elemento['id']} - Matriz de Rigidez Local (k')"):
                if elemento['id'] in st.session_state.matrices_elementos and 'local' in st.session_state.matrices_elementos[elemento['id']]:
                    matriz_local_np = np.array(st.session_state.matrices_elementos[elemento['id']]['local'])
                    
                    # Definir etiquetas para los ejes de la matriz local
                    if st.session_state.tipo_elemento == "barra":
                        labels = ["u1", "v1", "u2", "v2"]
                    elif st.session_state.tipo_elemento == "viga":
                        labels = ["v1", "θ1", "v2", "θ2"]
                    else: # viga_portico
                        labels = ["u1", "v1", "θ1", "u2", "v2", "θ2"]

                    df_local = pd.DataFrame(matriz_local_np, index=labels, columns=labels)
                    
                    # Formatear números para mejor visualización
                    df_local_formatted = df_local.applymap(lambda x: f"{x:.3e}")
                    
                    st.markdown(f"**Matriz k' Local - Elemento {elemento['id']}**")
                    st.dataframe(df_local_formatted, use_container_width=True)

                else:
                    st.warning("Matriz de rigidez local no disponible para este elemento.")

        # Matrices adicionales para viga pórtico - CORREGIDO
        if st.session_state.tipo_elemento == "viga_portico":
            st.markdown("#### 🔄 Matrices de Transformación Locales por Elemento")
            st.info("📝 **Nota:** Estas son matrices de transformación **locales** específicas para cada elemento individual.")
            
            for elemento in st.session_state.elementos:
                with st.expander(f"Elemento {elemento['id']} - Matrices Locales Detalladas"):
                    beta = elemento['beta']
                    
                    # Matriz de transformación LOCAL
                    T = generar_matriz_transformacion_viga_portico(beta)
                    st.markdown("##### Matriz de Transformación Local de Coordenadas")
                    st.markdown(f"**Ángulo β = {beta:.4f} rad = {math.degrees(beta):.2f}°**")
                    mostrar_matriz_formateada_moderna(T, f"Matriz T Local - Elemento {elemento['id']}", es_simbolica=False)
                    
                    # Vector de desplazamientos nodales locales
                    if st.session_state.resultados:
                        gl_globales = elemento['grados_libertad_global']
                        U_global = np.array([resultado['desplazamientos'][gl-1] for gl in gl_globales])
                        U_local = T @ U_global
                        
                        st.markdown("##### Vector de Desplazamientos Nodales")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**Globales:**")
                            df_global = pd.DataFrame({
                                'GL': [f'GL{gl}' for gl in gl_globales],
                                'Valor': [formatear_unidades(val, 'desplazamiento') if i < 4 else f"{val:.6f} rad" for i, val in enumerate(U_global)]
                            })
                            st.dataframe(df_global, use_container_width=True)
                        
                        with col2:
                            st.markdown("**Locales:**")
                            direcciones_locales = ['u1', 'v1', 'θ1', 'u2', 'v2', 'θ2']
                            df_local = pd.DataFrame({
                                'Dirección': direcciones_locales,
                                'Valor': [formatear_unidades(val, 'desplazamiento') if i in [0,1,3,4] else f"{val:.6f} rad" for i, val in enumerate(U_local)]
                            })
                            st.dataframe(df_local, use_container_width=True)

        st.markdown("#### 🔧 Matriz de Rigidez Global K")
        mostrar_matriz_formateada_moderna(resultado['K_global'], "Matriz de Rigidez Global K", es_simbolica=False)

        st.divider()

        # Visualización
        st.markdown("### 📊 Visualización de la Estructura")
        factor_escala_on_screen = st.slider("Factor de escala para visualización:", 1, 1000, 100, key="factor_escala_pantalla")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Estructura Deformada")
            fig_deformada = visualizar_estructura_moderna(mostrar_deformada=True, factor_escala=factor_escala_on_screen)
            if fig_deformada:
                st.pyplot(fig_deformada)
        with col2:
            st.markdown("#### Estructura Original")
            fig_original = visualizar_estructura_moderna(mostrar_deformada=False)
            if fig_original:
                st.pyplot(fig_original)
        
        st.divider()
        
        # Botón de descarga PDF - AGREGADO
        st.markdown("### 📄 Exportar Reporte")
        if st.button("📋 Descargar Reporte PDF", type="primary", use_container_width=True):
            pdf_buffer = generar_pdf_reporte()
            st.download_button(
                label="💾 Descargar PDF",
                data=pdf_buffer,
                file_name=f"Reporte_Analisis_Estructural_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )
        
        st.divider()
        
        # Botones de reinicio y nueva estructura
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Nuevo Análisis", type="primary", use_container_width=True):
                reset_app()
        with col2:
            if st.button("🔙 Cambiar Tipo de Elemento", type="secondary", use_container_width=True):
                st.session_state.step = 0
                st.session_state.tipo_elemento = None
                st.rerun()

else:
    st.error("Paso no reconocido o error en la carga de datos.")

# Footer con información adicional
st.markdown("""
<div style='background-color: #212529; padding: 2rem; margin-top: 3rem; border-radius: 15px;'>
    <div style='text-align: center; color: white;'>
        <h3 style='color: white; margin-bottom: 1rem;'>📝 Sistema de Análisis Estructural Avanzado</h3>
        <p style='color: rgba(255,255,255,0.8); line-height: 1.6;'>
            Desarrollado con soporte para múltiples tipos de elementos estructurales:<br>
            <strong>Barras</strong> • <strong>Vigas</strong> • <strong>Vigas Pórtico</strong><br>
            Incluye matrices de transformación, análisis de desplazamientos y visualización avanzada.<br>
            <strong>Modo Manual</strong> e <strong>Interactivo</strong> disponibles para todos los tipos de elementos.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
