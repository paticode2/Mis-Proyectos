# Kit de Instagram

Plantillas con la identidad de Patricia (colores y fonts de la guía, estilo de la web Archivo).
Los datos de las obras son provisionales (los del inventario); las medidas y el precio van en blanco.

| Archivo | Tamaño | Para qué |
|---|---|---|
| `post_01_obra` | 1080 × 1350 | Presentar una obra: foto grande + ficha (título, técnica, medidas, código) |
| `post_02_disponible` | 1080 × 1350 | Obra a la venta: etiqueta rosa DISPONIBLE + precio |
| `post_03_proceso` | 1080 × 1350 | Proceso: título cortado, dos obras en 1 bit y un texto corto |
| `post_04_cita` | 1080 × 1350 | Una frase suya del statement, con "añoranza" en gótica rosa |
| `carrusel_obra-2026` | 3240 × 1350 | Carrusel de 3 fotos con la obra corrida de una a otra. Ya está cortado en `preview/..._slide1/2/3.png` |
| `story_01_expo` | 1080 × 1920 | Story para anunciar una expo, con espacio para el sticker de enlace |
| `story_02_obra-nueva` | 1080 × 1920 | Story de obra nueva, con espacio para el sticker de pregunta |
| `destacado_01…05` | 1080 × 1920 | Portadas de destacados: Obras, Proceso, Expos, Textil, Contacto |

`feed_mockup.png` muestra cómo se vería el perfil con estas plantillas y los flyers.

## Cómo usarlas
- **Illustrator:** abre `illustrator/*.svg`, cambia la foto (clic en la imagen → Vincular/Reemplazar) y los textos. Guarda como .ai y exporta en PNG o JPG.
- **Photoshop:** `photoshop/*.psd`, una capa por parte. Para cambiar la obra, pon la foto nueva encima de la capa FOTO_OBRA. El texto viene en píxeles.
- Las capas que dicen **borrar** (guías de corte del carrusel, círculo de los destacados) están ocultas en Photoshop; en Illustrator bórralas antes de exportar.
- Carrusel: en Illustrator, Archivo → Exportar → Exportar para pantallas, cortando en 3 mesas de 1080 (o usa los PNG ya cortados).
- Instala antes las fonts de `../08-flyers/fonts/`.

Regla: casi todo en blanco y negro; una pieza de color cada dos o tres posts. Rosa o rojo, nunca los dos.
Para regenerar: `python3 build_instagram.py`.
