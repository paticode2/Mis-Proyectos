"""Genera los flyers de Patricia en tres formatos:
  illustrator/*.svg  -> abre en Illustrator (texto editable, capas = grupos con nombre)
  photoshop/*.psd    -> una capa por elemento
  preview/*.png      -> vista previa 1080x1350 (Instagram 4:5)

Uso: python3 build_flyers.py   (necesita pillow, psd-tools y playwright con Chromium)
Las fonts están en fonts/: instálalas antes de abrir los archivos.
"""
import base64, io, math, os, random
from pathlib import Path
from PIL import Image, ImageFont, ImageOps, ImageFilter

HERE = Path(__file__).parent
FOTOS = HERE.parent / "02-fotos-obras" / "web"
FONTS = HERE / "fonts"
W, H = 1080, 1350

# Colores de la guía de identidad
PAPEL, TINTA, ROSA, ROSA_HONDO, ROJO = "#F2EEE8", "#171515", "#E0508C", "#B0195C", "#A8141E"
ROSA_LUZ, HAIR, GRIS, NEGRO, BLANCO = "#FFC4DA", "#9A9A9A", "#6F6F6F", "#0D0D0D", "#FFFFFF"
IG = "@___________________1000gs"


# ---------- utilidades ----------
def font(name, w):
    return ImageFont.truetype(str(FONTS / f"{name}-{w}.ttf"), 1000)

def text_w(txt, name, w, size, tracking=0):
    return font(name, w).getlength(txt) * size / 1000 + tracking * max(len(txt) - 1, 0)

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

FAM = {"Arimo": "Arimo", "Unbounded": "Unbounded", "Bricolage": "Bricolage Grotesque",
       "Plex": "IBM Plex Mono", "Fraktur": "UnifrakturMaguntia"}
FILE = {"Bricolage": "BricolageGrotesque", "Plex": "IBMPlexMono", "Fraktur": "UnifrakturMaguntia"}

def T(x, y, s, fam="Arimo", w=400, size=20, fill=TINTA, anchor="start", ls=0, extra=""):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    l = f' letter-spacing="{ls}"' if ls else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FAM[fam]}" font-weight="{w}" '
            f'font-size="{size}" fill="{fill}"{a}{l} {extra}>{esc(s)}</text>')

def tw(s, fam, w, size, ls=0):
    return text_w(s, FILE.get(fam, fam), w, size, ls)

def png_uri(img):
    b = io.BytesIO(); img.save(b, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()

def jpg_uri(img):
    b = io.BytesIO(); img.convert("RGB").save(b, "JPEG", quality=88)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

def foto(code):
    return Image.open(next(FOTOS.glob(f"{code}_*.jpg"))).convert("RGB")

def cover(img, w, h, fx=0.5, fy=0.5):
    """Recorta la imagen para llenar w x h (como object-fit: cover)."""
    r = max(w / img.width, h / img.height)
    im = img.resize((math.ceil(img.width * r), math.ceil(img.height * r)), Image.LANCZOS)
    l = int((im.width - w) * fx); t = int((im.height - h) * fy)
    return im.crop((l, t, l + w, t + h))

def tinta_sola(img, umbral=110, color=(23, 21, 21), suave=1.2):
    """Deja solo la tinta (negro) sobre transparente."""
    g = ImageOps.autocontrast(img.convert("L"), cutoff=2).filter(ImageFilter.GaussianBlur(suave))
    a = g.point(lambda v: 255 if v < umbral else (0 if v > umbral + 40 else int(255 * (umbral + 40 - v) / 40)))
    out = Image.new("RGBA", img.size, color + (0,)); out.putalpha(a)
    return out

def trama_1bit(img, w, h):
    """Trama de puntos en 1 bit (como las obras de la web Archivo)."""
    g = ImageOps.autocontrast(cover(img, w // 2, h // 2).convert("L"), cutoff=3)
    d = g.convert("1").resize((w, h), Image.NEAREST).convert("L")
    out = Image.new("RGBA", (w, h), (10, 10, 10, 0)); out.putalpha(d.point(lambda v: 255 - v))
    return out

def image(uri, x, y, w, h, extra=""):
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" xlink:href="{uri}" {extra}/>'

def layer(name, body):
    return f'<g id="{name}">\n{body}\n</g>'

def svg(layers, bg_name="FONDO"):
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n' + "\n".join(layers) + "\n</svg>\n")


# ---------- pintura rosa (trazos vectoriales) ----------
def brochazo(rng, x0, y0, x1, y1, ancho, curva=0.25):
    """Polígono con forma de brochazo entre dos puntos."""
    n = 40
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
    cx, cy = mx + nx * L * curva * rng.uniform(-1, 1), my + ny * L * curva * rng.uniform(-1, 1)
    top, bot = [], []
    fase = rng.uniform(0, 6)
    for i in range(n + 1):
        t = i / n
        px = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1
        py = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1
        tx = 2 * (1 - t) * (cx - x0) + 2 * t * (x1 - cx); ty = 2 * (1 - t) * (cy - y0) + 2 * t * (y1 - cy)
        tl = math.hypot(tx, ty) or 1; qx, qy = -ty / tl, tx / tl
        wv = ancho * (math.sin(math.pi * t) ** 0.35) * (0.85 + 0.15 * math.sin(t * 9 + fase))
        wv *= 1 - 0.55 * t  # se seca hacia el final
        j = rng.uniform(-0.06, 0.06) * ancho
        top.append((px + qx * (wv / 2 + j), py + qy * (wv / 2 + j)))
        bot.append((px - qx * (wv / 2 - j), py - qy * (wv / 2 - j)))
    pts = top + bot[::-1]
    return "M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in pts) + " Z"

def pintura(seed, trazos, salpicaduras=40, color=ROSA, luz=ROSA_LUZ, zona=(0, 0, W, H)):
    rng = random.Random(seed)
    out = []
    for (x0, y0, x1, y1, a) in trazos:
        out.append(f'<path d="{brochazo(rng, x0, y0, x1, y1, a)}" fill="{color}" opacity="0.92"/>')
        out.append(f'<path d="{brochazo(rng, x0 + a*.1, y0 - a*.12, x1, y1 - a*.1, a * 0.28, 0.12)}" fill="{luz}" opacity="0.55"/>')
    zx, zy, zw, zh = zona
    for _ in range(salpicaduras):
        r = rng.choice([2, 3, 4, 5, 7, 10, 14])
        out.append(f'<circle cx="{zx + rng.random()*zw:.0f}" cy="{zy + rng.random()*zh:.0f}" r="{r}" fill="{color}"/>')
    return "\n".join(out)


# =====================================================================
# FLYER 1 — GASA NEGRA (estilo web Archivo: libro escaneado, blanco y negro)
# =====================================================================
def flyer_gasa():
    L = []
    L.append(layer("FONDO", f'<rect width="{W}" height="{H}" fill="{NEGRO}"/>'))
    # pliego con marcas de encuadernación
    m = 56
    marcas = []
    for (cx, cy) in [(m, m), (W - m, m), (m, H - m), (W - m, H - m)]:
        sx = -1 if cx == m else 1; sy = -1 if cy == m else 1
        marcas.append(f'<path d="M{cx + sx*8},{cy} h{sx*30} M{cx},{cy + sy*8} v{sy*30}" stroke="{GRIS}" stroke-width="1.5" fill="none"/>')
    L.append(layer("PLIEGO", f'<rect x="{m}" y="{m}" width="{W-2*m}" height="{H-2*m}" fill="{BLANCO}"/>\n' + "\n".join(marcas)))

    x0, x1 = 100, W - 100
    cab = [T(x0, 118, "(01)", size=20, fill=NEGRO),
           T(W / 2, 118, "PATRICIA DÍAZ — OBRA RECIENTE", size=20, fill=NEGRO, anchor="middle"),
           T(x1, 118, "11.12.26", size=20, fill=NEGRO, anchor="end"),
           f'<line x1="{x0}" y1="136" x2="{x1}" y2="136" stroke="{NEGRO}" stroke-width="1.5"/>']
    L.append(layer("CABECERA", "\n".join(cab)))

    # titular estirado: GASA arriba, NEGRA cortada en bandas (glitch del libro escaneado)
    size = 300
    def estirado(txt, y, sx_extra=1.0):
        w = tw(txt, "Arimo", 700, size)
        sx = (x1 - x0) / w * sx_extra
        return sx, f'<g transform="translate({x0},{y}) scale({sx:.4f},1)">{T(0, 0, txt, w=700, size=size, fill=NEGRO, ls=0)}</g>'
    _, gasa = estirado("GASA", 400)
    L.append(layer("TITULO_GASA", gasa))
    defs, bandas = [], []
    cortes = [(430, 520, 0), (520, 546, -30), (546, 600, 18), (600, 618, -10), (618, 690, 0)]
    for i, (ya, yb, dx) in enumerate(cortes):
        defs.append(f'<clipPath id="corte{i}"><rect x="0" y="{ya}" width="{W}" height="{yb-ya}"/></clipPath>')
        _, ng = estirado("NEGRA", 668)
        bandas.append(f'<g clip-path="url(#corte{i})"><g transform="translate({dx},0)">{ng}</g></g>')
    L.append(layer("TITULO_NEGRA_GLITCH", "<defs>" + "".join(defs) + "</defs>\n" + "\n".join(bandas)))

    # obra en trama de 1 bit
    iw, ih = 430, 520
    obra = trama_1bit(foto("2026-08"), iw, ih)
    L.append(layer("OBRA_2026-08", image(png_uri(obra), x0, 712, iw, ih)
                   + f'\n{T(x0, 1252, "fig. 03 — huellas verticales, 2026", size=15, fill=GRIS)}'))

    # columna de datos repetidos (estilo contacto Loïc)
    cx = x0 + iw + 40
    filas = []
    y = 726
    for i in range(16):
        destacada = i == 6
        col = NEGRO if destacada else "#BDBDBD"
        filas.append(T(cx, y, "11.12.26", size=15, fill=col, w=700 if destacada else 400))
        filas.append(T(cx + 92, y, "EL LOCAL", size=15, fill=col, w=700 if destacada else 400))
        filas.append(T(x1, y, "SANTURCE PR", size=15, fill=col, anchor="end", w=700 if destacada else 400))
        y += 20
    L.append(layer("DATOS_REPETIDOS", "\n".join(filas)))

    info = [T(cx, 1078, "Viernes 11 de diciembre", w=700, size=30, fill=NEGRO),
            T(cx, 1114, "7:00 — 11:00 pm", size=30, fill=NEGRO),
            T(cx, 1160, "El Local · Calle Cerra, Santurce", size=19, fill=NEGRO),
            T(cx, 1186, "Gasa, malla, imperdibles y tinta.", size=19, fill=NEGRO),
            T(cx, 1212, "Entrada libre.", size=19, fill=NEGRO),
            f'<line x1="{cx}" y1="1050" x2="{x1}" y2="1050" stroke="{NEGRO}" stroke-width="1.5"/>']
    L.append(layer("INFO", "\n".join(info)))
    pie = [f'<line x1="{x0}" y1="1266" x2="{x1}" y2="1266" stroke="{NEGRO}" stroke-width="1.5"/>',
           T(x0, 1286 - 4, IG, size=15, fill=NEGRO),
           T(x1, 1286 - 4, "(05) epílogo", size=15, fill=NEGRO, anchor="end")]
    L.append(layer("PIE", "\n".join(pie)))
    return svg(L)


# =====================================================================
# FLYER 2 — MALLA (estilo web Archivo en vivo: pintura rosa, letras que cambian, marco Illustrator)
# =====================================================================
def flyer_malla():
    L = []
    L.append(layer("FONDO", f'<rect width="{W}" height="{H}" fill="{BLANCO}"/>'))
    # marco tipo Illustrator: pestaña, regla y líneas de construcción
    reg = [f'<rect width="{W}" height="34" fill="#EDEDED"/>',
           T(16, 23, "malla_flyer.ai @ 100% (RGB/Vista previa)", fam="Plex", size=13, fill=GRIS),
           f'<line x1="0" y1="34" x2="{W}" y2="34" stroke="{HAIR}" stroke-width="1"/>']
    for x in range(0, W, 10):
        h = 10 if x % 100 == 0 else (6 if x % 50 == 0 else 3)
        reg.append(f'<line x1="{x}" y1="{34}" x2="{x}" y2="{34+h}" stroke="{HAIR}" stroke-width="1"/>')
        if x % 100 == 0 and x:
            reg.append(T(x + 3, 54, str(x), fam="Plex", size=9, fill=HAIR))
    guias = [f'<line x1="{gx}" y1="34" x2="{gx}" y2="{H}" stroke="{HAIR}" stroke-width="0.8"/>' for gx in (60, W - 60)]
    guias += [f'<line x1="0" y1="{gy}" x2="{W}" y2="{gy}" stroke="{HAIR}" stroke-width="0.8"/>' for gy in (430, 760, 1010)]
    guias.append(f'<circle cx="{W/2}" cy="600" r="330" fill="none" stroke="{HAIR}" stroke-width="0.8"/>')
    guias.append(f'<line x1="60" y1="1010" x2="{W-60}" y2="430" stroke="{HAIR}" stroke-width="0.8" stroke-dasharray="4 6"/>')
    L.append(layer("REGLA_Y_GUIAS", "\n".join(reg + guias)))

    # foto pegada como sticker
    st = cover(foto("2026-07"), 300, 390, fy=0.3)
    L.append(layer("OBRA_2026-07_STICKER",
                   f'<g transform="rotate(-5 860 1150)"><rect x="705" y="955" width="316" height="406" fill="{BLANCO}" stroke="{HAIR}"/>'
                   + image(jpg_uri(st), 713, 963, 300, 390) + "</g>"))

    # pintura rosa detrás de las letras
    L.append(layer("PINTURA_ROSA", pintura(7, [
        (40, 520, 1040, 380, 120), (120, 760, 980, 640, 70), (-20, 300, 520, 200, 50),
        (600, 980, 1100, 860, 60)], salpicaduras=46, zona=(40, 150, 1000, 900))))

    # letras gigantes: M A L L A — una gótica, una al revés
    size = 410
    letras = [("M", "Arimo", 700, 0), ("A", "Arimo", 700, 180), ("L", "Fraktur", 400, 0),
              ("L", "Arimo", 700, 0), ("A", "Arimo", 700, 0)]
    ws = [tw(c, f, w, size) for c, f, w, _ in letras]
    sx = (W - 120) / sum(ws)
    x = 60; base = 760; out = []
    for (c, f, w, rot), lw in zip(letras, ws):
        lw2 = lw * sx
        t = T(0, 0, c, fam=f, w=w, size=size, fill=NEGRO)
        if rot:
            out.append(f'<g transform="translate({x + lw2/2:.1f},{base - size*0.36:.1f}) rotate(180) translate({-lw2/2:.1f},{size*0.36:.1f}) scale({sx:.4f},1)">{t}</g>')
        else:
            out.append(f'<g transform="translate({x:.1f},{base}) scale({sx:.4f},1)">{t}</g>')
        x += lw2
    L.append(layer("LETRAS_MALLA", "\n".join(out)))

    top = [T(60, 110, "COLECTIVA + DJ SET", w=700, size=34, fill=NEGRO),
           T(W - 60, 110, "SÁB 16.01.27", w=700, size=34, fill=NEGRO, anchor="end"),
           T(60, 148, "una noche de textil, tinta y ruido", size=22, fill=NEGRO),
           T(W - 60, 148, "9:00 PM — 2:00 AM", size=22, fill=NEGRO, anchor="end")]
    L.append(layer("FECHA", "\n".join(top)))

    artistas = ["Patricia Díaz", "Ana Lucía Ferrer", "Iván Morales Cruz", "Colectivo Hebra"]
    lista = [T(60, 838, "OBRA", fam="Plex", w=500, size=15, fill=GRIS, ls=2)]
    for i, a in enumerate(artistas):
        lista.append(T(60, 884 + i * 44, a, w=700, size=38, fill=NEGRO))
    lista.append(T(60, 1090, "SONIDO", fam="Plex", w=500, size=15, fill=GRIS, ls=2))
    lista.append(T(60, 1136, "DJ Penumbra", w=700, size=38, fill=ROSA_HONDO))
    L.append(layer("LINEUP", "\n".join(lista)))

    pie = [T(60, 1230, "EL LOCAL", w=700, size=58, fill=NEGRO),
           T(60, 1272, "Santurce, San Juan · $10 en la puerta", size=22, fill=NEGRO),
           T(60, 1310, IG, fam="Plex", size=15, fill=GRIS)]
    L.append(layer("LUGAR", "\n".join(pie)))
    return svg(L)


# =====================================================================
# FLYER 3 — LO QUE QUEDA DE LA MANO (guía de identidad: papel, tinta, un acento rojo)
# =====================================================================
def flyer_mano():
    L = []
    L.append(layer("FONDO", f'<rect width="{W}" height="{H}" fill="{PAPEL}"/>'))
    tinta = tinta_sola(cover(foto("2026-10"), 1080, 960, fy=0.6), umbral=120)
    L.append(layer("OBRA_2026-10_TINTA", image(png_uri(tinta), 0, 420, 1080, 960, 'opacity="0.95"')))

    titulo = []
    y = 168
    for linea in ["LO QUE", "QUEDA DE", "LA MANO"]:
        titulo.append(T(64, y, linea, fam="Unbounded", w=800, size=104, fill=TINTA, ls=-3))
        y += 112
    L.append(layer("TITULO", "\n".join(titulo)))
    L.append(layer("ETIQUETA", T(66, 72, "EXPOSICIÓN COLECTIVA — GALERÍA HOLLÍN", fam="Plex", w=500, size=16, fill=TINTA, ls=1.5)))

    # tarjeta de información (papel encima de la tinta)
    cx, cy, cw, ch = 610, 880, 410, 400
    caja = [f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" fill="{PAPEL}"/>',
            T(cx + 28, cy + 42, "Apertura", fam="Plex", w=500, size=15, fill="#5E5854", ls=1.5),
            T(cx + 28, cy + 96, "Vie 5 de febrero", fam="Bricolage", w=800, size=36, fill=TINTA),
            T(cx + 28, cy + 146, "6:00 — 10:00 pm · 2027", fam="Bricolage", w=400, size=24, fill=TINTA),
            T(cx + 28, cy + 180, "Hasta el 6 de marzo", fam="Bricolage", w=400, size=20, fill="#5E5854"),
            f'<line x1="{cx+28}" y1="{cy+196}" x2="{cx+cw-28}" y2="{cy+196}" stroke="{TINTA}" stroke-width="1"/>']
    artistas = ["Patricia Díaz", "Mariela Santos Vega", "Kevin Ortiz Rivera", "Noelia Cancel"]
    for i, a in enumerate(artistas):
        caja.append(T(cx + 28, cy + 232 + i * 30, a, fam="Bricolage", w=600, size=22, fill=TINTA))
    caja.append(T(cx + 28, cy + 372, "Curaduría: Gabriel Torres", fam="Bricolage", w=400, size=17, fill="#5E5854"))
    L.append(layer("INFO", "\n".join(caja)))

    # acento rojo: óvalo a mano alrededor de la fecha (solo rojo en esta pieza)
    rng = random.Random(3)
    pts = []
    for i in range(0, 380, 8):
        a = math.radians(i - 15)
        r = 1 + 0.03 * math.sin(i / 23) + rng.uniform(-0.01, 0.01)
        pts.append((cx + 160 + 170 * r * math.cos(a), cy + 85 + 31 * r * math.sin(a) - i * 0.02))
    d = "M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in pts)
    L.append(layer("ACENTO_ROJO", f'<path d="{d}" fill="none" stroke="{ROJO}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'))

    pie = [f'<rect x="40" y="1236" width="520" height="84" fill="{PAPEL}"/>',
           T(64, 1300, "Galería Hollín · Calle Cerra, Santurce", fam="Bricolage", w=600, size=22, fill=TINTA),
           T(64, 1270, "Entrada libre", fam="Plex", w=500, size=15, fill=TINTA, ls=1.5)]
    L.append(layer("LUGAR", "\n".join(pie)))
    return svg(L)


# =====================================================================
# FLYER 4 — ESTUDIO ABIERTO (lineup tipo programa, fondo tinta, un acento rosa)
# =====================================================================
def flyer_estudio():
    L = []
    BG = "#0F0D0E"
    L.append(layer("FONDO", f'<rect width="{W}" height="{H}" fill="{BG}"/>'))
    col = 330
    L.append(layer("OBRA_2026-03_COLUMNA", image(jpg_uri(cover(foto("2026-03"), col, H, fx=0.45)), 0, 0, col, H)))
    x0, x1 = col + 50, W - 50
    tit = [T(x0, 120, "ESTUDIO", fam="Unbounded", w=800, size=88, fill=PAPEL, ls=-2),
           T(x0, 214, "ABIERTO", fam="Unbounded", w=800, size=88, fill=ROSA, ls=-2),
           T(x0, 262, "TRAMA — estudios de Santurce abren sus puertas", fam="Plex", w=400, size=17, fill="#A79F98")]
    L.append(layer("TITULO", "\n".join(tit)))

    head = [f'<line x1="{x0}" y1="300" x2="{x1}" y2="300" stroke="{PAPEL}" stroke-width="2"/>',
            T(x0, 346, "SÁB 13 MAR 2027", fam="Unbounded", w=500, size=30, fill=PAPEL),
            T(x1, 346, "2PM—8PM", fam="Unbounded", w=500, size=30, fill=PAPEL, anchor="end"),
            T(x0, 384, "Espacio Trama · Calle Loíza, Santurce", fam="Plex", w=400, size=18, fill=PAPEL),
            f'<line x1="{x0}" y1="410" x2="{x1}" y2="410" stroke="{PAPEL}" stroke-width="2"/>']
    L.append(layer("FECHA_LUGAR", "\n".join(head)))

    prog = [("2:00", "Patricia Díaz", "textil · tinta", True),
            ("2:45", "Noelia Cancel", "grabado", False),
            ("3:30", "Iván Morales Cruz", "escultura", False),
            ("4:15", "Ana Lucía Ferrer", "fotografía", False),
            ("5:00", "Kevin Ortiz Rivera", "video", False),
            ("6:00", "Colectivo Hebra", "performance", False),
            ("7:00", "DJ Penumbra", "cierre", False)]
    rows = [T(x0, 452, "HORA", fam="Plex", w=500, size=13, fill="#A79F98", ls=2),
            T(x0 + 110, 452, "ARTISTA", fam="Plex", w=500, size=13, fill="#A79F98", ls=2),
            T(x1, 452, "QUÉ", fam="Plex", w=500, size=13, fill="#A79F98", ls=2, anchor="end")]
    y = 470
    for hora, nom, que, dest in prog:
        c = ROSA if dest else PAPEL
        rows.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="#2E2A2B" stroke-width="1"/>')
        rows.append(T(x0, y + 56, hora, fam="Plex", w=500, size=22, fill=c))
        rows.append(T(x0 + 110, y + 58, nom, fam="Bricolage", w=800 if dest else 600, size=34, fill=c))
        rows.append(T(x1, y + 56, que, fam="Plex", w=400, size=17, fill="#A79F98", anchor="end"))
        y += 92
    rows.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="#2E2A2B" stroke-width="1"/>')
    L.append(layer("PROGRAMA", "\n".join(rows)))

    pie = [T(x0, 1268, "Entrada libre · todas las edades", fam="Plex", w=500, size=17, fill=PAPEL),
           T(x0, 1300, IG, fam="Plex", w=400, size=15, fill="#A79F98"),
           f'<rect x="{x1-118}" y="1250" width="118" height="58" fill="{ROSA}"/>',
           T(x1 - 59, 1288, "(04)", fam="Unbounded", w=800, size=24, fill="#0F0D0E", anchor="middle")]
    L.append(layer("PIE", "\n".join(pie)))
    return svg(L)


FLYERS = {
    "01_gasa-negra_el-local": flyer_gasa,
    "02_malla_colectiva-dj": flyer_malla,
    "03_lo-que-queda-de-la-mano_galeria-hollin": flyer_mano,
    "04_estudio-abierto_trama": flyer_estudio,
}


# ---------- render: PNG + PSD por capas ----------
def render(svgs):
    from playwright.sync_api import sync_playwright
    from psd_tools import PSDImage
    from psd_tools.api.layers import PixelLayer
    import re
    (HERE / "preview").mkdir(exist_ok=True); (HERE / "photoshop").mkdir(exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ.get("CHROMIUM", "/opt/pw-browsers/chromium") if os.path.exists("/opt/pw-browsers/chromium") else None)
        pg = b.new_page(viewport={"width": W, "height": H})
        for name, path in svgs.items():
            src = path.read_text()
            pg.set_content(f'<html><body style="margin:0;background:transparent">{src.split("?>",1)[1]}</body></html>')
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(300)
            pg.screenshot(path=str(HERE / "preview" / f"{name}.png"))
            ids = re.findall(r'^<g id="([^"]+)">', src, re.M)
            psd = PSDImage.new("RGB", (W, H))
            for lid in ids:
                pg.evaluate("""id => document.querySelectorAll('svg > g').forEach(g =>
                    g.style.visibility = g.id === id ? 'visible' : 'hidden')""", lid)
                png = pg.screenshot(omit_background=True)
                im = Image.open(io.BytesIO(png)).convert("RGBA")
                box = im.getbbox()
                if not box:
                    continue
                psd.append(PixelLayer.frompil(im.crop(box), psd, lid, top=box[1], left=box[0]))
            pg.evaluate("document.querySelectorAll('svg > g').forEach(g => g.style.visibility='visible')")
            psd.save(str(HERE / "photoshop" / f"{name}.psd"))
            print("ok", name, len(ids), "capas")
        b.close()


if __name__ == "__main__":
    out = HERE / "illustrator"; out.mkdir(exist_ok=True)
    paths = {}
    for name, fn in FLYERS.items():
        p = out / f"{name}.svg"; p.write_text(fn()); paths[name] = p
    render(paths)
