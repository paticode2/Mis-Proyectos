# Ideas para Blender · nombre de Patricia en 3D

Escrito el 27 oct 2026. Cada idea arma el nombre o usuario de Patricia con los materiales que usa en su obra: tachas, imperdibles, gasa, malla, cadenas y tinta.
Donde dice **[NOMBRE]** va el usuario que escoja (ej. `_trama`, `hilo.suelto`, `imperdible_`).
Sirven como guía para hacerlo a mano o como descripción para pegarle a una IA.

## Reglas para todas (de la guía de identidad)
- **Blanco y negro.** Si hay color, es un solo acento: rojo `#A8141E` o rosa `#E0508C`, nunca los dos juntos.
- **Fondo:** negro mate `#171515` o papel `#F2EEE8`. Nada de degradados ni fondos de colores.
- **Letra base:** una sans gruesa y ancha. Unbounded ExtraBold es la del logo provisional; se baja gratis de Google Fonts y se carga en Blender como fuente.
- **Render:** Cycles, 128–256 samples con denoise, color management **AgX** con look **High Contrast**.
- **Tamaños:** post 1080 × 1350 (4:5) · reel 1080 × 1920 (9:16) · foto de perfil 1080 × 1080, con el nombre centrado porque Instagram la recorta en círculo.

---

## 1. Tachas
**La imagen:** el nombre armado con cientos de tachas piramidales de metal cromado, apretadas como en una chaqueta punk, sobre cuero negro mate.

- **Modelado:** texto (Add → Text) → Convert to Mesh. Una tacha: un cono de 4 lados, bajito, con bevel.
- **Geometry Nodes:** Distribute Points on Faces en la cara de arriba de las letras (Poisson Disk, distancia ≈ tamaño de la tacha) → Instance on Points con la tacha → Rotate un poco al azar (±5°) para que se vea hecho a mano.
- **Materiales:** tacha con Principled BSDF, Metallic 1, Roughness 0.12. Fondo plano con textura de cuero (Noise + Bump), negro, Roughness 0.6.
- **Luz:** mundo negro. Una luz de área grande arriba a la izquierda y una de borde (rim) atrás, fina, para que brillen las puntas.
- **Animación para reel (5 s):** la cámara se acerca despacio en diagonal (dolly), con poca profundidad de campo (f/2.8) y el enfoque corriendo por las letras.

## 2. Imperdibles atravesando gasa
**La imagen:** las letras hechas de gasa blanca, deshilachada, con imperdibles plateados que la atraviesan como puntadas.

- **Modelado:** texto → mesh con poco grosor. Un plano subdividido encima con **Cloth** (preset Cotton) que cae sobre las letras (Collision en el texto). Aplicar el cloth en el frame donde se ve bien.
- **Gasa:** material con Alpha a partir de una textura de rejilla (Brick o Wave en bandas) para que se vea el tejido abierto. Los bordes, deshilachados con un Displace de Noise.
- **Imperdibles:** se modelan una vez (curva con bevel + cabeza) y se colocan a mano, 8–12, como si cosieran la gasa a las letras.
- **Luz:** fondo negro, luz suave lateral para que la gasa se vea translúcida.
- **Variante con acento:** un solo imperdible rojo.

## 3. Gasa que cae y revela el nombre (reel en loop)
**La imagen:** un velo de gasa blanca cae lento sobre un nombre invisible y lo dibuja al posarse.

- **Modelado:** texto → mesh, con el objeto oculto en el render (Visibility → Camera off) pero con Collision activo.
- **Cloth:** plano de 100 × 100 subdivisiones, preset Silk, Self Collision on, cae desde arriba en 3 segundos.
- **Loop:** al final la gasa se levanta (viento con Force Field → Wind) y vuelve a empezar. 6–8 segundos en total.
- **Luz:** cenital dura (Spot), sombras marcadas sobre fondo negro, para que el nombre se lea en los pliegues.
- **Para:** el primer reel del plan, o la foto de perfil animada.

## 4. Malla estirada (fishnet)
**La imagen:** letras negras brillantes envueltas con malla de media muy tensa, como piel. Va con su pieza 2026-04.

- **Modelado:** texto → mesh con bevel redondo. Encima, un **Shrinkwrap** de un plano en grilla con **Wireframe** (grosor fino) para hacer la red de diamantes. Un Displace leve para que la malla se hunda entre letras.
- **Materiales:** letras negras con Roughness 0.2 (como látex). Malla negra mate, o **roja** como acento.
- **Cámara:** lente larga (100 mm), casi de frente, mucho detalle en la textura.

## 5. Cadenas colgando
**La imagen:** cada letra cuelga de una cadena fina y se balancea, chocando suave con las otras.

- **Modelado:** cada letra es un objeto aparte (Separate → By Loose Parts). La cadena: un eslabón (toro alargado) con un Array siguiendo una curva.
- **Física:** Rigid Body en las letras (Active) y Rigid Body Constraints tipo Hinge en la cadena. Un empujón inicial a la primera letra.
- **Materiales:** cadena cromada, letras en metal oscuro rayado (Roughness con textura de rayas).
- **Animación:** 6 segundos de balanceo. Sirve como reel o como intro de videos.

## 6. Tinta sobre papel
**La imagen:** el nombre aparece como mancha de tinta negra que se absorbe en papel blanco hueso, como sus obras en papel.

- **Modelado:** un plano con textura de papel (Noise fino en el Bump, color `#F2EEE8`).
- **Tinta:** el texto se usa como máscara (render del texto en blanco y negro, o Text en un plano con Displace). Se mezcla con una foto de su obra 2026-09 (el goteo) como textura de borde, para que la tinta tenga sus manchas reales.
- **Animación:** la máscara crece de 0 a 100 % con un Noise animado en el borde, como tinta que se expande. 4 segundos.
- **Luz:** luz rasante (casi paralela al papel) para que se vea la textura.

---

## Cuál hacer primero
- **Para la foto de perfil:** la 1 (tachas) o la 4 (malla), centradas y en cuadrado.
- **Para el primer reel:** la 3 (gasa que cae), porque se mueve y es suya.
- **Para anunciar el nombre nuevo:** la 2 (imperdibles y gasa), en post 4:5, con el texto "nuevo nombre, misma obra".

## Descripción corta para pegarle a una IA (ejemplo con la idea 1)
> 3D typography of the word "[NOMBRE]" in a wide, heavy sans-serif, the letters fully covered in hundreds of small chrome pyramid studs packed tightly like a punk leather jacket, on a matte black leather surface. Studio lighting: soft key light from top left, thin rim light from behind, black background. Shallow depth of field, focus on the center letters. Monochrome, high contrast, photographic, 4:5 vertical.
