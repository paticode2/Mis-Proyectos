# Cricut · stencils

Empezado el 8 nov 2026.

## Hoja de lápiz de Patricia (separada por motivos)
Su dibujo `originales/07_hoja_lapiz.jpg`, separado en 9 motivos, cada uno en su SVG
(`svg/hoja/`). Vista previa: [`vista_previa/hoja_lapiz.png`](vista_previa/hoja_lapiz.png).
Lo genera `hoja.py`.

- **`_linea.svg`**: el trazo de lápiz redibujado con un grosor parejo de ~1.8 mm (se corta
  la línea y el stencil pinta la línea).
- **`_relleno.svg`** (corona, estrella y trío de estrellas): la forma rellena en sólido.

| Motivo | Tamaño | Versiones |
|---|---|---|
| 01 Corona | 5 × 1.9 in | línea, relleno (manchas como huecos) |
| 02 Espirales | 5 × 1.75 in | línea |
| 03 Enredadera izquierda | 3.7 × 11 in | línea |
| 04 Tribal de arriba | 5.2 × 5.2 in | línea |
| 05 Enredadera derecha | 2.6 × 6.1 in | línea |
| 06 Estrella grande | 2.8 × 5 in | línea, relleno. **Redibujada limpia** con las mismas puntas, porque en la foto el lápiz estaba claro y repasado. |
| 07 Trío de estrellas | 4.2 × 5 in | línea, relleno |
| 08 Garras | 4 × 5 in | línea (unos trazos muy claros salen cortados) |
| 09 Rizos | 4.9 × 5 in | línea |

Los tamaños se pueden cambiar en Design Space; si se achican mucho, la línea se vuelve más
fina que 1 mm y cuesta pelarla.

## Diseños nuevos estilo cybersigilism
Originales, hechos a partir del estilo de las referencias (`referencias/` y `originales/`):
espinas afiladas, simetría en espejo, estrellas de puntas largas, rizos y la red orgánica
del cuaderno. Vista previa: [`vista_previa/sigilos_nuevos.png`](vista_previa/sigilos_nuevos.png).
Los genera `sigilos.py`; cambiando la semilla de cada uno salen variantes distintas.

| Archivo `svg/nuevos/` | Tamaño | Piezas sueltas* | Qué es |
|---|---|---|---|
| `sigilo_01_espina_dorsal.svg` | 6 × 11 in | 12 | Columna afilada con garras curvas a los dos lados, en espejo. |
| `sigilo_02_tres_estrellas.svg` | 5.8 × 10.3 in | 4 | Tres estrellas de puntas largas unidas por una línea que serpentea y se enrosca. |
| `sigilo_03_red.svg` | 8.7 × 10.7 in | 16 / 1 | Red orgánica con membranas en las uniones. Dos colores: `_negro.svg` y `_rosa.svg` (estrellitas). |
| `sigilo_04_corona.svg` | 7 × 8.8 in | 7 | Halo de espinas con una estrella al centro. |
| `sigilo_05_alas.svg` | 10 × 8 in | 2 | Alas de garras en espejo alrededor de una estrella. |
| `sigilo_06_rizos.svg` | 4.7 × 10.9 in | 29 | Panel vertical de rizos y estrellas (mezcla de la reja con los sigilos). |

## Diseños subidos, pasados a vector
Vista previa: [`vista_previa/todos.png`](vista_previa/todos.png).

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
`python3 sigilos.py` para los nuevos; `python3 stencil.py` (o `python3 stencil.py pegaso`
para uno solo) para los subidos. Cada diseño tiene su
"receta" (limpieza, grosor, tamaño) dentro del script. Los dibujos originales están en
`originales/`.
