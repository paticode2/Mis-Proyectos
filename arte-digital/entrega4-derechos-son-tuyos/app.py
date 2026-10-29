"""
Derechos son tuyos — prototipo de experiencia educativa interactiva.
Arte Digital 1 · Entrega 4.

Ejecutar en local:   streamlit run app.py
Publicar:            Streamlit Community Cloud → New app → este repo → app.py
"""

from pathlib import Path
from urllib.parse import quote

import streamlit as st
import streamlit.components.v1 as components

from content import (
    APP_URL, BRAND, DERECHOS, HOTSPOTS, ORGANIZACIONES, PERFILES,
    PROYECTO_TEXTO, PROYECTO_URL, USO_IA,
)

BASE = Path(__file__).parent

st.set_page_config(
    page_title="Derechos son tuyos",
    page_icon="✊",
    layout="wide",
    initial_sidebar_state="auto",
)

# ---------------------------------------------------------------- estado

DEFAULTS = {
    "pagina": "inicio",       # inicio | derecho | ayuda
    "perfil": None,
    "indice": 0,              # derecho actual
    "completados": set(),     # ids de derechos con actividad completada
    "respuestas": {},         # id -> índice de opción elegida
    "reflexiones": {},        # id -> texto
    "texto_grande": False,
    "alto_contraste": False,
    "reducir_movimiento": False,
    "celebrar": False,
}
for k, v in DEFAULTS.items():
    st.session_state.setdefault(k, v)

S = st.session_state


def ir(pagina, indice=None):
    S.pagina = pagina
    if indice is not None:
        S.indice = indice


# ---------------------------------------------------------------- estilos

def estilos():
    c = dict(BRAND)
    if S.alto_contraste:
        c.update(primario="#000000", acento="#B00020", fondo_suave="#FFFFFF", texto="#000000")
    base_px = 19 if S.texto_grande else 16
    animacion = "none" if S.reducir_movimiento else "aparecer .45s ease-out"
    st.markdown(
        f"""
        <style>
        html, body, [class*="css"] {{ font-size: {base_px}px; }}
        .block-container {{ padding-top: 2rem; max-width: 1100px; }}
        h1, h2, h3 {{ color: {c['primario']}; letter-spacing: -0.01em; }}
        p, li, label {{ color: {c['texto']}; line-height: 1.6; }}

        @keyframes aparecer {{
            from {{ opacity: 0; transform: translateY(12px); }}
            to   {{ opacity: 1; transform: none; }}
        }}
        .entrada {{ animation: {animacion}; }}

        .hero {{
            background: {c['primario']}; color: #fff; border-radius: 18px;
            padding: 2.2rem 2rem; margin-bottom: 1.5rem; animation: {animacion};
        }}
        .hero h1 {{ color: #fff; margin: 0 0 .4rem; font-size: 2.4rem; }}
        .hero p  {{ color: #fff; font-size: 1.15rem; margin: 0; max-width: 46rem; }}
        .hero .lema {{ color: {c['acento'] if not S.alto_contraste else '#fff'};
                       font-weight: 700; text-transform: uppercase; letter-spacing: .08em;
                       font-size: .85rem; margin-bottom: .6rem; }}

        .tarjeta {{
            background: {c['fondo_suave']}; border-radius: 14px; padding: 1.2rem 1.3rem;
            border: 1px solid rgba(0,0,0,.08); height: 100%; animation: {animacion};
        }}
        .tarjeta h4 {{ color: {c['primario']}; margin: 0 0 .4rem; }}

        .migas {{ font-size: .9rem; color: #555; margin-bottom: .3rem; }}
        .migas b {{ color: {c['primario']}; }}

        .derecho-cabecera {{
            display: flex; align-items: center; gap: 1rem; animation: {animacion};
            border-left: 6px solid {c['acento']}; padding-left: 1rem; margin: .5rem 0 1rem;
        }}
        .derecho-cabecera .ico {{ font-size: 3rem; line-height: 1; }}
        .derecho-cabecera h2 {{ margin: 0; }}
        .derecho-cabecera p {{ margin: .2rem 0 0; font-size: 1.1rem; }}

        .consejo {{
            background: #fff; border: 2px dashed {c['acento']}; border-radius: 12px;
            padding: .9rem 1.1rem; margin-top: 1rem;
        }}
        .fuente {{ font-size: .85rem; color: #555; margin-top: .8rem; }}

        .stButton > button, .stLinkButton > a {{
            border-radius: 999px; font-weight: 600; min-height: 2.75rem;
        }}
        .stButton button[kind="primary"],
        .stFormSubmitButton > button[kind="primaryFormSubmit"] {{
            background: {c['primario']}; border-color: {c['primario']};
        }}
        .stButton button[kind="primary"] *,
        .stFormSubmitButton > button[kind="primaryFormSubmit"] * {{ color: #fff !important; }}
        a:focus-visible, button:focus-visible {{
            outline: 3px solid {c['acento']} !important; outline-offset: 2px;
        }}
        @media (max-width: 640px) {{
            .hero {{ padding: 1.5rem 1.2rem; }}
            .hero h1 {{ font-size: 1.8rem; }}
            .derecho-cabecera .ico {{ font-size: 2.2rem; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------- piezas

def logo(org_key, ancho=150):
    org = ORGANIZACIONES[org_key]
    ruta = BASE / org["logo"]
    if ruta.exists():
        st.image(str(ruta), width=ancho, caption=None)
    else:
        # Mientras no estén los logos oficiales, se muestra el nombre (no se recrea la marca).
        st.markdown(f"**{org['nombre']}**")


def progreso_global():
    hechos = len(S.completados)
    total = len(DERECHOS)
    st.progress(hechos / total, text=f"Progreso: {hechos} de {total} derechos completados")


def barra_lateral():
    with st.sidebar:
        st.markdown("### ✊ Derechos son tuyos")
        if S.perfil:
            p = PERFILES[S.perfil]
            st.caption(f"Perfil: {p['icono']} {p['etiqueta']}")
        progreso_global()

        st.markdown("**Navegación**")
        st.button("🏠 Inicio", use_container_width=True, on_click=ir, args=("inicio",),
                  type="primary" if S.pagina == "inicio" else "secondary")

        st.markdown("**Derechos**")
        for i, d in enumerate(DERECHOS):
            hecho = d["id"] in S.completados
            actual = S.pagina == "derecho" and S.indice == i
            # El estado se indica con texto y símbolo, no solo con color.
            marca = "✅" if hecho else "○"
            st.button(
                f"{marca} {i + 1}. {d['titulo']}",
                key=f"nav_{d['id']}",
                use_container_width=True,
                on_click=ir, args=("derecho", i),
                type="primary" if actual else "secondary",
                help="Completado" if hecho else "Pendiente",
            )

        st.divider()
        st.button("❓ Ayuda y configuración", use_container_width=True,
                  on_click=ir, args=("ayuda",),
                  type="primary" if S.pagina == "ayuda" else "secondary")


def compartir(titulo="Derechos son tuyos"):
    texto = f"{titulo}: aprende tus derechos en Puerto Rico"
    url = APP_URL
    st.markdown("#### Compartir este recurso")
    c1, c2, c3, c4 = st.columns(4)
    c1.link_button("WhatsApp", f"https://wa.me/?text={quote(texto + ' ' + url)}", use_container_width=True)
    c2.link_button("Facebook", f"https://www.facebook.com/sharer/sharer.php?u={quote(url)}", use_container_width=True)
    c3.link_button("X / Twitter", f"https://twitter.com/intent/tweet?text={quote(texto)}&url={quote(url)}", use_container_width=True)
    c4.link_button("Correo", f"mailto:?subject={quote(titulo)}&body={quote(texto + ' ' + url)}", use_container_width=True)
    st.caption("O copia el enlace:")
    st.code(url, language=None)


def ilustracion_comunidad():
    """Ilustración SVG propia con puntos interactivos (botones accesibles)."""
    puntos = "".join(
        f"""<button class="pt" style="left:{h['x']}%;top:{h['y']}%"
                aria-label="{h['titulo']}: ver información" data-i="{i}">{i + 1}</button>"""
        for i, h in enumerate(HOTSPOTS)
    )
    datos = [
        {"t": h["titulo"], "d": h["derecho"], "x": h["texto"]} for h in HOTSPOTS
    ]
    import json
    movimiento = "none" if S.reducir_movimiento else "latido 2s infinite"
    html = f"""
    <style>
      * {{ box-sizing: border-box; font-family: system-ui, -apple-system, Segoe UI, sans-serif; }}
      .wrap {{ position: relative; width: 100%; max-width: 900px; margin: 0 auto; }}
      svg {{ width: 100%; height: auto; display: block; border-radius: 14px; }}
      .pt {{
        position: absolute; transform: translate(-50%,-50%);
        width: 44px; height: 44px; border-radius: 50%;
        border: 3px solid #fff; background: {BRAND['acento']}; color: #fff;
        font-weight: 800; font-size: 18px; cursor: pointer;
        box-shadow: 0 2px 8px rgba(0,0,0,.35); animation: {movimiento};
      }}
      .pt[aria-pressed="true"] {{ background: {BRAND['primario']}; animation: none; }}
      .pt:focus-visible {{ outline: 3px solid #000; outline-offset: 3px; }}
      @keyframes latido {{ 0%,100% {{ box-shadow: 0 0 0 0 rgba(228,87,46,.6); }}
                           50% {{ box-shadow: 0 0 0 12px rgba(228,87,46,0); }} }}
      .panel {{
        margin-top: 12px; background: #fff; border-left: 6px solid {BRAND['acento']};
        border-radius: 10px; padding: 14px 16px; box-shadow: 0 2px 10px rgba(0,0,0,.08);
        min-height: 92px; transition: opacity .3s;
      }}
      .panel h4 {{ margin: 0 0 4px; color: {BRAND['primario']}; font-size: 18px; }}
      .panel .der {{ font-size: 13px; text-transform: uppercase; letter-spacing: .06em;
                     color: #6b3a20; font-weight: 700; margin-bottom: 6px; }}
      .panel p {{ margin: 0; color: #1f1f1f; line-height: 1.5; font-size: 16px; }}
      .cont {{ font-size: 13px; color: #555; margin-top: 6px; }}
    </style>
    <div class="wrap">
      <svg viewBox="0 0 900 480" role="img"
           aria-labelledby="t d">
        <title id="t">Ilustración de una comunidad</title>
        <desc id="d">Una calle de pueblo con una escuela a la izquierda, una casa, un edificio
          de gobierno, un kiosco de prensa a la derecha y una plaza al frente con personas
          que sostienen pancartas. Los números marcan lugares que puedes explorar.</desc>
        <rect width="900" height="480" fill="#CFE6F2"/>
        <circle cx="790" cy="80" r="42" fill="#F6C343"/>
        <rect y="300" width="900" height="180" fill="#9BC48A"/>
        <rect y="330" width="900" height="40" fill="#D9D2C3"/>
        <!-- escuela -->
        <rect x="70" y="170" width="190" height="160" fill="#F1E3C6" stroke="#1B3A6B" stroke-width="3"/>
        <polygon points="60,170 165,110 270,170" fill="#B5543A"/>
        <rect x="145" y="260" width="40" height="70" fill="#1B3A6B"/>
        <rect x="95" y="200" width="36" height="30" fill="#fff" stroke="#1B3A6B" stroke-width="2"/>
        <rect x="200" y="200" width="36" height="30" fill="#fff" stroke="#1B3A6B" stroke-width="2"/>
        <text x="165" y="160" text-anchor="middle" font-size="16" font-weight="700" fill="#fff">ESCUELA</text>
        <!-- casa -->
        <rect x="290" y="130" width="70" height="60" fill="#F7B7A3" stroke="#1B3A6B" stroke-width="2"/>
        <polygon points="282,130 325,95 368,130" fill="#1B3A6B"/>
        <!-- gobierno -->
        <rect x="520" y="110" width="170" height="220" fill="#E9ECEF" stroke="#1B3A6B" stroke-width="3"/>
        <polygon points="505,110 605,60 705,110" fill="#1B3A6B"/>
        <g fill="#fff" stroke="#1B3A6B" stroke-width="2">
          <rect x="540" y="140" width="18" height="170"/><rect x="580" y="140" width="18" height="170"/>
          <rect x="620" y="140" width="18" height="170"/><rect x="660" y="140" width="18" height="170"/>
        </g>
        <!-- kiosco -->
        <rect x="690" y="200" width="130" height="130" fill="#FFF" stroke="#1B3A6B" stroke-width="3"/>
        <rect x="680" y="185" width="150" height="25" fill="#E4572E"/>
        <text x="755" y="203" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">PRENSA</text>
        <rect x="705" y="230" width="45" height="60" fill="#DDD" stroke="#333"/>
        <rect x="760" y="230" width="45" height="60" fill="#DDD" stroke="#333"/>
        <!-- plaza con personas -->
        <ellipse cx="450" cy="415" rx="230" ry="45" fill="#E8DCC2"/>
        <g>
          <circle cx="380" cy="360" r="12" fill="#6B4226"/><rect x="370" y="372" width="20" height="40" rx="6" fill="#1B3A6B"/>
          <rect x="350" y="318" width="60" height="30" fill="#fff" stroke="#E4572E" stroke-width="3"/>
          <line x1="380" y1="348" x2="380" y2="372" stroke="#333" stroke-width="3"/>
          <circle cx="450" cy="365" r="12" fill="#C68B59"/><rect x="440" y="377" width="20" height="40" rx="6" fill="#E4572E"/>
          <circle cx="520" cy="360" r="12" fill="#3D2B1F"/><rect x="510" y="372" width="20" height="40" rx="6" fill="#1E7B4A"/>
          <rect x="490" y="318" width="60" height="30" fill="#fff" stroke="#1B3A6B" stroke-width="3"/>
          <line x1="520" y1="348" x2="520" y2="372" stroke="#333" stroke-width="3"/>
        </g>
      </svg>
      {puntos}
    </div>
    <div class="panel" id="panel" aria-live="polite">
      <h4>Explora la comunidad</h4>
      <p>Pulsa los números sobre la ilustración para descubrir qué derecho se vive en cada lugar.</p>
    </div>
    <script>
      const datos = {json.dumps(datos, ensure_ascii=False)};
      const vistos = new Set();
      const panel = document.getElementById('panel');
      document.querySelectorAll('.pt').forEach(b => {{
        b.addEventListener('click', () => {{
          const i = +b.dataset.i, d = datos[i];
          document.querySelectorAll('.pt').forEach(o => o.setAttribute('aria-pressed','false'));
          b.setAttribute('aria-pressed','true');
          vistos.add(i);
          panel.style.opacity = 0;
          setTimeout(() => {{
            panel.innerHTML = `<div class="der">${{d.d}}</div><h4>${{i+1}}. ${{d.t}}</h4><p>${{d.x}}</p>
              <div class="cont">Has descubierto ${{vistos.size}} de ${{datos.length}} lugares.</div>`;
            panel.style.opacity = 1;
          }}, 150);
        }});
      }});
    </script>
    """
    components.html(html, height=720, scrolling=False)


# ---------------------------------------------------------------- páginas

def pagina_inicio():
    st.markdown(
        """
        <div class="hero">
          <div class="lema">Derechos. Son tuyos. Defiéndelos.</div>
          <h1>Conoce tus derechos para poder defenderlos</h1>
          <p>Una experiencia interactiva para aprender, paso a paso, los derechos que
          te protegen en Puerto Rico.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 1. Perfil de usuario
    st.markdown("### 1. ¿Quién eres?")
    st.write("Elige tu perfil para que la experiencia se adapte a ti. Puedes cambiarlo cuando quieras.")
    claves = list(PERFILES)
    elegido = st.radio(
        "Perfil de usuario",
        claves,
        index=claves.index(S.perfil) if S.perfil else None,
        format_func=lambda k: f"{PERFILES[k]['icono']}  {PERFILES[k]['etiqueta']}",
        horizontal=True,
        label_visibility="collapsed",
    )
    if elegido and elegido != S.perfil:
        S.perfil = elegido
        st.rerun()
    if S.perfil:
        st.success(PERFILES[S.perfil]["saludo"], icon="👋")

    # 2. El proyecto
    st.markdown("### 2. Sobre el proyecto")
    st.markdown(PROYECTO_TEXTO)
    c1, c2 = st.columns(2)
    for col, key in ((c1, "ea"), (c2, "cpi")):
        org = ORGANIZACIONES[key]
        with col:
            with st.container(border=True):
                logo(key)
                st.markdown(f"#### {org['nombre']}")
                st.write(org["texto"])
                st.link_button(f"Visitar {org['nombre']} ↗", org["url"])
    st.link_button("Ver el proyecto original en Espacios Abiertos ↗", PROYECTO_URL)

    # 3. Ilustración interactiva
    st.markdown("### 3. Explora la comunidad")
    st.write("Cada lugar de la comunidad está conectado con un derecho.")
    ilustracion_comunidad()

    # 4. Los derechos
    st.markdown("### 4. Elige un derecho para empezar")
    cols = st.columns(2)
    for i, d in enumerate(DERECHOS):
        with cols[i % 2]:
            with st.container(border=True):
                estado = "✅ Completado" if d["id"] in S.completados else "○ Pendiente"
                st.markdown(f"#### {d['icono']} {d['titulo']}")
                st.write(d["resumen"])
                st.caption(estado)
                st.button("Explorar →", key=f"ini_{d['id']}", on_click=ir, args=("derecho", i))

    st.divider()
    compartir()


def pagina_derecho():
    i = S.indice
    d = DERECHOS[i]
    total = len(DERECHOS)

    st.markdown(
        f'<div class="migas">Inicio › Derechos › <b>{i + 1} de {total}: {d["titulo"]}</b></div>',
        unsafe_allow_html=True,
    )
    st.progress((i + 1) / total, text=f"Derecho {i + 1} de {total}")
    st.markdown(
        f"""<div class="derecho-cabecera">
              <div class="ico" role="img" aria-label="{d['imagen_alt']}">{d['icono']}</div>
              <div><h2>{d['titulo']}</h2><p>{d['resumen']}</p></div>
            </div>""",
        unsafe_allow_html=True,
    )

    if not S.perfil:
        st.info("Consejo: elige tu perfil en **Inicio** para ver contenido adaptado a ti.", icon="💡")

    t1, t2, t3, t4 = st.tabs(["📖 Aprende", "🎬 Video", "📄 Documentos", "✏️ Actividad"])

    with t1:
        for parrafo in d["explicacion"]:
            st.markdown(f"- {parrafo}")
        if S.perfil:
            p = PERFILES[S.perfil]
            st.markdown(
                f'<div class="consejo"><b>{p["icono"]} Para ti:</b> {d["consejo"][S.perfil]}</div>',
                unsafe_allow_html=True,
            )
        st.markdown(f'<div class="fuente">Fuentes: {d["fuentes"]}</div>', unsafe_allow_html=True)

    with t2:
        if d["video"]:
            st.video(d["video"])
            st.caption("Activa los subtítulos (CC) en el reproductor si están disponibles.")
            st.link_button("Abrir el video en una pestaña nueva ↗", d["video"])
        else:
            st.warning(
                "Video oficial pendiente de enlazar. En la entrega final aquí se integra "
                "el video de la serie *Derechos. Son tuyos.* correspondiente a este derecho.",
                icon="🎬",
            )
            st.link_button("Ver los videos en Espacios Abiertos ↗", PROYECTO_URL)

    with t3:
        pdfs = list(d["pdfs"])
        carpeta = BASE / "documents"
        for archivo in sorted(carpeta.glob(f"{d['id']}*.pdf")):
            pdfs.append({"titulo": archivo.stem.replace("-", " ").capitalize(), "archivo": archivo})
        if not pdfs:
            st.info("Documentos PDF pendientes de añadir para este derecho.", icon="📄")
            st.link_button("Ver materiales en Espacios Abiertos ↗", PROYECTO_URL)
        for doc in pdfs:
            if "archivo" in doc:
                st.download_button(f"⬇️ Descargar PDF: {doc['titulo']}", doc["archivo"].read_bytes(),
                                   file_name=doc["archivo"].name, mime="application/pdf")
            else:
                st.link_button(f"📄 Abrir PDF: {doc['titulo']} ↗", doc["url"])

    with t4:
        actividad(d)

    st.divider()
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        if i > 0:
            st.button(f"← Anterior: {DERECHOS[i - 1]['titulo']}", on_click=ir,
                      args=("derecho", i - 1), use_container_width=True)
        else:
            st.button("← Volver al inicio", on_click=ir, args=("inicio",), use_container_width=True)
    with c2:
        st.button("🏠 Inicio", on_click=ir, args=("inicio",), use_container_width=True)
    with c3:
        if i < total - 1:
            st.button(f"Siguiente: {DERECHOS[i + 1]['titulo']} →", on_click=ir,
                      args=("derecho", i + 1), type="primary", use_container_width=True)
        else:
            st.button("Terminar →", on_click=ir, args=("inicio",), type="primary",
                      use_container_width=True)

    with st.expander("Compartir este derecho"):
        compartir(d["titulo"])


def actividad(d):
    q = d["pregunta"]
    st.markdown(f"**Pregunta:** {q['texto']}")
    previa = S.respuestas.get(d["id"])
    with st.form(key=f"form_{d['id']}"):
        eleccion = st.radio("Elige una respuesta", range(len(q["opciones"])),
                            format_func=lambda k: q["opciones"][k], index=previa,
                            key=f"radio_{d['id']}")
        enviado = st.form_submit_button("Comprobar respuesta", type="primary")

    if enviado:
        if eleccion is None:
            st.warning("Elige una opción antes de comprobar.", icon="⚠️")
            return
        S.respuestas[d["id"]] = eleccion
        previa = eleccion
        if eleccion == q["correcta"] and d["id"] not in S.completados:
            S.completados.add(d["id"])
            S.celebrar = len(S.completados) == len(DERECHOS)
            st.rerun()  # para que la barra de progreso lateral se actualice ya

    if previa is not None:
        # Retroalimentación con icono y texto (no depende solo del color).
        if previa == q["correcta"]:
            st.success(f"**¡Correcto!** {q['explicacion']}", icon="✅")
            st.caption(f"Has completado este derecho. Llevas {len(S.completados)} de {len(DERECHOS)}.")
        else:
            st.error("**Todavía no.** Revisa la pestaña *Aprende* e inténtalo otra vez.", icon="✖️")

    st.markdown("**Reflexión**")
    prefijo = PERFILES[S.perfil]["reflexion_prefijo"] + " " if S.perfil else ""
    texto = st.text_area(prefijo + d["reflexion"], value=S.reflexiones.get(d["id"], ""),
                         key=f"refl_{d['id']}", placeholder="Escribe aquí tu reflexión (solo la ves tú).")
    if texto != S.reflexiones.get(d["id"], ""):
        S.reflexiones[d["id"]] = texto
    if texto.strip():
        st.caption("✓ Reflexión guardada en esta sesión.")

    if len(S.completados) == len(DERECHOS):
        st.success("🎉 ¡Completaste los 7 derechos! Compártelo para que más personas los conozcan.")


def pagina_ayuda():
    st.markdown('<div class="entrada">', unsafe_allow_html=True)
    st.title("Ayuda y configuración")

    st.markdown("### Accesibilidad")
    # Los widgets usan claves propias: Streamlit borra el estado de un widget al salir
    # de la página, así que el valor se copia a una clave persistente.
    for clave, etiqueta in (("texto_grande", "Texto más grande"),
                            ("alto_contraste", "Alto contraste"),
                            ("reducir_movimiento", "Reducir animaciones")):
        st.toggle(etiqueta, value=S[clave], key=f"w_{clave}",
                  on_change=lambda c=clave: S.__setitem__(c, S[f"w_{c}"]))

    st.markdown("### Perfil")
    claves = list(PERFILES)
    nuevo = st.selectbox("Tu perfil", claves,
                         index=claves.index(S.perfil) if S.perfil else None,
                         format_func=lambda k: f"{PERFILES[k]['icono']} {PERFILES[k]['etiqueta']}",
                         placeholder="Sin elegir")
    if nuevo != S.perfil:
        S.perfil = nuevo
        st.rerun()

    st.markdown("### Cómo usar esta app")
    st.markdown(
        """
- **Dónde estás:** arriba de cada derecho verás la ruta (*Inicio › Derechos › …*) y el número del derecho.
- **Navegar:** usa el menú lateral (en el teléfono, ábrelo con el botón **›** arriba a la izquierda) o los botones *Anterior* / *Siguiente*.
- **Progreso:** la barra del menú lateral muestra cuántos derechos has completado. Un derecho queda ✅ completado al responder bien su pregunta.
- **Videos y documentos:** cada derecho tiene las pestañas **🎬 Video** y **📄 Documentos**. Los enlaces externos están marcados con ↗ y abren una pestaña nueva.
- **Tu información:** tus respuestas y reflexiones solo se guardan mientras la página esté abierta. No se envían a nadie.
        """
    )

    if st.button("Reiniciar mi progreso"):
        S.completados = set()
        S.respuestas = {}
        S.reflexiones = {}
        st.toast("Progreso reiniciado")

    st.markdown("### Créditos")
    st.markdown(
        f"""
- Contenido educativo basado en el proyecto **Derechos. Son tuyos. Defiéndelos.** de
  [Espacios Abiertos ↗]({ORGANIZACIONES['ea']['url']}) y el
  [Centro de Periodismo Investigativo ↗]({ORGANIZACIONES['cpi']['url']}).
  Videos y documentos © de sus autores, enlazados desde sus fuentes oficiales.
- Ilustración de la comunidad: creación propia para este prototipo.
- Rediseño de la experiencia: *[tu nombre]*, Arte Digital 1, Universidad de Puerto Rico.
        """
    )
    st.markdown("### Uso de inteligencia artificial")
    st.write(USO_IA)
    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------------- main

estilos()
barra_lateral()
if S.celebrar:
    S.celebrar = False
    if not S.reducir_movimiento:
        st.balloons()

if S.pagina == "derecho":
    pagina_derecho()
elif S.pagina == "ayuda":
    pagina_ayuda()
else:
    pagina_inicio()
