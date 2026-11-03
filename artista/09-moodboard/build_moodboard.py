"""Mood board de Patricia alrededor de la web (Archivo y Archivo en vivo).
  moodboard_patricia.svg -> Illustrator (texto editable, cada bloque es un grupo con nombre)
  moodboard_patricia.psd -> Photoshop (una capa por bloque)
  moodboard_patricia.png -> vista previa
Uso: python3 build_moodboard.py   (usa las capturas de capturas/ y los ayudantes de 08-flyers)
"""
import io, sys
from pathlib import Path
from PIL import Image

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "08-flyers"))
from build_flyers import (T, tw, layer, image, cover, foto, trama_1bit, tinta_sola, pintura,
                          png_uri, jpg_uri, PAPEL, TINTA, ROSA, ROSA_HONDO, ROJO, ROSA_LUZ,
                          HAIR, GRIS, NEGRO, BLANCO, IG)

W, H = 3000, 2000
CAP = HERE / "capturas"
FLY = HERE.parent / "08-flyers" / "preview"
REF = HERE.parent / "03-identidad-visual" / "referencias"


def cap(name, w):
    im = Image.open(CAP / f"{name}.png").convert("RGB")
    h = round(im.height * w / im.width)
    return im.resize((w, h), Image.LANCZOS), h

def etiqueta(x, y, n, txt, sub=""):
    out = [T(x, y, n, fam="Plex", w=500, size=15, fill=NEGRO),
           T(x + 46, y, txt, fam="Plex", w=500, size=15, fill=NEGRO)]
    if sub:
        out.append(T(x + 46, y + 22, sub, fam="Plex", size=13, fill=GRIS))
    return "\n".join(out)

def titulo_bloque(x, y, w, n, txt):
    return "\n".join([f'<line x1="{x}" y1="{y}" x2="{x+w}" y2="{y}" stroke="{NEGRO}" stroke-width="2"/>',
                      T(x, y + 34, f"({n})", w=700, size=26, fill=NEGRO),
                      T(x + 62, y + 34, txt, w=700, size=26, fill=NEGRO)])

def foto_con_borde(uri, x, y, w, h):
    return image(uri, x, y, w, h) + f'\n<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{NEGRO}" stroke-width="1"/>'


def moodboard():
    L = [layer("FONDO", f'<rect width="{W}" height="{H}" fill="{BLANCO}"/>')]

    # ---------- cabecera ----------
    cab = [T(80, 150, "Patricia Díaz", w=700, size=96, fill=NEGRO, ls=-2),
           T(80 + tw("Patricia Díaz", "Arimo", 700, 96, -2) + 24, 150, "(mood board)", w=400, size=96, fill=NEGRO, ls=-2),
           T(W - 80, 104, "ARCHIVO · ARCHIVO EN VIVO · FLYERS", fam="Plex", w=500, size=18, fill=NEGRO, anchor="end", ls=1.5),
           T(W - 80, 132, "Caguas, Puerto Rico — noviembre 2026", fam="Plex", size=18, fill=GRIS, anchor="end"),
           T(W - 80, 160, IG, fam="Plex", size=18, fill=GRIS, anchor="end"),
           f'<line x1="80" y1="190" x2="{W-80}" y2="190" stroke="{NEGRO}" stroke-width="3"/>']
    L.append(layer("CABECERA", "\n".join(cab)))

    # ---------- columna A: la web ----------
    ax, aw = 80, 1100
    web = [titulo_bloque(ax, 230, aw, "01", "La web: un libro escaneado")]
    im, h = cap("archivo_1", aw)
    web.append(foto_con_borde(jpg_uri(im), ax, 290, aw, h)); y = 290 + h + 30
    web.append(etiqueta(ax, y, "01", "Archivo — portada", "nombre en cascada cortada y pixelada; índice como libro")); y += 64
    third = (aw - 2 * 30) // 3
    filas = [[("archivo_3", "03", "Obras en 1 bit", "color al pasar el cursor"),
              ("vivo_1", "04", "Archivo en vivo", "pintura rosa, letras al ritmo"),
              ("archivo_4", "05", "Contacto (Loïc)", "palabra gigante estirada")],
             [("archivo_2", "06", "Proceso", "gesto → caos → añoranza"),
              ("vivo_2", "07", "Proceso en vivo", "trazos encima del texto"),
              ("vivo_3", "08", "Obras en vivo", "destello al pasar")]]
    for fila in filas:
        hs = []
        for i, (n, num, t1, t2) in enumerate(fila):
            im, h = cap(n, third); hs.append(h)
            x = ax + i * (third + 30)
            web.append(foto_con_borde(jpg_uri(im), x, y, third, h))
            web.append(etiqueta(x, y + h + 30, num, t1, t2))
        y += max(hs) + 92
    L.append(layer("WEB_CAPTURAS", "\n".join(web)))

    # ---------- columna B: tipografía + texturas ----------
    bx, bw = 1240, 700
    ty = [titulo_bloque(bx, 230, bw, "02", "Tipografía")]
    fuentes = [("Arimo", 700, "Patricia Díaz", "Arimo Bold — titulares de la web y flyers", 64),
               ("Fraktur", 400, "Malla", "UnifrakturMaguntia — una letra gótica que interrumpe", 64),
               ("Unbounded", 800, "LO QUE QUEDA", "Unbounded ExtraBold — títulos de la guía", 50),
               ("Bricolage", 600, "Gesto, caos, añoranza", "Bricolage Grotesque — textos y fichas", 44),
               ("Plex", 500, "11.12.26  EL LOCAL", "IBM Plex Mono — fechas, datos, etiquetas", 36)]
    y = 340
    for fam, w, muestra, nota, size in fuentes:
        ty.append(T(bx, y, muestra, fam=fam, w=w, size=size, fill=NEGRO))
        ty.append(T(bx, y + 30, nota, fam="Plex", size=14, fill=GRIS))
        ty.append(f'<line x1="{bx}" y1="{y+48}" x2="{bx+bw}" y2="{y+48}" stroke="{HAIR}" stroke-width="1"/>')
        y += 118
    L.append(layer("TIPOGRAFIA", "\n".join(ty)))

    tx = [titulo_bloque(bx, 940, bw, "03", "Texturas")]
    s = (bw - 30) // 2; y0 = 1000
    # 1. trama de 1 bit
    tx.append(image(png_uri(trama_1bit(foto("2026-08"), s, s)), bx, y0, s, s))
    # 2. nombre cortado y desplazado (glitch)
    defs, g = [], []
    for i, (ya, yb, dx) in enumerate([(0, 60, 0), (60, 90, -30), (90, 150, 20), (150, 175, -12), (175, s, 0)]):
        defs.append(f'<clipPath id="mbc{i}"><rect x="{bx+s+30}" y="{y0+ya}" width="{s}" height="{yb-ya}"/></clipPath>')
        g.append(f'<g clip-path="url(#mbc{i})"><g transform="translate({dx},0)">'
                 + "".join(T(bx + s + 30, y0 + 120 + k * 92, "Patricia", w=700, size=110, fill=NEGRO, ls=-4) for k in range(4))
                 + "</g></g>")
    tx.append(f'<rect x="{bx+s+30}" y="{y0}" width="{s}" height="{s}" fill="none" stroke="{HAIR}"/>')
    defs.append(f'<clipPath id="mbtile"><rect x="{bx+s+30}" y="{y0}" width="{s}" height="{s}"/></clipPath>')
    tx.append("<defs>" + "".join(defs) + "</defs>" + '<g clip-path="url(#mbtile)">' + "".join(g) + "</g>")
    # 3. pintura rosa
    y1 = y0 + s + 60
    tx.append(f'<g><rect x="{bx}" y="{y1}" width="{s}" height="{s}" fill="{BLANCO}" stroke="{HAIR}"/>'
              + pintura(11, [(bx + 20, y1 + 120, bx + s - 20, y1 + 60, 90), (bx + 40, y1 + 260, bx + s, y1 + 220, 60)],
                        salpicaduras=24, zona=(bx + 10, y1 + 10, s - 20, s - 20)) + "</g>")
    # 4. tinta sola
    tx.append(image(png_uri(tinta_sola(cover(foto("2026-02"), s, s), umbral=120)), bx + s + 30, y1, s, s))
    tx.append(f'<rect x="{bx+s+30}" y="{y1}" width="{s}" height="{s}" fill="none" stroke="{HAIR}"/>')
    for (x, yy, n, t) in [(bx, y0 + s + 28, "a", "trama de puntos, 1 bit"), (bx + s + 30, y0 + s + 28, "b", "texto cortado en bandas"),
                          (bx, y1 + s + 28, "c", "pintura rosa con brillo"), (bx + s + 30, y1 + s + 28, "d", "tinta sola, sin fondo")]:
        tx.append(T(x, yy, f"({n}) {t}", fam="Plex", size=14, fill=GRIS))
    L.append(layer("TEXTURAS", "\n".join(tx)))

    # ---------- columna C: color, obras + teléfono, flyers ----------
    cx, cw = 2000, 920
    co = [titulo_bloque(cx, 230, cw, "04", "Color: negro sobre blanco, un solo acento")]
    sw = [("Blanco", BLANCO, "#FFFFFF"), ("Papel", PAPEL, "#F2EEE8"), ("Tinta", TINTA, "#171515"),
          ("Rosa", ROSA, "#E0508C"), ("Rosa hondo", ROSA_HONDO, "#B0195C"), ("Rojo", ROJO, "#A8141E")]
    sw_w = (cw - 5 * 16) / 6
    for i, (n, c, hx) in enumerate(sw):
        x = cx + i * (sw_w + 16)
        co.append(f'<rect x="{x:.1f}" y="290" width="{sw_w:.1f}" height="150" fill="{c}" stroke="{NEGRO}" stroke-width="1"/>')
        co.append(T(x, 466, n, w=700, size=17, fill=NEGRO))
        co.append(T(x, 488, hx, fam="Plex", size=14, fill=GRIS))
    # barra de proporción 70 / 22 / 6 / 2
    x = cx
    for frac, c, lab, fc in [(.70, BLANCO, "70% blanco", NEGRO), (.22, TINTA, "22%", BLANCO), (.06, ROSA, "6%", NEGRO), (.02, ROJO, "", BLANCO)]:
        co.append(f'<rect x="{x:.1f}" y="516" width="{cw*frac:.1f}" height="40" fill="{c}" stroke="{NEGRO}" stroke-width="1"/>')
        if lab:
            co.append(T(x + 10, 542, lab, fam="Plex", w=500, size=14, fill=fc))
        x += cw * frac
    co.append(T(cx, 584, "Rosa o rojo, nunca los dos en la misma pieza.", fam="Plex", size=14, fill=GRIS))
    L.append(layer("COLOR", "\n".join(co)))

    ob = [titulo_bloque(cx, 630, cw, "05", "Obras + la web en el teléfono")]
    ph_w = 300
    im, ph_h = cap("archivo_movil", ph_w)
    ph_h = min(ph_h, 610)
    ob.append(f'<rect x="{cx-10}" y="680" width="{ph_w+20}" height="{ph_h+20}" rx="34" fill="{NEGRO}"/>')
    ob.append(f'<clipPath id="tel"><rect x="{cx}" y="690" width="{ph_w}" height="{ph_h}" rx="26"/></clipPath>')
    ob.append(f'<g clip-path="url(#tel)">' + image(jpg_uri(im), cx, 690, ph_w, round(im.height)) + "</g>")
    gx = cx + ph_w + 40; gw = cw - ph_w - 40
    codes = ["2026-02", "2026-03", "2026-04", "2026-05", "2026-07", "2026-09"]
    tw_, th_ = (gw - 2 * 14) / 3, 0
    th_ = (ph_h + 20 - 14 - 2 * 26) / 2
    for i, c in enumerate(codes):
        x = gx + (i % 3) * (tw_ + 14); yy = 680 + (i // 3) * (th_ + 14 + 26)
        ob.append(foto_con_borde(jpg_uri(cover(foto(c), int(tw_), int(th_))), round(x), round(yy), int(tw_), int(th_)))
        ob.append(T(x, yy + th_ + 18, c, fam="Plex", size=13, fill=GRIS))
    L.append(layer("OBRAS_Y_TELEFONO", "\n".join(ob)))

    fl = [titulo_bloque(cx, 1350, cw, "06", "Flyers")]
    fw = (cw - 3 * 16) / 4; fh = fw * 1350 / 1080
    for i, f in enumerate(sorted(FLY.glob("*.png"))):
        x = cx + i * (fw + 16)
        im = Image.open(f).convert("RGB").resize((int(fw * 2), int(fh * 2)), Image.LANCZOS)
        fl.append(foto_con_borde(jpg_uri(im), round(x), 1410, int(fw), int(fh)))
        fl.append(T(x, 1410 + fh + 22, f.stem.split("_")[1].replace("-", " "), fam="Plex", size=13, fill=GRIS))
    L.append(layer("FLYERS", "\n".join(fl)))

    # ---------- banda de abajo: palabras + referencias ----------
    by = 1790
    pal = [f'<line x1="80" y1="{by}" x2="{W-80}" y2="{by}" stroke="{NEGRO}" stroke-width="3"/>',
           T(80, by + 96, "gesto", w=700, size=84, fill=NEGRO, ls=-2),
           T(80 + tw("gesto ", "Arimo", 700, 84), by + 96, "→ caos →", w=400, size=84, fill=NEGRO, ls=-2),
           T(80 + tw("gesto → caos → ", "Arimo", 700, 84), by + 96, "añoranza", fam="Fraktur", size=92, fill=ROSA_HONDO),
           T(80, by + 150, "gasa · malla · imperdibles · tachas · encaje · tinta · aerosol · carboncillo", fam="Plex", w=500, size=20, fill=NEGRO)]
    L.append(layer("PALABRAS", "\n".join(pal)))

    rx = 1960
    gif = Image.open(REF / "aeforia_transition.gif"); gif.seek(min(120, gif.n_frames - 1))
    refs = [T(rx, by + 40, "REFERENCIAS", fam="Plex", w=700, size=15, fill=NEGRO, ls=2)]
    for i, r in enumerate(["libro escaneado con glitch — “(05) Epíleg”",
                           "página de contacto de Loïc Dupasquier",
                           "afiche de gira de DJ con pintura rosa (Pinterest)",
                           "“Space Exists in Object” — collage",
                           "aeforia — transición (GIF)"]):
        refs.append(T(rx, by + 72 + i * 24, f"— {r}", fam="Plex", size=15, fill=GRIS))
    refs.append(foto_con_borde(jpg_uri(gif.convert("RGB").resize((240, 180))), W - 80 - 200, by + 22, 200, 150))
    L.append(layer("REFERENCIAS", "\n".join(refs)))

    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n'
            + "\n".join(L) + "\n</svg>\n")


def render(svg_path):
    import re
    from playwright.sync_api import sync_playwright
    from psd_tools import PSDImage
    from psd_tools.api.layers import PixelLayer
    src = svg_path.read_text()
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        pg = b.new_page(viewport={"width": W, "height": H})
        pg.set_content(f'<html><body style="margin:0;background:transparent">{src.split("?>",1)[1]}</body></html>')
        pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500)
        pg.screenshot(path=str(HERE / "moodboard_patricia.png"))
        psd = PSDImage.new("RGB", (W, H))
        for lid in re.findall(r'^<g id="([^"]+)">', src, re.M):
            pg.evaluate("""id => document.querySelectorAll('svg > g').forEach(g =>
                g.style.visibility = g.id === id ? 'visible' : 'hidden')""", lid)
            im = Image.open(io.BytesIO(pg.screenshot(omit_background=True))).convert("RGBA")
            box = im.getbbox()
            if box:
                psd.append(PixelLayer.frompil(im.crop(box), psd, lid, top=box[1], left=box[0]))
        psd.save(str(HERE / "moodboard_patricia.psd"))
        b.close()


if __name__ == "__main__":
    out = HERE / "moodboard_patricia.svg"
    out.write_text(moodboard())
    render(out)
    print("listo:", out)
