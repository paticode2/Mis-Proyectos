"""Diseños nuevos estilo cybersigilism, generados como stencils para Cricut.

Uso:  python3 sigilos.py            (todos)
      python3 sigilos.py estrellas  (solo los que contengan esa palabra)

Se dibuja en grande (PX por pulgada), se suavizan las uniones para que parezcan
"membranas" (como en los dibujos de referencia) y se vectoriza con potrace,
así todo queda como una sola pieza sin cortes encimados (no hace falta Weld).
Cada diseño tiene una semilla: cambiándola sale otra variante del mismo tipo.
Salida: svg/nuevos/<nombre>.svg
"""
import sys, math, json, pathlib
import numpy as np
import cv2

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from stencil import a_path, islas  # mismo trazado que los otros stencils

AQUI = pathlib.Path(__file__).parent
OUT = AQUI / "svg" / "nuevos"
PX = 300                 # píxeles por pulgada al dibujar
PUNTA = 0.035 * PX       # grosor mínimo de las puntas (~0.9 mm), para que el vinil no se rompa


# ------------------------------------------------------------ geometría
def catmull(pts, n=40):
    """Curva suave que pasa por todos los puntos."""
    pts = np.asarray(pts, float)
    p = np.vstack([pts[0], pts, pts[-1]])
    out = []
    for i in range(len(p) - 3):
        p0, p1, p2, p3 = p[i:i + 4]
        for t in np.linspace(0, 1, n, endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    out.append(pts[-1])
    return np.array(out)


def remuestrear(c, paso=1.5):
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(c, axis=0).T))]
    s = np.arange(0, d[-1], paso)
    return np.c_[np.interp(s, d, c[:, 0]), np.interp(s, d, c[:, 1])]


def trazo(lienzo, pts, w0, w1=None, perfil="punta", suave=True):
    """Dibuja un trazo de grosor variable.
    perfil: 'punta'  grueso al inicio -> fino al final (espina)
            'huso'   fino - grueso - fino (línea caligráfica)
            'fijo'   mismo grosor"""
    c = catmull(pts) if suave else np.asarray(pts, float)
    c = remuestrear(c)
    n = len(c)
    t = np.linspace(0, 1, n)
    w1 = PUNTA if w1 is None else w1
    if perfil == "punta":
        w = w1 + (w0 - w1) * (1 - t) ** 1.6
    elif perfil == "huso":
        w = w1 + (w0 - w1) * np.sin(np.pi * t) ** 0.8
    else:
        w = np.full(n, w0)
    for (x, y), r in zip(c, w / 2):
        cv2.circle(lienzo, (int(round(x)), int(round(y))), max(int(round(r)), 1), 255, -1, cv2.LINE_AA)


def espina(lienzo, base, ang, largo, grosor, curva=0.0, rng=None):
    """Espina afilada que sale de 'base' en dirección 'ang' (radianes), algo curvada."""
    bx, by = base
    pts = []
    for k in range(5):
        t = k / 4
        a = ang + curva * t * t
        pts.append((bx + math.cos(a) * largo * t, by + math.sin(a) * largo * t))
    trazo(lienzo, pts, grosor)


def estrella(lienzo, centro, radio, n, rng, grosor=None, giro=0.0):
    """Estrella de puntas largas y desiguales (como una neurona)."""
    grosor = grosor or radio * 0.16
    cv2.circle(lienzo, tuple(int(v) for v in centro), int(grosor * 0.9), 255, -1, cv2.LINE_AA)
    for k in range(n):
        a = giro + 2 * math.pi * k / n + rng.uniform(-0.25, 0.25)
        largo = radio * rng.uniform(0.55, 1.15)
        espina(lienzo, centro, a, largo, grosor, curva=rng.uniform(-0.25, 0.25))


def garra(lienzo, inicio, ang, largo, grosor, curva=0.6, puntas=2):
    """Trazo curvo afilado (el elemento básico del cybersigilism).
    puntas=2: afilado en los dos extremos; puntas=1: sale grueso y termina en punta."""
    x, y = inicio
    pts = []
    for k in range(7):
        t = k / 6
        a = ang + curva * t
        pts.append((x, y))
        x, y = x + math.cos(a) * largo / 6, y + math.sin(a) * largo / 6
    pts.append((x, y))
    trazo(lienzo, pts, grosor, perfil="huso" if puntas == 2 else "punta")


def gancho(lienzo, inicio, ang, largo, grosor, sentido=1, vueltas=0.85):
    """Línea que termina enroscada (los 'rizos' de los dibujos)."""
    x, y = inicio
    pts = [(x, y)]
    a = ang
    paso = largo / 14
    for k in range(28):
        frac = k / 27
        giro = 0.0 if frac < 0.45 else sentido * (2 * math.pi * vueltas) / 15 * (1 + 1.5 * (frac - 0.45))
        a += giro
        p = paso * (1 - 0.55 * max(frac - 0.45, 0))
        x, y = x + math.cos(a) * p, y + math.sin(a) * p
        pts.append((x, y))
    trazo(lienzo, pts[::2], grosor, perfil="punta")


def membrana(m, px):
    """Une los trazos con 'membranas' suaves donde se juntan (cierre + blur)."""
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * px + 1, 2 * px + 1))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, k)
    b = cv2.GaussianBlur(m.astype(np.float32), (0, 0), px * 0.35)
    return (b > 127).astype(np.uint8) * 255


def espejo(m):
    """Simetría izquierda-derecha: copia la mitad izquierda en la derecha."""
    w = m.shape[1]
    izq = m[:, : w // 2]
    m[:, w - w // 2:] = np.maximum(m[:, w - w // 2:], izq[:, ::-1])
    m[:, : w // 2] = np.maximum(izq, m[:, w - w // 2:][:, ::-1])
    return m


def lienzo(ancho_in, alto_in):
    return np.zeros((int(alto_in * PX), int(ancho_in * PX)), np.uint8)


# ------------------------------------------------------------ diseños
def d_espina_dorsal(rng):
    """Sigilo vertical en espejo: columna afilada y garras curvas que salen a los lados."""
    W, H = 6, 11
    m = lienzo(W, H)
    cx = W * PX / 2
    trazo(m, [(cx, 0.1 * PX), (cx, 5.5 * PX), (cx, 10.9 * PX)], 0.2 * PX, perfil="huso")
    for y in np.linspace(1.3, 9.6, 7):
        sube = rng.choice([-1, 1])
        a = math.pi + sube * rng.uniform(0.35, 0.9)
        garra(m, (cx - 0.05 * PX, y * PX), a, rng.uniform(1.6, 2.8) * PX, 0.13 * PX,
              curva=-sube * rng.uniform(0.7, 1.4), puntas=1)
        garra(m, (cx - 0.3 * PX, (y + 0.35) * PX), math.pi + sube * 1.3, rng.uniform(0.6, 1.1) * PX,
              0.07 * PX, curva=-sube * 0.9, puntas=1)
    # garras largas que cruzan de arriba a abajo
    garra(m, (cx - 0.15 * PX, 0.9 * PX), math.pi * 0.62, 5.0 * PX, 0.12 * PX, curva=0.75)
    garra(m, (cx - 0.15 * PX, 10.2 * PX), -math.pi * 0.62, 4.0 * PX, 0.1 * PX, curva=-0.7)
    estrella(m, (cx, 5.5 * PX), 1.0 * PX, 4, rng, grosor=0.22 * PX, giro=math.pi / 4)
    m = espejo(m)
    return membrana(m, int(0.05 * PX))


def d_tres_estrellas(rng):
    """Tres estrellas en diagonal unidas por líneas que se enroscan."""
    W, H = 6, 11
    m = lienzo(W, H)
    centros = [(2.2, 2.3), (3.9, 5.4), (2.6, 8.6)]
    for (x, y) in centros:
        estrella(m, (x * PX, y * PX), rng.uniform(1.4, 1.9) * PX, rng.integers(5, 8), rng, grosor=0.2 * PX)
    # cintas dobles que serpentean entre las estrellas
    for off in (0, 0.13):
        pts = [(4.6 + off, 0.5), (3.2 + off, 1.0), (3.6 + off, 2.8), (4.9 + off, 3.9), (3.2 + off, 4.7),
               (1.2 + off, 4.5), (1.0 + off, 6.0), (3.6 + off, 6.6), (4.7 + off, 7.8), (3.8 + off, 9.6),
               (2.0 + off, 10.4), (0.9 + off, 9.8)]
        trazo(m, [(x * PX, y * PX) for x, y in pts], 0.05 * PX, perfil="huso", w1=PUNTA)
    gancho(m, (4.6 * PX, 0.5 * PX), 0.2, 1.0 * PX, 0.06 * PX, sentido=1)
    gancho(m, (1.0 * PX, 9.8 * PX), math.pi * 0.9, 1.0 * PX, 0.06 * PX, sentido=-1)
    return membrana(m, int(0.04 * PX))


def d_red(rng):
    """Red orgánica como el dibujo del cuaderno: celdas redondeadas separadas por
    líneas negras que se ensanchan en membranas donde se juntan. Capa 2: estrellas rosas."""
    W, H = 9, 11
    s = 4  # se calcula a 1/4 de resolución y luego se amplía
    h, w = H * PX // s, W * PX // s
    n = 34
    pts = np.c_[rng.uniform(0, w, n), rng.uniform(0, h, n)]
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    # deforma el plano con ruido suave para que las líneas salgan curvas, no rectas
    def ruido(amp):
        r = cv2.resize(rng.normal(0, 1, (5, 4)), (w, h), interpolation=cv2.INTER_CUBIC)
        return r * amp
    xx += ruido(0.35 * PX / s); yy += ruido(0.35 * PX / s)
    for _ in range(4):  # Lloyd: reparte las celdas para que tengan tamaños parecidos
        d = np.stack([np.hypot(xx - px_, yy - py_) for px_, py_ in pts])
        cerca = d.argmin(0)
        for i in range(n):
            sel = cerca == i
            if sel.any():
                pts[i] = xx[sel].mean(), yy[sel].mean()
    d = np.sort(np.stack([np.hypot(xx - px_, yy - py_) for px_, py_ in pts]), axis=0)
    borde = (d[1] - d[0]) < 0.06 * PX / s          # líneas entre celdas
    celdas = (~borde).astype(np.uint8) * 255
    r = int(0.3 * PX / s)                           # redondea las esquinas -> membranas
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    celdas = cv2.morphologyEx(celdas, cv2.MORPH_OPEN, k)
    # algunas celdas se parten en dos "burbujas"
    m = cv2.resize(255 - celdas, (W * PX, H * PX), interpolation=cv2.INTER_CUBIC)
    m = membrana((m > 127).astype(np.uint8) * 255, int(0.03 * PX))
    marco = np.zeros_like(m)
    cv2.rectangle(marco, (int(0.3 * PX), int(0.3 * PX)), (int((W - 0.3) * PX), int((H - 0.3) * PX)), 255, -1)
    negro = cv2.bitwise_and(m, marco)
    # capa rosa: estrellitas de 4 puntas dentro de algunas celdas
    rosa = np.zeros_like(negro)
    for i in np.nonzero(rng.random(n) < 0.6)[0]:
        cy, cx = np.argwhere(cerca == i).mean(0) * s
        if 0.8 * PX < cx < (W - 0.8) * PX and 0.8 * PX < cy < (H - 0.8) * PX:
            estrella(rosa, (cx, cy), rng.uniform(0.35, 0.6) * PX, 4, rng, grosor=0.09 * PX,
                     giro=rng.uniform(0, math.pi))
    rosa = membrana(rosa, int(0.03 * PX))
    rosa[cv2.dilate(negro, np.ones((25, 25), np.uint8)) > 0] = 0   # que no toque lo negro
    return negro, rosa


def d_corona(rng):
    """Halo de espinas en espejo, con una estrella en el centro."""
    W, H = 9, 9
    m = lienzo(W, H)
    c = np.array([W, H]) * PX / 2
    R = 2.6 * PX
    angs = np.linspace(0, 2 * np.pi, 200)
    trazo(m, [(c[0] + math.cos(a) * R, c[1] + math.sin(a) * R * 1.08) for a in angs], 0.1 * PX, perfil="fijo")
    for a in np.linspace(-math.pi / 2, math.pi / 2, 9):
        a += rng.uniform(-0.08, 0.08)
        base = (c[0] - math.cos(a) * R, c[1] + math.sin(a) * R * 1.08)
        hacia_afuera = math.pi - a
        espina(m, base, hacia_afuera + rng.uniform(-0.3, 0.3), rng.uniform(0.8, 1.7) * PX, 0.14 * PX,
               curva=rng.uniform(-0.9, 0.9))
        espina(m, base, -a + rng.uniform(-0.3, 0.3) + 0.0, rng.uniform(0.4, 0.9) * PX, 0.09 * PX,
               curva=rng.uniform(-0.6, 0.6))
    estrella(m, tuple(c), 2.0 * PX, 8, rng, grosor=0.24 * PX, giro=math.pi / 2)
    m = espejo(m)
    return membrana(m, int(0.06 * PX))


def d_alas(rng):
    """Alas de garras en espejo, con una columna afilada al centro."""
    W, H = 10, 8
    m = lienzo(W, H)
    cx, cy = W * PX / 2, H * PX * 0.42
    trazo(m, [(cx, 0.1 * PX), (cx, cy), (cx, 7.9 * PX)], 0.2 * PX, perfil="huso")
    for k in range(6):
        a = math.pi + 0.75 - k * 0.27
        largo = (4.6 - abs(k - 1.5) * 0.45) * PX
        garra(m, (cx - 0.1 * PX, cy + k * 0.12 * PX), a, largo, 0.16 * PX, curva=-0.55 + k * 0.08, puntas=1)
        if k < 4:
            bx, by = cx + math.cos(a) * largo * 0.45, cy + math.sin(a) * largo * 0.45
            garra(m, (bx, by), a - 0.9, largo * 0.25, 0.06 * PX, curva=0.6, puntas=1)
    garra(m, (cx - 0.1 * PX, cy + 0.6 * PX), math.pi * 0.55, 3.2 * PX, 0.12 * PX, curva=0.9)
    estrella(m, (cx, cy), 0.9 * PX, 4, rng, grosor=0.22 * PX, giro=math.pi / 4)
    m = espejo(m)
    return membrana(m, int(0.05 * PX))


def d_rizos(rng):
    """Panel en espejo de rizos con espinas (cruce entre la reja y los sigilos)."""
    W, H = 6, 11
    m = lienzo(W, H)
    cx = W * PX / 2
    trazo(m, [(cx, 0.2 * PX), (cx, 10.8 * PX)], 0.08 * PX, perfil="huso")
    for y in np.linspace(1.0, 9.8, 7):
        s = rng.choice([-1, 1])
        gancho(m, (cx, y * PX), math.pi + s * rng.uniform(0.2, 0.7), rng.uniform(1.6, 2.4) * PX, 0.1 * PX,
               sentido=-s, vueltas=rng.uniform(0.7, 1.0))
        espina(m, (cx, y * PX + 0.3 * PX), math.pi - 0.3, rng.uniform(0.7, 1.2) * PX, 0.07 * PX, curva=0.5)
    for y in (2.4, 5.4, 8.4):
        estrella(m, (cx, y * PX), 0.75 * PX, 4, rng, grosor=0.14 * PX, giro=math.pi / 4)
    m = espejo(m)
    return membrana(m, int(0.05 * PX))


DISENOS = {
    "sigilo_01_espina_dorsal": (d_espina_dorsal, 7),
    "sigilo_02_tres_estrellas": (d_tres_estrellas, 3),
    "sigilo_03_red": (d_red, 11),
    "sigilo_04_corona": (d_corona, 5),
    "sigilo_05_alas": (d_alas, 2),
    "sigilo_06_rizos": (d_rizos, 9),
}


COLOR = {"negro": "#000000", "rosa": "#e5148f"}


def guardar(nombre, res):
    capas = res if isinstance(res, tuple) else (res,)
    masks = [c > 127 for c in capas]
    todo = np.logical_or.reduce(masks)
    ys, xs = np.nonzero(todo)
    pad = int(0.15 * PX)
    y0, y1 = max(ys.min() - pad, 0), min(ys.max() + pad, todo.shape[0])
    x0, x1 = max(xs.min() - pad, 0), min(xs.max() + pad, todo.shape[1])
    masks = [mk[y0:y1, x0:x1] for mk in masks]
    h, w = masks[0].shape
    nombres = ["negro", "rosa"][: len(masks)]
    paths = [f'<path id="{n}" fill="{COLOR[n]}" fill-rule="evenodd" d="{a_path(mk)}"/>' for n, mk in zip(nombres, masks)]
    cab = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w / PX:.3f}in" height="{h / PX:.3f}in" '
           f'viewBox="0 0 {w} {h}">')
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{nombre}.svg").write_text(cab + "".join(paths) + "</svg>\n")
    if len(masks) > 1:
        for n, p in zip(nombres, paths):
            (OUT / f"{nombre}_{n}.svg").write_text(cab + p + "</svg>\n")
    info = {"nombre": nombre, "pulgadas": [round(w / PX, 2), round(h / PX, 2)],
            "islas": [islas(mk) for mk in masks]}
    print(json.dumps(info, ensure_ascii=False))


if __name__ == "__main__":
    filtro = sys.argv[1] if len(sys.argv) > 1 else ""
    for nombre, (fn, semilla) in DISENOS.items():
        if filtro in nombre:
            guardar(nombre, fn(np.random.default_rng(semilla)))
