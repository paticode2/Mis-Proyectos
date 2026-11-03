# Papelería (paso 2)

Nombre: **Patricia Díaz** (hasta que decida el nombre artístico). El correo va en blanco: hay una línea para escribirlo después.

| Pieza | Tamaño | Archivos |
|---|---|---|
| Tarjeta A — **Archivo** (nombre cortado / dorso negro con obra en 1 bit) | 3.5 × 2 in | `illustrator/tarjeta_A_*` · `imprenta/tarjeta_A_archivo.pdf` |
| Tarjeta B — **Tinta** (papel crema, tinta de la 2026-02, acento rojo) | 3.5 × 2 in | `tarjeta_B_*` |
| Tarjeta C — **Rosa** (pintura rosa, la D de Díaz en gótica) | 3.5 × 2 in | `tarjeta_C_*` |
| Membrete | carta 8.5 × 11 | `membrete_carta` |
| Factura / cotización | carta 8.5 × 11 | `factura_cotizacion` |
| Firma de email | — | `firma_email.html` |

## Para la imprenta (tarjetas)
- Los SVG y PDF miden **3.75 × 2.25 in**: ya traen **0.125 in de sangrado** por cada lado. El corte final es 3.5 × 2 in.
- En Illustrator, la capa **GUIAS_borrar** muestra el corte (rosa) y el margen seguro (azul). Bórrala o escóndela antes de exportar; en los PDF ya está escondida.
- Los PDF traen frente (página 1) y dorso (página 2).
- Los colores están en RGB. Si la imprenta pide CMYK: Archivo → Modo de color del documento → CMYK, y revisa el rosa (en CMYK sale un poco más apagado).
- Papel sugerido: 16 pt mate, o algodón de 600 g si se quiere más fino.
- Antes de imprimir: escribir el correo, y si ya hay nombre artístico, cambiarlo.

## Membrete y factura
- `[Nombre de la LLC]` en el pie: cambiarlo cuando esté registrada.
- Factura: número, fecha, cliente, obras, subtotal, **IVU 11.5 % (si aplica)**, envío, total, formas de pago y notas (certificado de autenticidad, derechos de reproducción, depósito). Rafael (CPA) confirma lo del IVU.
- Para usarla en el día a día se puede abrir el PDF y llenarlo, o editar el SVG en Illustrator.

## Firma de email
Abre `firma_email.html` en el navegador, selecciona todo, copia y pega en Gmail → Configuración → Firma. Cambia `[correo]`.

Para regenerar todo: `python3 build_papeleria.py`. Las fonts están en `../08-flyers/fonts/`.
