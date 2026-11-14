# Genera 08-productos/certificados.html (una hoja carta por obra + una para prints) y su PDF.
import base64, io, glob
from PIL import Image
A = '/home/user/Mis-Proyectos/artista'
OBRAS = [
    ("2026-01", "Escultura blanca", "Foam board"),
    ("2026-02", "Manchas negras", "Tinta sobre papel"),
    ("2026-03", "Rosa spray", "Aerosol sobre lienzo"),
    ("2026-04", "Rojo y negro, mallas", "Medias y mallas sobre bastidor"),
    ("2026-05", "Garabatos y manos", "Tinta y carboncillo sobre papel"),
    ("2026-06", "Trazos horizontales", "Tinta sobre papel"),
    ("2026-07", "Rosa y negro, gestual", "Acrílico y aerosol sobre papel"),
    ("2026-08", "Huellas verticales", "Tinta sobre papel"),
    ("2026-09", "Goteo horizontal", "Tinta sobre papel"),
    ("2026-10", "Manchas diagonales", "Tinta sobre papel"),
]

def thumb(code):
    f = glob.glob(f'{A}/02-fotos-obras/web/{code}_*_web.jpg')[0]
    im = Image.open(f).convert('RGB'); im.thumbnail((700, 700))
    b = io.BytesIO(); im.save(b, 'JPEG', quality=82)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()

def page(code, title, tech, edition=False):
    kind = "Print de edición limitada" if edition else "Obra original"
    ed = '<div class="f"><span>Edición</span><span class="line">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; / 25</span></div>' if edition else ''
    img = f'<img src="{thumb(code)}" alt="">' if code else '<div class="noimg">Foto de la obra</div>'
    return f'''<section class="sheet">
  <header><div class="bars"></div><div><p class="k">Certificado de autenticidad</p><h1>{kind}</h1></div><p class="code">{code or "PRINT"}</p></header>
  <div class="body">
    <div class="pic">{img}</div>
    <div class="data">
      <div class="f"><span>Artista</span><b>Patricia Díaz</b></div>
      <div class="f"><span>Título</span><b>{title}</b></div>
      <div class="f"><span>Año</span><b>2026</b></div>
      <div class="f"><span>Técnica</span><b>{tech}</b></div>
      <div class="f"><span>Medidas</span><span class="line"></span></div>
      {ed}
      <div class="f"><span>Comprador/a</span><span class="line"></span></div>
      <div class="f"><span>Fecha de venta</span><span class="line"></span></div>
    </div>
  </div>
  <p class="text">Certifico que esta {"impresión es parte de una edición limitada de 25 copias numeradas y firmadas" if edition else "obra es original y única, hecha a mano por mí"}. Los derechos de autor y de reproducción pertenecen a la artista: la obra no se puede reproducir ni usar comercialmente sin su permiso escrito.</p>
  <p class="text en">I certify that this {"print is part of a limited edition of 25 numbered and signed copies" if edition else "artwork is an original, one-of-a-kind piece made by hand by me"}. Copyright and reproduction rights remain with the artist.</p>
  <footer><div><span class="sig"></span><p>Firma de la artista</p></div><div><span class="sig"></span><p>Lugar y fecha · Caguas, Puerto Rico</p></div></footer>
</section>'''

css = '''
@page{size:letter;margin:0}
*{box-sizing:border-box}
body{margin:0;background:#888;font-family:Arimo,"Helvetica Neue",Helvetica,Arial,sans-serif;color:#0a0a0a}
.sheet{width:8.5in;height:11in;margin:0 auto 20px;background:#fff;padding:.7in .75in .6in 1in;position:relative;display:flex;flex-direction:column;page-break-after:always}
.bars{position:absolute;left:.3in;top:.4in;bottom:.4in;width:.16in;background:repeating-linear-gradient(to bottom,#0a0a0a 0 .17in,transparent .17in .31in)}
header{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:2px solid #0a0a0a;padding-bottom:12px}
.k{margin:0;font-size:12px;letter-spacing:.14em;text-transform:uppercase}
h1{margin:4px 0 0;font-size:42px;line-height:1;letter-spacing:-.02em}
.code{margin:0;font-size:14px;font-weight:700}
.body{display:grid;grid-template-columns:3.1in 1fr;gap:.35in;margin-top:.4in}
.pic img{width:100%;height:4in;object-fit:contain;object-position:left top}
.noimg{height:4in;border:1px dashed #999;display:grid;place-items:center;color:#999;font-size:13px}
.f{display:grid;grid-template-columns:1.25in 1fr;gap:8px;align-items:end;padding:9px 0;border-bottom:1px solid #ddd;font-size:14px}
.f span:first-child{color:#666;font-size:11px;text-transform:uppercase;letter-spacing:.08em}
.line{border-bottom:1px solid #0a0a0a;height:18px}
.text{font-size:13px;line-height:1.5;margin:.35in 0 0;max-width:6.2in}
.text.en{margin-top:8px;color:#666;font-size:11.5px}
footer{margin-top:auto;display:grid;grid-template-columns:1fr 1fr;gap:.5in}
.sig{display:block;border-bottom:1px solid #0a0a0a;height:.6in}
footer p{margin:6px 0 0;font-size:11px;color:#666;text-transform:uppercase;letter-spacing:.08em}
@media print{body{background:#fff}.sheet{margin:0}}
'''
pages = [page(c, t, m) for c, t, m in OBRAS] + [page("", "______________________", "Impresión giclée sobre papel", edition=True)]
html = f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Certificados de autenticidad</title><link href="https://fonts.googleapis.com/css2?family=Arimo:wght@400;700&display=swap" rel="stylesheet"><style>{css}</style></head><body>{"".join(pages)}</body></html>'
open(f'{A}/08-productos/certificados.html', 'w').write(html)
print('ok', len(html) // 1024, 'KB')
