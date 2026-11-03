"""Ilustraciones para la presentación de la computadora de Patricia.
  escritorio.png   - cómo se vería su escritorio (monitor con su web, torre, tableta)
  por_dentro_f1.png / por_dentro_f2.png - la torre por dentro (fase 1 y con la tarjeta de la fase 2)
  mac_vs_torre.png - tamaño y diferencia entre Mac mini y torre
Uso: python3 build_ilustraciones.py  (necesita playwright y las fonts de artista/08-flyers/fonts)
"""
import base64, io
from pathlib import Path
from PIL import Image

HERE = Path(__file__).parent
REPO = HERE.parents[2] if (HERE.parents[2] / "artista").exists() else HERE.parents[1]
ART = REPO / "artista"
PAPEL, TINTA, ROSA, ROSA_H, GRIS = "#F2EEE8", "#171515", "#E0508C", "#B0195C", "#6F6F6F"


def uri(path, w=None, fmt="JPEG"):
    im = Image.open(path).convert("RGB")
    if w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, fmt, quality=88)
    return f"data:image/{fmt.lower()};base64," + base64.b64encode(b.getvalue()).decode()

def T(x, y, s, size=22, fill=TINTA, w=400, anchor="start", fam="Arimo"):
    return f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}">{s}</text>'

def mono(x, y, s, size=18, fill=GRIS, anchor="start"):
    return T(x, y, s, size, fill, 500, anchor, "IBM Plex Mono")

DEFS = f"""<defs>
<linearGradient id="caja" x1="0" x2="1"><stop offset="0" stop-color="#2A2627"/><stop offset="1" stop-color="#151314"/></linearGradient>
<linearGradient id="vidrio" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3A3537" stop-opacity=".95"/><stop offset="1" stop-color="#1B1819" stop-opacity=".95"/></linearGradient>
<linearGradient id="brillo" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".18"/><stop offset=".35" stop-color="#fff" stop-opacity="0"/></linearGradient>
<radialGradient id="glow"><stop offset="0" stop-color="{ROSA}" stop-opacity=".55"/><stop offset="1" stop-color="{ROSA}" stop-opacity="0"/></radialGradient>
<linearGradient id="mesa" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#CFC6BA"/><stop offset="1" stop-color="#B9AFA2"/></linearGradient>
<linearGradient id="pared" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F6F3EE"/><stop offset="1" stop-color="#E9E3DA"/></linearGradient>
<pattern id="malla" width="10" height="10" patternUnits="userSpaceOnUse"><circle cx="5" cy="5" r="2.2" fill="#0B0A0A"/></pattern>
<filter id="sombra" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="14" stdDeviation="14" flood-color="#000" flood-opacity=".28"/></filter>
</defs>"""

def svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{DEFS}{body}</svg>'

def ventilador(cx, cy, r, color="#2E2A2B", aspa="#4A4446"):
    s = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" stroke="#0E0D0D" stroke-width="3"/>']
    for k in range(7):
        s.append(f'<ellipse cx="{cx}" cy="{cy - r*0.5}" rx="{r*0.2}" ry="{r*0.45}" fill="{aspa}" transform="rotate({k*360/7} {cx} {cy})"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.22}" fill="#1B1819"/>')
    return "".join(s)


def interior(x, y, w, h, gpu=False, etiquetas=True, escala=1.0):
    """Lo de adentro de la torre visto de lado (placa, CPU, RAM, disco, fuente, tarjeta)."""
    k = escala
    s = []
    # placa base
    px, py, pw, ph = x + w * 0.10, y + h * 0.06, w * 0.72, h * 0.62
    s.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="6" fill="#1F2324" stroke="#0E0D0D" stroke-width="2"/>')
    for i in range(9):  # pistas
        s.append(f'<line x1="{px+10}" y1="{py+20+i*ph/9}" x2="{px+pw*0.35}" y2="{py+20+i*ph/9}" stroke="#2C3334" stroke-width="2"/>')
    # disipador del CPU
    cx, cy = px + pw * 0.38, py + ph * 0.26
    cw, ch = pw * 0.30, ph * 0.30
    s.append(f'<rect x="{cx-cw/2}" y="{cy-ch/2}" width="{cw}" height="{ch}" rx="4" fill="#BFC3C4"/>')
    for i in range(14):
        s.append(f'<line x1="{cx-cw/2+4}" y1="{cy-ch/2+6+i*(ch-12)/13}" x2="{cx+cw/2-4}" y2="{cy-ch/2+6+i*(ch-12)/13}" stroke="#8C9192" stroke-width="2"/>')
    s.append(ventilador(cx - cw / 2 - 6, cy, ch * 0.42, "#2E2A2B"))
    # RAM: 2 llenas + 2 vacías
    rx0 = px + pw * 0.66
    for i in range(4):
        rx = rx0 + i * pw * 0.06
        if i in (1, 3):
            s.append(f'<rect x="{rx}" y="{py+ph*0.08}" width="{pw*0.035}" height="{ph*0.40}" rx="3" fill="#0F0E0E" stroke="#D9D2C8" stroke-width="1"/>'
                     f'<rect x="{rx}" y="{py+ph*0.08}" width="{pw*0.035}" height="{ph*0.06}" fill="{ROSA}"/>')
        else:
            s.append(f'<rect x="{rx}" y="{py+ph*0.08}" width="{pw*0.035}" height="{ph*0.40}" rx="3" fill="none" stroke="#7A7476" stroke-width="2" stroke-dasharray="6 5"/>')
    # disco NVMe + ranura libre
    nx, ny = px + pw * 0.22, py + ph * 0.60
    s.append(f'<rect x="{nx}" y="{ny}" width="{pw*0.36}" height="{ph*0.06}" rx="3" fill="#2B2B2B" stroke="#D9D2C8" stroke-width="1.2"/>'
             f'<rect x="{nx+8}" y="{ny+5}" width="{pw*0.08}" height="{ph*0.06-10}" fill="#8C9192"/>')
    s.append(f'<rect x="{nx}" y="{py+ph*0.86}" width="{pw*0.36}" height="{ph*0.06}" rx="3" fill="none" stroke="#7A7476" stroke-width="2" stroke-dasharray="6 5"/>')
    # ranura PCIe y tarjeta gráfica
    gy = py + ph * 0.72
    s.append(f'<rect x="{px+pw*0.08}" y="{gy}" width="{pw*0.70}" height="8" fill="#0B0A0A"/>')
    if gpu:
        gx, gw, gh = px + pw * 0.04, pw * 0.86, ph * 0.20
        s.append(f'<rect x="{gx}" y="{gy-4}" width="{gw}" height="{gh}" rx="8" fill="#2A2627" stroke="#0E0D0D" stroke-width="2"/>'
                 f'<rect x="{gx}" y="{gy-4}" width="{gw}" height="6" fill="{ROSA}"/>')
        s.append(ventilador(gx + gw * 0.30, gy + gh / 2 - 2, gh * 0.40) + ventilador(gx + gw * 0.70, gy + gh / 2 - 2, gh * 0.40))
    else:
        s.append(f'<rect x="{px+pw*0.04}" y="{gy-4}" width="{pw*0.86}" height="{ph*0.20}" rx="8" fill="none" stroke="{ROSA}" stroke-width="2.5" stroke-dasharray="10 8"/>')
    # fuente abajo
    s.append(f'<rect x="{x+w*0.06}" y="{y+h*0.80}" width="{w*0.50}" height="{h*0.15}" rx="6" fill="#121011" stroke="#2E2A2B" stroke-width="2"/>'
             + T(x + w * 0.31, y + h * 0.80 + h * 0.095, "750 W", 16 * k, "#8C8486", 700, "middle"))
    # ventiladores delanteros (a la derecha)
    for i in range(3):
        s.append(ventilador(x + w * 0.91, y + h * (0.16 + i * 0.22), w * 0.065, "#2E2A2B"))
    return "".join(s)


# ======================= ESCRITORIO =======================
def escritorio():
    W, H = 1600, 1000
    b = [f'<rect width="{W}" height="{H}" fill="url(#pared)"/>',
         f'<rect y="690" width="{W}" height="{H-690}" fill="url(#mesa)"/>',
         f'<rect y="690" width="{W}" height="6" fill="#A99E90"/>']
    # obra enmarcada en la pared
    b.append(f'<g filter="url(#sombra)"><rect x="70" y="110" width="210" height="280" fill="#141213"/>'
             f'<rect x="84" y="124" width="182" height="252" fill="#F7F4EF"/>'
             f'<image x="100" y="140" width="150" height="220" preserveAspectRatio="xMidYMid slice" xlink:href="{uri(ART/"02-fotos-obras/web/2026-03_rosa-spray_web.jpg", 400)}"/></g>')
    # monitor
    mx, my, mw, mh = 340, 130, 820, 470
    b.append(f'<g filter="url(#sombra)"><rect x="{mx}" y="{my}" width="{mw}" height="{mh}" rx="14" fill="#121011"/>'
             f'<image x="{mx+14}" y="{my+14}" width="{mw-28}" height="{mh-46}" preserveAspectRatio="xMidYMin slice" xlink:href="{uri(ART/"09-moodboard/capturas/archivo_1.png", 1200)}"/>'
             f'<rect x="{mx+14}" y="{my+14}" width="{mw-28}" height="{mh-46}" fill="url(#brillo)"/>'
             f'<circle cx="{mx+mw/2}" cy="{my+mh-16}" r="4" fill="#3A3537"/></g>')
    b.append(f'<rect x="{mx+mw/2-26}" y="{my+mh}" width="52" height="70" fill="#1B1819"/>'
             f'<ellipse cx="{mx+mw/2}" cy="{my+mh+76}" rx="150" ry="16" fill="#1B1819"/>')
    # torre (frente + lado de vidrio)
    tx, ty, tw_, th = 1215, 250, 190, 450
    side = 120
    b.append(f'<ellipse cx="{tx+tw_/2+side/2}" cy="{ty+th+8}" rx="190" ry="20" fill="#000" opacity=".18"/>')
    b.append(f'<polygon points="{tx+tw_},{ty} {tx+tw_+side},{ty-40} {tx+tw_+side},{ty+th-40} {tx+tw_},{ty+th}" fill="url(#vidrio)" stroke="#0E0D0D" stroke-width="3"/>')
    b.append(f'<ellipse cx="{tx+tw_+side/2}" cy="{ty+th/2-20}" rx="90" ry="200" fill="url(#glow)"/>')
    b.append(f'<g transform="translate({tx+tw_},{ty}) matrix(1,-0.333,0,1,0,0) scale({side/300},{th/450})">{interior(0, 0, 300, 450)}</g>')
    b.append(f'<polygon points="{tx+tw_},{ty} {tx+tw_+side},{ty-40} {tx+tw_+side},{ty+th-40} {tx+tw_},{ty+th}" fill="url(#brillo)"/>')
    b.append(f'<rect x="{tx}" y="{ty}" width="{tw_}" height="{th}" rx="6" fill="url(#caja)" stroke="#0E0D0D" stroke-width="3"/>'
             f'<rect x="{tx+18}" y="{ty+60}" width="{tw_-36}" height="{th-90}" rx="4" fill="url(#malla)" opacity=".9"/>'
             f'<circle cx="{tx+tw_/2}" cy="{ty+30}" r="9" fill="none" stroke="{ROSA}" stroke-width="3"/>'
             f'<rect x="{tx+tw_/2-30}" y="{ty+22}" width="12" height="16" rx="2" fill="#3A3537"/>')
    # tableta y lápiz
    b.append(f'<g filter="url(#sombra)"><polygon points="430,760 900,760 940,900 390,900" fill="#1B1819"/>'
             f'<polygon points="470,780 860,780 890,880 440,880" fill="#262223"/></g>'
             f'<line x1="760" y1="840" x2="960" y2="740" stroke="#121011" stroke-width="12" stroke-linecap="round"/>'
             f'<line x1="760" y1="840" x2="780" y2="830" stroke="{ROSA}" stroke-width="12" stroke-linecap="round"/>')
    # teclado
    b.append(f'<polygon points="990,770 1300,770 1325,840 965,840" fill="#E4DED5" stroke="#B9AFA2" stroke-width="2"/>')
    for r in range(3):
        for c in range(12):
            b.append(f'<rect x="{1000+c*25+r*6}" y="{780+r*19}" width="20" height="14" rx="2" fill="#F7F4EF"/>')
    # disco externo
    b.append(f'<rect x="200" y="640" width="90" height="56" rx="8" fill="#2A2627"/><circle cx="276" cy="682" r="4" fill="{ROSA}"/>')
    # etiquetas
    b += [mono(mx, 112, "MONITOR 27\" — TU WEB, A COLOR REAL", 18, "#4A4543"),
          mono(tx - 10, 230 - 20, "TU TORRE", 18, "#4A4543"),
          mono(390, 935, "TABLETA DE DIBUJO + LÁPIZ", 18, "#4A4543"),
          mono(150, 735, "DISCO DE RESPALDO", 16, "#4A4543"),
          mono(70, 420, "TU OBRA 2026-03", 16, "#4A4543")]
    return svg(W, H, "".join(b))


# ======================= POR DENTRO =======================
def por_dentro(gpu):
    W, H = 1600, 1000
    x, y, w, h = 200, 80, 760, 840
    b = [f'<rect width="{W}" height="{H}" fill="{PAPEL}"/>',
         f'<g filter="url(#sombra)"><rect x="{x-20}" y="{y-20}" width="{w+40}" height="{h+40}" rx="18" fill="#141213"/>'
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#1B1819"/></g>',
         f'<ellipse cx="{x+w/2}" cy="{y+h/2}" rx="{w*0.45}" ry="{h*0.45}" fill="url(#glow)" opacity=".6"/>',
         interior(x, y, w, h, gpu=gpu, escala=1.6)]
    # flechas y etiquetas a la derecha
    px, py, pw, ph = x + w * 0.10, y + h * 0.06, w * 0.72, h * 0.62
    puntos = [
        (px + pw * 0.75, py + ph * 0.20, "Memoria 32 GB", "2 ranuras libres → 64 GB (fase 3)", TINTA),
        (px + pw * 0.38, py + ph * 0.26, "Procesador Ryzen 5 9600X", "el cerebro · fase 4: Ryzen 7 o 9", TINTA),
        (px + pw * 0.40, py + ph * 0.63, "Disco NVMe 1 TB", "+ espacio para otro (fase 3)", TINTA),
        (px + pw * 0.50, py + ph * 0.80, "Tarjeta RTX 5060 Ti 16 GB" if gpu else "Aquí va la tarjeta gráfica",
         "fase 2 · lista para Blender" if gpu else "fase 2 · cuando empieces con Blender", ROSA_H),
        (x + w * 0.12, y + h * 0.87, "Fuente 750 W", "ya aguanta la tarjeta", TINTA)]
    lx = 1070
    for i, (ax, ay, t1, t2, col) in enumerate(puntos):
        ly = 170 + i * 165
        b.append(f'<circle cx="{ax}" cy="{ay}" r="9" fill="{ROSA}" stroke="#fff" stroke-width="3"/>'
                 f'<path d="M{ax},{ay} L{lx-40},{ly-8} L{lx-14},{ly-8}" fill="none" stroke="{ROSA}" stroke-width="2.5"/>')
        b.append(T(lx, ly, t1, 30, col, 700) + T(lx, ly + 36, t2, 22, "#4A4543"))
    b.append(mono(x, H - 30, "FASE 2 — CON TARJETA GRÁFICA" if gpu else "FASE 1 — LO PUNTEADO ES LO QUE SE AÑADE DESPUÉS", 18, "#4A4543"))
    return svg(W, H, "".join(b))


# ======================= MAC MINI VS TORRE =======================
def mac_vs_torre():
    W, H = 1600, 900
    base = 720
    b = [f'<rect width="{W}" height="{H}" fill="{PAPEL}"/>',
         f'<line x1="80" y1="{base}" x2="{W-80}" y2="{base}" stroke="#B9AFA2" stroke-width="3"/>']
    # Mac mini (12.7 x 12.7 x 5 cm aprox) a escala 1 cm = 11 px
    s = 11
    mw, mh = 12.7 * s * 2.2, 5 * s * 1.6
    mx = 330
    b.append(f'<g filter="url(#sombra)"><rect x="{mx}" y="{base-mh}" width="{mw}" height="{mh}" rx="16" fill="#D7D9DB" stroke="#A9ACAF" stroke-width="2"/>'
             f'<rect x="{mx+10}" y="{base-mh+8}" width="{mw-20}" height="8" rx="4" fill="#fff" opacity=".6"/>'
             f'<circle cx="{mx+mw-26}" cy="{base-mh/2}" r="5" fill="#7FD07A"/></g>')
    # candado
    lx, ly = mx + mw / 2, base - mh - 120
    b.append(f'<rect x="{lx-34}" y="{ly}" width="68" height="54" rx="8" fill="{TINTA}"/>'
             f'<path d="M{lx-20},{ly} v-18 a20,20 0 0 1 40,0 v18" fill="none" stroke="{TINTA}" stroke-width="9"/>')
    b.append(T(mx + mw / 2, base + 70, "Mac mini", 40, TINTA, 700, "middle")
             + T(mx + mw / 2, base + 110, "Cerrado: lo que compras se queda así", 24, "#4A4543", 400, "middle"))
    # torre (45 x 21 cm aprox)
    th, tw_ = 540, 250
    tx = 980
    b.append(f'<g filter="url(#sombra)"><rect x="{tx}" y="{base-th}" width="{tw_}" height="{th}" rx="8" fill="url(#caja)" stroke="#0E0D0D" stroke-width="3"/>'
             f'<rect x="{tx+22}" y="{base-th+70}" width="{tw_-44}" height="{th-110}" rx="4" fill="url(#malla)"/>'
             f'<circle cx="{tx+tw_/2}" cy="{base-th+34}" r="10" fill="none" stroke="{ROSA}" stroke-width="3"/></g>')
    # tapa abierta con flechas de mejora
    b.append(f'<polygon points="{tx+tw_+10},{base-th} {tx+tw_+110},{base-th-30} {tx+tw_+110},{base-30} {tx+tw_+10},{base}" fill="url(#vidrio)" opacity=".85"/>')
    for i, t in enumerate(["+ tarjeta", "+ memoria", "+ disco", "+ procesador"]):
        yy = base - th + 90 + i * 110
        b.append(f'<p/>' if False else "")
        b.append(f'<text x="{tx+tw_+140}" y="{yy}" font-family="Arimo" font-size="28" font-weight="700" fill="{ROSA_H}">{t}</text>')
    b.append(T(tx + tw_ / 2, base + 70, "Torre", 40, TINTA, 700, "middle")
             + T(tx + tw_ / 2, base + 110, "Se abre y se mejora con los años", 24, "#4A4543", 400, "middle"))
    b.append(mono(80, 60, "TAMAÑOS APROXIMADOS, NO A ESCALA EXACTA", 16, "#6F6F6F"))
    return svg(W, H, "".join(b))


PIEZAS = {"escritorio": (1600, 1000, escritorio), "por_dentro_f1": (1600, 1000, lambda: por_dentro(False)),
          "por_dentro_f2": (1600, 1000, lambda: por_dentro(True)), "mac_vs_torre": (1600, 900, mac_vs_torre)}

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        for name, (w, h, fn) in PIEZAS.items():
            s = fn(); (HERE / f"{name}.svg").write_text(s)
            pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1.5)
            pg.set_content(f'<html><body style="margin:0">{s}</body></html>')
            pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
            pg.screenshot(path=str(HERE / f"{name}.png")); pg.close(); print("ok", name)
        b.close()
