# Patrixxia: la web (studio.template.html) servida desde Streamlit.
# En Streamlit Community Cloud: repo paticode2/mis-proyectos, branch main,
# main file path: artista/06-web/streamlit/app.py
import base64, io, re
from pathlib import Path

import streamlit as st
from PIL import Image

SITE = Path(__file__).resolve().parent.parent / "sitio"

st.set_page_config(page_title="Patrixxia", page_icon="✶", layout="wide", initial_sidebar_state="collapsed")

# Quitar el marco de Streamlit para que se vea solo la página
st.markdown("""<style>
  header, footer, #MainMenu, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] {display:none !important;}
  html, body, .stApp, [data-testid="stAppViewContainer"] {background:#0A0A0A !important;}
  .block-container, [data-testid="stMainBlockContainer"] {padding:0 !important; max-width:100% !important;}
  iframe {display:block; border:0; height:100dvh !important;}
</style>""", unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def build_page() -> str:
    """Mete las fotos dentro del HTML (Streamlit no sirve la carpeta img/)."""
    html = (SITE / "studio.template.html").read_text(encoding="utf-8")

    def embed(m):
        f = SITE / "img" / f"{m.group(1)}.jpg"
        im = Image.open(f).convert("RGB")
        im.thumbnail((1000, 1000))
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=78)
        return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

    html = re.sub(r"\{\{IMG:([\d-]+)\}\}", embed, html)
    return "<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>" + html + "</html>"


# The page is our own file (not user input), so embedding it as-is is safe.
html = build_page()
if hasattr(st, "iframe"):
    st.iframe(html, height=900)
else:  # older Streamlit
    import streamlit.components.v1 as components
    components.html(html, height=900, scrolling=True)
