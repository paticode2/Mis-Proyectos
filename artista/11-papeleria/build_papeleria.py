"""Papelería de Patricia: tarjetas de presentación, membrete, factura/cotización y firma de email.
  illustrator/*.svg -> Illustrator (tamaño real en pulgadas, texto editable, grupos con nombre)
  imprenta/*.pdf    -> PDF para imprimir (tarjetas con sangrado de 0.125", frente y dorso)
  preview/*.png     -> vista previa
  firma_email.html  -> firma para pegar en Gmail
Unidades: puntos (72 pt = 1 pulgada). Uso: python3 build_papeleria.py
"""
import sys
from pathlib import Path
from PIL import Image

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "08-flyers"))
from build_flyers import (T, tw, layer, image, cover, foto, trama_1bit, tinta_sola, pintura,
                          png_uri, jpg_uri, PAPEL, TINTA, ROSA, ROSA_HONDO, ROJO,
                          HAIR, GRIS, NEGRO, BLANCO, IG)

NOMBRE = "Patricia Díaz"
OFICIO = "artista visual"
LUGAR = "Caguas, Puerto Rico"
LLC = "[Nombre de la LLC]"

# ---- tarjeta 3.5 x 2 in + sangrado 0.125 in ----
B = 9                      # sangrado (pt)
CW, CH = 252 + 2 * B, 144 + 2 * B   # 270 x 162 pt = 3.75 x 2.25 in
S = B + 12                 # margen seguro (0.167 in dentro del corte)


def svg(w_pt, h_pt, layers):
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{w_pt/72:.4f}in" height="{h_pt/72:.4f}in" viewBox="0 0 {w_pt} {h_pt}">\n'
            + "\n".join(layers) + "\n</svg>\n")

def guias_tarjeta():
    return layer("GUIAS_borrar",
                 f'<rect x="{B}" y="{B}" width="252" height="144" fill="none" stroke="{ROSA}" stroke-width="0.5"/>'
                 f'<rect x="{S}" y="{S}" width="{CW-2*S}" height="{CH-2*S}" fill="none" stroke="#3FA9F5" stroke-width="0.4" stroke-dasharray="2 2"/>')

def estirado(txt, x0, x1, y, size, fill=NEGRO, fam="Arimo", w=700):
    sx = (x1 - x0) / tw(txt, fam, w, size)
    return f'<g transform="translate({x0},{y}) scale({sx:.4f},1)">{T(0, 0, txt, fam=fam, w=w, size=size, fill=fill)}</g>'

def glitch(txt, x0, x1, y, size, cortes, pref, fill=NEGRO):
    defs, g = [], []
    for i, (ya, yb, dx) in enumerate(cortes):
        defs.append(f'<clipPath id="{pref}{i}"><rect x="0" y="{ya}" width="2000" height="{yb-ya}"/></clipPath>')
        g.append(f'<g clip-path="url(#{pref}{i})"><g transform="translate({dx},0)">{estirado(txt, x0, x1, y, size, fill)}</g></g>')
    return "<defs>" + "".join(defs) + "</defs>" + "".join(g)

def linea_correo(x, y, fill=NEGRO, fam="Plex", size=6.5, largo=110):
    """'correo' con una línea en blanco para escribirlo después."""
    return (T(x, y, "correo", fam=fam, size=size, fill=fill)
            + f'<line x1="{x + 30}" y1="{y + 1}" x2="{x + 30 + largo}" y2="{y + 1}" stroke="{fill}" stroke-width="0.4"/>')


# ================= TARJETA A — ARCHIVO =================
def tarjeta_a_frente():
    L = [layer("FONDO", f'<rect width="{CW}" height="{CH}" fill="{BLANCO}"/>')]
    L.append(layer("CABECERA", T(S, S + 7, "(01)", size=6.5, fill=NEGRO) + T(CW - S, S + 7, "obra 2026", size=6.5, fill=NEGRO, anchor="end")
                   + f'<line x1="{S}" y1="{S+11}" x2="{CW-S}" y2="{S+11}" stroke="{NEGRO}" stroke-width="0.5"/>'))
    L.append(layer("NOMBRE_GLITCH", glitch(NOMBRE, S, CW - S, 104, 40,
                                           [(60, 80, 0), (80, 86, -5), (86, 96, 3), (96, 100, -2), (100, 110, 0)], "ta")))
    L.append(layer("PIE", f'<line x1="{S}" y1="{CH-S-11}" x2="{CW-S}" y2="{CH-S-11}" stroke="{NEGRO}" stroke-width="0.5"/>'
                   + T(S, CH - S, OFICIO, size=6.5, fill=NEGRO) + T(CW - S, CH - S, LUGAR, size=6.5, fill=NEGRO, anchor="end")))
    L.append(guias_tarjeta())
    return svg(CW, CH, L)

def tarjeta_a_dorso():
    L = [layer("FONDO", f'<rect width="{CW}" height="{CH}" fill="{NEGRO}"/>')]
    iw = 120
    L.append(layer("OBRA_1BIT", f'<rect x="{CW-iw-B}" y="0" width="{iw+B}" height="{CH}" fill="{BLANCO}"/>'
                   + image(png_uri(trama_1bit(foto("2026-08"), (iw + B) * 4, CH * 4)), CW - iw - B, 0, iw + B, CH)))
    info = [T(S, S + 14, NOMBRE, w=700, size=12, fill=BLANCO),
            T(S, S + 25, OFICIO, size=7, fill=BLANCO),
            T(S, CH - S - 26, IG, fam="Plex", size=6.5, fill=BLANCO),
            linea_correo(S, CH - S - 14, fill=BLANCO, largo=72),
            T(S, CH - S - 2, LUGAR, fam="Plex", size=6.5, fill=BLANCO)]
    L.append(layer("CONTACTO", "\n".join(info)))
    L.append(guias_tarjeta())
    return svg(CW, CH, L)


# ================= TARJETA B — TINTA (papel + un acento rojo) =================
def tarjeta_b_frente():
    L = [layer("FONDO", f'<rect width="{CW}" height="{CH}" fill="{PAPEL}"/>')]
    L.append(layer("TINTA_2026-02", image(png_uri(tinta_sola(cover((lambda im: im.crop((int(im.width*.09), int(im.height*.06), int(im.width*.90), int(im.height*.97))))(foto("2026-02")), 1080, 648), umbral=120)), 0, 0, CW, CH)))
    L.append(layer("NOMBRE", f'<rect x="{S-4}" y="{CH-S-30}" width="{tw(NOMBRE,"Unbounded",800,15,-0.4)+8:.1f}" height="34" fill="{PAPEL}"/>'
                   + T(S, CH - S - 12, NOMBRE, fam="Unbounded", w=800, size=15, fill=TINTA, ls=-0.4)
                   + T(S, CH - S, OFICIO, fam="Bricolage", size=7, fill=TINTA)))
    L.append(guias_tarjeta())
    return svg(CW, CH, L)

def tarjeta_b_dorso():
    L = [layer("FONDO", f'<rect width="{CW}" height="{CH}" fill="{PAPEL}"/>')]
    info = [T(S, S + 16, NOMBRE, fam="Unbounded", w=800, size=13, fill=TINTA, ls=-0.3),
            T(S, S + 28, "gesto · caos · añoranza", fam="Bricolage", size=7.5, fill=TINTA),
            f'<rect x="{S}" y="{S+38}" width="18" height="2.5" fill="{ROJO}"/>',
            T(S, CH - S - 26, IG, fam="Plex", size=6.5, fill=TINTA),
            linea_correo(S, CH - S - 14, fill=TINTA),
            T(S, CH - S - 2, LUGAR, fam="Plex", size=6.5, fill=TINTA)]
    L.append(layer("CONTACTO", "\n".join(info)))
    L.append(guias_tarjeta())
    return svg(CW, CH, L)


# ================= TARJETA C — ROSA (pintura + gótica) =================
def tarjeta_c_frente():
    L = [layer("FONDO", f'<rect width="{CW}" height="{CH}" fill="{NEGRO}"/>')]
    L.append(layer("PINTURA_ROSA", pintura(21, [(-5, 95, 280, 60, 40), (90, 34, 285, 18, 14)],
                                           salpicaduras=14, zona=(10, 10, CW - 20, 100))))
    # Patricia en Arimo + la D de Díaz en gótica
    size = 30
    x = S
    nom = T(x, 86, "Patricia", w=700, size=size, fill=BLANCO)
    x2 = x + tw("Patricia ", "Arimo", 700, size)
    nom += T(x2, 86, "D", fam="Fraktur", size=size + 4, fill=BLANCO)
    nom += T(x2 + tw("D", "UnifrakturMaguntia", 400, size + 4), 86, "íaz", w=700, size=size, fill=BLANCO)
    L.append(layer("NOMBRE", nom))
    L.append(layer("OFICIO", T(S, CH - S, f"{OFICIO} — {LUGAR}", fam="Plex", size=6.5, fill=BLANCO)))
    L.append(guias_tarjeta())
    return svg(CW, CH, L)

def tarjeta_c_dorso():
    L = [layer("FONDO", f'<rect width="{CW}" height="{CH}" fill="{BLANCO}"/>')]
    info = [T(S, S + 14, NOMBRE, w=700, size=12, fill=NEGRO),
            T(S, S + 25, OFICIO, size=7, fill=NEGRO),
            f'<circle cx="{CW-S-5}" cy="{S+5}" r="5" fill="{ROSA}"/>',
            T(S, CH - S - 26, IG, fam="Plex", size=6.5, fill=NEGRO),
            linea_correo(S, CH - S - 14),
            T(S, CH - S - 2, LUGAR, fam="Plex", size=6.5, fill=NEGRO)]
    L.append(layer("CONTACTO", "\n".join(info)))
    L.append(guias_tarjeta())
    return svg(CW, CH, L)


# ================= MEMBRETE (carta 8.5 x 11) =================
LW, LH = 612, 792
M = 54  # 0.75 in

def encabezado(titulo_doc=None):
    out = [T(M, M + 22, NOMBRE, w=700, size=24, fill=NEGRO),
           T(M, M + 36, f"{OFICIO} · {LUGAR}", size=9, fill=NEGRO),
           T(LW - M, M + 12, IG, fam="Plex", size=8, fill=NEGRO, anchor="end"),
           T(LW - M - 112, M + 26, "correo", fam="Plex", size=8, fill=NEGRO),
           f'<line x1="{LW-M-82}" y1="{M+27}" x2="{LW-M}" y2="{M+27}" stroke="{NEGRO}" stroke-width="0.5"/>',
           f'<line x1="{M}" y1="{M+48}" x2="{LW-M}" y2="{M+48}" stroke="{NEGRO}" stroke-width="1"/>']
    if titulo_doc:
        out.append(T(LW - M, M + 40, titulo_doc, fam="Plex", w=500, size=8, fill=NEGRO, anchor="end"))
    return "\n".join(out)

def pie_doc(n="(01)"):
    return "\n".join([f'<line x1="{M}" y1="{LH-M-14}" x2="{LW-M}" y2="{LH-M-14}" stroke="{NEGRO}" stroke-width="0.5"/>',
                      T(M, LH - M, f"{LLC} · {LUGAR}", fam="Plex", size=7, fill=GRIS),
                      T(LW - M, LH - M, n, fam="Plex", size=7, fill=GRIS, anchor="end")])

def membrete():
    L = [layer("FONDO", f'<rect width="{LW}" height="{LH}" fill="{BLANCO}"/>'),
         layer("ENCABEZADO", encabezado())]
    L.append(layer("MARCA_1BIT", image(png_uri(trama_1bit(foto("2026-09"), 400, 160)), LW - M - 100, LH - M - 64, 100, 40)))
    txt = [T(M, 170, "3 de noviembre de 2026", size=10, fill=NEGRO),
           T(M, 210, "Saludos:", size=10, fill="#BDBDBD"),
           T(M, 230, "Aquí va el texto de la carta. Arimo, 10 pt, interlineado de 15 pt.", size=10, fill="#BDBDBD")]
    L.append(layer("TEXTO_BORRAR_Y_ESCRIBIR", "\n".join(txt)))
    L.append(layer("PIE", pie_doc()))
    return svg(LW, LH, L)


# ================= FACTURA / COTIZACIÓN =================
def factura():
    L = [layer("FONDO", f'<rect width="{LW}" height="{LH}" fill="{BLANCO}"/>'),
         layer("ENCABEZADO", encabezado("FACTURA / COTIZACIÓN"))]
    y0 = 150
    campos = [T(M, y0, "Factura", w=700, size=40, fill=NEGRO, ls=-1),
              T(LW - M - 150, y0 - 26, "Número", fam="Plex", size=8, fill=GRIS),
              T(LW - M, y0 - 26, "2026-001", fam="Plex", w=500, size=9, fill=NEGRO, anchor="end"),
              T(LW - M - 150, y0 - 12, "Fecha", fam="Plex", size=8, fill=GRIS),
              T(LW - M, y0 - 12, "__ / __ / ____", fam="Plex", w=500, size=9, fill=NEGRO, anchor="end"),
              T(LW - M - 150, y0 + 2, "Válida hasta", fam="Plex", size=8, fill=GRIS),
              T(LW - M, y0 + 2, "__ / __ / ____", fam="Plex", w=500, size=9, fill=NEGRO, anchor="end")]
    yc = y0 + 40
    campos.append(T(M, yc, "PARA", fam="Plex", w=500, size=8, fill=GRIS, ls=1))
    for i, lab in enumerate(["Nombre", "Correo", "Teléfono", "Dirección"]):
        yy = yc + 20 + i * 18
        campos.append(T(M, yy, lab, size=9, fill=NEGRO))
        campos.append(f'<line x1="{M+60}" y1="{yy+2}" x2="{LW/2-10}" y2="{yy+2}" stroke="{HAIR}" stroke-width="0.5"/>')
    campos.append(T(LW / 2 + 10, yc, "PAGO", fam="Plex", w=500, size=8, fill=GRIS, ls=1))
    for i, lab in enumerate(["ATH Móvil", "Transferencia", "Tarjeta", "Depósito (50%)"]):
        yy = yc + 20 + i * 18
        campos.append(f'<rect x="{LW/2+10}" y="{yy-7}" width="8" height="8" fill="none" stroke="{NEGRO}" stroke-width="0.6"/>')
        campos.append(T(LW / 2 + 24, yy, lab, size=9, fill=NEGRO))
    L.append(layer("DATOS", "\n".join(campos)))

    # tabla
    yt = yc + 110
    cols = [(M, "CÓDIGO"), (M + 62, "OBRA"), (M + 232, "TÉCNICA"), (M + 352, "MEDIDAS"), (LW - M, "PRECIO")]
    tab = [f'<rect x="{M}" y="{yt}" width="{LW-2*M}" height="20" fill="{NEGRO}"/>']
    for x, lab in cols:
        tab.append(T(x + (6 if lab != "PRECIO" else -6), yt + 13.5, lab, fam="Plex", w=500, size=7.5, fill=BLANCO,
                     anchor="end" if lab == "PRECIO" else "start", ls=0.8))
    filas = [("2026-07", "Sin título (rosa negro gestual)", "Acrílico y carboncillo", "— × — cm", "$ —")] + [("", "", "", "", "")] * 5
    for i, f in enumerate(filas):
        yy = yt + 20 + (i + 1) * 26
        for (x, lab), v in zip(cols, f):
            if v:
                tab.append(T(x + (6 if lab != "PRECIO" else -6), yy - 9, v, fam="Plex" if lab in ("CÓDIGO", "MEDIDAS", "PRECIO") else "Arimo",
                             size=8.5, fill=NEGRO, anchor="end" if lab == "PRECIO" else "start"))
        tab.append(f'<line x1="{M}" y1="{yy}" x2="{LW-M}" y2="{yy}" stroke="{HAIR}" stroke-width="0.5"/>')
    L.append(layer("TABLA_OBRAS", "\n".join(tab)))

    ys = yt + 20 + 6 * 26 + 30
    tot = []
    for i, (lab, val) in enumerate([("Subtotal", "$"), ("IVU 11.5 % (si aplica)", "$"), ("Envío / instalación", "$")]):
        yy = ys + i * 18
        tot.append(T(LW - M - 200, yy, lab, size=9, fill=NEGRO))
        tot.append(T(LW - M, yy, val, fam="Plex", size=9, fill=NEGRO, anchor="end"))
        tot.append(f'<line x1="{LW-M-200}" y1="{yy+5}" x2="{LW-M}" y2="{yy+5}" stroke="{HAIR}" stroke-width="0.5"/>')
    yy = ys + 3 * 18 + 16
    tot.append(f'<rect x="{LW-M-206}" y="{yy-18}" width="206" height="26" fill="{NEGRO}"/>')
    tot.append(T(LW - M - 200, yy, "TOTAL", w=700, size=12, fill=BLANCO))
    tot.append(T(LW - M - 6, yy, "$", fam="Plex", w=700, size=12, fill=BLANCO, anchor="end"))
    L.append(layer("TOTALES", "\n".join(tot)))

    notas = ["Toda obra se entrega con su certificado de autenticidad firmado.",
             "Los derechos de reproducción de la imagen se quedan con la artista.",
             "La obra se reserva con el depósito; el balance se paga antes de la entrega."]
    nb = [T(M, ys - 2, "NOTAS", fam="Plex", w=500, size=8, fill=GRIS, ls=1)]
    nb += [T(M, ys + 16 + i * 14, n, size=8.5, fill=NEGRO) for i, n in enumerate(notas)]
    nb.append(T(M, ys + 100, "Firma", size=9, fill=NEGRO))
    nb.append(f'<line x1="{M+34}" y1="{ys+102}" x2="{M+220}" y2="{ys+102}" stroke="{NEGRO}" stroke-width="0.5"/>')
    nb.append(T(M, LH - M - 30, "¡Gracias por apoyar el arte local!", fam="Fraktur", size=14, fill=NEGRO))
    L.append(layer("NOTAS_Y_FIRMA", "\n".join(nb)))
    L.append(layer("PIE", pie_doc("(02)")))
    return svg(LW, LH, L)


# ================= FIRMA DE EMAIL =================
FIRMA = f"""<!-- Firma de email de Patricia: abre este archivo en el navegador, selecciona la firma,
     cópiala y pégala en Gmail → Configuración → Firma. Escribe el correo donde dice [correo]. -->
<table cellpadding="0" cellspacing="0" style="font-family:Arimo,Arial,Helvetica,sans-serif;color:#0D0D0D;border-collapse:collapse">
  <tr><td style="padding:0 0 6px 0;border-bottom:1px solid #0D0D0D">
    <span style="font-size:18px;font-weight:700;letter-spacing:-0.3px">{NOMBRE}</span>
    <span style="font-size:13px;padding-left:8px">{OFICIO}</span></td></tr>
  <tr><td style="padding:6px 0 0 0;font-family:'IBM Plex Mono',Consolas,monospace;font-size:12px;line-height:18px">
    {LUGAR}<br>
    IG <a href="https://instagram.com/___________________1000gs" style="color:#0D0D0D">{IG}</a><br>
    <span style="color:#6F6F6F">[correo]</span></td></tr>
  <tr><td style="padding:8px 0 0 0"><span style="display:inline-block;width:18px;height:3px;background:#E0508C"></span></td></tr>
</table>
"""


PIEZAS = {
    "tarjeta_A_archivo_frente": (CW, CH, tarjeta_a_frente),
    "tarjeta_A_archivo_dorso": (CW, CH, tarjeta_a_dorso),
    "tarjeta_B_tinta_frente": (CW, CH, tarjeta_b_frente),
    "tarjeta_B_tinta_dorso": (CW, CH, tarjeta_b_dorso),
    "tarjeta_C_rosa_frente": (CW, CH, tarjeta_c_frente),
    "tarjeta_C_rosa_dorso": (CW, CH, tarjeta_c_dorso),
    "membrete_carta": (LW, LH, membrete),
    "factura_cotizacion": (LW, LH, factura),
}
PDFS = {"tarjeta_A_archivo": ["tarjeta_A_archivo_frente", "tarjeta_A_archivo_dorso"],
        "tarjeta_B_tinta": ["tarjeta_B_tinta_frente", "tarjeta_B_tinta_dorso"],
        "tarjeta_C_rosa": ["tarjeta_C_rosa_frente", "tarjeta_C_rosa_dorso"],
        "membrete_carta": ["membrete_carta"], "factura_cotizacion": ["factura_cotizacion"]}


def render(srcs):
    from playwright.sync_api import sync_playwright
    for d in ("preview", "imprenta"):
        (HERE / d).mkdir(exist_ok=True)
    def body(names, scale_css):
        parts = []
        for n in names:
            s = srcs[n].split("?>", 1)[1].replace('<g id="GUIAS_borrar">', '<g id="GUIAS_borrar" style="display:none">')
            parts.append(f'<div style="page-break-after:always;line-height:0">{s}</div>')
        return f'<html><head><style>@page{{margin:0}} body{{margin:0}} {scale_css}</style></head><body>{"".join(parts)}</body></html>'
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        for name, (w, h, _) in PIEZAS.items():
            k = 4 if w == CW else 2    # vista previa nítida
            pg = b.new_page(viewport={"width": round(w / 72 * 96), "height": round(h / 72 * 96)}, device_scale_factor=k * 0.75)
            src = srcs[name].split("?>", 1)[1]
            pg.set_content(f'<html><body style="margin:0;line-height:0">{src.replace('<g id="GUIAS_borrar">', '<g id="GUIAS_borrar" style="display:none">')}</body></html>')
            pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(200)
            pg.screenshot(path=str(HERE / "preview" / f"{name}.png"))
            pg.close()
        for pdf, names in PDFS.items():
            w, h, _ = PIEZAS[names[0]]
            pg = b.new_page()
            pg.set_content(body(names, ""))
            pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(200)
            pg.pdf(path=str(HERE / "imprenta" / f"{pdf}.pdf"), width=f"{w/72}in", height=f"{h/72}in",
                   print_background=True, page_ranges=f"1-{len(names)}")
            pg.close()
        pg = b.new_page(viewport={"width": 520, "height": 150}, device_scale_factor=2)
        pg.set_content(f'<html><body style="margin:20px;background:white">{FIRMA}</body></html>')
        pg.wait_for_timeout(200)
        pg.screenshot(path=str(HERE / "preview" / "firma_email.png"))
        b.close()


if __name__ == "__main__":
    out = HERE / "illustrator"; out.mkdir(exist_ok=True)
    srcs = {}
    for name, (w, h, fn) in PIEZAS.items():
        s = fn(); (out / f"{name}.svg").write_text(s); srcs[name] = s
    (HERE / "firma_email.html").write_text(FIRMA)
    render(srcs)
    print("listo")
