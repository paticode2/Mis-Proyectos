# Patricia Díaz: la web (libreta) (archivo.template.html) servida desde Streamlit.
# En Streamlit Community Cloud: repo paticode2/mis-proyectos, branch main,
# main file path: artista/06-web/streamlit/app.py
# Las fotos se sirven como archivos desde static/img (ver build_static.py), así la página abre rápido.
import re
from pathlib import Path

import streamlit as st

HERE = Path(__file__).resolve().parent
SITE = HERE.parent / "sitio"

st.set_page_config(page_title="Patricia Díaz", page_icon="✶", layout="wide", initial_sidebar_state="collapsed")

# Quitar el marco de Streamlit para que se vea solo la página
st.markdown("""<style>
  header, footer, #MainMenu, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] {display:none !important;}
  html, body, .stApp, [data-testid="stAppViewContainer"] {background:#0A0A0A !important;}
  .block-container, [data-testid="stMainBlockContainer"] {padding:0 !important; max-width:100% !important;}
  iframe {display:block; border:0; height:100dvh !important;}
</style>""", unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def build_page(mtime: float) -> str:
    html = (SITE / "archivo.template.html").read_text(encoding="utf-8")
    # /app/static/... is Streamlit's static file route for the static/ folder next to this file
    html = re.sub(r"\{\{IMG:([\d-]+)\}\}", r"/app/static/img/\1.jpg", html)
    return ("<!doctype html><html lang='es'><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>" + html + "</html>")


# The page is our own file (not user input), so embedding it as-is is safe.
page = build_page((SITE / "archivo.template.html").stat().st_mtime)
if hasattr(st, "iframe"):
    st.iframe(page, height=900)
else:  # older Streamlit
    import streamlit.components.v1 as components
    components.html(page, height=900, scrolling=True)
