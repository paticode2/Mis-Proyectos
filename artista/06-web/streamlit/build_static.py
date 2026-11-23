# Copia las fotos que usa la web a static/img/, livianas, para que Streamlit las sirva como archivos.
# Correr después de añadir o cambiar fotos:  python3 artista/06-web/streamlit/build_static.py
import re
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
SITE = HERE.parent / "sitio"
OUT = HERE / "static" / "img"
OUT.mkdir(parents=True, exist_ok=True)

keys = sorted(set(re.findall(r"\{\{IMG:([\d-]+)\}\}", (SITE / "archivo.template.html").read_text(encoding="utf-8"))))
for old in OUT.glob("*.jpg"):
    if old.stem not in keys:
        old.unlink()
total = 0
for k in keys:
    im = Image.open(SITE / "img" / f"{k}.jpg").convert("RGB")
    im.thumbnail((1100, 1100))
    dst = OUT / f"{k}.jpg"
    im.save(dst, "JPEG", quality=72, optimize=True, progressive=True)
    total += dst.stat().st_size
print(len(keys), "fotos,", total // 1024, "KB")
