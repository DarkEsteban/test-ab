"""
================================================================================
 AB TEST SIMULATOR | Growth & Marketing Digital — Executive Edition
 App interactiva en Streamlit para simular y analizar Tests A/B de campañas.

 SISTEMA DE DISEÑO
 ------------------
 Paleta:    grafito (#0b0e14) · superficie (#141922) · borde (#262c3a)
            texto (#eef0f5) · emerald=mejora (#34d399) · coral=empeora (#f25f5c)
 Tipografía: Space Grotesk (títulos) · Inter (cuerpo) · JetBrains Mono (cifras)
 Elemento distintivo: banner "Veredicto en vivo" — resume la decisión de
            negocio en una sola línea, con las cifras clave en mono grande.
================================================================================
"""

import streamlit as st

# ==============================================================================
# 1. CONFIGURACIÓN GENERAL DE LA PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="AB Test Simulator | Growth Lab",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==============================================================================
# 2. SISTEMA DE DISEÑO (CSS GLOBAL)
#    Fondo y tipografía forzados de forma explícita para que la app se vea
#    siempre igual sin importar el tema (claro/oscuro) del navegador del
#    usuario. Todo el color vive en variables --token para mantener
#    consistencia entre secciones.
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;700&display=swap');

    :root {
        --bg:            #0b0e14;
        --surface:       #141922;
        --surface-alt:   #1b212c;
        --border:        #262c3a;
        --text:          #eef0f5;
        --text-muted:    #8b93a7;
        --emerald:       #34d399;
        --emerald-bg:    rgba(52, 211, 153, 0.12);
        --coral:         #f25f5c;
        --coral-bg:      rgba(242, 95, 92, 0.12);
        --amber:         #f5a623;
    }

    /* Fondo forzado de toda la app (independiente del tema del usuario) */
    .stApp { background-color: var(--bg) !important; }
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0) !important; }
    .block-container { padding-top: 2.2rem; padding-bottom: 2.5rem; max-width: 1180px; }

    /* Tipografía base + forzado de color en todo elemento de texto,
       para que nunca herede blanco-sobre-blanco o negro-sobre-negro
       del tema del sistema. */
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    [data-testid="stWidgetLabel"] p,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stCaptionContainer"],
    label, span, div { color: var(--text); }

    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; }

    /* ---------- ENCABEZADO ---------- */
    .eyebrow {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        color: var(--emerald);
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .main-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.3rem;
        font-weight: 700;
        color: var(--text);
        margin: 0 0 4px 0;
        line-height: 1.15;
    }
    .subtitle {
        font-size: 0.95rem;
        color: var(--text-muted);
        margin: 0 0 1.4rem 0;
    }

    /* ---------- BANNER DE VEREDICTO (elemento distintivo) ---------- */
    .verdict {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 24px;
        border-radius: 14px;
        padding: 22px 28px;
        margin: 4px 0 1.8rem 0;
        border: 1px solid var(--border);
    }
    .verdict-left { display: flex; align-items: center; gap: 16px; }
    .verdict-icon { font-size: 2rem; line-height: 1; }
    .verdict-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--text-muted);
        margin-bottom: 2px;
    }
    .verdict-headline {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--text);
    }
    .verdict-stats { display: flex; gap: 28px; }
    .verdict-stat { text-align: right; }
    .verdict-stat-num {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.5rem;
        font-weight: 700;
    }
    .verdict-stat-cap {
        font-size: 0.68rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    /* ---------- TARJETAS ---------- */
    .panel-card {
        background-color: var(--surface);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.3rem 1.4rem;
        margin-bottom: 1rem;
        height: 100%;
    }
    .panel-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        font-weight: 700;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.9rem;
    }

    /* ---------- FUENTES DEL EXPERIMENTO (links) ---------- */
    input[type="text"] {
        background-color: var(--surface-alt) !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.85rem !important;
    }
    input[type="text"]:focus {
        border-color: var(--emerald) !important;
        box-shadow: 0 0 0 2px rgba(52,211,153,0.15) !important;
    }
    .link-status {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        margin-top: 6px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .link-status.ok { color: var(--emerald); }
    .link-status.empty { color: var(--text-muted); font-style: italic; }
    .link-status a { color: var(--emerald); text-decoration: none; border-bottom: 1px dotted var(--emerald); }

    /* ---------- MÉTRICAS NATIVAS ---------- */
    div[data-testid="stMetric"] {
        background-color: var(--surface-alt);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 0.8rem 1rem;
    }
    div[data-testid="stMetricValue"] {
        color: var(--text) !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    div[data-testid="stMetricLabel"] { color: var(--text-muted) !important; }

    /* Toggle / slider labels con más peso */
    [data-testid="stWidgetLabel"] p { font-size: 0.9rem; font-weight: 500; }

    hr { border-color: var(--border); margin: 1.6rem 0; }

    /* ---------- TABLA DE RESULTADOS ---------- */
    .ab-table {
        width: 100%;
        border-collapse: collapse;
        font-family: 'Inter', sans-serif;
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid var(--border);
    }
    .ab-table th {
        background-color: var(--surface-alt);
        color: var(--text-muted) !important;
        text-align: left;
        padding: 13px 20px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        border-bottom: 1px solid var(--border);
    }
    .ab-table td {
        padding: 15px 20px;
        font-size: 0.95rem;
        color: var(--text) !important;
        border-bottom: 1px solid var(--border);
        font-family: 'JetBrains Mono', monospace;
    }
    .ab-table td.label-cell { font-family: 'Inter', sans-serif; font-weight: 600; }
    .row-a { background-color: var(--surface); }
    .row-b { background-color: var(--surface); box-shadow: inset 4px 0 0 0 var(--emerald); }
    .row-cro { background-color: var(--surface-alt); }
    .row-cro td { border-bottom: none; }

    .badge-live {
        display: inline-block;
        background-color: var(--emerald-bg);
        color: var(--emerald) !important;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        font-weight: 700;
        padding: 3px 9px;
        border-radius: 20px;
        letter-spacing: 0.05em;
        border: 1px solid rgba(52,211,153,0.35);
        margin-left: 8px;
    }
    .delta-chip {
        display: inline-block;
        padding: 3px 11px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 3. INICIALIZACIÓN DEL SESSION STATE
#    (evita que la app reinicie los valores al interactuar con los widgets)
# ==============================================================================
defaults = {
    "link_a": "",
    "link_b": "",
    "cta_activo": False,          # Botones CTA independientes
    "formato_video": False,       # Cambio de formato estático -> video/reel
    "etiqueta_descuento": False,  # Etiqueta de descuento visible
    "inversion_extra": 0,         # Slider de inversión adicional en variante B
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==============================================================================
# 4. ENCABEZADO
# ==============================================================================
st.markdown('<div class="eyebrow">GROWTH LAB · ANALÍTICA DE EXPERIMENTOS</div>', unsafe_allow_html=True)
st.markdown('<p class="main-title">🧪 AB Test Simulator</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Simulá el impacto de cambios creativos y de formato '
    'sobre el rendimiento real de tu campaña — con veredicto de negocio en vivo.</p>',
    unsafe_allow_html=True
)

# Reservamos el espacio del banner de veredicto AQUÍ (arriba), pero lo
# llenamos más abajo, una vez calculadas las métricas con los controles.
# Esto permite que el elemento más importante (la decisión) quede primero
# en el layout aunque dependa de datos calculados después en el código.
verdict_slot = st.empty()


# ==============================================================================
# 5. FUENTES DEL EXPERIMENTO (enlaces dinámicos A / B)
# ==============================================================================
def render_link_status(url: str, etiqueta: str):
    """Confirma visualmente que el link fue capturado, con acceso directo."""
    if url.strip():
        st.markdown(
            f'<div class="link-status ok">● {etiqueta} capturada &nbsp;·&nbsp; '
            f'<a href="{url}" target="_blank" rel="noopener noreferrer">abrir enlace ↗</a></div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="link-status empty">○ Esperando el link de la {etiqueta.lower()}...</div>',
            unsafe_allow_html=True
        )

link_col1, link_col2 = st.columns(2)
with link_col1:
    st.session_state.link_a = st.text_input(
        "Link Variante A (Original)",
        value=st.session_state.link_a,
        placeholder="https://... (ej. carrusel original)"
    )
    render_link_status(st.session_state.link_a, "Variante A")

with link_col2:
    st.session_state.link_b = st.text_input(
        "Link Variante B (Optimizada)",
        value=st.session_state.link_b,
        placeholder="https://... (ej. reel / variante con cambios)"
    )
    render_link_status(st.session_state.link_b, "Variante B")

st.markdown("<hr>", unsafe_allow_html=True)


# ==============================================================================
# 6. DATOS BASE DEL EXPERIMENTO (Variante A - Control, valores fijos)
# ==============================================================================
INVERSION_A = 500.0      # Inversión en Soles (S/)
CLICS_A = 2500            # Clics totales
CONVERSIONES_A = 75       # Conversiones totales

# ------------------------------------------------------------------------------
# 6.1 Lógica de simulación: partimos de los mismos valores base para B
#     y les aplicamos el efecto de cada control activado.
# ------------------------------------------------------------------------------
inversion_b = INVERSION_A
clics_b = CLICS_A
conversiones_b = CONVERSIONES_A

if st.session_state.cta_activo:
    inversion_b += 50; clics_b += 300; conversiones_b += 25
if st.session_state.formato_video:
    inversion_b += 150; clics_b += 650; conversiones_b += 8
if st.session_state.etiqueta_descuento:
    inversion_b += 80; clics_b += 100; conversiones_b += 45

inversion_b += st.session_state.inversion_extra  # presupuesto manual adicional


# ==============================================================================
# 7. PANEL PRINCIPAL: DOS COLUMNAS (Controles | Métricas en tiempo real)
# ==============================================================================
col_controles, col_metricas = st.columns([1, 1.4], gap="large")

with col_controles:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<p class="panel-title">⚙ Panel de control — Variante B</p>', unsafe_allow_html=True)

    st.session_state.cta_activo = st.toggle(
        "Añadir botones CTA independientes",
        value=st.session_state.cta_activo,
        help="Agrega un botón de acción propio en lugar de depender del link del post."
    )
    st.session_state.formato_video = st.toggle(
        "Cambiar formato a video / Reel",
        value=st.session_state.formato_video,
        help="Convierte la pieza estática en un formato de video corto."
    )
    st.session_state.etiqueta_descuento = st.toggle(
        "Activar etiqueta de descuento",
        value=st.session_state.etiqueta_descuento,
        help="Muestra un badge de oferta/descuento sobre la pieza creativa."
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.session_state.inversion_extra = st.slider(
        "Presupuesto adicional para B (S/)",
        min_value=0, max_value=300, step=10,
        value=st.session_state.inversion_extra,
        help="Simula un aumento manual de inversión en la variante optimizada."
    )
    st.markdown('</div>', unsafe_allow_html=True)

    activos = []
    if st.session_state.cta_activo: activos.append("CTA propio")
    if st.session_state.formato_video: activos.append("Video/Reel")
    if st.session_state.etiqueta_descuento: activos.append("Descuento")
    resumen = ", ".join(activos) if activos else "Sin cambios (igual a la variante original)"
    st.caption(f"**Cambios activos en B:** {resumen}")


# ==============================================================================
# 8. CÁLCULO DE MÉTRICAS (CR% y CPA) PARA AMBAS VARIANTES
# ==============================================================================
def calcular_cr(conversiones, clics):
    """Tasa de conversión (%) = conversiones / clics * 100"""
    return (conversiones / clics) * 100 if clics else 0.0

def calcular_cpa(inversion, conversiones):
    """Costo por adquisición = inversión / conversiones"""
    return (inversion / conversiones) if conversiones else 0.0

def variacion_pct(valor_a, valor_b):
    """Variación porcentual: ((B - A) / A) * 100"""
    return ((valor_b - valor_a) / valor_a) * 100 if valor_a else 0.0

cr_a = calcular_cr(CONVERSIONES_A, CLICS_A)
cr_b = calcular_cr(conversiones_b, clics_b)
cpa_a = calcular_cpa(INVERSION_A, CONVERSIONES_A)
cpa_b = calcular_cpa(inversion_b, conversiones_b)

delta_cr = variacion_pct(cr_a, cr_b)      # positivo = mejora (sube CR)
delta_cpa = variacion_pct(cpa_a, cpa_b)   # negativo = mejora (baja CPA)

with col_metricas:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<p class="panel-title">◈ Métricas en tiempo real</p>', unsafe_allow_html=True)

    m1, m2 = st.columns(2)
    with m1:
        st.metric("Tasa de Conversión (CR%) — B", f"{cr_b:.2f}%",
                   delta=f"{delta_cr:.1f}% vs A", delta_color="normal")
    with m2:
        st.metric("Costo por Adquisición (CPA) — B", f"S/ {cpa_b:.2f}",
                   delta=f"{delta_cpa:.1f}% vs A", delta_color="inverse")

    st.markdown("<br>", unsafe_allow_html=True)
    m3, m4, m5 = st.columns(3)
    with m3: st.metric("Inversión (B)", f"S/ {inversion_b:,.0f}")
    with m4: st.metric("Clics (B)", f"{clics_b:,}")
    with m5: st.metric("Conversiones (B)", f"{conversiones_b:,}")

    st.markdown('</div>', unsafe_allow_html=True)


# ==============================================================================
# 9. BANNER DE VEREDICTO (se llena aquí, pero se muestra arriba por verdict_slot)
# ==============================================================================
mejora_cr = delta_cr > 0
mejora_cpa = delta_cpa < 0

if mejora_cr and mejora_cpa:
    icono, label, headline = "🚀", "RECOMENDACIÓN", "Escalar la Variante B — mejora conversión y reduce costo"
    color_borde, color_bg = "var(--emerald)", "var(--emerald-bg)"
elif mejora_cr and not mejora_cpa:
    icono, label, headline = "⚖️", "EVALUAR RENTABILIDAD", "B convierte más, pero también cuesta más por adquisición"
    color_borde, color_bg = "var(--amber)", "rgba(245,166,35,0.10)"
elif not mejora_cr and mejora_cpa:
    icono, label, headline = "🔎", "REVISAR VOLUMEN", "B es más barata, pero no mejora la tasa de conversión"
    color_borde, color_bg = "var(--amber)", "rgba(245,166,35,0.10)"
else:
    icono, label, headline = "🛑", "MANTENER CONTROL", "B no supera a la Original en ninguna métrica clave"
    color_borde, color_bg = "var(--coral)", "var(--coral-bg)"

color_num_cr = "var(--emerald)" if delta_cr >= 0 else "var(--coral)"
color_num_cpa = "var(--emerald)" if delta_cpa <= 0 else "var(--coral)"

verdict_slot.markdown(f"""
<div class="verdict" style="background-color:{color_bg}; border-color:{color_borde};">
    <div class="verdict-left">
        <div class="verdict-icon">{icono}</div>
        <div>
            <div class="verdict-label">{label}</div>
            <div class="verdict-headline">{headline}</div>
        </div>
    </div>
    <div class="verdict-stats">
        <div class="verdict-stat">
            <div class="verdict-stat-num" style="color:{color_num_cr};">{delta_cr:+.1f}%</div>
            <div class="verdict-stat-cap">CR vs A</div>
        </div>
        <div class="verdict-stat">
            <div class="verdict-stat-num" style="color:{color_num_cpa};">{delta_cpa:+.1f}%</div>
            <div class="verdict-stat-cap">CPA vs A</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)


# ==============================================================================
# 10. REPORTE VISUAL: TABLA HTML ESTILIZADA
# ==============================================================================
chip_cr_bg, chip_cr_fg = ("rgba(52,211,153,0.15)", "#34d399") if delta_cr >= 0 else ("rgba(242,95,92,0.15)", "#f25f5c")
chip_cpa_bg, chip_cpa_fg = ("rgba(52,211,153,0.15)", "#34d399") if delta_cpa <= 0 else ("rgba(242,95,92,0.15)", "#f25f5c")

tabla_html = f"""
<table class="ab-table">
    <thead>
        <tr><th>Resultados</th><th>CR%</th><th>CPA</th></tr>
    </thead>
    <tbody>
        <tr class="row-a">
            <td class="label-cell">A · Variante Original</td>
            <td>{cr_a:.2f}%</td>
            <td>S/ {cpa_a:.2f}</td>
        </tr>
        <tr class="row-b">
            <td class="label-cell">B · Variante Optimizada <span class="badge-live">● LIVE</span></td>
            <td>{cr_b:.2f}%</td>
            <td>S/ {cpa_b:.2f}</td>
        </tr>
        <tr class="row-cro">
            <td class="label-cell">CRO% · Variación B vs A</td>
            <td><span class="delta-chip" style="background-color:{chip_cr_bg}; color:{chip_cr_fg};">{delta_cr:+.1f}%</span></td>
            <td><span class="delta-chip" style="background-color:{chip_cpa_bg}; color:{chip_cpa_fg};">{delta_cpa:+.1f}%</span></td>
        </tr>
    </tbody>
</table>
"""
st.markdown(tabla_html, unsafe_allow_html=True)

st.caption("CR% = Conversiones / Clics × 100 · CPA = Inversión / Conversiones · CRO% = ((B − A) / A) × 100")