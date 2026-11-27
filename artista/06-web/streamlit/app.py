# Patricia Díaz: la web pública servida desde Streamlit (se abre sin cuenta).
# En Streamlit Community Cloud: repo paticode2/mis-proyectos, branch main,
# main file path: artista/06-web/streamlit/app.py
# Muestra la copia de la web que ya trae fotos y video dentro del archivo (sitio/compartir/),
# así no depende de que Streamlit sirva archivos aparte.
#   patrixxia.streamlit.app            -> modo oscuro
#   patrixxia.streamlit.app/?v=claro   -> versión clara
from pathlib import Path

import streamlit as st

HERE = Path(__file__).resolve().parent
SHARE = HERE.parent / "sitio" / "compartir"
PAGES = {"oscuro": SHARE / "patricia_diaz_dark.html", "claro": SHARE / "patricia_diaz.html"}

st.set_page_config(page_title="Patricia Díaz", page_icon="✶", layout="wide", initial_sidebar_state="collapsed")

# Quitar el marco de Streamlit para que se vea solo la página
st.markdown("""<style>
  header, footer, #MainMenu, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] {display:none !important;}
  html, body, .stApp, [data-testid="stAppViewContainer"] {background:#0B0B0D !important;}
  .block-container, [data-testid="stMainBlockContainer"] {padding:0 !important; max-width:100% !important;}
  iframe {display:block; border:0; height:100dvh !important;}
</style>""", unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def build_page(path: str, mtime: float) -> str:
    html = Path(path).read_text(encoding="utf-8")
    return ("<!doctype html><html lang='es'><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>" + html + "</html>")


version = st.query_params.get("v", "oscuro")
path = PAGES.get(version, PAGES["oscuro"])
# The page is our own file (not user input), so embedding it as-is is safe.
page = build_page(str(path), path.stat().st_mtime)
if hasattr(st, "iframe"):
    st.iframe(page, height=900)
else:  # older Streamlit
    import streamlit.components.v1 as components
    components.html(page, height=900, scrolling=True)
