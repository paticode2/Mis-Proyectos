"""Convierte los dibujos de originales/ en SVG listos para Cricut Design Space.

Uso:  python3 stencil.py            (procesa todos)
      python3 stencil.py pegaso     (solo los que contengan esa palabra)

Necesita: pip install opencv-python-headless numpy potracer
Cada diseño tiene su receta en RECETAS: cómo se separa la tinta del fondo,
cuánto se limpia y de qué tamaño sale (en pulgadas).
Salida: svg/<nombre>.svg  (+ una capa por color si tiene varios)
"""
import sys, json, pathlib
import numpy as np
import cv2
import potrace

AQUI = pathlib.Path(__file__).parent
ORIG, SVG = AQUI / "originales", AQUI / "svg"


def gris(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def quitar_motas(mask, area_min):
    """Quita manchitas de tinta y rellena huequitos más pequeños que area_min."""
    n, lab, st, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), 8)
    keep = np.zeros(n, bool)
    keep[1:] = st[1:, cv2.CC_STAT_AREA] >= area_min
    mask = keep[lab]
    inv = ~mask
    n, lab, st, _ = cv2.connectedComponentsWithStats(inv.astype(np.uint8), 4)
    fill = np.zeros(n, bool)
    fill[1:] = st[1:, cv2.CC_STAT_AREA] < area_min
    return mask | fill[lab]


def quitar_borde(mask):
    """Quita lo que toca el borde de la foto (sombras, esquinas de la carta)."""
    n, lab, _, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), 8)
    borde = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    for b in borde:
        mask[lab == b] = False
    return mask


def engrosar(mask, px):
    if px <= 0:
        return mask
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * px + 1, 2 * px + 1))
    return cv2.dilate(mask.astype(np.uint8), k) > 0


def cerrar(mask, px):
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * px + 1, 2 * px + 1))
    return cv2.morphologyEx(mask.astype(np.uint8), cv2.MORPH_CLOSE, k) > 0


def suavizar(mask, px):
    """Suaviza bordes temblorosos (blur + umbral)."""
    b = cv2.GaussianBlur(mask.astype(np.float32), (0, 0), px)
    return b > 0.5


def rellenar_tubos(lineas, ancho_max):
    """Para dibujos de contorno: rellena por dentro las formas del dibujo.
    Las formas que se cruzan quedan unidas en una sola zona (la más grande que
    no toca el borde); además se rellenan las zonitas estrechas entre cruces."""
    inv = (~lineas).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(inv, 4)
    dist = cv2.distanceTransform(inv, cv2.DIST_L2, 5)
    maxd = np.zeros(n)
    np.maximum.at(maxd, lab.ravel(), dist.ravel())
    borde = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])))
    dentro = [i for i in range(1, n) if i not in borde]
    red = max(dentro, key=lambda i: st[i, cv2.CC_STAT_AREA])
    fill = np.zeros(n, bool)
    for i in dentro:
        fill[i] = i == red or maxd[i] <= ancho_max
    return lineas | fill[lab]


# ---------------------------------------------------------------- recetas
def m_monograma(img, relleno):
    g = cv2.GaussianBlur(gris(img), (3, 3), 0)
    m = quitar_motas(g < 140, 60)
    if relleno:
        m = rellenar_tubos(m, 13)
        m = quitar_motas(m, 200)
    return suavizar(m, 1.2)


def m_diablita(img):
    b, g, r = cv2.split(img.astype(int))
    m = (r > 140) & (g < 110) & (b > 60)
    return suavizar(quitar_motas(m, 80), 1.0)


def m_pegaso(img):
    m = gris(img) < 110
    m = quitar_motas(m, 900)  # tapa los brillos de la pintura, deja el ojo
    return suavizar(m, 2.0)


def m_reja(img):
    g = cv2.GaussianBlur(gris(img), (3, 3), 0)
    m = g < 105
    m = quitar_motas(m, 250)
    return suavizar(m, 1.5)


def m_caballo(img):
    b, g, r = cv2.split(img.astype(int))
    negro = (r < 90) & (g < 90) & (b < 90)
    negro = quitar_borde(quitar_motas(negro, 300))
    rojo = (r > 150) & (g < 110) & (b < 110)
    rojo = quitar_motas(cerrar(rojo, 2), 150)
    return suavizar(negro, 1.5), suavizar(rojo, 1.0)


def m_firma(img):
    g = gris(img)
    m = cv2.GaussianBlur(g, (0, 0), 2.5) < 200  # el bolígrafo dejó el trazo punteado
    h, w = m.shape
    m[: int(h * 0.12), : int(w * 0.25)] = False  # la "a" suelta de arriba
    m = cerrar(m, 9)                              # une el trazo punteado
    m = quitar_motas(m, 400)
    m = engrosar(m, 2)                            # grosor mínimo para cortar
    m = suavizar(m, 1.5)
    return np.rot90(m, -1).copy()                 # se lee de izquierda a derecha


# nombre: (archivo, escala, función, alto_o_ancho_en_pulgadas, colores)
RECETAS = {
    "01_monograma_contorno": ("01_monograma.jpg", 2, lambda i: m_monograma(i, False), ("alto", 10)),
    "01_monograma_relleno":  ("01_monograma.jpg", 2, lambda i: m_monograma(i, True),  ("alto", 10)),
    "02_diablita":           ("02_diablita.jpg",  3, m_diablita, ("alto", 8)),
    "03_pegaso":             ("03_pegaso.jpg",    2, m_pegaso,   ("alto", 10)),
    "04_reja":               ("04_reja.jpg",      2, m_reja,     ("alto", 12)),
    "05_caballo_trebol":     ("05_caballo_trebol.jpg", 2, m_caballo, ("alto", 10)),
    "06_firma":              ("06_firma.jpg",     3, m_firma,    ("ancho", 8)),
}
COLORES = {"05_caballo_trebol": [("negro", "#000000"), ("rojo", "#d8141e")]}


# ---------------------------------------------------------------- trazado
def a_path(mask):
    bm = potrace.Bitmap(~mask)  # potrace rellena lo "oscuro" (valor 0)
    plist = bm.trace(turdsize=10, alphamax=1.0, opticurve=True, opttolerance=0.3)
    d = []
    for c in plist:
        p0 = c.start_point
        d.append(f"M{p0.x:.1f},{p0.y:.1f}")
        for s in c.segments:
            if s.is_corner:
                d.append(f"L{s.c.x:.1f},{s.c.y:.1f}L{s.end_point.x:.1f},{s.end_point.y:.1f}")
            else:
                d.append(f"C{s.c1.x:.1f},{s.c1.y:.1f} {s.c2.x:.1f},{s.c2.y:.1f} {s.end_point.x:.1f},{s.end_point.y:.1f}")
        d.append("Z")
    return "".join(d)


def islas(mask):
    """Piezas de material que quedan sueltas (huecos dentro de lo que se corta)."""
    inv = (~mask).astype(np.uint8)
    n, lab, _, _ = cv2.connectedComponentsWithStats(inv, 4)
    borde = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])))
    return n - len(borde)


def recortar(masks, margen):
    todo = np.zeros_like(masks[0])
    for m in masks:
        todo |= m
    ys, xs = np.nonzero(todo)
    y0, y1 = max(ys.min() - margen, 0), min(ys.max() + margen, todo.shape[0])
    x0, x1 = max(xs.min() - margen, 0), min(xs.max() + margen, todo.shape[1])
    return [m[y0:y1, x0:x1] for m in masks]


def procesar(nombre):
    archivo, escala, fn, (lado, pulg) = RECETAS[nombre]
    img = cv2.imread(str(ORIG / archivo))
    img = cv2.resize(img, None, fx=escala, fy=escala, interpolation=cv2.INTER_CUBIC)
    res = fn(img)
    masks = list(res) if isinstance(res, tuple) else [res]
    masks = recortar(masks, 20)
    h, w = masks[0].shape
    ppi = (h if lado == "alto" else w) / pulg
    W, H = w / ppi, h / ppi
    colores = COLORES.get(nombre, [("negro", "#000000")])
    capas = [(n, col, m, a_path(m)) for (n, col), m in zip(colores, masks)]

    def svg(cs):
        g = "".join(f'<path id="{n}" fill="{col}" fill-rule="evenodd" d="{d}"/>' for n, col, _, d in cs)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.3f}in" height="{H:.3f}in" '
                f'viewBox="0 0 {w} {h}">{g}</svg>\n')

    SVG.mkdir(exist_ok=True)
    (SVG / f"{nombre}.svg").write_text(svg(capas))
    if len(capas) > 1:
        for c in capas:
            (SVG / f"{nombre}_{c[0]}.svg").write_text(svg([c]))
    # trazo más fino (en mm) para avisar si algo es demasiado delgado
    finos = []
    for n, _, m, _ in capas:
        dist = cv2.distanceTransform(m.astype(np.uint8), cv2.DIST_L2, 5)
        finos.append(round(float(np.percentile(dist[dist > 0], 50)) * 2 / ppi * 25.4, 2))
    info = {"nombre": nombre, "pulgadas": [round(W, 2), round(H, 2)],
            "capas": [c[0] for c in capas], "islas": [islas(c[2]) for c in capas],
            "grosor_tipico_mm": finos}
    print(json.dumps(info, ensure_ascii=False))
    return info


if __name__ == "__main__":
    filtro = sys.argv[1] if len(sys.argv) > 1 else ""
    out = [procesar(n) for n in RECETAS if filtro in n]
    if not filtro:
        (SVG / "resumen.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
