import random
from datetime import datetime

import requests
import streamlit as st

st.set_page_config(page_title="Smart City AI Challenge", page_icon="🏙️", layout="wide")

st.markdown("""
<style>
.main-title{text-align:center;font-size:2.5rem;font-weight:900;margin-bottom:0}
.subtitle{text-align:center;font-size:1.12rem;color:#555;margin-top:.2rem;margin-bottom:1.5rem}
.sensor-card{border-radius:16px;padding:14px;background:linear-gradient(135deg,#f5f8ff,#eef4ff);border:1px solid #d2ddf2;min-height:105px;margin-bottom:12px}
.ai-card{border-radius:18px;padding:18px;background:linear-gradient(135deg,#f2f7ff,#e9f0ff);border-left:7px solid #4b7bec}
.warning-card{border-radius:18px;padding:18px;background:linear-gradient(135deg,#fff7e6,#fff1cf);border-left:7px solid #f0ad4e;margin-top:16px}
.metric-big{font-size:1.7rem;font-weight:900;text-align:center}
.profile-box{border-radius:20px;padding:24px;background:linear-gradient(135deg,#f8fbff,#edf4ff);border:1px solid #cbdaf5}
</style>
""", unsafe_allow_html=True)

SCENARIOS = [
    {"title":"🚦 Congestión escolar","story":"A las 7:15 AM se detecta alta congestión cerca de una zona escolar. Hay estudiantes cruzando y vehículos detenidos.","sensors":{"Tráfico":"92%","Escuelas cercanas":"3","Velocidad promedio":"8 km/h","Hora crítica":"7:15 AM"},"ai_recommendation":"Activar semáforos inteligentes y priorizar rutas escolares.","ai_confidence":87,"ai_score":12,"options":[
        {"text":"Seguir recomendación IA","score":12,"result":"Los semáforos se ajustaron automáticamente y el flujo escolar mejoró.","impact":"Tráfico -22% | Seguridad +15% | Energía -4%","profile":"ia"},
        {"text":"Habilitar carril reversible","score":15,"result":"La vía adicional redujo la congestión más rápido que la recomendación inicial.","impact":"Tráfico -30% | Seguridad +8% | Coordinación +12%","profile":"automatizacion"},
        {"text":"Enviar alerta a conductores","score":8,"result":"Algunos conductores cambiaron de ruta, pero el problema continuó en la zona escolar.","impact":"Tráfico -12% | Seguridad +6%","profile":"datos"},
        {"text":"No intervenir","score":-8,"result":"La congestión aumentó y se generó riesgo para los peatones.","impact":"Tráfico +15% | Seguridad -18%","profile":"riesgo"}]},
    {"title":"🚑 Emergencia médica","story":"Una ambulancia necesita llegar al hospital. El sistema detecta tráfico alto en la ruta principal.","sensors":{"Ambulancia":"Detectada","Tráfico":"85%","Distancia al hospital":"4 km","Tiempo estimado":"18 min"},"ai_recommendation":"Priorizar ruta de emergencia con semáforos en verde.","ai_confidence":94,"ai_score":14,"options":[
        {"text":"Seguir recomendación IA","score":14,"result":"La ambulancia avanzó con prioridad y llegó antes del tiempo estimado.","impact":"Tiempo -40% | Seguridad +18%","profile":"ia"},
        {"text":"Enviar notificación a conductores","score":9,"result":"Los conductores recibieron la alerta, pero la respuesta fue parcial.","impact":"Tiempo -18% | Seguridad +10%","profile":"software"},
        {"text":"Cerrar intersecciones manualmente","score":11,"result":"La medida ayudó, aunque generó retrasos en otras zonas.","impact":"Tiempo -25% | Tráfico secundario +12%","profile":"automatizacion"},
        {"text":"Mantener tráfico normal","score":-10,"result":"La ambulancia perdió tiempo crítico en las intersecciones.","impact":"Tiempo +20% | Seguridad -25%","profile":"riesgo"}]},
    {"title":"🌧️ Inundación inminente","story":"Sensores de lluvia y drenajes alertan riesgo de inundación en una avenida principal.","sensors":{"Probabilidad de lluvia":"95%","Drenajes":"88% ocupación","Nivel de río":"Alto","Zona vulnerable":"Avenida principal"},"ai_recommendation":"Activar protocolo de inundación y desviar tráfico.","ai_confidence":91,"ai_score":13,"options":[
        {"text":"Seguir recomendación IA","score":13,"result":"El tráfico fue desviado antes de que la avenida se saturara.","impact":"Riesgo -35% | Tráfico controlado","profile":"ia"},
        {"text":"Enviar rutas alternas preventivas","score":12,"result":"La población evitó la zona crítica y el impacto fue moderado.","impact":"Tráfico -20% | Ciudadanos +8%","profile":"datos"},
        {"text":"Monitorear solamente","score":3,"result":"La ciudad reaccionó tarde y varias calles se saturaron.","impact":"Riesgo +12% | Respuesta lenta","profile":"datos"},
        {"text":"Ignorar la alerta","score":-12,"result":"La inundación afectó movilidad y seguridad ciudadana.","impact":"Seguridad -25% | Tráfico +30%","profile":"riesgo"}]},
    {"title":"⚡ Apagón energético","story":"El consumo eléctrico supera la capacidad normal y la reserva energética está bajando.","sensors":{"Consumo":"98%","Reserva":"22%","Alumbrado público":"Activo","Demanda residencial":"Alta"},"ai_recommendation":"Reducir alumbrado no crítico y priorizar zonas esenciales.","ai_confidence":82,"ai_score":11,"options":[
        {"text":"Seguir recomendación IA","score":11,"result":"La ciudad redujo consumo sin afectar servicios esenciales.","impact":"Energía +20% | Seguridad estable","profile":"ia"},
        {"text":"Apagar zonas completas","score":-3,"result":"Se ahorró energía, pero aumentaron quejas y riesgos de seguridad.","impact":"Energía +30% | Ciudadanos -18% | Seguridad -12%","profile":"energia"},
        {"text":"Activar respaldo energético","score":14,"result":"El respaldo estabilizó el sistema y evitó apagones mayores.","impact":"Energía +25% | Continuidad +18%","profile":"energia"},
        {"text":"No intervenir","score":-10,"result":"La red se sobrecargó y ocurrió un corte parcial.","impact":"Energía -30% | Ciudadanos -20%","profile":"riesgo"}]},
    {"title":"🌫️ Mala calidad del aire","story":"La ciudad detecta contaminación elevada por acumulación vehicular.","sensors":{"AQI":"180","Vehículos":"Alto","Viento":"Bajo","Zona afectada":"Centro urbano"},"ai_recommendation":"Optimizar semáforos para reducir tiempo de motores encendidos.","ai_confidence":89,"ai_score":12,"options":[
        {"text":"Seguir recomendación IA","score":12,"result":"Los tiempos de espera bajaron y la contaminación empezó a reducirse.","impact":"AQI -18% | Tráfico -15%","profile":"ia"},
        {"text":"Promover transporte compartido","score":9,"result":"La medida ayuda, pero su efecto no es inmediato.","impact":"AQI -8% | Participación ciudadana +10%","profile":"software"},
        {"text":"Aplicar restricción vehicular temporal","score":15,"result":"La contaminación bajó rápido, aunque hubo molestias ciudadanas.","impact":"AQI -28% | Ciudadanos -6%","profile":"datos"},
        {"text":"No hacer nada","score":-10,"result":"La calidad del aire siguió empeorando.","impact":"AQI +15% | Salud pública -15%","profile":"riesgo"}]},
    {"title":"🌡️ Ola de calor","story":"La temperatura sube y el consumo eléctrico se dispara por uso de aire acondicionado.","sensors":{"Temperatura":"39°C","Consumo energético":"90%","Centros educativos":"Activos","Riesgo salud":"Medio-Alto"},"ai_recommendation":"Activar enfriamiento inteligente en edificios públicos.","ai_confidence":84,"ai_score":11,"options":[
        {"text":"Seguir recomendación IA","score":11,"result":"Los edificios críticos bajaron temperatura sin exceder demasiado el consumo.","impact":"Riesgo salud -18% | Energía -8%","profile":"ia"},
        {"text":"Abrir refugios climáticos","score":14,"result":"La población vulnerable recibió atención y se redujo el riesgo de salud.","impact":"Salud +22% | Ciudadanos +14%","profile":"energia"},
        {"text":"Reducir consumo eléctrico general","score":4,"result":"Se protegió la red eléctrica, pero aumentó la incomodidad ciudadana.","impact":"Energía +18% | Ciudadanos -12%","profile":"energia"},
        {"text":"No actuar","score":-9,"result":"El calor afectó a la población y aumentó la demanda eléctrica.","impact":"Riesgo salud +20% | Energía -15%","profile":"riesgo"}]},
    {"title":"🏟️ Evento masivo","story":"Un evento deportivo reúne a miles de personas y el tráfico aumenta alrededor del estadio.","sensors":{"Asistencia":"25,000","Tráfico":"88%","Parqueos":"92% ocupados","Hora de salida":"Próxima"},"ai_recommendation":"Desviar tráfico automáticamente y activar rutas de salida.","ai_confidence":86,"ai_score":12,"options":[
        {"text":"Seguir recomendación IA","score":12,"result":"Las rutas automáticas distribuyeron mejor la salida del evento.","impact":"Tráfico -24% | Orden +15%","profile":"ia"},
        {"text":"Habilitar transporte público gratuito","score":16,"result":"Muchos asistentes evitaron usar vehículo particular.","impact":"Tráfico -35% | Ciudadanos +18%","profile":"software"},
        {"text":"Abrir rutas temporales","score":10,"result":"Las rutas ayudaron, aunque faltó coordinación con parqueos.","impact":"Tráfico -18%","profile":"automatizacion"},
        {"text":"No intervenir","score":-8,"result":"La salida del evento colapsó varias calles.","impact":"Tráfico +25% | Ciudadanos -15%","profile":"riesgo"}]},
    {"title":"💧 Escasez de agua","story":"Los reservorios bajan y el consumo se mantiene alto en varias zonas.","sensors":{"Reservorios":"25%","Consumo":"Alto","Fugas reportadas":"12","Pronóstico lluvia":"Bajo"},"ai_recommendation":"Aplicar distribución inteligente y detectar fugas prioritarias.","ai_confidence":90,"ai_score":14,"options":[
        {"text":"Seguir recomendación IA","score":14,"result":"El sistema priorizó zonas críticas y redujo pérdidas por fugas.","impact":"Agua +22% | Equidad +14%","profile":"ia"},
        {"text":"Racionamiento general","score":6,"result":"El consumo bajó, pero la medida afectó a todos por igual.","impact":"Agua +18% | Ciudadanos -15%","profile":"energia"},
        {"text":"Reparar fugas críticas primero","score":16,"result":"La recuperación fue efectiva al atacar el mayor desperdicio.","impact":"Agua +28% | Eficiencia +20%","profile":"datos"},
        {"text":"No actuar","score":-11,"result":"Los niveles siguieron bajando y aumentó el riesgo de desabastecimiento.","impact":"Agua -25% | Ciudadanos -20%","profile":"riesgo"}]},
    {"title":"🅿️ Saturación de parqueos","story":"El centro urbano está lleno y los vehículos dan vueltas buscando espacios.","sensors":{"Ocupación parqueos":"98%","Vehículos en espera":"400","Velocidad promedio":"10 km/h","Emisiones":"Altas"},"ai_recommendation":"Mostrar espacios disponibles desde una app ciudadana.","ai_confidence":83,"ai_score":11,"options":[
        {"text":"Seguir recomendación IA","score":11,"result":"Los conductores encontraron parqueo con menos vueltas innecesarias.","impact":"Tráfico -18% | Emisiones -10%","profile":"ia"},
        {"text":"Abrir parqueo temporal","score":14,"result":"La capacidad adicional redujo rápidamente la saturación.","impact":"Tráfico -25% | Ciudadanos +12%","profile":"automatizacion"},
        {"text":"Aplicar cobro dinámico","score":7,"result":"La demanda bajó un poco, pero algunos ciudadanos se molestaron.","impact":"Ocupación -12% | Ciudadanos -8%","profile":"datos"},
        {"text":"No actuar","score":-7,"result":"La saturación continuó y aumentaron los bloqueos.","impact":"Tráfico +18% | Emisiones +12%","profile":"riesgo"}]},
    {"title":"🔐 Ciberataque a la ciudad","story":"El centro de monitoreo detecta intentos masivos de acceso contra sistemas municipales.","sensors":{"Intentos de acceso":"15,000","Sistemas afectados":"3","Origen":"Desconocido","Nivel de riesgo":"Crítico"},"ai_recommendation":"Aislar sistemas comprometidos y bloquear tráfico sospechoso.","ai_confidence":96,"ai_score":16,"options":[
        {"text":"Seguir recomendación IA","score":16,"result":"El ataque fue contenido sin apagar servicios esenciales.","impact":"Riesgo -40% | Continuidad +20%","profile":"ciberseguridad"},
        {"text":"Desconectar toda la red","score":7,"result":"El ataque se detuvo, pero también se interrumpieron servicios importantes.","impact":"Riesgo -45% | Servicios -30%","profile":"ciberseguridad"},
        {"text":"Monitorear sin intervenir","score":-6,"result":"El ataque avanzó mientras se observaba la situación.","impact":"Riesgo +25% | Sistemas afectados +2","profile":"datos"},
        {"text":"Ignorar alerta","score":-15,"result":"El ataque comprometió más sistemas de la ciudad.","impact":"Riesgo +50% | Servicios -35%","profile":"riesgo"}]}
]

def get_webhook_url():
    try:
        return st.secrets["apps_script_webhook_url"]
    except Exception:
        return ""

def post_to_apps_script(payload, action="save"):
    url = get_webhook_url()
    if not url:
        st.session_state.sheet_error = "No se configuró apps_script_webhook_url en Secrets."
        return None

    try:
        payload["action"] = action
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as error:
        st.session_state.sheet_error = str(error)
        return None

def save_score_to_google_sheets():
    data = {
        "fecha_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nombre": st.session_state.player_name,
        "colegio": st.session_state.player_school,
        "puntaje_participante": st.session_state.human_score,
        "puntaje_ia": st.session_state.ai_score,
        "resultado": get_final_comparison(),
        "perfil": get_engineering_profile(),
        "decisiones_superiores_ia": st.session_state.beat_ai_count,
        "decisiones_iguales_ia": st.session_state.tie_ai_count,
        "decisiones_inferiores_ia": st.session_state.lost_ai_count,
    }
    response = post_to_apps_script(data, action="save")
    return bool(response and response.get("status") == "ok")

def get_ranking(limit=10):
    response = post_to_apps_script({"limit": limit}, action="ranking")
    if response and response.get("status") == "ok":
        return response.get("ranking", [])
    return []

def init_game():
    st.session_state.selected_scenarios = random.sample(SCENARIOS, 6)
    st.session_state.current_index = 0
    st.session_state.human_score = 0
    st.session_state.ai_score = 0
    st.session_state.beat_ai_count = 0
    st.session_state.tie_ai_count = 0
    st.session_state.lost_ai_count = 0
    st.session_state.history = []
    st.session_state.game_started = False
    st.session_state.story_seen = False
    st.session_state.game_finished = False
    st.session_state.score_saved = False
    st.session_state.last_result = None
    st.session_state.profile_counter = {"ia":0,"datos":0,"software":0,"automatizacion":0,"energia":0,"ciberseguridad":0,"riesgo":0}

def reset_keep_player():
    name = st.session_state.get("player_name", "")
    school = st.session_state.get("player_school", "")
    init_game()
    st.session_state.player_name = name
    st.session_state.player_school = school
    st.session_state.game_started = True
    st.session_state.story_seen = True

def current_scenario():
    return st.session_state.selected_scenarios[st.session_state.current_index]

def choose_option(option):
    scenario = current_scenario()
    human_points = option["score"]
    ai_points = scenario["ai_score"]
    st.session_state.human_score += human_points
    st.session_state.ai_score += ai_points

    if human_points > ai_points:
        comparison = "✅ Superaste a la IA en este escenario."
        st.session_state.beat_ai_count += 1
    elif human_points == ai_points:
        comparison = "➖ Empataste con la IA en este escenario."
        st.session_state.tie_ai_count += 1
    else:
        comparison = "🤖 La IA obtuvo mejor resultado en este escenario."
        st.session_state.lost_ai_count += 1

    profile = option.get("profile", "riesgo")
    st.session_state.profile_counter[profile] = st.session_state.profile_counter.get(profile, 0) + 1

    st.session_state.last_result = {
        "scenario": scenario["title"],
        "choice": option["text"],
        "result": option["result"],
        "impact": option["impact"],
        "human_points": human_points,
        "ai_points": ai_points,
        "comparison": comparison
    }
    st.session_state.history.append(st.session_state.last_result)
    st.session_state.current_index += 1
    if st.session_state.current_index >= len(st.session_state.selected_scenarios):
        st.session_state.game_finished = True

def get_final_comparison():
    if st.session_state.human_score > st.session_state.ai_score:
        return "Participante superó a la IA"
    if st.session_state.human_score == st.session_state.ai_score:
        return "Empate con la IA"
    return "IA superó al participante"

def get_engineering_profile():
    counter = st.session_state.get("profile_counter", {})
    best = max(counter, key=counter.get) if counter else "riesgo"
    profiles = {
        "ia":"Ingeniería en Inteligencia Artificial",
        "datos":"Ingeniería de Datos",
        "software":"Ingeniería de Software",
        "automatizacion":"Ingeniería en Automatización",
        "energia":"Ingeniería en Energía y Sostenibilidad",
        "ciberseguridad":"Ingeniería en Ciberseguridad",
        "riesgo":"Ingeniería en Sistemas Inteligentes"
    }
    return profiles.get(best, "Ingeniería en Sistemas Inteligentes")

def get_profile_explanation():
    explanations = {
        "Ingeniería en Inteligencia Artificial":"Tus decisiones se apoyaron en análisis predictivo, recomendaciones automatizadas y modelos inteligentes.",
        "Ingeniería de Datos":"Priorizaste métricas, monitoreo, evidencias y análisis de información para decidir.",
        "Ingeniería de Software":"Seleccionaste soluciones basadas en aplicaciones, plataformas digitales y servicios para usuarios.",
        "Ingeniería en Automatización":"Preferiste mecanismos de control automático, sensores, rutas inteligentes y procesos optimizados.",
        "Ingeniería en Energía y Sostenibilidad":"Te enfocaste en eficiencia, recursos críticos, sostenibilidad y continuidad operativa.",
        "Ingeniería en Ciberseguridad":"Destacaste en decisiones de protección, aislamiento, continuidad y respuesta ante incidentes.",
        "Ingeniería en Sistemas Inteligentes":"Tu perfil combina varias áreas de ingeniería aplicada a sistemas complejos."
    }
    return explanations.get(get_engineering_profile(), "Tu perfil combina varias áreas de ingeniería aplicada a sistemas complejos.")

def confidence_label(confidence):
    if confidence >= 90:
        return "Alta"
    if confidence >= 80:
        return "Media-Alta"
    return "Media"

def show_scoreboard():
    col1, col2, col3 = st.columns(3)
    col1.metric("👤 Participante", f"{st.session_state.human_score} pts")
    col2.metric("🤖 SmartCity AI", f"{st.session_state.ai_score} pts")
    col3.metric("Escenario", f"{min(st.session_state.current_index + 1, 6)} / 6")

if "human_score" not in st.session_state:
    init_game()
if "player_name" not in st.session_state:
    st.session_state.player_name = ""
if "player_school" not in st.session_state:
    st.session_state.player_school = ""

st.markdown('<h1 class="main-title">🏙️ Smart City AI Challenge</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">¿Podrás tomar mejores decisiones que la Inteligencia Artificial?</p>', unsafe_allow_html=True)

if not st.session_state.game_started:
    left, right = st.columns([1, 1])
    with left:
        st.markdown("## 👋 Inicia tu misión")
        name = st.text_input("Nombre del participante")
        school = st.text_input("Colegio o institución")
        if st.button("🚀 Iniciar Smart City AI Challenge", use_container_width=True):
            if not name.strip():
                st.warning("Ingresa tu nombre para iniciar.")
            elif not school.strip():
                st.warning("Ingresa tu colegio o institución.")
            else:
                st.session_state.player_name = name.strip()
                st.session_state.player_school = school.strip()
                st.session_state.game_started = True
                st.rerun()
        st.markdown("### ¿Cómo funciona?\n1. Verás datos de sensores IoT.\n2. La IA recomendará una acción.\n3. Tú decides si sigues a la IA o eliges otra estrategia.\n4. El sistema compara tu resultado contra la IA.")

    with right:
        st.markdown("## 🏆 Ranking del taller")
        ranking = get_ranking()
        if ranking:
            for index, row in enumerate(ranking, start=1):
                medal = "🥇" if index == 1 else "🥈" if index == 2 else "🥉" if index == 3 else "🏅"
                st.write(f"{medal} **{index}. {row.get('nombre','')}** - {row.get('puntaje_participante',0)} pts")
                st.caption(f"{row.get('colegio','')} | {row.get('perfil','')}")
        else:
            st.info("El ranking aparecerá cuando los participantes terminen el reto.")
            if "sheet_error" in st.session_state:
                st.caption(f"Detalle técnico: {st.session_state.sheet_error}")
    st.stop()

if not st.session_state.story_seen:
    st.markdown("""
    ## 🧠 Tu rol

    Has sido contratado como **Director de Innovación de Smart City Jalapa**.

    Durante los próximos incidentes deberás tomar decisiones para mantener la ciudad funcionando.

    La Inteligencia Artificial te dará una recomendación, pero la decisión final será tuya.

    # ¿Confiarás siempre en la IA?
    """)
    if st.button("Comenzar misión", use_container_width=True):
        st.session_state.story_seen = True
        st.rerun()
    st.stop()

if st.session_state.game_finished:
    if not st.session_state.score_saved:
        st.session_state.score_saved = save_score_to_google_sheets()

    st.markdown("## 🎉 Resultado final")
    col1, col2 = st.columns([1.1, 1])

    with col1:
        st.markdown(f"""
        <div class="profile-box">
            <h2>{st.session_state.player_name}</h2>
            <p><strong>Colegio:</strong> {st.session_state.player_school}</p>
            <h1>👤 {st.session_state.human_score} pts vs 🤖 {st.session_state.ai_score} pts</h1>
            <h3>{get_final_comparison()}</h3>
            <hr>
            <h3>🧠 Perfil detectado</h3>
            <h2>{get_engineering_profile()}</h2>
            <p>{get_profile_explanation()}</p>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.score_saved:
            st.success("Resultado guardado en el ranking.")
        else:
            st.warning("El resultado no se pudo guardar en Google Sheets.")
            if "sheet_error" in st.session_state:
                st.caption(f"Detalle técnico: {st.session_state.sheet_error}")

        if st.button("🔄 Jugar de nuevo", use_container_width=True):
            reset_keep_player()
            st.rerun()

    with col2:
        st.markdown("### Comparación contra IA")
        c1, c2, c3 = st.columns(3)
        c1.metric("Superaste IA", st.session_state.beat_ai_count)
        c2.metric("Empates", st.session_state.tie_ai_count)
        c3.metric("IA ganó", st.session_state.lost_ai_count)

        st.markdown("### 🏆 Top 10")
        ranking = get_ranking()
        if ranking:
            for index, row in enumerate(ranking, start=1):
                medal = "🥇" if index == 1 else "🥈" if index == 2 else "🥉" if index == 3 else "🏅"
                st.write(f"{medal} **{index}. {row.get('nombre','')}** - {row.get('puntaje_participante',0)} pts")
                st.caption(f"{row.get('colegio','')} | {row.get('resultado','')}")
        else:
            st.info("Todavía no hay ranking disponible.")

    st.divider()
    st.markdown("## 📝 Historial de decisiones")
    for item in st.session_state.history:
        st.markdown(f"### {item['scenario']}")
        st.write(f"**Tu decisión:** {item['choice']}")
        st.write(f"**Resultado:** {item['result']}")
        st.write(f"**Impacto:** {item['impact']}")
        st.write(f"👤 Tú: **{item['human_points']} pts** | 🤖 IA: **{item['ai_points']} pts**")
        st.caption(item["comparison"])
    st.stop()

show_scoreboard()

if st.session_state.last_result is not None:
    with st.expander("Resultado del escenario anterior", expanded=False):
        item = st.session_state.last_result
        st.success(item["comparison"])
        st.write(f"**Decisión:** {item['choice']}")
        st.write(f"**Resultado:** {item['result']}")
        st.write(f"**Impacto:** {item['impact']}")
        st.write(f"👤 Tú: **{item['human_points']} pts** | 🤖 IA: **{item['ai_points']} pts**")

scenario = current_scenario()
st.markdown(f"## {scenario['title']}")
st.write(scenario["story"])

left, right = st.columns([1.05, 1])
with left:
    st.markdown("### 📡 Datos de sensores IoT")
    sensor_cols = st.columns(2)
    for i, (label, value) in enumerate(scenario["sensors"].items()):
        with sensor_cols[i % 2]:
            st.markdown(f'<div class="sensor-card"><strong>{label}</strong><div class="metric-big">{value}</div></div>', unsafe_allow_html=True)

    st.markdown("### 🤖 SmartCity AI")
    st.markdown(f"""
    <div class="ai-card">
        <h3>Recomendación</h3>
        <p>{scenario['ai_recommendation']}</p>
        <h3>Confianza IA: {scenario['ai_confidence']}%</h3>
        <p>Nivel: {confidence_label(scenario['ai_confidence'])}</p>
        <p><strong>Puntaje estimado IA:</strong> {scenario['ai_score']} pts</p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown("### 🧑‍💼 Tu decisión")
    st.write("Elige una estrategia. Puedes seguir a la IA o desafiar su recomendación.")
    for option in scenario["options"]:
        if st.button(option["text"], use_container_width=True):
            choose_option(option)
            st.rerun()

    st.markdown('<div class="warning-card"><strong>Pregunta clave:</strong><br>¿La IA siempre tiene la mejor respuesta o el criterio humano puede mejorar la decisión?</div>', unsafe_allow_html=True)

st.divider()
st.markdown("### 🧠 Conceptos que estás experimentando")
st.write("""
**IoT:** sensores que generan datos.  
**IA:** sistema que analiza y recomienda.  
**Humano en el ciclo:** la persona decide si acepta o no la recomendación.  
**Métricas:** cada decisión se evalúa por impacto y puntaje.
""")
st.caption("Versión demostrativa sin hardware. La misma lógica puede conectarse a sensores, APIs, ESP32, Arduino, WiWok u otra plataforma IoT.")