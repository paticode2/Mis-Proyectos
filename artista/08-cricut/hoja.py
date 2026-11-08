"""Separa los motivos de la hoja de lápiz (originales/07_hoja_lapiz.jpg) y los
convierte en SVG para Cricut, cada uno por separado.

Uso:  python3 hoja.py           (todos)
      python3 hoja.py estrella  (solo los que contengan esa palabra)

- Versión "linea": el trazo de lápiz se redibuja con un grosor parejo (LINEA pulgadas),
  para que la Cricut lo pueda cortar y el stencil pinte la línea.
- Versión "relleno" (estrellas y corona): la forma cerrada se rellena en sólido.
Salida: svg/hoja/<motivo>_linea.svg y <motivo>_relleno.svg
"""
import sys, json, pathlib
import numpy as np
import cv2
from skimage.morphology import skeletonize

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from stencil import a_path, islas

AQUI = pathlib.Path(__file__).parent
OUT = AQUI / "svg" / "hoja"
PPI = 300            # resolución de trabajo al tamaño final
LINEA = 0.07         # grosor de línea en pulgadas (~1.8 mm)
PAGINA_IN = 9.0      # ancho aproximado de la hoja original, para conservar proporciones

# motivo: (esquinas sup-izq de sus piezas en la foto, rectángulo extra opcional, relleno?, tamaño mín/máx)
MOTIVOS = {
    "01_corona":          ([(376, 40)], (360, 30, 900, 235), True),
    "02_espirales":       ([(962, 72), (1165, 67), (1304, 170), (1455, 71)], None, False),
    "03_enredadera_izq":  ([(10, 199), (479, 1519)], None, False),
    "04_tribal_arriba":   ([(650, 238), (1198, 341)], None, False),
    "05_enredadera_der":  ([(1251, 679), (1615, 1689), (1697, 1536)], None, False),
    "06_estrella":        ([(622, 1087), (766, 1694)], None, True),
    "07_estrellas_trio":  ([(439, 1751)], None, True),
    "08_garras":          ([(898, 1381), (1000, 1629), (929, 1749)], None, False),
    "09_rizos":           ([(1100, 1872)], None, False),
}
TAM_MIN, TAM_MAX = 5.0, 11.0   # pulgadas del lado más largo


def separar():
    img = cv2.imread(str(AQUI / "originales" / "07_hoja_lapiz.jpg"))
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    plano = cv2.divide(g, cv2.GaussianBlur(g, (0, 0), 25), scale=255)  # quita la sombra
    m = (plano < 200).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    m[:40] = 0; m[-15:] = 0; m[:, :10] = 0; m[:, -25:] = 0   # bordes y espiral del cuaderno
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    return lab, st


def mascara_motivo(lab, st, esquinas, rect):
    ids = set()
    for (x, y) in esquinas:
        cand = [i for i in range(1, len(st)) if abs(st[i, 0] - x) <= 5 and abs(st[i, 1] - y) <= 5]
        assert cand, f"no encuentro la pieza en {(x, y)}"
        ids.add(max(cand, key=lambda i: st[i, 4]))
    if rect:
        x0, y0, x1, y1 = rect
        for i in range(1, len(st)):
            x, y, w, h, a = st[i]
            if a >= 40 and x >= x0 and y >= y0 and x + w <= x1 and y + h <= y1:
                ids.add(i)
    return np.isin(lab, list(ids))


def estrella_redibujada(forma):
    """La estrella grande está hecha con trazos de lápiz repetidos y claros: se redibuja
    limpia con las mismas puntas (medidas sobre la foto) y lados curvos hacia dentro."""
    ox, oy = 580, 1050
    puntas = np.array([(300, 40), (470, 280), (200, 820), (45, 312)], float) + (ox, oy)  # arriba, der, abajo, izq
    # "cintura" entre cada par de puntas (donde los brazos se unen), medida sobre la foto
    cinturas = np.array([(318, 300), (272, 395), (196, 390), (175, 296)], float) + (ox, oy)
    centro = np.array([240, 335], float) + (ox, oy)
    pts = []
    for i in range(4):
        tramo = [puntas[i], cinturas[i], puntas[(i + 1) % 4]]
        for a, b in zip(tramo[:-1], tramo[1:]):
            mid = (a + b) / 2
            ctrl = mid + 0.18 * (centro - mid)           # lado curvo hacia dentro
            for t in np.linspace(0, 1, 50, endpoint=False):
                pts.append((1 - t) ** 2 * a + 2 * (1 - t) * t * ctrl + t * t * b)
    m = np.zeros(forma, np.uint8)
    cv2.fillPoly(m, [np.round(np.array(pts)).astype(np.int32)], 1, cv2.LINE_AA)
    return m > 0


def rellenar_huecos(m):
    inv = (~m).astype(np.uint8)
    n, lab, _, _ = cv2.connectedComponentsWithStats(inv, 4)
    borde = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])))
    fuera = np.isin(lab, list(borde))
    return m | ~fuera


def disco(r):
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def procesar(nombre, lab, st):
    esquinas, rect, relleno = MOTIVOS[nombre]
    redibujada = nombre == "06_estrella"
    m = estrella_redibujada(lab.shape) if redibujada else mascara_motivo(lab, st, esquinas, rect)
    ys, xs = np.nonzero(m)
    pad = 12
    y0, y1, x0, x1 = ys.min() - pad, ys.max() + pad, xs.min() - pad, xs.max() + pad
    y0, x0 = max(y0, 0), max(x0, 0)
    m = m[y0:y1, x0:x1]
    h, w = m.shape
    ppi_foto = lab.shape[1] / PAGINA_IN
    lado_in = float(np.clip(max(h, w) / ppi_foto, TAM_MIN, TAM_MAX))
    esc = PPI * lado_in / max(h, w)
    grande = cv2.resize(m.astype(np.uint8) * 255, None, fx=esc, fy=esc, interpolation=cv2.INTER_CUBIC)
    grande = cv2.GaussianBlur(grande, (0, 0), esc * 0.8) > 90
    salida = {}

    # versión línea: esqueleto (línea central) + grosor parejo
    esq = skeletonize(grande & ~cv2.erode(grande.astype(np.uint8), disco(2)).astype(bool)) if redibujada else skeletonize(grande)
    r = max(int(LINEA * PPI / 2), 1)
    linea = cv2.dilate(esq.astype(np.uint8), disco(r)) > 0
    linea = cv2.GaussianBlur(linea.astype(np.float32), (0, 0), r * 0.5) > 0.5
    n, l2, s2, _ = cv2.connectedComponentsWithStats(linea.astype(np.uint8), 8)  # quita motas
    linea = np.isin(l2, [i for i in range(1, n) if s2[i, 4] > (3 * r) ** 2])
    salida["linea"] = linea

    if relleno:
        c = cv2.morphologyEx(grande.astype(np.uint8), cv2.MORPH_CLOSE, disco(int(0.06 * PPI))) > 0
        if nombre == "01_corona":
            # corona: contorno exterior relleno, con las manchas como huecos
            n, l3, s3, _ = cv2.connectedComponentsWithStats(grande.astype(np.uint8), 8)
            mayor = 1 + np.argmax(s3[1:, 4])
            fuera = rellenar_huecos(cv2.morphologyEx((l3 == mayor).astype(np.uint8), cv2.MORPH_CLOSE, disco(int(0.06 * PPI))) > 0)
            manchas = rellenar_huecos(grande & (l3 != mayor))
            sol = fuera & ~cv2.dilate(manchas.astype(np.uint8), disco(r)).astype(bool)
        elif redibujada:
            sol = grande
        else:
            sol = rellenar_huecos(c)
        sol = cv2.GaussianBlur(sol.astype(np.float32), (0, 0), PPI * 0.012) > 0.5
        salida["relleno"] = sol

    OUT.mkdir(parents=True, exist_ok=True)
    infos = []
    for tipo, mk in salida.items():
        H, W = mk.shape
        (OUT / f"{nombre}_{tipo}.svg").write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W / PPI:.3f}in" height="{H / PPI:.3f}in" '
            f'viewBox="0 0 {W} {H}"><path fill="#000" fill-rule="evenodd" d="{a_path(mk)}"/></svg>\n')
        infos.append({"archivo": f"{nombre}_{tipo}.svg", "pulgadas": [round(W / PPI, 2), round(H / PPI, 2)],
                      "islas": islas(mk)})
    for i in infos:
        print(json.dumps(i, ensure_ascii=False))
    return infos


if __name__ == "__main__":
    filtro = sys.argv[1] if len(sys.argv) > 1 else ""
    lab, st = separar()
    for nombre in MOTIVOS:
        if filtro in nombre:
            procesar(nombre, lab, st)
