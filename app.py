import random
import streamlit as st

# ----------------------------
# CONFIGURACIÓN GENERAL
# ----------------------------
st.set_page_config(
    page_title="Smart City Challenge",
    page_icon="🏙️",
    layout="wide"
)

# ----------------------------
# ESTILOS
# ----------------------------
st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 2.4rem;
    font-weight: 800;
    margin-bottom: 0;
}
.subtitle {
    text-align: center;
    font-size: 1.1rem;
    color: #555;
    margin-top: 0;
    margin-bottom: 1.5rem;
}
.city-card {
    border-radius: 18px;
    padding: 18px;
    background: linear-gradient(135deg, #f5f7fa, #e8edf5);
    border: 1px solid #d8dee9;
}
.city-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-top: 12px;
}
.zone {
    min-height: 105px;
    border-radius: 16px;
    padding: 14px;
    text-align: center;
    font-size: 1.05rem;
    font-weight: 700;
    border: 2px solid #d0d7e2;
    background: white;
}
.zone span {
    display: block;
    font-size: 2.2rem;
    margin-bottom: 5px;
}
.good {
    border-color: #78c27a;
    background: #eefbea;
}
.warn {
    border-color: #f0c36a;
    background: #fff7df;
}
.danger {
    border-color: #e57373;
    background: #fff0f0;
}
.event-box {
    border-left: 6px solid #4b7bec;
    padding: 12px 16px;
    background: #f2f6ff;
    border-radius: 10px;
    margin-bottom: 10px;
}
.small-note {
    color: #666;
    font-size: 0.9rem;
}
.score-box {
    font-size: 1.3rem;
    font-weight: 800;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


# ----------------------------
# ESTADO INICIAL
# ----------------------------
def init_game():
    st.session_state.score = 0
    st.session_state.energy = 60
    st.session_state.traffic = 60
    st.session_state.safety = 60
    st.session_state.environment = 60
    st.session_state.citizens = 60
    st.session_state.round = 1
    st.session_state.history = []
    st.session_state.current_event = random.choice(EVENTS)


EVENTS = [
    {
        "title": "🚦 Congestión en la zona escolar",
        "description": "Muchos vehículos están entrando al mismo tiempo. Los estudiantes deben llegar seguros.",
        "actions": {
            "Activar semáforo inteligente": {"traffic": 15, "safety": 10, "energy": -5, "score": 12},
            "Apagar semáforos para ahorrar energía": {"traffic": -20, "safety": -15, "energy": 10, "score": -8},
            "Enviar alerta a conductores": {"traffic": 8, "safety": 8, "energy": -2, "score": 8},
        }
    },
    {
        "title": "💡 Alto consumo de energía nocturna",
        "description": "El alumbrado público está encendido en zonas sin movimiento.",
        "actions": {
            "Activar sensores de movimiento": {"energy": 18, "environment": 8, "safety": 5, "score": 12},
            "Apagar todo el alumbrado": {"energy": 20, "safety": -20, "citizens": -12, "score": -6},
            "Reducir intensidad al 50%": {"energy": 10, "environment": 5, "safety": 2, "score": 7},
        }
    },
    {
        "title": "🌧️ Lluvia intensa en la ciudad",
        "description": "Los sensores reportan riesgo de inundación en una avenida principal.",
        "actions": {
            "Activar monitoreo de drenajes": {"safety": 15, "traffic": 6, "score": 10},
            "Enviar rutas alternas": {"traffic": 15, "citizens": 7, "score": 10},
            "Ignorar la alerta": {"safety": -25, "traffic": -15, "citizens": -15, "score": -12},
        }
    },
    {
        "title": "🅿️ Parqueo saturado",
        "description": "Los visitantes no encuentran parqueo y están bloqueando calles.",
        "actions": {
            "Mostrar espacios disponibles en app": {"traffic": 12, "citizens": 12, "energy": -3, "score": 10},
            "Abrir parqueo inteligente": {"traffic": 10, "citizens": 10, "safety": 4, "score": 9},
            "Cerrar acceso al centro": {"traffic": 5, "citizens": -18, "score": -5},
        }
    },
    {
        "title": "🌫️ Mala calidad del aire",
        "description": "Los sensores ambientales detectan contaminación elevada.",
        "actions": {
            "Optimizar semáforos para reducir tráfico": {"environment": 12, "traffic": 10, "score": 11},
            "Enviar recomendación de transporte compartido": {"environment": 10, "citizens": 6, "score": 8},
            "No hacer nada": {"environment": -20, "citizens": -10, "score": -10},
        }
    }
]

if "score" not in st.session_state:
    init_game()


# ----------------------------
# FUNCIONES
# ----------------------------
def clamp(value):
    return max(0, min(100, value))


def apply_action(action_name, effect):
    for key in ["energy", "traffic", "safety", "environment", "citizens"]:
        if key in effect:
            st.session_state[key] = clamp(st.session_state[key] + effect[key])

    st.session_state.score += effect.get("score", 0)
    st.session_state.history.append(
        f"Ronda {st.session_state.round}: {action_name} | Puntos: {effect.get('score', 0)}"
    )
    st.session_state.round += 1
    st.session_state.current_event = random.choice(EVENTS)


def status_class(value):
    if value >= 70:
        return "good"
    if value >= 40:
        return "warn"
    return "danger"


def emoji_status(value):
    if value >= 70:
        return "🟢"
    if value >= 40:
        return "🟡"
    return "🔴"


def city_visual():
    energy = st.session_state.energy
    traffic = st.session_state.traffic
    safety = st.session_state.safety
    environment = st.session_state.environment
    citizens = st.session_state.citizens

    html = f"""
    <div class="city-card">
        <div class="city-grid">
            <div class="zone {status_class(energy)}"><span>💡</span>Energía<br>{emoji_status(energy)} {energy}%</div>
            <div class="zone {status_class(traffic)}"><span>🚦</span>Tráfico<br>{emoji_status(traffic)} {traffic}%</div>
            <div class="zone {status_class(safety)}"><span>🛡️</span>Seguridad<br>{emoji_status(safety)} {safety}%</div>
            <div class="zone {status_class(environment)}"><span>🌱</span>Ambiente<br>{emoji_status(environment)} {environment}%</div>
            <div class="zone {status_class(citizens)}"><span>🙂</span>Ciudadanos<br>{emoji_status(citizens)} {citizens}%</div>
            <div class="zone good"><span>📡</span>Sensores IoT<br>Activos</div>
            <div class="zone warn"><span>☁️</span>Nube<br>Procesando</div>
            <div class="zone good"><span>📱</span>Control<br>Desde celular</div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def final_result():
    avg = (
        st.session_state.energy +
        st.session_state.traffic +
        st.session_state.safety +
        st.session_state.environment +
        st.session_state.citizens
    ) / 5

    if st.session_state.score >= 45 and avg >= 60:
        return "🏆 Excelente gestión: tu ciudad inteligente funciona muy bien."
    elif st.session_state.score >= 20:
        return "✅ Buena gestión: tomaste varias decisiones correctas."
    else:
        return "⚠️ Tu ciudad necesita mejorar: algunas decisiones afectaron los indicadores."


# ----------------------------
# INTERFAZ
# ----------------------------
st.markdown('<h1 class="main-title">🏙️ Smart City Challenge</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Conviértete en ingeniero de una ciudad inteligente: toma decisiones usando IoT, sensores, datos y automatización.</p>',
    unsafe_allow_html=True
)

left, right = st.columns([1.35, 1])

with left:
    city_visual()

    st.markdown("### 📊 Indicadores de la ciudad")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Energía", f"{st.session_state.energy}%")
    c2.metric("Tráfico", f"{st.session_state.traffic}%")
    c3.metric("Seguridad", f"{st.session_state.safety}%")
    c4.metric("Ambiente", f"{st.session_state.environment}%")
    c5.metric("Ciudadanos", f"{st.session_state.citizens}%")

with right:
    st.markdown("### 🎯 Misión actual")
    event = st.session_state.current_event

    st.markdown(
        f"""
        <div class="event-box">
            <strong>{event['title']}</strong><br>
            {event['description']}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("#### Elige una acción")
    for action_name, effect in event["actions"].items():
        if st.button(action_name, use_container_width=True):
            apply_action(action_name, effect)
            st.rerun()

    st.divider()
    st.markdown(f'<div class="score-box">Puntaje: {st.session_state.score}</div>', unsafe_allow_html=True)
    st.markdown(f"**Ronda:** {st.session_state.round} / 6")

    if st.session_state.round > 5:
        st.success(final_result())
        st.balloons()
        if st.button("🔄 Reiniciar experiencia", use_container_width=True):
            init_game()
            st.rerun()

st.divider()

col_a, col_b = st.columns([1, 1])

with col_a:
    st.markdown("### 🧠 ¿Qué tecnología estás usando?")
    st.write("""
    - **IoT:** dispositivos y sensores conectados.
    - **Datos:** indicadores que ayudan a decidir.
    - **Automatización:** acciones que cambian el comportamiento de la ciudad.
    - **Ingeniería:** diseño de soluciones para problemas reales.
    """)

with col_b:
    st.markdown("### 📝 Historial de decisiones")
    if st.session_state.history:
        for item in reversed(st.session_state.history[-5:]):
            st.write("•", item)
    else:
        st.write("Todavía no has tomado decisiones.")

st.markdown(
    '<p class="small-note">Versión demostrativa sin hardware. La misma lógica puede conectarse luego a LEDs, sensores, ESP32, Arduino o una plataforma IoT real.</p>',
    unsafe_allow_html=True
)