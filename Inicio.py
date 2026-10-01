"""
☁️ WordCloud Studio — Generador de Nubes de Palabras
Aplicación Streamlit con interfaz limpia en tonos rosa pastel / blush

Instalación:
    pip install streamlit wordcloud matplotlib pandas Pillow numpy

Ejecución:
    streamlit run wordcloud_app.py
"""

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
import io
from collections import Counter
from wordcloud import WordCloud, STOPWORDS

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="WordCloud Studio | Analizador de Texto",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# ESTILOS — Tema Rosa Pastel / Blush
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Fondo general rosa muy claro / blush suave */
    .stApp {
        background-color: #fdf6f7;
    }

    /* Sidebar blanco rosado con borde delicado */
    [data-testid="stSidebar"] {
        background-color: #fff9fa !important;
        border-right: 1px solid #f3dbe0;
    }
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #7a3e4d !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
    }
    [data-testid="stSidebar"] label {
        color: #5c3843 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }
    [data-testid="stSidebar"] p {
        color: #8c6873 !important;
        font-size: 0.88rem !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: #f3dbe0 !important;
        margin: 16px 0 !important;
    }

    /* Campos de entrada */
    textarea, input[type="text"] {
        background-color: #ffffff !important;
        border: 1px solid #ebd0d5 !important;
        border-radius: 8px !important;
        color: #3d232a !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.9rem !important;
    }
    textarea:focus, input[type="text"]:focus {
        border-color: #d88295 !important;
        box-shadow: 0 0 0 2px rgba(216, 130, 149, 0.2) !important;
    }

    /* Selectbox */
    [data-baseweb="select"] > div {
        background: #ffffff !important;
        border: 1px solid #ebd0d5 !important;
        border-radius: 8px !important;
        color: #3d232a !important;
        font-size: 0.9rem !important;
    }

    /* Títulos generales */
    h1 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #4a212b !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px !important;
    }
    h2, h3 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #5c2936 !important;
        font-weight: 600 !important;
    }
    p, li {
        color: #4a333a !important;
        font-size: 0.95rem !important;
        line-height: 1.65 !important;
    }

    /* Botón principal — Rosa Frambuesa Suave */
    .stButton > button {
        background: linear-gradient(135deg, #d88295 0%, #c46b80 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.3px !important;
        padding: 0.65rem 1.4rem !important;
        width: 100% !important;
        box-shadow: 0 3px 10px rgba(216, 130, 149, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #c46b80 0%, #b0576c 100%) !important;
        box-shadow: 0 4px 14px rgba(216, 130, 149, 0.45) !important;
    }

    /* Botón descarga */
    [data-testid="stDownloadButton"] button {
        background: #a8586c !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        transition: background 0.2s !important;
    }
    [data-testid="stDownloadButton"] button:hover {
        background: #8e4356 !important;
    }

    /* Tarjetas de métricas */
    [data-testid="metric-container"] {
        background: #ffffff;
        border: 1px solid #f3dbe0;
        border-top: 3px solid #d88295;
        border-radius: 10px;
        padding: 18px 22px;
        box-shadow: 0 2px 8px rgba(216, 130, 149, 0.08);
    }
    [data-testid="metric-container"] label {
        color: #8c6873 !important;
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.6px !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #4a212b !important;
        font-weight: 700 !important;
        font-size: 1.55rem !important;
    }

    /* Contenedor Header */
    .header-card {
        background: #ffffff;
        border: 1px solid #f3dbe0;
        border-left: 5px solid #d88295;
        border-radius: 10px;
        padding: 26px 34px;
        margin-bottom: 24px;
        box-shadow: 0 2px 10px rgba(216, 130, 149, 0.06);
    }

    /* Tarjetas de sección */
    .section-card {
        background: #ffffff;
        border: 1px solid #f3dbe0;
        border-radius: 10px;
        padding: 24px 28px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(216, 130, 149, 0.05);
    }

    /* Filas de frecuencia */
    .freq-row {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 8px 14px;
        margin: 4px 0;
        background: #fff9fa;
        border: 1px solid #fceef1;
        border-radius: 8px;
        transition: background 0.15s;
    }
    .freq-row:hover { background: #fceef1; }

    .freq-bar {
        height: 8px;
        background: #d88295;
        border-radius: 4px;
        display: inline-block;
        vertical-align: middle;
    }

    /* Etiqueta de ranking */
    .rank-tag {
        background: #f8e5e8;
        border: 1px solid #f3dbe0;
        border-radius: 6px;
        padding: 1px 8px;
        font-size: 0.75rem;
        font-weight: 700;
        color: #8c5060;
        font-family: 'JetBrains Mono', monospace;
        min-width: 36px;
        text-align: center;
    }

    /* Elementos explicativos */
    .info-item {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 12px 16px;
        background: #fff9fa;
        border: 1px solid #f3dbe0;
        border-radius: 8px;
        margin-bottom: 8px;
    }

    /* Etiquetas de uso */
    .uso-tag {
        display: inline-block;
        background: #f8e5e8;
        border: 1px solid #ebd0d5;
        border-radius: 20px;
        padding: 5px 14px;
        font-size: 0.85rem;
        font-weight: 500;
        color: #5c2936;
        margin: 4px 3px;
    }

    /* Desplegables */
    div[data-testid="stExpander"] {
        border: 1px solid #f3dbe0 !important;
        border-radius: 10px !important;
        background: #ffffff !important;
    }

    hr { border-color: #f3dbe0 !important; }

    /* Contenedor de la Nube */
    .wc-container {
        background: #ffffff;
        border: 1px solid #f3dbe0;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(216, 130, 149, 0.08);
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# STOPWORDS (Palabras vacías)
# ─────────────────────────────────────────────
STOPWORDS_ES = {
    "de","la","el","en","y","a","los","del","se","las","un","por","con","no","una","su",
    "para","es","al","lo","como","mas","pero","sus","le","ya","o","este","si","porque",
    "esta","entre","cuando","muy","sin","sobre","tambien","me","hasta","hay","donde",
    "quien","desde","nos","durante","ni","contra","ese","eso","ante","bajo","tras",
    "que","fue","son","han","ha","ser","era","estan","siendo","sido","he","has","hemos",
    "habian","tiene","tienen","hacer","puede","pueden","asi","tan","parte","todo","todos",
    "todas","cada","otro","otra","otros","otras","mismo","misma","nuestro","nuestra",
    "ellos","ellas","nosotros","les","esa","esos","esas","aquel","aquella","aquellos",
}

def obtener_stopwords(idioma):
    sw = set(STOPWORDS)
    if idioma in ("Español", "Ambos"):
        sw |= STOPWORDS_ES
    return sw


# ─────────────────────────────────────────────
# PALETAS DE COLOR REVISIONADAS
# ─────────────────────────────────────────────
PALETAS = {
    "Rosa & Rubí":            ["#4a1525", "#7a223c", "#a83254", "#d8527a", "#e882a0", "#f3b2c4"],
    "Blush Romántico":        ["#5c2936", "#8c4356", "#b85c74", "#d88295", "#eaabb8", "#f5d3dc"],
    "Vino & Rosé":            ["#2b0d17", "#4d1a2b", "#782845", "#a63a61", "#d45b84", "#e892b0"],
    "Gris Cálido & Rosa":     ["#2b2829", "#4a4547", "#736c6f", "#a68892", "#cfa3b0", "#ebcad4"],
    "Borgoña & Coral":        ["#3d0c1e", "#661834", "#992950", "#cc4371", "#e6739a", "#f2a6c1"],
    "Pastel Monocromático":   ["#4a212b", "#6b3341", "#8c4758", "#ad5d71", "#ce768c", "#e394a8"],
}

FORMAS = {
    "Rectángulo": None,
    "Círculo":    "circle",
}

def crear_mascara(forma, size=500):
    if forma == "circle":
        y, x = np.ogrid[:size, :size]
        cx, cy = size // 2, size // 2
        mascara = np.ones((size, size), dtype=np.uint8) * 255
        mascara[(x - cx)**2 + (y - cy)**2 <= (size // 2 - 12)**2] = 0
        return mascara
    return None


# ─────────────────────────────────────────────
# FUNCIONES PRINCIPALES
# ─────────────────────────────────────────────
def limpiar_texto(texto, stopwords, min_longitud):
    texto = texto.lower()
    texto = re.sub(r"http\S+|www\S+", "", texto)
    texto = re.sub(r"[^a-záéíóúüñàâèêîôùûäëïöü\s]", " ", texto, flags=re.UNICODE)
    palabras = [p for p in texto.split() if p not in stopwords and len(p) >= min_longitud]
    return " ".join(palabras)


def contar_palabras(texto_limpio):
    return pd.DataFrame(Counter(texto_limpio.split()).most_common(50),
                        columns=["Palabra", "Frecuencia"])


def generar_wordcloud(texto_limpio, paleta_nombre, max_words, fondo, forma, ancho=1000, alto=520):
    import random
    colores = PALETAS[paleta_nombre]

    def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        rng = random_state or random.Random()
        return colores[rng.randint(0, len(colores) - 1)]

    mascara = crear_mascara(forma, size=min(ancho, alto))
    wc = WordCloud(
        width=ancho, height=alto, max_words=max_words,
        background_color=fondo, color_func=color_func,
        mask=mascara, collocations=False,
        min_font_size=11, max_font_size=120,
        prefer_horizontal=0.75, relative_scaling=0.5, margin=5,
    ).generate(texto_limpio)

    fig, ax = plt.subplots(figsize=(ancho / 100, alto / 100))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    fig.patch.set_facecolor(fondo)
    plt.tight_layout(pad=0)
    return fig


def fig_a_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    buf.seek(0)
    return buf.read()


# ─────────────────────────────────────────────
# PANEL LATERAL (SIDEBAR)
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌸 WordCloud Studio")
    st.caption("Herramienta visual de análisis léxico")
    st.divider()

    # ── Fuente de datos ──
    st.markdown("### ORIGEN DEL TEXTO")
    fuente = st.radio("fuente", ["✍️️ Pegar texto directo", "📂 Subir archivo"],
                      label_visibility="collapsed")
    texto_input = ""

    if fuente == "✍️ Pegar texto directo":
        texto_input = st.text_area(
            "Texto:", height=190,
            placeholder="Introduce aquí tus respuestas de encuestas, ensayos, críticas o artículos...")

        with st.expander("Usar textos de muestra"):
            ejemplos = {
                "Inteligencia Artificial": """
                La inteligencia artificial es una disciplina de la informática orientada a desarrollar
                sistemas capaces de ejecutar tareas que requieren capacidades cognitivas humanas.
                El aprendizaje automático, las redes neuronales profundas y el procesamiento del
                lenguaje natural constituyen los pilares técnicos de los sistemas modernos de
                inteligencia artificial. Los modelos de lenguaje de gran escala, la visión
                computacional y la robótica autónoma representan aplicaciones de vanguardia.
                """,
                "Biodiversidad Colombiana": """
                Colombia es una nación situada en el extremo noroccidental de América del Sur,
                reconocida por su excepcional biodiversidad, riqueza cultural y diversidad de paisajes.
                Bogotá es la capital y principal centro económico, seguida de Medellín, Cali y
                Barranquilla como ciudades de relevancia nacional. El café colombiano goza de
                reconocimiento internacional por su calidad y perfil aromático.
                """,
                "Transformación Digital": """
                La cuarta revolución industrial redefine los modelos productivos mediante la
                convergencia de tecnologías digitales avanzadas. El Internet de las cosas,
                la inteligencia artificial, el análisis de grandes datos, la robótica colaborativa
                y la automatización inteligente son pilares estratégicos de la industria moderna.
                """,
            }
            ejemplo_sel = st.selectbox("Muestra:", list(ejemplos.keys()),
                                       label_visibility="collapsed")
            if st.button("Cargar texto seleccionado"):
                st.session_state["texto_ejemplo"] = ejemplos[ejemplo_sel]
                st.rerun()

        if "texto_ejemplo" in st.session_state and not texto_input:
            texto_input = st.session_state["texto_ejemplo"]

    else:
        archivo = st.file_uploader("Archivo de datos:", type=["txt", "csv"],
                                   label_visibility="collapsed")
        if archivo:
            if archivo.name.endswith(".txt"):
                texto_input = archivo.read().decode("utf-8", errors="ignore")
            elif archivo.name.endswith(".csv"):
                df_csv = pd.read_csv(archivo)
                col_txt = st.selectbox("Selecciona columna de texto:", df_csv.columns.tolist())
                texto_input = " ".join(df_csv[col_txt].dropna().astype(str).tolist())
            st.success(f"Cargado con éxito — {len(texto_input):,} caracteres")

    st.divider()

    # ── Filtrado y Limpieza ──
    st.markdown("### FILTRADO Y REGLAS")
    idioma         = st.selectbox("Excluir stopwords:", ["Español", "Inglés", "Ambos", "Ninguno"])
    min_longitud   = st.slider("Mínimo de caracteres por palabra", 2, 8, 3)
    palabras_extra = st.text_input("Omitir palabras específicas:",
                                   placeholder="ej: además, cada, según")

    st.divider()

    # ── Estilo y Diseño ──
    st.markdown("### ESTILO DE LA NUBE")
    paleta_sel  = st.selectbox("Combinación de color:", list(PALETAS.keys()))
    fondo_sel   = st.radio("Fondo del gráfico:", ["Blanco", "Negro"], horizontal=True)
    fondo_color = "white" if fondo_sel == "Blanco" else "black"
    forma_sel   = st.selectbox("Silueta:", list(FORMAS.keys()))
    max_words   = st.slider("Límite de palabras visible:", 20, 200, 80)

    st.divider()
    generar = st.button("DISEÑAR NUBE DE PALABRAS  ✨", use_container_width=True)


# ─────────────────────────────────────────────
# ÁREA PRINCIPAL
# ─────────────────────────────────────────────

# Encabezado
st.markdown("""
<div class="header-card">
    <h1 style="margin:0; font-size:1.9rem;">🌸 WordCloud Studio</h1>
    <p style="margin:6px 0 0 0; color:#8c6873 !important; font-size:0.97rem;">
        Plataforma estética de minería de texto e identificación de palabras clave
    </p>
</div>
""", unsafe_allow_html=True)

# ── Pantalla de Inicio / Instrucciones ──
if not generar or not texto_input.strip():
    col_izq, col_der = st.columns([3, 2], gap="large")

    with col_izq:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### ¿Cómo funciona la herramienta?")
        st.markdown("""
        Esta solución permite explorar patrones de lenguaje en segundos. Las **nubes de términos**
        resaltan visualmente los conceptos más recurrentes en tus documentos, facilitando
        resúmenes visuales inmediatos para presentaciones o informes.
        """)

        for icono, titulo, desc in [
            ("🧠", "Mapeo léxico directo", "Detecta las palabras con mayor impacto dentro del escrito."),
            ("🧹", "Depuración automática", "Limpia palabras comunes o vacías (*stopwords*) de forma inteligente."),
            ("🎨", "Estética personalizable", "Selecciona paletas en tonos pastel y adapta la silueta de la figura."),
            ("📦", "Descarga de entregables", "Obtén el gráfico resultante en alta definición y los datos en CSV."),
        ]:
            st.markdown(
                f'<div class="info-item">'
                f'<span style="font-size:1.3rem; flex-shrink:0;">{icono}</span>'
                f'<div><strong style="color:#4a212b;">{titulo}</strong>'
                f'<p style="margin:2px 0 0 0; color:#8c6873 !important; font-size:0.88rem;">{desc}</p></div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("#### Pasos rápidos")
        for i, paso in enumerate([
            "Añade o pega tu contenido textual en el panel de la izquierda.",
            "Ajusta los filtros de idioma y personaliza la gama cromática.",
            "Presiona el botón **DISEÑAR NUBE DE PALABRAS ✨**.",
            "Exporta tu gráfico terminado o el listado numérico.",
        ], 1):
            st.markdown(f"**{i}.** {paso}")

        st.markdown('</div>', unsafe_allow_html=True)

    with col_der:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### Casos de uso ideales")
        for caso in [
            "📝 Análisis de encuestas y satisfacción",
            "📊 Resúmenes visuales para reportes",
            "🎓 Revisión de papers y documentos",
            "💬 Feedback de usuarios y clientes",
            "💡 Brainstorming y síntesis conceptual",
            "🔍 Estudios de contenido de marca",
        ]:
            st.markdown(
                f'<span class="uso-tag">{caso}</span>',
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card" style="margin-top:16px;">', unsafe_allow_html=True)
        st.markdown("### Colección de paletas")
        for nombre in PALETAS.keys():
            st.markdown(
                f'<div style="padding:6px 0; border-bottom:1px solid #f8e5e8;">'
                f'<span style="color:#5c2936; font-size:0.88rem; font-weight:500;">🌸 {nombre}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

    if not texto_input.strip() and generar:
        st.warning("Por favor agrega un texto en el panel izquierdo antes de generar el diseño.")
    st.stop()


# ─────────────────────────────────────────────
# PROCESAMIENTO Y GENERACIÓN
# ─────────────────────────────────────────────
stopwords_set = obtener_stopwords(idioma) if idioma != "Ninguno" else set()
if palabras_extra.strip():
    stopwords_set |= {p.strip().lower() for p in palabras_extra.split(",") if p.strip()}

texto_limpio = limpiar_texto(texto_input, stopwords_set, min_longitud)

if not texto_limpio.strip():
    st.error("No quedan suficientes palabras válidas. Ajusta la longitud mínima o revisa las reglas de exclusión.")
    st.stop()

df_freq         = contar_palabras(texto_limpio)
total_palabras = len(texto_limpio.split())
vocabulario    = len(df_freq)

# ── Resumen de Métricas ──
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total palabras",          f"{total_palabras:,}")
m2.metric("Palabras únicas",         f"{vocabulario:,}")
m3.metric("Término estrella",        df_freq.iloc[0]["Palabra"] if not df_freq.empty else "—")
m4.metric("Máxima frecuencia",       int(df_freq.iloc[0]["Frecuencia"]) if not df_freq.empty else 0)

st.markdown("<br>", unsafe_allow_html=True)

# ── Despliegue del Gráfico ──
with st.spinner("Construyendo el diseño visual..."):
    fig_wc = generar_wordcloud(
        texto_limpio, paleta_sel, max_words, fondo_color,
        FORMAS[forma_sel], ancho=1000, alto=520,
    )

st.markdown('<div class="wc-container">', unsafe_allow_html=True)
st.markdown(f"**Visualización de Nube** &nbsp;·&nbsp; Paleta seleccionada: *{paleta_sel}* &nbsp;·&nbsp; Fondo: *{fondo_sel}*")
st.pyplot(fig_wc, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

img_bytes = fig_a_bytes(fig_wc)
st.download_button(
    "📥 Guardar imagen en formato PNG",
    data=img_bytes, file_name="nube_de_palabras_studio.png", mime="image/png",
    use_container_width=True,
)

st.divider()

# ── Desglose de Frecuencias ──
col_freq, col_tabla = st.columns([3, 2], gap="large")

with col_freq:
    st.markdown("### Términos con mayor presencia (Top 20)")
    top20    = df_freq.head(20)
    max_freq = top20["Frecuencia"].max()

    for rank, (_, row) in enumerate(top20.iterrows(), 1):
        p = row["Palabra"]
        f = int(row["Frecuencia"])
        barra_w = max(12, int((f / max_freq) * 210))
        st.markdown(
            f'<div class="freq-row">'
            f'<span class="rank-tag">#{rank:02d}</span>'
            f'<span style="font-weight:600; color:#4a212b; min-width:130px; font-size:0.93rem;">{p}</span>'
            f'<div class="freq-bar" style="width:{barra_w}px; opacity:{0.5 + 0.5*(f/max_freq):.2f};"></div>'
            f'<span style="font-family:\'JetBrains Mono\',monospace; font-size:0.88rem; '
            f'color:#8c5060; min-width:28px; text-align:right; font-weight:500;">{f}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

with col_tabla:
    st.markdown("### Ficha de frecuencias")
    st.dataframe(
        df_freq.head(30).style
               .background_gradient(subset=["Frecuencia"], cmap="PuRd")
               .format({"Frecuencia": "{:,}"}),
        use_container_width=True, height=500,
    )
    csv_bytes = df_freq.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Exportar listado (.csv)",
        data=csv_bytes, file_name="frecuencia_de_palabras.csv", mime="text/csv",
        use_container_width=True,
    )

st.divider()

with st.expander("Inspeccionar texto filtrado (después del tratamiento)"):
    preview = texto_limpio[:2500] + ("..." if len(texto_limpio) > 2500 else "")
    st.markdown(
        f'<p style="font-family:JetBrains Mono,monospace; font-size:0.85rem; '
        f'color:#5c2936; background:#fff9fa; padding:16px; border-radius:8px; '
        f'border:1px solid #f3dbe0; line-height:1.8;">{preview}</p>',
        unsafe_allow_html=True,
    )

plt.close("all")


