"""
Contenido de la app "Derechos son tuyos" (prototipo).

Todo el texto vive aquí para poder editarlo sin tocar app.py.

IMPORTANTE: el contenido de cada derecho es un borrador de prototipo basado en la
Carta de Derechos de la Constitución de Puerto Rico (Art. II) y la Declaración
Universal de Derechos Humanos (DUDH). Antes de entregar hay que:
  - verificarlo contra los materiales oficiales del proyecto
    (https://espaciosabiertos.org/derecho-a-tener-derechos-2/),
  - pegar el enlace oficial de cada video en "video",
  - colocar los PDF oficiales en documents/ o pegar su enlace en "pdfs".
"""

PROYECTO_URL = "https://espaciosabiertos.org/derecho-a-tener-derechos-2/"
EA_URL = "https://espaciosabiertos.org/"
CPI_URL = "https://periodismoinvestigativo.com/"

# Cambia esta URL por la de tu app publicada en Streamlit Community Cloud.
APP_URL = "https://derechos-son-tuyos.streamlit.app"

# Paleta de trabajo. SUSTITUIR por los colores oficiales del manual de marca
# de Espacios Abiertos / CPI (no alterar los colores corporativos).
BRAND = {
    "primario": "#1B3A6B",     # azul profundo (texto de títulos, botones)
    "acento": "#E4572E",       # naranja (llamadas a la acción)
    "fondo_suave": "#F4F1EA",  # crema (tarjetas)
    "texto": "#1F1F1F",
    "exito": "#1E7B4A",
    "error": "#B3261E",
}

ORGANIZACIONES = {
    "ea": {
        "nombre": "Espacios Abiertos",
        "logo": "images/logo-espacios-abiertos.png",
        "url": EA_URL,
        "texto": (
            "Organización sin fines de lucro de Puerto Rico que promueve la "
            "transparencia, el acceso a la información y la participación ciudadana "
            "para fortalecer la democracia y los derechos de las comunidades."
        ),
    },
    "cpi": {
        "nombre": "Centro de Periodismo Investigativo",
        "logo": "images/logo-cpi.png",
        "url": CPI_URL,
        "texto": (
            "Organización periodística sin fines de lucro que investiga y publica "
            "historias de interés público en Puerto Rico, defiende el acceso a la "
            "información y la libertad de prensa, y forma a periodistas y ciudadanía."
        ),
    },
}

PROYECTO_TEXTO = (
    "**Derechos. Son tuyos. Defiéndelos.** es una serie educativa de videos y "
    "materiales complementarios de Espacios Abiertos y el Centro de Periodismo "
    "Investigativo sobre los derechos humanos universales y los derechos "
    "constitucionales en Puerto Rico. Parte de una idea sencilla: no se puede "
    "defender lo que no se conoce."
)

# Perfiles de usuario: cambian el saludo, la forma de presentar los consejos
# y el tipo de reflexión que se propone en cada derecho.
PERFILES = {
    "joven": {
        "etiqueta": "Soy joven o estudiante",
        "icono": "🎒",
        "saludo": "Vamos a ver qué derechos tienes y cómo usarlos en tu día a día.",
        "reflexion_prefijo": "Piensa en tu escuela, tu barrio o tus redes sociales:",
    },
    "comunidad": {
        "etiqueta": "Soy parte de una comunidad u organización",
        "icono": "🏘️",
        "saludo": "Conoce los derechos que protegen a tu comunidad y cómo exigirlos en colectivo.",
        "reflexion_prefijo": "Piensa en tu comunidad o grupo:",
    },
    "educador": {
        "etiqueta": "Soy educador o educadora",
        "icono": "🧑‍🏫",
        "saludo": "Explora cada derecho y usa las actividades para trabajar con tu grupo.",
        "reflexion_prefijo": "Piensa cómo trabajarías esto con tu grupo:",
    },
}

DERECHOS = [
    {
        "id": "tener-derechos",
        "titulo": "El derecho a tener derechos",
        "icono": "✊",
        "imagen_alt": "Personas diversas de pie, juntas, bajo un mismo techo.",
        "resumen": (
            "Es el primer derecho: el que permite que cada persona, sin excepción, "
            "pueda exigir que se protejan todos los demás."
        ),
        "explicacion": [
            "La idea viene de la filósofa Hannah Arendt: antes de cualquier derecho "
            "concreto, toda persona necesita ser reconocida como alguien que tiene derechos.",
            "La Constitución de Puerto Rico abre su Carta de Derechos diciendo que "
            "**la dignidad del ser humano es inviolable** (Art. II, Sec. 1).",
            "La DUDH (Art. 6) reconoce que toda persona, en todas partes, tiene "
            "derecho a que se le reconozca su personalidad jurídica.",
        ],
        "fuentes": "Constitución de PR, Art. II, Sec. 1 · DUDH, Art. 6",
        "consejo": {
            "joven": "Nadie tiene que ganarse sus derechos: los tienes por ser persona.",
            "comunidad": "Una comunidad organizada puede exigir que el gobierno reconozca y proteja a todas las personas.",
            "educador": "Pregunta al grupo: ¿quién decide quién tiene derechos?",
        },
        "pregunta": {
            "texto": "¿Quién tiene derecho a tener derechos?",
            "opciones": [
                "Solo las personas ciudadanas",
                "Toda persona, sin excepción",
                "Solo las personas mayores de edad",
            ],
            "correcta": 1,
            "explicacion": "Los derechos humanos son universales: pertenecen a toda persona por el hecho de serlo.",
        },
        "reflexion": "¿Alguna vez has visto que a alguien se le trate como si no tuviera derechos?",
        "video": "",  # Pega aquí el enlace oficial (YouTube/Vimeo)
        "pdfs": [],   # [{"titulo": "...", "url": "..."}] o archivos en documents/
    },
    {
        "id": "igualdad",
        "titulo": "Igualdad y no discriminación",
        "icono": "⚖️",
        "imagen_alt": "Una balanza equilibrada.",
        "resumen": "Todas las personas son iguales ante la ley y no pueden ser discriminadas.",
        "explicacion": [
            "La Constitución prohíbe el discrimen por **raza, color, sexo, nacimiento, "
            "origen o condición social, ni ideas políticas o religiosas** (Art. II, Sec. 1).",
            "La igualdad no es solo tratar a todos igual: también exige eliminar las "
            "barreras que ponen a algunas personas en desventaja.",
            "Si te discriminan en el empleo, la vivienda o un servicio público, "
            "puedes presentar una queja ante las agencias correspondientes.",
        ],
        "fuentes": "Constitución de PR, Art. II, Sec. 1 · DUDH, Arts. 1, 2 y 7",
        "consejo": {
            "joven": "Si en la escuela te tratan distinto por cómo luces o de dónde vienes, eso tiene nombre: discrimen.",
            "comunidad": "Documentar casos (fechas, testigos, fotos) ayuda a sostener una denuncia colectiva.",
            "educador": "Una dinámica de privilegios (dar un paso al frente) ayuda a ver las desigualdades.",
        },
        "pregunta": {
            "texto": "¿Cuál de estas situaciones es discrimen según la Constitución de PR?",
            "opciones": [
                "Negar un empleo a alguien por sus ideas políticas",
                "Pedir que una persona espere su turno en una fila",
                "Exigir una licencia para conducir un auto",
            ],
            "correcta": 0,
            "explicacion": "Las ideas políticas son una de las razones protegidas: nadie puede ser excluido por ellas.",
        },
        "reflexion": "¿Dónde ves desigualdades que la ley todavía no ha logrado resolver?",
        "video": "",
        "pdfs": [],
    },
    {
        "id": "expresion",
        "titulo": "Libertad de expresión y de prensa",
        "icono": "📢",
        "imagen_alt": "Un megáfono y un periódico.",
        "resumen": "Puedes expresar tus ideas y la prensa puede informar sin censura del gobierno.",
        "explicacion": [
            "La Constitución dice que **no se aprobará ley alguna que restrinja la "
            "libertad de palabra o de prensa** (Art. II, Sec. 4).",
            "Incluye hablar, escribir, publicar en redes, crear arte y criticar al gobierno.",
            "Tiene límites estrechos: por ejemplo, la difamación o las amenazas reales "
            "no están protegidas.",
        ],
        "fuentes": "Constitución de PR, Art. II, Sec. 4 · DUDH, Art. 19",
        "consejo": {
            "joven": "Criticar una decisión del gobierno en tus redes es parte de tu libertad de expresión.",
            "comunidad": "Los medios comunitarios y el periodismo independiente también están protegidos.",
            "educador": "Compara un titular de prensa con una publicación anónima: ¿cómo verificamos?",
        },
        "pregunta": {
            "texto": "¿Qué protege la libertad de prensa?",
            "opciones": [
                "Que el gobierno revise las noticias antes de publicarse",
                "Que los medios puedan informar sin censura del gobierno",
                "Que solo los periodistas puedan opinar",
            ],
            "correcta": 1,
            "explicacion": "La censura previa del gobierno es justo lo que la libertad de prensa prohíbe.",
        },
        "reflexion": "¿Qué tema te gustaría que se investigara y publicara en tu comunidad?",
        "video": "",
        "pdfs": [],
    },
    {
        "id": "reunion",
        "titulo": "Reunión y protesta pacífica",
        "icono": "🪧",
        "imagen_alt": "Personas con pancartas en una plaza.",
        "resumen": "Puedes reunirte pacíficamente y pedir al gobierno que corrija lo que está mal.",
        "explicacion": [
            "La Constitución protege **el derecho del pueblo a reunirse en asamblea "
            "pacífica y a pedir al gobierno la reparación de agravios** (Art. II, Sec. 4).",
            "Protestar, marchar, hacer piquetes y recoger firmas son formas de ejercerlo.",
            "La clave es que sea pacífico. La policía debe proteger la manifestación, no impedirla.",
        ],
        "fuentes": "Constitución de PR, Art. II, Sec. 4 · DUDH, Art. 20",
        "consejo": {
            "joven": "Organizar una reunión de estudiantes para pedir cambios a la escuela es ejercer este derecho.",
            "comunidad": "Antes de una protesta: acuerden roles, tengan contactos de abogados y documenten.",
            "educador": "Analiza con el grupo una protesta histórica de Puerto Rico: ¿qué logró?",
        },
        "pregunta": {
            "texto": "¿Qué condición debe cumplir una reunión para estar protegida?",
            "opciones": [
                "Tener permiso de la policía siempre",
                "Ser pacífica",
                "Tener menos de diez personas",
            ],
            "correcta": 1,
            "explicacion": "La Constitución protege la asamblea pacífica.",
        },
        "reflexion": "¿Qué problema de tu entorno merecería que la gente se organizara para pedir un cambio?",
        "video": "",
        "pdfs": [],
    },
    {
        "id": "intimidad",
        "titulo": "Intimidad y protección contra registros",
        "icono": "🛡️",
        "imagen_alt": "Una casa con un escudo.",
        "resumen": "Tu cuerpo, tu casa, tus papeles y tu teléfono están protegidos contra registros irrazonables.",
        "explicacion": [
            "La Constitución protege a las personas, casas, papeles y efectos contra "
            "**registros, incautaciones y allanamientos irrazonables** (Art. II, Sec. 10).",
            "Por lo general, la policía necesita una **orden judicial** para registrar. "
            "Lo obtenido ilegalmente no puede usarse como prueba.",
            "La Constitución también protege la honra, la reputación y la vida privada (Art. II, Sec. 8).",
        ],
        "fuentes": "Constitución de PR, Art. II, Secs. 8 y 10 · DUDH, Art. 12",
        "consejo": {
            "joven": "Si un agente te pide revisar tu teléfono, puedes decir con calma que no das tu consentimiento.",
            "comunidad": "Grabar a la policía en un espacio público, sin interferir, es una forma de documentar.",
            "educador": "Juego de roles: un intercambio con la policía, qué decir y qué no.",
        },
        "pregunta": {
            "texto": "Por lo general, ¿qué necesita la policía para registrar tu casa?",
            "opciones": [
                "Nada, si sospecha algo",
                "Una orden judicial",
                "El permiso de un vecino",
            ],
            "correcta": 1,
            "explicacion": "La regla general es que un juez debe autorizar el registro con una orden.",
        },
        "reflexion": "¿Qué información tuya consideras privada y quién debería poder verla?",
        "video": "",
        "pdfs": [],
    },
    {
        "id": "debido-proceso",
        "titulo": "Debido proceso",
        "icono": "🏛️",
        "imagen_alt": "La fachada de un tribunal.",
        "resumen": "Nadie puede ser privado de su libertad o propiedad sin un proceso justo.",
        "explicacion": [
            "**Ninguna persona será privada de su libertad o propiedad sin debido "
            "proceso de ley** (Art. II, Sec. 7).",
            "Si te acusan de un delito: tienes derecho a la **presunción de inocencia**, "
            "a **asistencia de abogado**, a un **juicio rápido y público** y a no "
            "declarar en tu contra (Art. II, Sec. 11).",
            "Si no puedes pagar un abogado en un caso criminal, el Estado debe proveerlo.",
        ],
        "fuentes": "Constitución de PR, Art. II, Secs. 7 y 11 · DUDH, Arts. 10 y 11",
        "consejo": {
            "joven": "Si te arrestan: mantén la calma, di que quieres un abogado y no declares nada más.",
            "comunidad": "Tener a mano el contacto de una clínica de asistencia legal puede hacer la diferencia.",
            "educador": "Simula un juicio en el salón para practicar los roles y los derechos.",
        },
        "pregunta": {
            "texto": "Si te acusan de un delito, ¿cómo se te considera hasta que se pruebe lo contrario?",
            "opciones": ["Culpable", "Sospechoso sin derechos", "Inocente"],
            "correcta": 2,
            "explicacion": "La presunción de inocencia obliga al Estado a probar la culpabilidad.",
        },
        "reflexion": "¿Por qué crees que es importante que los juicios sean públicos?",
        "video": "",
        "pdfs": [],
    },
    {
        "id": "informacion",
        "titulo": "Acceso a la información pública",
        "icono": "🔎",
        "imagen_alt": "Una lupa sobre documentos.",
        "resumen": "Puedes pedir y recibir información sobre lo que hace el gobierno.",
        "explicacion": [
            "El Tribunal Supremo de Puerto Rico ha reconocido el acceso a la información "
            "pública como parte de la libertad de expresión (Art. II, Sec. 4).",
            "La **Ley 141-2019** (Ley de Transparencia y Procedimiento Expedito para el "
            "Acceso a la Información Pública) establece cómo pedirla y los plazos para responder.",
            "Sin información no hay participación real: es la base para fiscalizar al gobierno.",
        ],
        "fuentes": "Constitución de PR, Art. II, Sec. 4 · Ley 141-2019 · DUDH, Art. 19",
        "consejo": {
            "joven": "Puedes pedir, por ejemplo, cuánto se gastó en arreglar tu escuela.",
            "comunidad": "Una solicitud de información bien escrita puede revelar datos para defender a tu comunidad.",
            "educador": "Redacten en grupo una solicitud de información real sobre un tema local.",
        },
        "pregunta": {
            "texto": "¿Qué ley de Puerto Rico regula las solicitudes de información pública?",
            "opciones": ["Ley 141-2019", "Ley de Tránsito", "No existe ninguna ley"],
            "correcta": 0,
            "explicacion": "La Ley 141-2019 establece el procedimiento y los plazos para solicitar información pública.",
        },
        "reflexion": "¿Qué información del gobierno te gustaría conocer y para qué la usarías?",
        "video": "",
        "pdfs": [],
    },
]

# Puntos interactivos de la ilustración de la comunidad (posición en % sobre la imagen).
HOTSPOTS = [
    {"x": 18, "y": 42, "titulo": "La escuela", "derecho": "Igualdad y no discriminación",
     "texto": "Todo estudiante merece el mismo trato y las mismas oportunidades, sin importar su origen o condición social."},
    {"x": 50, "y": 62, "titulo": "La plaza", "derecho": "Reunión y protesta pacífica",
     "texto": "La plaza es un espacio público: aquí la gente puede reunirse y pedir cambios de forma pacífica."},
    {"x": 84, "y": 58, "titulo": "El kiosco de prensa", "derecho": "Libertad de expresión y de prensa",
     "texto": "Los medios pueden investigar y publicar sin censura del gobierno."},
    {"x": 36, "y": 26, "titulo": "La casa", "derecho": "Intimidad y protección contra registros",
     "texto": "Tu hogar está protegido: por lo general, la policía necesita una orden judicial para entrar."},
    {"x": 66, "y": 22, "titulo": "El edificio de gobierno", "derecho": "Acceso a la información pública",
     "texto": "Lo que hace el gobierno es asunto de todas las personas: puedes pedir documentos e información."},
]

USO_IA = (
    "Este prototipo se desarrolló con apoyo de inteligencia artificial (Claude, de "
    "Anthropic) para generar una primera versión del código y organizar el contenido. "
    "Las decisiones de UX/UI, la revisión del contenido y la verificación del "
    "funcionamiento son responsabilidad del estudiante."
)
