"""Kit de Instagram de Patricia: plantillas de post, carrusel, stories y portadas de destacados.
  illustrator/*.svg -> Illustrator (texto editable, grupos con nombre)
  photoshop/*.psd   -> Photoshop (una capa por grupo)
  preview/*.png     -> vista previa (y el carrusel ya cortado en 3)
  feed_mockup.png   -> cómo se ve el perfil con las plantillas
Uso: python3 build_instagram.py
"""
import io, re, sys
from pathlib import Path
from PIL import Image

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "08-flyers"))
from build_flyers import (T, tw, layer, image, cover, foto, trama_1bit, tinta_sola, pintura,
                          png_uri, jpg_uri, PAPEL, TINTA, ROSA, ROSA_HONDO, ROSA_LUZ,
                          HAIR, GRIS, NEGRO, BLANCO, IG)

NOMBRE = "Patricia Díaz"
CITA = ["Quiero que quien", "mire mi obra sienta", "algo que no sentía", "hace mucho tiempo:"]


def svg(w, h, layers):
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n' + "\n".join(layers) + "\n</svg>\n")

def hline(x1, y, x2, c=NEGRO, sw=1.5):
    return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{c}" stroke-width="{sw}"/>'

def estirado(txt, x0, x1, y, size, fill=NEGRO, fam="Arimo", w=700):
    sx = (x1 - x0) / tw(txt, fam, w, size)
    return f'<g transform="translate({x0},{y}) scale({sx:.4f},1)">{T(0, 0, txt, fam=fam, w=w, size=size, fill=fill)}</g>'

def glitch(txt, x0, x1, y, size, cortes, pref, fill=NEGRO):
    """Texto estirado y cortado en bandas desplazadas (como la web Archivo)."""
    defs, g = [], []
    for i, (ya, yb, dx) in enumerate(cortes):
        defs.append(f'<clipPath id="{pref}{i}"><rect x="0" y="{ya}" width="4000" height="{yb-ya}"/></clipPath>')
        g.append(f'<g clip-path="url(#{pref}{i})"><g transform="translate({dx},0)">{estirado(txt, x0, x1, y, size, fill)}</g></g>')
    return "<defs>" + "".join(defs) + "</defs>\n" + "\n".join(g)

def cabecera(w, idx, y=86, fill=NEGRO):
    return "\n".join([T(60, y, NOMBRE, w=700, size=28, fill=fill),
                      T(w - 60, y, idx, size=28, fill=fill, anchor="end"),
                      hline(60, y + 22, w - 60, fill)])

def ficha(x, y, w, code, titulo, tecnica, medidas="— × — cm", fill=NEGRO, sub=GRIS):
    return "\n".join([T(x, y, titulo, w=700, size=34, fill=fill),
                      T(x, y + 38, tecnica, size=22, fill=fill),
                      T(x, y + 74, medidas, fam="Plex", size=18, fill=sub),
                      T(x + w, y + 74, code, fam="Plex", size=18, fill=sub, anchor="end")])


# =================== POSTS 1080 x 1350 ===================
PW, PH = 1080, 1350

def post_obra():
    L = [layer("FONDO", f'<rect width="{PW}" height="{PH}" fill="{BLANCO}"/>'),
         layer("CABECERA", cabecera(PW, "(07)"))]
    L.append(layer("FOTO_OBRA", image(jpg_uri(cover(foto("2026-07"), 960, 960, fy=0.35)), 60, 140, 960, 960)
                   + f'\n<rect x="60" y="140" width="960" height="960" fill="none" stroke="{NEGRO}"/>'))
    L.append(layer("FICHA", ficha(60, 1160, 960, "2026-07", "Sin título (rosa negro gestual)",
                                  "Acrílico y carboncillo sobre papel · 2026")))
    L.append(layer("PIE", hline(60, 1268, 1020) + T(60, 1300, IG, fam="Plex", size=16, fill=GRIS)
                   + T(1020, 1300, "obra 2026", fam="Plex", size=16, fill=GRIS, anchor="end")))
    return svg(PW, PH, L)

def post_disponible():
    L = [layer("FONDO", f'<rect width="{PW}" height="{PH}" fill="{BLANCO}"/>'),
         layer("FOTO_OBRA", image(jpg_uri(cover(foto("2026-03"), PW, 980, fy=0.4)), 0, 0, PW, 980))]
    L.append(layer("ETIQUETA_DISPONIBLE",
                   f'<rect x="60" y="60" width="{tw("DISPONIBLE","Arimo",700,40)+48:.0f}" height="66" fill="{ROSA}"/>'
                   + T(84, 108, "DISPONIBLE", w=700, size=40, fill=NEGRO)))
    L.append(layer("FICHA", ficha(60, 1050, 960, "2026-03", "Sin título (rosa spray)",
                                  "Aerosol sobre lienzo · 2026")))
    L.append(layer("PRECIO", hline(60, 1160, 1020)
                   + T(60, 1240, "$ ———", w=700, size=64, fill=NEGRO)
                   + T(1020, 1214, "Escríbeme por DM", size=24, fill=NEGRO, anchor="end")
                   + T(1020, 1246, "o al correo", size=24, fill=NEGRO, anchor="end")
                   + T(60, 1300, IG, fam="Plex", size=16, fill=GRIS)))
    return svg(PW, PH, L)

def post_proceso():
    L = [layer("FONDO", f'<rect width="{PW}" height="{PH}" fill="{NEGRO}"/>'),
         layer("PLIEGO", f'<rect x="40" y="40" width="{PW-80}" height="{PH-80}" fill="{BLANCO}"/>'),
         layer("CABECERA", cabecera(PW, "02.1", y=100))]
    L.append(layer("TITULO_GLITCH", glitch("PROCESO", 70, 1010, 370, 250,
                                           [(150, 240, 0), (240, 262, -26), (262, 312, 16), (312, 330, -8), (330, 400, 0)], "pc")))
    iw = 455
    L.append(layer("OBRAS_1BIT", image(png_uri(trama_1bit(foto("2026-05"), iw, 540)), 60, 430, iw, 540)
                   + image(png_uri(trama_1bit(foto("2026-09"), iw, 540)), 60 + iw + 50, 430, iw, 540)))
    txt = ["Trabajo desde el gesto. Muchas de mis piezas empiezan sin",
           "una idea fija: la obra se va armando mientras la hago, y el",
           "movimiento de la mano decide tanto como yo."]
    L.append(layer("TEXTO", T(60, 1048, "Desde el gesto", w=700, size=34, fill=NEGRO)
                   + "".join(T(60, 1094 + i * 30, t, size=22, fill=NEGRO) for i, t in enumerate(txt))
                   + T(60, 1002, "fig. a — 2026-05     fig. b — 2026-09", fam="Plex", size=14, fill=GRIS)))
    L.append(layer("PIE", hline(60, 1246, 1020) + T(60, 1282, IG, fam="Plex", size=16, fill=GRIS)
                   + T(1020, 1282, "(02) proceso", fam="Plex", size=16, fill=GRIS, anchor="end")))
    return svg(PW, PH, L)

def post_cita():
    L = [layer("FONDO", f'<rect width="{PW}" height="{PH}" fill="{PAPEL}"/>'),
         layer("TINTA_ESQUINA", image(png_uri(tinta_sola(cover(foto("2026-09"), PW, 520, fy=0.55), umbral=115)), 0, 830, PW, 520))]
    L.append(layer("CABECERA", cabecera(PW, "“ ”", fill=TINTA)))
    y = 270
    q = []
    for linea in CITA:
        q.append(T(60, y, linea, fam="Bricolage", w=800, size=82, fill=TINTA, ls=-2)); y += 92
    q.append(T(56, y + 110, "añoranza.", fam="Fraktur", size=190, fill=ROSA_HONDO))
    L.append(layer("CITA", "\n".join(q)))
    L.append(layer("FIRMA", f'<rect x="40" y="1250" width="560" height="70" fill="{PAPEL}"/>'
                   + T(60, 1296, "— Patricia Díaz, statement 2026", fam="Plex", w=500, size=18, fill=TINTA)))
    return svg(PW, PH, L)


# =================== CARRUSEL PANORÁMICO 3 x 1080 ===================
CW = PW * 3

def carrusel():
    L = [layer("FONDO", f'<rect width="{CW}" height="{PH}" fill="{BLANCO}"/>')]
    obra = cover(foto("2026-09"), CW, 760, fy=0.5)
    L.append(layer("OBRA_PANORAMICA", image(jpg_uri(obra), 0, 430, CW, 760)))
    L.append(layer("TITULO", estirado("OBRA 2026", 60, 1020 + 1080 - 60, 360, 300)))
    marcas = []
    for i in range(3):
        x = i * PW
        marcas.append(T(x + 60, 86, NOMBRE if i == 0 else "", w=700, size=28, fill=NEGRO))
        marcas.append(T(x + PW - 60, 86, f"{i+1}/3", size=28, fill=NEGRO, anchor="end"))
        marcas.append(hline(x + 60, 108, x + PW - 60))
    L.append(layer("MARCAS_SLIDES", "\n".join(marcas)))
    lado = [T(2 * PW + 60, 220, "(01—10)", w=700, size=64, fill=NEGRO),
            T(2 * PW + 60, 270, "Tinta, aerosol, carboncillo,", size=26, fill=NEGRO),
            T(2 * PW + 60, 304, "mallas y medias.", size=26, fill=NEGRO),
            T(2 * PW + 60, 338, "Negro sobre blanco.", size=26, fill=NEGRO)]
    L.append(layer("TEXTO_SLIDE3", "\n".join(lado)))
    pie = [hline(60, 1240, CW - 60),
           T(60, 1280, "fig. 2026-09 — goteo horizontal", fam="Plex", size=16, fill=GRIS),
           T(PW + 60, 1280, "desliza →", fam="Plex", w=500, size=16, fill=NEGRO),
           T(CW - 60, 1280, IG, fam="Plex", size=16, fill=GRIS, anchor="end")]
    L.append(layer("PIE", "\n".join(pie)))
    guias = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{PH}" stroke="{ROSA}" stroke-width="2" stroke-dasharray="10 8"/>' for x in (PW, 2 * PW))
    L.append(layer("GUIAS_CORTE_borrar_antes_de_exportar", guias))
    return svg(CW, PH, L)


# =================== STORIES 1080 x 1920 ===================
SW, SH = 1080, 1920

def story_expo():
    L = [layer("FONDO", f'<rect width="{SW}" height="{SH}" fill="{NEGRO}"/>'),
         layer("PLIEGO", f'<rect x="40" y="200" width="{SW-80}" height="{SH-420}" fill="{BLANCO}"/>'),
         layer("CABECERA", cabecera(SW, "11.12.26", y=270))]
    L.append(layer("TITULO_GASA", estirado("GASA", 70, 1010, 560, 290)))
    L.append(layer("TITULO_NEGRA_GLITCH", glitch("NEGRA", 70, 1010, 830, 290,
                                                 [(590, 680, 0), (680, 704, -30), (704, 760, 18), (760, 778, -10), (778, 860, 0)], "sg")))
    L.append(layer("OBRA_1BIT", image(png_uri(trama_1bit(foto("2026-08"), 960, 420)), 60, 880, 960, 420)))
    info = [T(60, 1370, "Viernes 11 de diciembre · 7—11 pm", w=700, size=38, fill=NEGRO),
            T(60, 1418, "El Local · Calle Cerra, Santurce", size=30, fill=NEGRO),
            T(60, 1458, "Entrada libre", size=30, fill=NEGRO),
            T(60, 1660, "zona segura: no pongas texto debajo de esta línea", fam="Plex", size=13, fill=HAIR)]
    L.append(layer("INFO", "\n".join(info)))
    L.append(layer("ESPACIO_STICKER_ENLACE", f'<rect x="300" y="1520" width="480" height="96" rx="48" fill="none" stroke="{GRIS}" stroke-dasharray="8 8"/>'
                   + T(540, 1578, "sticker de enlace aquí", fam="Plex", size=18, fill=GRIS, anchor="middle")))
    L.append(layer("PIE", T(SW / 2, 1810, IG, fam="Plex", size=20, fill=BLANCO, anchor="middle")))
    return svg(SW, SH, L)

def story_obra_nueva():
    L = [layer("FONDO", f'<rect width="{SW}" height="{SH}" fill="{BLANCO}"/>'),
         layer("FOTO_OBRA", image(jpg_uri(cover(foto("2026-10"), SW, SH, fy=0.5)), 0, 0, SW, SH))]
    L.append(layer("ETIQUETA", f'<rect x="0" y="230" width="{SW}" height="150" fill="{BLANCO}"/>'
                   + estirado("OBRA NUEVA", 60, 1020, 350, 120)))
    L.append(layer("FICHA", f'<rect x="0" y="1360" width="{SW}" height="170" fill="{BLANCO}"/>'
                   + T(60, 1420, "2026-10 — manchas diagonales", w=700, size=34, fill=NEGRO)
                   + T(60, 1464, "Acrílico negro, brocha seca", size=24, fill=NEGRO)
                   + T(1020, 1464, IG, fam="Plex", size=16, fill=GRIS, anchor="end")))
    L.append(layer("ESPACIO_ENCUESTA", f'<rect x="140" y="1560" width="800" height="150" rx="24" fill="{BLANCO}" stroke="{NEGRO}" stroke-dasharray="8 8"/>'
                   + T(540, 1630, "¿Qué título le pondrías?", w=700, size=30, fill=NEGRO, anchor="middle")
                   + T(540, 1672, "(pon aquí el sticker de pregunta)", fam="Plex", size=16, fill=GRIS, anchor="middle")))
    return svg(SW, SH, L)

DESTACADOS = [("01", "OBRAS"), ("02", "PROCESO"), ("03", "EXPOS"), ("04", "TEXTIL"), ("05", "CONTACTO")]

def portada(n, palabra):
    L = [layer("FONDO", f'<rect width="{SW}" height="{SH}" fill="{NEGRO}"/>')]
    L.append(layer("GUIA_CIRCULO_borrar", f'<circle cx="540" cy="960" r="430" fill="none" stroke="#333" stroke-width="2" stroke-dasharray="10 10"/>'))
    L.append(layer("NUMERO", T(540, 1010, f"({n})", w=700, size=230, fill=BLANCO, anchor="middle", ls=-6)))
    L.append(layer("PALABRA", T(540, 1120, palabra, fam="Plex", w=500, size=58, fill=BLANCO, anchor="middle", ls=4)))
    if palabra == "EXPOS":
        L.append(layer("PUNTO_ROSA", f'<circle cx="540" cy="760" r="18" fill="{ROSA}"/>'))
    return svg(SW, SH, L)


# =================== render ===================
def render(items):
    from playwright.sync_api import sync_playwright
    from psd_tools import PSDImage
    from psd_tools.api.layers import PixelLayer
    for d in ("preview", "photoshop"):
        (HERE / d).mkdir(exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        for name, (w, h, path) in items.items():
            src = path.read_text()
            pg = b.new_page(viewport={"width": w, "height": h})
            pg.set_content(f'<html><body style="margin:0;background:transparent">{src.split("?>",1)[1]}</body></html>')
            pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
            # vista previa sin las guías
            pg.evaluate("document.querySelectorAll('svg > g').forEach(g => g.style.visibility = g.id.includes('borrar') ? 'hidden' : 'visible')")
            prev = Image.open(io.BytesIO(pg.screenshot())).convert("RGB")
            prev.save(HERE / "preview" / f"{name}.png")
            if w == CW:
                for i in range(3):
                    prev.crop((i * PW, 0, (i + 1) * PW, PH)).save(HERE / "preview" / f"{name}_slide{i+1}.png")
            psd = PSDImage.new("RGB", (w, h))
            for lid in re.findall(r'^<g id="([^"]+)">', src, re.M):
                pg.evaluate("""id => document.querySelectorAll('svg > g').forEach(g =>
                    g.style.visibility = g.id === id ? 'visible' : 'hidden')""", lid)
                im = Image.open(io.BytesIO(pg.screenshot(omit_background=True))).convert("RGBA")
                box = im.getbbox()
                if box:
                    lay = PixelLayer.frompil(im.crop(box), psd, lid, top=box[1], left=box[0])
                    if "borrar" in lid:
                        lay.visible = False
                    psd.append(lay)
            psd.save(str(HERE / "photoshop" / f"{name}.psd"))
            pg.close()
            print("ok", name)
        b.close()


def feed_mockup():
    """Perfil de Instagram simulado con 9 posts (solo vista previa)."""
    pv, fl = HERE / "preview", HERE.parent / "08-flyers" / "preview"
    orden = [pv / "post_01_obra.png", fl / "01_gasa-negra_el-local.png", pv / "post_04_cita.png",
             pv / "carrusel_obra-2026_slide1.png", pv / "post_03_proceso.png", fl / "02_malla_colectiva-dj.png",
             pv / "post_02_disponible.png", fl / "03_lo-que-queda-de-la-mano_galeria-hollin.png", fl / "04_estudio-abierto_trama.png"]
    cw, ch, gap, top = 360, 450, 4, 330
    m = Image.new("RGB", (cw * 3 + gap * 2, top + ch * 3 + gap * 2), "white")
    from PIL import ImageDraw, ImageFont
    d = ImageDraw.Draw(m)
    F = lambda n, s: ImageFont.truetype(str(HERE.parent / "08-flyers" / "fonts" / n), s)
    d.ellipse((30, 40, 190, 200), fill=(13, 13, 13))
    d.text((110, 120), "PD", font=F("Arimo-700.ttf", 56), fill="white", anchor="mm")
    d.text((230, 60), IG, font=F("Arimo-700.ttf", 26), fill="black")
    for i, (num, lab) in enumerate([("15", "posts"), ("396", "seguidores"), ("0", "seguidos")]):
        d.text((230 + i * 170, 110), num, font=F("Arimo-700.ttf", 28), fill="black")
        d.text((230 + i * 170, 146), lab, font=F("Arimo-400.ttf", 20), fill="black")
    for i, t in enumerate([NOMBRE + " · artista", "Material Research. / Textile Systems.", "Caguas, Puerto Rico"]):
        d.text((30, 230 + i * 28), t, font=F("Arimo-700.ttf" if i == 0 else "Arimo-400.ttf", 22), fill="black")
    for i, p in enumerate(orden):
        im = Image.open(p).convert("RGB").resize((cw, ch), Image.LANCZOS)
        m.paste(im, ((i % 3) * (cw + gap), top + (i // 3) * (ch + gap)))
    m.save(HERE / "feed_mockup.png")


PIEZAS = {
    "post_01_obra": (PW, PH, post_obra),
    "post_02_disponible": (PW, PH, post_disponible),
    "post_03_proceso": (PW, PH, post_proceso),
    "post_04_cita": (PW, PH, post_cita),
    "carrusel_obra-2026": (CW, PH, carrusel),
    "story_01_expo": (SW, SH, story_expo),
    "story_02_obra-nueva": (SW, SH, story_obra_nueva),
}
for n, w in DESTACADOS:
    PIEZAS[f"destacado_{n}_{w.lower()}"] = (SW, SH, (lambda n=n, w=w: portada(n, w)))

if __name__ == "__main__":
    out = HERE / "illustrator"; out.mkdir(exist_ok=True)
    items = {}
    for name, (w, h, fn) in PIEZAS.items():
        p = out / f"{name}.svg"; p.write_text(fn()); items[name] = (w, h, p)
    render(items)
    feed_mockup()
