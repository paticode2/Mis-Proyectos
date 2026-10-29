# Derechos son tuyos · Prototipo (Arte Digital 1, Entrega 4)

Webapp en Streamlit que rediseña la experiencia educativa de **Derechos. Son tuyos. Defiéndelos.**
(Espacios Abiertos + Centro de Periodismo Investigativo). Fecha de entrega: **3 de diciembre**.

## Archivos
| Archivo | Qué es |
|---|---|
| `app.py` | La aplicación (páginas, navegación, estilos, ilustración interactiva) |
| `content.py` | **Todo el texto**: derechos, preguntas, perfiles, colores, enlaces. Edita aquí. |
| `images/` | Logotipos oficiales (ver `images/LEEME.md`) |
| `documents/` | PDF oficiales (ver `documents/LEEME.md`) |
| `.streamlit/config.toml` | Tema de colores de Streamlit |
| `requirements.txt` | Dependencias para Streamlit Cloud |

## Cómo cumple los requisitos
| Requisito | Dónde |
|---|---|
| Perfil de usuario | Inicio → "¿Quién eres?" (joven, comunidad, educador). Cambia saludo, consejo "Para ti" y la reflexión. |
| Presentación EA, CPI y proyecto | Inicio → "Sobre el proyecto" |
| Información de cada derecho + navegación | 7 derechos; menú lateral, botones Anterior / Siguiente, migas de pan |
| Videos y PDF | Pestañas 🎬 Video y 📄 Documentos de cada derecho |
| Compartir | Botones WhatsApp, Facebook, X, correo y enlace para copiar |
| Ayuda / configuración | Página "Ayuda y configuración" (texto grande, alto contraste, reducir animaciones, perfil, créditos, uso de IA) |
| Actividad por derecho + retroalimentación | Pestaña ✏️ Actividad: pregunta con respuesta correcta/incorrecta y reflexión |
| Indicador de progreso | Barra en el menú lateral + "Derecho X de 7" |
| Animación / transición | Entrada animada de la portada y cabeceras, puntos que laten en la ilustración, transición del panel, globos al completar todo |
| 3+ elementos interactivos sobre una imagen | Inicio → "Explora la comunidad": ilustración propia con 5 puntos |
| Accesibilidad | Texto alternativo en la ilustración, estado con ✅/○ además del color, foco visible, botones grandes, diseño adaptable a móvil |

## Pendiente antes de entregar
1. **Verificar el contenido** de cada derecho en `content.py` contra el sitio oficial:
   https://espaciosabiertos.org/derecho-a-tener-derechos-2/ (el texto actual es un borrador
   basado en la Carta de Derechos de PR y la DUDH; ajusta los derechos a los 7 de la serie).
2. **Videos:** pega el enlace oficial de cada video en el campo `"video"` de cada derecho.
3. **PDF:** pon los PDF en `documents/` o sus enlaces en `"pdfs"`.
4. **Identidad corporativa:** coloca los logos oficiales en `images/` y cambia `BRAND` en
   `content.py` (y `.streamlit/config.toml`) por los colores oficiales.
5. Escribe tu nombre en los créditos (`app.py`, página de ayuda) y pon la URL final en `APP_URL`.

## Publicar en Streamlit Community Cloud
1. Entra a https://share.streamlit.io con tu cuenta de GitHub.
2. **Create app** → repositorio `paticode2/mis-proyectos`, rama donde esté este código (`main` una vez fusionado).
3. **Main file path:** `arte-digital/entrega4-derechos-son-tuyos/app.py`
4. Elige la URL (p. ej. `derechos-son-tuyos`) y pulsa **Deploy**. Ese link es el entregable.

## Probar en local (opcional)
```bash
pip install -r requirements.txt
streamlit run app.py
```
