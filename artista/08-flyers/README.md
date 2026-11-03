# Flyers (borradores para seguir editando)

Las fechas, los lugares y los otros artistas son **inventados**: son para probar el formato.
Tamaño: 1080 × 1350 px (post de Instagram 4:5).

| # | Flyer | Estilo | Acento |
|---|---|---|---|
| 01 | **Gasa Negra**: individual en El Local, Santurce · vie 11 dic 2026 | Web *Archivo*: pliego escaneado, titular estirado con glitch, obra en trama de 1 bit | solo blanco y negro |
| 02 | **Malla**: colectiva + DJ en El Local · sáb 16 ene 2027 | Web *Archivo en vivo*: pintura rosa, letras con una gótica y una al revés, marco de Illustrator | rosa |
| 03 | **Lo que queda de la mano**: colectiva en Galería Hollín, Calle Cerra · vie 5 feb 2027 | Guía de identidad: papel, tinta de la obra 2026-10, Unbounded + Bricolage | rojo |
| 04 | **Estudio abierto**: Trama, Calle Loíza · sáb 13 mar 2027 | Programa con horas, fondo tinta, columna con la obra 2026-03 | rosa |

## Carpetas
- `illustrator/*.svg`: **para Illustrator.** Archivo → Abrir. El texto se puede editar y cada parte es un grupo con nombre (FONDO, TITULO, INFO, LINEUP…). Guárdalo como .ai.
- `photoshop/*.psd`: **para Photoshop.** Una capa por parte, con el mismo nombre. Ojo: aquí el texto está en píxeles (no se edita); para cambiar el texto, usa el SVG, o arrastra el SVG dentro de Photoshop (queda como objeto inteligente vectorial).
- `preview/*.png`: cómo se ven.
- `fonts/`: **instala estas fonts antes de abrir** (doble clic → Instalar): Arimo, Unbounded, Bricolage Grotesque, IBM Plex Mono y UnifrakturMaguntia. Son gratis (Google Fonts, licencia OFL).

## Colores (guía de identidad)
Papel `#F2EEE8` · Tinta `#171515` · Rosa `#E0508C` (sobre papel: `#B0195C`) · Rojo `#A8141E` · Blanco `#FFFFFF` · Negro `#0D0D0D`.
Regla: mucho blanco, el negro para el nombre y los textos, **un solo acento: rosa o rojo, nunca los dos.**

## Volver a generarlos
`python3 build_flyers.py` (necesita pillow, psd-tools y playwright). Los textos, fechas y artistas están arriba de cada función `flyer_...`.
Para imprimir en grande, cambia las fotos por las de `02-fotos-obras/originales/`.
