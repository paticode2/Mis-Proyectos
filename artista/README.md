# Patricia · perfil profesional de artista

Proyecto para preparar a Patricia como artista profesional: inventario de obras, fotos, portafolio, web con tienda y lista de oportunidades para exhibir.

**Empieza aquí:** lee `LOG_ARTISTA_PATRICIA.txt` (estado actual, hecho, pendiente, hoja de ruta) y `PLAN.md`.

| Carpeta | Qué hay |
|---|---|
| `01-inventario/` | `inventario_obras.xlsx` – 12 obras (títulos provisionales) |
| `02-fotos-obras/` | `originales/` y `web/` (1600 px) |
| `03-identidad-visual/` | referencias de diseño |
| `04-documentos/` | portafolio PDF (borrador) y entrevista para el statement |
| `06-web/sitio/` | la web (`index.html`) y la landing para el teléfono (`ad.html`) |
| `06-web/sitio/compartir/` | las mismas páginas con las fotos dentro: estas son las que se publican |
| `07-exhibicion/` | `oportunidades.xlsx` – galerías, convocatorias y becas |
| `presentacion/` | la presentación (slides en HTML) |

## Seguir trabajando con Claude
Abre este repo en **claude.ai/code** (funciona en el navegador, no hay que instalar nada) y di:
"sigue con lo de Patricia: lee artista/LOG_ARTISTA_PATRICIA.txt".

## Editar la web
1. Edita `06-web/sitio/index.html` o `ad.html` (las fotos están en `06-web/sitio/img/`).
2. Corre `python .inline_fotos.py` (necesita `pip install pillow`) para regenerar `compartir/`.

Todo es borrador: faltan títulos, técnicas, medidas, precios, la bio y 2 obras (2026-11 y 2026-12).
