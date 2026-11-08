# Cricut · stencils

Diseños pasados a vector (SVG) para cortarlos en la Cricut y usarlos como stencil.
Empezado el 8 nov 2026. Vista previa de todos: [`vista_previa/todos.png`](vista_previa/todos.png).

| Archivo | Tamaño de salida | Piezas sueltas* | Notas |
|---|---|---|---|
| `svg/01_monograma_contorno.svg` | 5.5 × 10 in | 23 | Solo las líneas, como el dibujo. Líneas de ~1 mm: cortar a 10 in o más. |
| `svg/01_monograma_relleno.svg` | 5.5 × 10 in | 17 | Las formas rellenas en negro (estilo tribal). Más fácil de cortar y pintar. |
| `svg/02_diablita.svg` | 6.3 × 8 in | 5 | Silueta (la parte rosa de la imagen). |
| `svg/03_pegaso.svg` | 7.6 × 10 in | 2 | Se quitaron los brillos de la pintura; queda el ojo. |
| `svg/04_reja.svg` | 8 × 12 in | 110 | Muy detallado. Las dos líneas verticales de los lados son finísimas. |
| `svg/05_caballo_trebol.svg` | 6.8 × 10 in | 3 + 1 | Dos colores: `_negro.svg` (caballo) y `_rojo.svg` (tréboles), un stencil por color. |
| `svg/06_firma.svg` | 8 × 1.9 in | 7 | Girada para que se lea horizontal; se le quitó la "a" suelta y se unió el trazo punteado. |

\* **Piezas sueltas (islas):** partes del material que quedan flotando dentro del corte
(el centro de una "O", el ojo del pegaso). Con **vinil adhesivo + transfer tape** no pasa
nada: la cinta las mantiene en su sitio. Con **stencil film / Mylar** (no pega) se caen; en
ese caso hay que añadirles puentes. Pídelo y se hace.

## Cómo usarlos en Cricut Design Space
1. **Upload → Upload Image** → escoge el `.svg`. Sale ya a tamaño real (se puede cambiar).
2. En el lienzo: **Operation = Basic Cut**. Si quieres el diseño en el centro de una hoja,
   añade un cuadrado del tamaño del stencil, ponlo detrás, selecciona ambos y **Slice**.
3. Material: vinil adhesivo (removible, tipo Oracal 631) o stencil vinyl.
4. Cortar → pelar (weed) **lo que va pintado** (las partes negras del SVG) → transfer tape →
   pegar en la superficie → pintar con poca pintura, a toques o con spray en capas finas →
   quitar con la pintura todavía un poco húmeda.
5. Caballo con tréboles: corta el negro y el rojo por separado y pinta un color a la vez.

## Volver a generarlos
`python3 stencil.py` (o `python3 stencil.py pegaso` para uno solo). Cada diseño tiene su
"receta" (limpieza, grosor, tamaño) dentro del script. Los dibujos originales están en
`originales/`.
