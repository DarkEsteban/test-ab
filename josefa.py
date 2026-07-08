"""
================================================================================
 AB TEST SIMULATOR | Growth & Marketing Digital — Executive Edition
 App interactiva en Streamlit para simular y analizar Tests A/B de campañas.

 FIXES DE ESTA VERSIÓN
 -----------------------
 1) BUG DE RENDERIZADO: el HTML de la tabla se armaba con líneas en blanco
    e indentación dentro del f-string. El parser Markdown de Streamlit
    interpretaba eso como un bloque de código (por eso se veían las
    etiquetas <tr> literales). Ahora TODO el HTML dinámico se arma en una
    sola línea, sin saltos de línea ni indentación, para que siempre se
    renderice como HTML real.
 2) "ESTADO BASE" como 4ta opción del mismo selector: ya no es una fila
    aparte y fija; ahora vive junto a las 3 estrategias, así un solo
    control decide qué se compara y todo se recalcula igual para las 4.
 3) Slider de "Presupuesto adicional" de vuelta, aplicado sobre la opción
    que esté seleccionada en ese momento (solo afecta la vista en vivo,
    no los datos "oficiales" de la tabla comparativa).
================================================================================
"""

import streamlit as st
import streamlit.components.v1 as components

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
        --amber-bg:      rgba(245, 166, 35, 0.10);
    }

    .stApp { background-color: var(--bg) !important; }
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0) !important; }
    .block-container { padding-top: 2.2rem; padding-bottom: 2.5rem; max-width: 1180px; }

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    [data-testid="stWidgetLabel"] p,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stCaptionContainer"],
    label, span, div { color: var(--text); }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; }

    .eyebrow {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem; font-weight: 700; letter-spacing: 0.14em;
        color: var(--emerald); text-transform: uppercase; margin-bottom: 6px;
    }
    .main-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.3rem; font-weight: 700; color: var(--text);
        margin: 0 0 4px 0; line-height: 1.15;
    }
    .subtitle { font-size: 0.95rem; color: var(--text-muted); margin: 0 0 1.4rem 0; }

    .verdict {
        display: flex; align-items: center; justify-content: space-between;
        gap: 24px; border-radius: 14px; padding: 22px 28px;
        margin: 4px 0 1.8rem 0; border: 1px solid var(--border);
    }
    .verdict-left { display: flex; align-items: center; gap: 16px; }
    .verdict-icon { font-size: 2rem; line-height: 1; }
    .verdict-label {
        font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; font-weight: 700;
        letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-muted);
        margin-bottom: 2px;
    }
    .verdict-headline {
        font-family: 'Space Grotesk', sans-serif; font-size: 1.1rem;
        font-weight: 700; color: var(--text);
    }
    .verdict-stats { display: flex; gap: 28px; }
    .verdict-stat { text-align: right; }
    .verdict-stat-num { font-family: 'JetBrains Mono', monospace; font-size: 1.5rem; font-weight: 700; }
    .verdict-stat-cap { font-size: 0.68rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.06em; }

    .panel-card {
        background-color: var(--surface); border: 1px solid var(--border);
        border-radius: 12px; padding: 1.3rem 1.4rem; margin-bottom: 1rem; height: 100%;
    }
    .panel-title {
        font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; font-weight: 700;
        color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.08em;
        margin-bottom: 0.9rem;
    }

    input[type="text"] {
        background-color: var(--surface-alt) !important; color: var(--text) !important;
        border: 1px solid var(--border) !important; border-radius: 8px !important;
        font-family: 'JetBrains Mono', monospace !important; font-size: 0.85rem !important;
    }
    input[type="text"]:focus {
        border-color: var(--emerald) !important; box-shadow: 0 0 0 2px rgba(52,211,153,0.15) !important;
    }
    .embed-caption {
        font-family: 'JetBrains Mono', monospace; font-size: 0.7rem;
        color: var(--text-muted); margin-top: 6px;
    }

    div[data-testid="stMetric"] {
        background-color: var(--surface-alt); border: 1px solid var(--border);
        border-radius: 10px; padding: 0.8rem 1rem;
    }
    div[data-testid="stMetricValue"] { color: var(--text) !important; font-family: 'JetBrains Mono', monospace !important; }
    div[data-testid="stMetricLabel"] { color: var(--text-muted) !important; }
    [data-testid="stWidgetLabel"] p { font-size: 0.9rem; font-weight: 500; }

    hr { border-color: var(--border); margin: 1.6rem 0; }

    .insight-box {
        border-radius: 12px; padding: 18px 20px; border: 1px solid;
        margin-top: 0.8rem; display: flex; gap: 14px; align-items: flex-start;
    }
    .insight-icon { font-size: 1.4rem; line-height: 1.2; }
    .insight-tag {
        font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px; display: block;
    }
    .insight-text { font-size: 0.92rem; line-height: 1.5; color: var(--text); }

    .ab-table {
        width: 100%; border-collapse: collapse; font-family: 'Inter', sans-serif;
        border-radius: 12px; overflow: hidden; border: 1px solid var(--border);
    }
    .ab-table th {
        background-color: var(--surface-alt); color: var(--text-muted) !important;
        text-align: left; padding: 13px 20px; font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em;
        border-bottom: 1px solid var(--border);
    }
    .ab-table td {
        padding: 15px 20px; font-size: 0.93rem; color: var(--text) !important;
        border-bottom: 1px solid var(--border); font-family: 'JetBrains Mono', monospace;
    }
    .ab-table td.label-cell { font-family: 'Inter', sans-serif; font-weight: 600; }
    .row-live { background-color: var(--surface); box-shadow: inset 4px 0 0 0 var(--emerald); }
    .row-plain { background-color: var(--surface); }
    .badge-live {
        display: inline-block; background-color: var(--emerald-bg); color: var(--emerald) !important;
        font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; font-weight: 700;
        padding: 3px 9px; border-radius: 20px; letter-spacing: 0.05em;
        border: 1px solid rgba(52,211,153,0.35); margin-left: 6px;
    }
    .badge-winner {
        display: inline-block; background-color: var(--amber-bg); color: var(--amber) !important;
        font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; font-weight: 700;
        padding: 3px 9px; border-radius: 20px; letter-spacing: 0.05em;
        border: 1px solid rgba(245,166,35,0.35); margin-left: 6px;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 3. MODELO DE DATOS DEL EXPERIMENTO
#    En vez de inventar Conversiones directamente, cada escenario se define
#    con 3 parámetros de medios reales (Clics, CPC, CR% esperado) — igual
#    que se arma un forecast de growth real. La Inversión y las Conversiones
#    se DERIVAN de esos parámetros, y las conversiones incluyen variación
#    estadística (aproximación normal a una binomial) para que cada
#    simulación se sienta como un test real, no un número fijo mágico.
#
#    Los CR% esperados están calibrados para ser creíbles:
#    - CTA: fricción eliminada -> lift fuerte pero realista (+~120%)
#    - Otoño: mucho interés/clics, pero CR apenas sube (no llega a la meta)
#    - Día de la Madre: pico de clics, pero el CR cae y el CPA empeora
#      (el abandono de carrito le pasa factura real al costo por venta)
# ==============================================================================
import random

ESTRATEGIAS = {
    "base": {
        "nombre": "Estado Base (creatividad original)",
        "clics": 2500, "cpc": 0.20, "cr_mean": 0.030,
        "insight": "Resultado de la campaña original, sin ningún cambio aplicado. "
                    "Es el punto de comparación (control) para medir el impacto real "
                    "de cada estrategia que se pruebe.",
    },
    "cta": {
        "nombre": "1 · Implementar los botones CTA",
        "clics": 2650, "cpc": 0.21, "cr_mean": 0.065,
        "insight": "Al redirigir al usuario al modelo exacto, la tasa de conversión "
                    "subió con fuerza. Se eliminó la pérdida de clientes en el "
                    "proceso de búsqueda manual en la web, superando el impacto proyectado.",
    },
    "otono": {
        "nombre": "2 · Colección Otoño-Invierno (cuero 100%)",
        "clics": 4200, "cpc": 0.18, "cr_mean": 0.032,
        "insight": "El anuncio generó muchos clics e interés por la calidad del cuero, "
                    "pero al no contar aún con la experiencia optimizada de enlaces "
                    "directos por tarjeta, la tasa de conversión final no alcanzó la meta del 10%.",
    },
    "diamadre": {
        "nombre": "3 · Campaña Día de la Madre (ventas)",
        "clics": 5200, "cpc": 0.22, "cr_mean": 0.028,
        "insight": "Aunque hubo un pico de clics por la festividad, el anuncio genérico "
                    "de carrusel sufrió abandono de carritos debido a que los usuarios se "
                    "confunden al buscar las promociones dentro del sitio web principal — "
                    "el CPA terminó siendo peor que el del control.",
    },
}


def simular_conversiones(clics: int, cr_mean: float, seed: int) -> int:
    """
    Simula conversiones reales a partir de una tasa de conversión esperada,
    usando una aproximación normal a la distribución binomial (válida porque
    clics es grande). Esto agrega variación estadística realista: cada
    simulación puede dar un resultado ligeramente distinto, igual que un
    test A/B real, en vez de un número fijo siempre idéntico.
    """
    rng = random.Random(seed)
    media = clics * cr_mean
    sigma = (clics * cr_mean * (1 - cr_mean)) ** 0.5
    return max(round(rng.gauss(media, sigma)), 0)


def calcular_cr(conversiones, clics):
    return (conversiones / clics) * 100 if clics else 0.0

def calcular_cpa(inversion, conversiones):
    return (inversion / conversiones) if conversiones else 0.0

def variacion_pct(valor_a, valor_b):
    return ((valor_b - valor_a) / valor_a) * 100 if valor_a else 0.0


# ==============================================================================
# 4. SESSION STATE (todo con key=, sin value= manual -> sin bug de doble clic)
# ==============================================================================
st.session_state.setdefault("modo_media_a", "Link de Instagram")
st.session_state.setdefault("modo_media_b", "Link de Instagram")
st.session_state.setdefault("link_a", "")
st.session_state.setdefault("link_b", "")
st.session_state.setdefault("estrategia_b", "base")     # arranca en Estado Base
st.session_state.setdefault("presupuesto_extra", 0)
st.session_state.setdefault("simulacion_seed", 42)       # semilla de la variación estadística


# ==============================================================================
# 5. ENCABEZADO
# ==============================================================================
st.markdown('<div class="eyebrow">GROWTH LAB · ANALÍTICA DE EXPERIMENTOS</div>', unsafe_allow_html=True)
st.markdown('<p class="main-title">🧪 AB Test Simulator</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Elegí una estrategia y compará sus resultados en vivo contra el Estado Base.</p>', unsafe_allow_html=True)

verdict_slot = st.empty()  # se llena más abajo, una vez calculadas las métricas


# ==============================================================================
# 6. FUENTES CREATIVAS (Instagram embed en vivo + alternativa de upload)
# ==============================================================================
def render_ig_embed(url: str, height: int = 600):
    """Embebe un post/reel público de Instagram DENTRO de la app (no redirige)."""
    embed_code = (
        f'<blockquote class="instagram-media" data-instgrm-permalink="{url}" '
        f'data-instgrm-version="14" style="background:#141922;border:1px solid #262c3a;'
        f'border-radius:12px;margin:0;max-width:540px;width:100%;"></blockquote>'
        f'<script async src="//www.instagram.com/embed.js"></script>'
    )
    components.html(embed_code, height=height, scrolling=True)


def render_media_slot(prefix: str, etiqueta: str):
    """
    Entrada de creatividad para una variante: link de Instagram (embebido en
    vivo) o subir imagen/video directamente. La detección de tipo de archivo
    es automática (st.image para imágenes, st.video para videos), sin que el
    usuario tenga que indicar el formato.
    """
    modo_key = f"modo_media_{prefix}"
    st.radio(f"Fuente — {etiqueta}", options=["Link de Instagram", "Subir archivo"],
             key=modo_key, horizontal=True)

    if st.session_state[modo_key] == "Link de Instagram":
        link_key = f"link_{prefix}"
        st.text_input("Pegar link del post/reel", key=link_key,
                       placeholder="https://www.instagram.com/p/...")
        url = st.session_state[link_key].strip()
        if url:
            render_ig_embed(url)
            st.markdown('<div class="embed-caption">Vista previa en vivo · solo posts públicos</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="embed-caption">○ Esperando el link...</div>', unsafe_allow_html=True)
    else:
        file_key = f"file_{prefix}"
        archivo = st.file_uploader("Subir imagen o video", type=["png", "jpg", "jpeg", "mp4", "mov", "webm"], key=file_key)
        if archivo is not None:
            # Detección automática del tipo de archivo: imagen -> st.image, video -> st.video
            if archivo.type.startswith("video"):
                st.video(archivo)
            else:
                st.image(archivo, use_container_width=True)
        else:
            st.markdown('<div class="embed-caption">○ Esperando el archivo...</div>', unsafe_allow_html=True)


media_col_a, media_col_b = st.columns(2)
with media_col_a:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<p class="panel-title">🅰 Control — Creatividad original</p>', unsafe_allow_html=True)
    render_media_slot("a", "Variante A")
    st.markdown('</div>', unsafe_allow_html=True)

with media_col_b:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<p class="panel-title">🅱 Variante en prueba</p>', unsafe_allow_html=True)
    render_media_slot("b", "Variante B")
    st.markdown('</div>', unsafe_allow_html=True)
    st.caption("💡 Al subir un archivo, la variante arranca en *Estado Base* y sus resultados cambian automáticamente al elegir una de las 3 estrategias abajo.")

st.markdown("<hr>", unsafe_allow_html=True)


# ==============================================================================
# 7. PANEL DE CONTROL: un único selector con las 4 opciones (Base + 3 estrategias)
# ==============================================================================
col_controles, col_metricas = st.columns([1, 1.4], gap="large")

def _nueva_simulacion():
    st.session_state["simulacion_seed"] += 1

with col_controles:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<p class="panel-title">⚙ Qué estás probando ahora</p>', unsafe_allow_html=True)

    st.radio(
        "Seleccioná el estado a simular:",
        options=list(ESTRATEGIAS.keys()),
        format_func=lambda k: ESTRATEGIAS[k]["nombre"],
        key="estrategia_b",
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.slider(
        "Presupuesto adicional (S/)",
        min_value=0, max_value=300, step=10,
        key="presupuesto_extra",
        help="Simula qué pasaría si le sumás más presupuesto a la opción seleccionada. "
             "Solo afecta esta vista en vivo, no los datos oficiales de la tabla."
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.button("🔄 Nueva simulación (variación estadística)", on_click=_nueva_simulacion, use_container_width=True)
    st.caption("Cada simulación redibuja las conversiones con una pequeña variación real, "
               "como en un test A/B de verdad — el CR% esperado se mantiene, pero el número exacto fluctúa.")

    st.markdown('</div>', unsafe_allow_html=True)


# ==============================================================================
# 8. CÁLCULO DE MÉTRICAS: se derivan de Clics × CPC × CR% para cada escenario.
#    "base" usa su valor esperado exacto (dato de control, sin ruido).
#    Las 3 estrategias usan simular_conversiones() para incorporar variación
#    estadística realista, controlada por simulacion_seed (cambia solo al
#    apretar el botón "Nueva simulación").
# ==============================================================================
for k, e in ESTRATEGIAS.items():
    if k == "base":
        conversiones = round(e["clics"] * e["cr_mean"])
    else:
        seed = st.session_state["simulacion_seed"] + hash(k) % 1000
        conversiones = simular_conversiones(e["clics"], e["cr_mean"], seed)
    e["conversiones"] = conversiones
    e["inversion"] = e["clics"] * e["cpc"]
    e["cr"] = calcular_cr(conversiones, e["clics"])
    e["cpa"] = calcular_cpa(e["inversion"], conversiones)

BASE = ESTRATEGIAS["base"]
# La ganadora real = menor CPA entre las 3 estrategias (excluye el estado base)
CANDIDATAS = {k: v for k, v in ESTRATEGIAS.items() if k != "base"}
GANADORA_KEY = min(CANDIDATAS, key=lambda k: CANDIDATAS[k]["cpa"])

seleccionada_key = st.session_state["estrategia_b"]
seleccionada = ESTRATEGIAS[seleccionada_key]

# El presupuesto adicional se aplica SOLO a la vista en vivo (no a la tabla oficial)
inversion_b_vivo = seleccionada["inversion"] + st.session_state["presupuesto_extra"]
cr_b = seleccionada["cr"]
cpa_b_vivo = calcular_cpa(inversion_b_vivo, seleccionada["conversiones"])

delta_cr = variacion_pct(BASE["cr"], cr_b)
delta_cpa = variacion_pct(BASE["cpa"], cpa_b_vivo)
es_ganadora = (seleccionada_key == GANADORA_KEY)
es_base = (seleccionada_key == "base")


with col_metricas:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<p class="panel-title">◈ Métricas en tiempo real</p>', unsafe_allow_html=True)

    m1, m2 = st.columns(2)
    with m1:
        st.metric("Tasa de Conversión (CR%)", f"{cr_b:.2f}%",
                   delta=None if es_base else f"{delta_cr:.1f}% vs Base", delta_color="normal")
    with m2:
        st.metric("Costo por Adquisición (CPA)", f"S/ {cpa_b_vivo:.2f}",
                   delta=None if es_base else f"{delta_cpa:.1f}% vs Base", delta_color="inverse")

    st.markdown("<br>", unsafe_allow_html=True)
    m3, m4, m5 = st.columns(3)
    with m3: st.metric("Inversión", f"S/ {inversion_b_vivo:,.0f}")
    with m4: st.metric("Clics", f"{seleccionada['clics']:,}")
    with m5: st.metric("Conversiones", f"{seleccionada['conversiones']:,}")

    st.markdown('</div>', unsafe_allow_html=True)

    if es_base:
        tag_color, tag_bg, tag_icon, tag_text = "var(--text-muted)", "rgba(139,147,167,0.10)", "📍", "PUNTO DE PARTIDA"
    elif es_ganadora:
        tag_color, tag_bg, tag_icon, tag_text = "var(--emerald)", "var(--emerald-bg)", "🏆", "GANADORA DEFINITIVA"
    else:
        tag_color, tag_bg, tag_icon, tag_text = "var(--coral)", "var(--coral-bg)", "⚠️", "POR DEBAJO DEL BENCHMARK"

    insight_html = (
        f'<div class="insight-box" style="border-color:{tag_color};background-color:{tag_bg};">'
        f'<div class="insight-icon">{tag_icon}</div>'
        f'<div><span class="insight-tag" style="color:{tag_color};">{tag_text}</span>'
        f'<div class="insight-text">{seleccionada["insight"]}</div></div></div>'
    )
    st.markdown(insight_html, unsafe_allow_html=True)


# ==============================================================================
# 9. BANNER DE VEREDICTO
# ==============================================================================
if es_base:
    icono, label = "📍", "ESTADO BASE"
    headline = "Viendo la campaña original — elegí una estrategia para comparar"
    color_borde, color_bg = "var(--text-muted)", "rgba(139,147,167,0.10)"
elif es_ganadora:
    icono, label = "🚀", "RECOMENDACIÓN"
    headline = f'{seleccionada["nombre"]} — escalar de inmediato'
    color_borde, color_bg = "var(--emerald)", "var(--emerald-bg)"
else:
    icono, label = "🛑", "MANTENER EL BENCHMARK"
    headline = f'{seleccionada["nombre"]} queda por debajo de "{ESTRATEGIAS[GANADORA_KEY]["nombre"]}"'
    color_borde, color_bg = "var(--coral)", "var(--coral-bg)"

color_num_cr = "var(--text-muted)" if es_base else ("var(--emerald)" if delta_cr >= 0 else "var(--coral)")
color_num_cpa = "var(--text-muted)" if es_base else ("var(--emerald)" if delta_cpa <= 0 else "var(--coral)")
txt_cr = "—" if es_base else f"{delta_cr:+.1f}%"
txt_cpa = "—" if es_base else f"{delta_cpa:+.1f}%"

verdict_html = (
    f'<div class="verdict" style="background-color:{color_bg};border-color:{color_borde};">'
    f'<div class="verdict-left"><div class="verdict-icon">{icono}</div>'
    f'<div><div class="verdict-label">{label}</div>'
    f'<div class="verdict-headline">{headline}</div></div></div>'
    f'<div class="verdict-stats">'
    f'<div class="verdict-stat"><div class="verdict-stat-num" style="color:{color_num_cr};">{txt_cr}</div>'
    f'<div class="verdict-stat-cap">CR vs Base</div></div>'
    f'<div class="verdict-stat"><div class="verdict-stat-num" style="color:{color_num_cpa};">{txt_cpa}</div>'
    f'<div class="verdict-stat-cap">CPA vs Base</div></div></div></div>'
)
verdict_slot.markdown(verdict_html, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)


# ==============================================================================
# 10. REPORTE VISUAL: TABLA COMPARATIVA (las 4 opciones, datos oficiales fijos)
#     IMPORTANTE: todo el HTML se arma en una sola línea por fila (sin saltos
#     de línea ni indentación) para evitar que Markdown lo interprete como
#     bloque de código en vez de HTML.
# ==============================================================================
filas = []
for k, e in ESTRATEGIAS.items():
    badges = ""
    fila_clase = "row-live" if k == seleccionada_key else "row-plain"
    if k == seleccionada_key:
        badges += '<span class="badge-live">● LIVE</span>'
    if k == GANADORA_KEY:
        badges += '<span class="badge-winner">🏆 GANADORA</span>'
    fila = (
        f'<tr class="{fila_clase}"><td class="label-cell">{e["nombre"]} {badges}</td>'
        f'<td>{e["cr"]:.2f}%</td><td>S/ {e["cpa"]:.2f}</td></tr>'
    )
    filas.append(fila)

tabla_html = (
    '<table class="ab-table"><thead><tr><th>Resultados</th><th>CR%</th><th>CPA</th></tr></thead>'
    f'<tbody>{"".join(filas)}</tbody></table>'
)
st.markdown(tabla_html, unsafe_allow_html=True)

st.caption("CR% = Conversiones / Clics × 100 · CPA = Inversión / Conversiones · Datos oficiales (sin presupuesto adicional). La fila LIVE es la opción seleccionada arriba; GANADORA es la de mejor CPA entre las 3 estrategias.")
