# Stripe: links de pago · guía paso a paso (14 nov 2026)

Stripe no cobra mensualidad: solo 2.9% + 30¢ por venta. Cada producto tiene su propio link; la web Archivo
muestra "Comprar" cuando el link está puesto, y "Escríbenos" mientras no.

## 1. Abrir la cuenta (una sola vez, ~15 min)
1. Entrar a stripe.com → **Start now** → email y contraseña.
2. **Activate payments**: tipo de negocio **Individual / Sole proprietor** (cuando exista la LLC se cambia a Company con el EIN).
3. Datos personales de quien cobra (nombre, dirección en PR, fecha de nacimiento, SSN).
4. **Cuenta de banco** donde Stripe deposita (llega en 2–7 días al principio).
5. **Public details**: nombre del negocio = el nombre artístico; descripción: "Arte original y prints"; Instagram como web si todavía no hay dominio.
6. Activar el recibo por email: Settings → Customer emails → **Successful payments**.

## 1b. Políticas (ya están en la web, sección "Políticas", ancla #politicas)
Envíos · Devoluciones y reembolsos · Obra dañada o perdida · Términos y derechos de autor · Privacidad.
Cuando la web esté pública con su dominio:
- Settings → Public details: poner el link de la web y el de la política (…/#politicas) en **Terms of service** y **Refund policy**.
- En cada Payment link → Advanced: activar **"Require customers to accept your terms of service"**.
No son asesoría legal: conviene que un abogado de PR las revise (sobre todo devoluciones y reglas de DACO) cuando se forme la LLC.

### Quién hace qué cuando entra una venta
| Cosa | Quién |
|---|---|
| Cobro, recibo al cliente, depósito al banco (menos 2.9% + 30¢) | Stripe, automático |
| Tarifas de envío (precio fijo que paga el cliente) | Rafael las crea en Stripe |
| **Etiqueta de envío** | Rafael, aparte: Stripe NO crea etiquetas. Dirección del email de la venta → Pirate Ship o usps.com |
| Empacar con certificado, llevar al correo | Rafael o Patricia |
| Mandar el número de rastreo al cliente | Rafael, por email |
| Marcar "Vendido" en el inventario | Rafael o Claude |

## 2. Tarifas de envío (crear una vez, se reusan en todos los links)
Product catalog → Shipping rates:
| Nombre | Precio | Para |
|---|---|---|
| Recogido en Caguas | $0 | todo |
| Envío en Puerto Rico | $15 | originales |
| Envío a EE. UU. | $45 | originales en papel y lienzo |
| Envío de print | $6 | prints 8×10 |

(Son estimados; ajustarlos cuando se cotice el primer envío real. Ver 04-documentos/plan_ventas_envios.md.)

## 3. Los links (Payment links → New)
En cada link: **Collect customers' addresses → Billing and shipping**, países: **Puerto Rico y Estados Unidos**,
añadir las tarifas de envío que dice la tabla, y en **Advanced → Limit the number of payments** poner el límite.

| Clave en la web | Producto (nombre en Stripe) | Precio | Límite | Envíos |
|---|---|---|---|---|
| `"03"` | Rosa spray · aerosol sobre lienzo · original | $275 | 1 | Caguas, PR, EE. UU. |
| `"04"` | Rojo y negro, mallas · técnica mixta · original | $225 | 1 | Caguas, PR, EE. UU. |
| `"02"` | Manchas negras · original sin marco | $175 | 1 | Caguas, PR, EE. UU. |
| `"05"` | Garabatos y manos · original sin marco | $175 | 1 | Caguas, PR, EE. UU. |
| `"06"` | Trazos horizontales · original sin marco | $175 | 1 | Caguas, PR, EE. UU. |
| `"07"` | Rosa y negro, gestual · original sin marco | $175 | 1 | Caguas, PR, EE. UU. |
| `"08"` | Huellas verticales · original sin marco | $200 | 1 | Caguas, PR, EE. UU. |
| `"09"` | Goteo horizontal · original sin marco | $275 | 1 | Caguas, PR, EE. UU. |
| `"10"` | Manchas diagonales · original sin marco | $200 | 1 | Caguas, PR, EE. UU. |
| `"01"` | Escultura blanca · original | $450 | 1 | **solo Caguas y PR** |
| `"print-03"` | Print 8×10 · Rosa spray · ed. 25 | $35 | 25 | Caguas, print |
| `"print-04"` | Print 8×10 · Rojo y negro · ed. 25 | $35 | 25 | Caguas, print |
| `"print-06"` | Print 8×10 · Trazos horizontales · ed. 25 | $35 | 25 | Caguas, print |
| `"print-07"` | Print 8×10 · Rosa y negro · ed. 25 | $35 | 25 | Caguas, print |

Para empezar basta con **3**: la 03, la 04 y un print. Los demás se crean cuando haga falta.
En cada producto, subir como foto la imagen de `02-fotos-obras/web/`.

## 4. Pegar los links en la web
Mandarle a Claude los links (o pegarlos en `06-web/sitio/archivo.template.html`, en el bloque `const TIENDA`):
```
"03": "https://buy.stripe.com/xxxx",
```
Luego se reconstruye y se vuelve a publicar la web (Archivo y Archivo en vivo).

## 5. Cuando entra una venta
1. Llega el email de Stripe con el nombre y la dirección.
2. Marcar la obra como **Vendido** en el inventario.
3. Empacar (ver plan_ventas_envios.md), con certificado de autenticidad.
4. Si es original: el link ya se apagó solo (límite 1).
5. Si se vende en persona antes que en la web: en Stripe, **desactivar** ese link.

Precio mínimo de negociación de los lienzos (en persona, nunca en la web): 03 → $200, 04 → $175.
