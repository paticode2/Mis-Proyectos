# Portafolio 2026 para galerías y convocatorias, con el estilo de la web Archivo.
# Uso: python3 04-documentos/portafolio_build.py  -> 04-documentos/portafolio_2026.html
# El PDF se saca con Playwright (ver portafolio_pdf.js en el scratchpad o imprimir a PDF, carta horizontal).
import base64, io, glob, html
from PIL import Image, ImageOps

A = '/home/user/Mis-Proyectos/artista'
ARTIST = 'Patricia Díaz'
# código, título de trabajo, técnica, medidas (estimadas hasta que Patricia mida)
OBRAS = [
    ("2026-01", "Escultura blanca", "Foam board", "76 × 76 × 76 cm (aprox.)"),
    ("2026-02", "Manchas negras", "Tinta sobre papel", "46 × 61 cm (aprox.)"),
    ("2026-03", "Rosa spray", "Aerosol sobre lienzo", "51 × 41 cm (aprox.)"),
    ("2026-04", "Rojo y negro, mallas", "Medias y mallas sobre bastidor", "41 × 30 × 3 cm (aprox.)"),
    ("2026-05", "Garabatos y manos", "Tinta y carboncillo sobre papel", "61 × 46 cm (aprox.)"),
    ("2026-06", "Trazos horizontales", "Tinta sobre papel", "61 × 46 cm (aprox.)"),
    ("2026-07", "Rosa y negro, gestual", "Acrílico y aerosol sobre papel", "61 × 46 cm (aprox.)"),
    ("2026-08", "Huellas verticales", "Tinta sobre papel", "76 × 56 cm (aprox.)"),
    ("2026-09", "Goteo horizontal", "Tinta sobre papel", "91 × 76 cm (aprox.)"),
    ("2026-10", "Manchas diagonales", "Tinta sobre papel", "76 × 56 cm (aprox.)"),
]

def img(code, size=1500):
    f = glob.glob(f'{A}/02-fotos-obras/web/{code}_*_web.jpg')[0]
    im = ImageOps.exif_transpose(Image.open(f)).convert('RGB'); im.thumbnail((size, size))
    b = io.BytesIO(); im.save(b, 'JPEG', quality=84)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()

def ph(s):  # pendiente
    return f'<span class="ph">{html.escape(s)}</span>'

pages = []
n = 0
def page(inner, cls=''):
    global n
    n += 1
    pages.append(f'<section class="pg {cls}"><div class="bars"></div>{inner}<span class="folio">{n:02d}</span></section>')

# 1 portada
page(f'''<div class="cover">
  <div><p class="k">Portafolio · 2026</p><h1>{ARTIST}</h1><p class="sub">Artista visual · Caguas, Puerto Rico</p></div>
  <img class="hero" src="{img('2026-07', 1800)}" alt="">
</div>''', 'c')

# 2 statement
page('''<div class="two">
  <div><p class="k">Artist statement</p><h2>Desde el gesto</h2>
  <p>Trabajo desde el gesto. Muchas de mis piezas empiezan sin una idea fija: la obra se va armando mientras la hago, y el movimiento de la mano decide tanto como yo. Otras veces parto de un concepto y lo construyo poco a poco, o dejo que todo sea gesto. En los tres casos busco lo mismo: que el caos y el sentimiento queden en la superficie.</p>
  <p>Casi toda mi obra es negro sobre blanco, los colores con los que me identifico. Cuando una pieza necesita decir algo más fuerte, entra el rojo o el rosa. Quiero que quien mire mi obra sienta algo que no sentía hace mucho tiempo: añoranza, nostalgia, ese tipo de sentimiento.</p></div>
  <div class="en"><p class="k">English</p><h2>From gesture</h2>
  <p>My work starts with gesture. Many of my pieces begin without a fixed idea: the work takes shape as I make it, and the movement of my hand decides as much as I do. Other times I start from a concept and build it slowly, or let the whole piece be gesture. Either way, I am after the same thing: leaving chaos and feeling on the surface.</p>
  <p>Almost all my work is black on white, the colors I identify with. When a piece needs to say something louder, red or pink comes in. I want people who look at my work to feel something they haven't felt in a long time: longing, nostalgia, that kind of feeling.</p></div>
</div>''')

# 3-12 obras
for i, (code, title, tech, size) in enumerate(OBRAS, 1):
    page(f'''<div class="work">
  <div class="im"><img src="{img(code)}" alt="{html.escape(title)}"></div>
  <div class="cap"><p class="k">Obra {i:02d} / 10</p><h2>{html.escape(title)}</h2>
  <p>2026<br>{html.escape(tech)}<br>{html.escape(size)}</p><p class="code">{code}</p></div>
</div>''')

# 13 bio + cv
page(f'''<div class="two">
  <div><p class="k">Bio</p><h2>{ARTIST}</h2>
  <p>{ARTIST} nació en Caguas, Puerto Rico, donde vive y trabaja. Lleva diez años haciendo arte en muchos medios: empezó editando fotos y haciendo collage, tuvo su propia marca de ropa e hizo diseño gráfico, graffiti, stickers y patrones antes de llegar a la pintura. También ha experimentado con grabado, la creación de papel y la escultura en metal.</p>
  <p>Su obra es abstracción gestual en tinta, acrílico, aerosol y carboncillo, a veces con materiales como medias y mallas. Hoy busca colaborar con otros artistas, bandas y músicos locales, y exponer.</p></div>
  <div><p class="k">CV</p><h2>Datos</h2>
  <dl>
    <dt>Nacimiento</dt><dd>Caguas, Puerto Rico</dd>
    <dt>Vive y trabaja</dt><dd>Caguas, Puerto Rico</dd>
    <dt>Estudios</dt><dd>Autodidacta · estudios universitarios en curso {ph('[universidad, programa]')}</dd>
    <dt>Exhibiciones</dt><dd>{ph('[nombre, lugar, año]')}</dd>
    <dt>Otros</dt><dd>Marca de ropa propia · diseño gráfico · graffiti y stickers</dd>
  </dl></div>
</div>''')

# 14 contacto
page(f'''<div class="contact">
  <h1 class="big">Contacto</h1>
  <dl>
    <dt>Correo</dt><dd>{ph('[correo]')}</dd>
    <dt>Instagram</dt><dd>{ph('@[nombre artístico]')}</dd>
    <dt>Web</dt><dd>{ph('[dominio]')}</dd>
    <dt>Estudio</dt><dd>Caguas, Puerto Rico</dd>
  </dl>
  <p class="note">Precios y disponibilidad por correo. Medidas aproximadas hasta su confirmación.</p>
</div>''')

css = '''
@page{size:11in 8.5in;margin:0}
*{box-sizing:border-box}
body{margin:0;background:#0d0d0d;font-family:Arimo,"Helvetica Neue",Helvetica,Arial,sans-serif;color:#0a0a0a}
.pg{width:11in;height:8.5in;margin:0 auto 18px;background:#fff;position:relative;padding:.6in .7in .6in 1in;page-break-after:always;overflow:hidden}
.bars{position:absolute;left:.3in;top:.35in;bottom:.35in;width:.15in;background:repeating-linear-gradient(to bottom,#0a0a0a 0 .17in,transparent .17in .3in)}
.folio{position:absolute;right:.7in;bottom:.35in;font-size:11px;font-weight:700}
.k{margin:0 0 6px;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#555}
h1{margin:0;font-size:84px;line-height:.9;letter-spacing:-.04em}
h2{margin:0 0 14px;font-size:30px;line-height:1;letter-spacing:-.02em}
p{font-size:13px;line-height:1.55;margin:0 0 10px}
.cover{display:grid;grid-template-columns:1fr 4.2in;gap:.5in;height:100%;align-items:end}
.sub{font-size:16px;margin-top:14px}
.hero{width:100%;height:7.3in;object-fit:cover;align-self:center}
.two{display:grid;grid-template-columns:1fr 1fr;gap:.6in;height:100%;align-content:center}
.two p{text-align:justify;hyphens:auto}
.en p{color:#444}
.work{display:grid;grid-template-columns:1fr 2.7in;gap:.5in;height:100%;align-items:center}
.work .im{height:7.2in;display:flex;align-items:center;justify-content:center;background:#f4f4f4}
.work img{max-width:100%;max-height:100%;object-fit:contain}
.code{font-size:11px;font-weight:700;margin-top:20px}
dl{display:grid;grid-template-columns:1.4in 1fr;gap:10px 16px;margin:0;font-size:13px}
dt{color:#555;font-size:11px;text-transform:uppercase;letter-spacing:.08em;padding-top:2px}
dd{margin:0}
.ph{background:#eee;color:#666;padding:0 4px}
.contact{height:100%;display:flex;flex-direction:column;justify-content:center}
.big{font-size:150px;transform:scaleY(1.6);transform-origin:left bottom;margin:0 0 .9in}
.note{margin-top:30px;color:#666;font-size:12px}
@media print{body{background:#fff}.pg{margin:0}}
'''
doc = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Portafolio · {ARTIST}</title>
<link href="https://fonts.googleapis.com/css2?family=Arimo:wght@400;700&display=swap" rel="stylesheet"><style>{css}</style></head>
<body>{"".join(pages)}</body></html>'''
open(f'{A}/04-documentos/portafolio_2026.html', 'w').write(doc)
print('pages', n, len(doc) // 1024, 'KB')
