import telebot
import schedule
import time
import pytz
import http.server
import socketserver
import random
import os
from datetime import datetime
from threading import Thread

# ==========================================
# 1. CONFIGURACIÓN (TOKEN NUEVO Y IDs)
# ==========================================
TOKEN = "8375170883:AAEo82_IKNHs9jBErXUhA2BUyH0pMkxV04E"
GRUPO_ID = -1003716695186
ADMIN_ID = 212466214
ZONA_HORARIA = 'Europe/Madrid'

bot = telebot.TeleBot(TOKEN)
madrid_tz = pytz.timezone(ZONA_HORARIA)
FILE_ENVIADAS = "enviadas.txt"
FILE_FRASES_VISTAS = "frases_vistas.txt"

# ==========================================
# 2. SERVIDOR PARA RENDER (PUERTO 10000)
# ==========================================
def run_dummy_server():
    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot Nabil Pro Online")
    
    # Render usa el puerto 10000 por defecto
    port = int(os.environ.get("PORT", 10000))
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"🌍 Servidor activo en puerto {port}")
        httpd.serve_forever()

Thread(target=run_dummy_server, daemon=True).start()

# ==========================================
# 3. LISTA DE 100 FRASES (SIN REPETICIÓN)
# ==========================================
frases_motivadoras = [
    "🚀 El éxito es la suma de pequeños esfuerzos repetidos día tras día.",
    "📈 Opera con el plan, no con la emoción. ¡Disciplina ante todo!",
    "💰 No busques el dinero, busca la habilidad y el dinero te seguirá.",
    "🔥 Los ganadores no son los que nunca fallan, sino los que nunca se rinden.",
    "📊 Gestiona tu riesgo. Perder una batalla no es perder la guerra.",
    "🌟 La paciencia es la clave del éxito en el trading.",
    "📉 Un mal día de trading no define tu carrera. ¡Sigue adelante!",
    "💸 Tu mente es tu activo más valioso. Entrénala bien.",
    "🏆 La constancia separa a los amateurs de los profesionales.",
    "💡 Aprende de tus errores y nunca dejarás de ganar.",
    "🚀 El mercado no te quita el dinero, se lo das tú por falta de disciplina.",
    "📈 Haz del trading un negocio, no un juego de azar.",
    "💰 La libertad financiera comienza con una decisión hoy.",
    "🔥 No cuentes los días, haz que los días cuenten.",
    "📊 El mejor indicador técnico es tu propia psicología.",
    "🌟 Sé humilde cuando ganes y resiliente cuando pierdas.",
    "📉 El trading es 10% técnica y 90% mentalidad.",
    "💸 Tu único competidor es la persona que fuiste ayer.",
    "🏆 El éxito llega para quienes trabajan mientras otros descansan.",
    "💡 No operes por necesidad, opera por oportunidad.",
    "🚀 La disciplina es hacer lo que debes, incluso cuando no quieres.",
    "📈 El trading es el camino más difícil para hacer dinero fácil.",
    "💰 Protege tu capital como si fuera tu vida.",
    "🔥 El miedo y la codicia son los enemigos del trader.",
    "📊 Los gráficos no mienten, las emociones sí.",
    "🌟 El éxito no es el destino, es el proceso.",
    "📉 Si no puedes controlar tus emociones, no puedes controlar tu dinero.",
    "💸 El mercado es una transferencia de dinero de los impacientes a los pacientes.",
    "🏆 La mejor inversión que puedes hacer es en ti mismo.",
    "💡 Simplifica tu estrategia. Menos es más.",
    "🚀 La confianza viene de la preparación.",
    "📈 No persigas el precio, deja que el precio venga a ti.",
    "💰 Una pérdida es una lección pagada.",
    "🔥 Mantén tu mente fría y tu corazón enfocado.",
    "📊 Opera lo que ves, no lo que piensas.",
    "🌟 El trading profesional es aburrido, el trading emocional es caro.",
    "📉 No intentes predecir, intenta reaccionar.",
    "💸 Ganar es genial, pero sobrevivir es vital.",
    "🏆 Sé un maestro de una estrategia, no un aprendiz de cien.",
    "💡 El trading es libertad, pero requiere responsabilidad.",
    "🚀 Visualiza tu éxito y trabaja por él.",
    "📈 Cada vela tiene una historia, aprende a leerla.",
    "💰 Riqueza rápida desaparece rápido. Construye con base.",
    "🔥 Tu plan de trading es tu mapa en la tormenta.",
    "📊 No hay atajos para la maestría.",
    "🌟 Acepta el riesgo o no operes.",
    "📉 El ego es el asesino de cuentas más grande.",
    "💸 Trata el trading como una profesión y te pagará como tal.",
    "🏆 Rendirse no es una opción.",
    "💡 La calidad de tus entradas define la calidad de tu vida.",
    "🚀 Cree en ti mismo cuando nadie más lo haga.",
    "📈 El volumen confirma, el precio manda.",
    "💰 No arriesgues más de lo que puedes permitirte perder.",
    "🔥 La consistencia es el resultado de la disciplina.",
    "📊 El análisis técnico es un mapa, no una bola de cristal.",
    "🌟 Mantente enfocado en el largo plazo.",
    "📉 Corta tus pérdidas y deja correr tus ganancias.",
    "💸 El conocimiento es poder, pero la acción es resultados.",
    "🏆 Los sueños no se cumplen, se trabajan.",
    "💡 Sé agresivo con tus metas y paciente con tus trades.",
    "🚀 Un ganador es un perdedor que lo intentó una vez más.",
    "📈 El mercado siempre tiene la razón.",
    "💰 La riqueza mental precede a la riqueza material.",
    "🔥 Domina tus demonios internos antes de dominar el mercado.",
    "📊 La suerte no existe en el trading, existe la probabilidad.",
    "🌟 Hazlo hoy, mañana podría ser tarde.",
    "📉 Una cuenta pequeña se cuida igual que una grande.",
    "💸 No trabajes por dinero, haz que el dinero trabaje por ti.",
    "🏆 El trading es libertad de tiempo, no solo de dinero.",
    "💡 Tu disciplina determinará tu destino.",
    "🚀 El camino al éxito está en construcción permanente.",
    "📈 Analiza, opera, aprende y repite.",
    "💰 Tu cuenta bancaria refleja tu nivel de disciplina.",
    "🔥 No te compares con otros, compárate con tu ayer.",
    "📊 El mercado es un maestro cruel pero justo.",
    "🌟 La excelencia no es un acto, es un hábito.",
    "📉 Piensa en grande, opera con inteligencia.",
    "💸 Invierte en conocimiento y nunca serás pobre.",
    "🏆 Solo fallas cuando dejas de intentar.",
    "💡 Mantén tu estrategia simple y tu ejecución perfecta.",
    "🚀 El éxito requiere sacrificio.",
    "📈 Escucha lo que el mercado te dice, no lo que quieres oír.",
    "💰 Cada operación es una nueva oportunidad.",
    "🔥 Controla el riesgo y el beneficio vendrá solo.",
    "📊 Sé un francotirador, no un ametrallador.",
    "🌟 La perseverancia vence a la inteligencia.",
    "📉 No te enamores de una operación.",
    "💸 Aprender a no operar es tan importante como operar.",
    "🏆 Los campeones se hacen en los días difíciles.",
    "💡 El trading es un maratón, no un sprint.",
    "🚀 Tu futuro depende de lo que hagas hoy.",
    "📈 Los retrocesos son oportunidades disfrazadas.",
    "💰 La gratitud atrae la abundancia.",
    "🔥 No dejes que un trade defina tu felicidad.",
    "📊 Lee libros, estudia gráficos, mejora siempre.",
    "🌟 La disciplina es el puente entre metas y logros.",
    "📉 Deja de buscar el santo grial y busca tu disciplina.",
    "💸 El trading te enseña quién eres realmente.",
    "🏆 El éxito es inevitable si no te rindes.",
    "💡 ¡Vamos equipo, hoy es un gran día para ganar!"
]

# ==========================================
# 4. FUNCIONES DE ENVÍO Y FIJADO
# ==========================================
def enviar_p_senal():
    try:
        bot.unpin_all_chat_messages(GRUPO_ID)
        carpeta = "imagenes"
        if not os.path.exists(carpeta): os.makedirs(carpeta)
        fotos = [f for f in os.listdir(carpeta) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
        if not fotos: return
        enviadas = []
        if os.path.exists(FILE_ENVIADAS):
            with open(FILE_ENVIADAS, "r") as f: enviadas = f.read().splitlines()
        pendientes = [f for f in fotos if f not in enviadas]
        if not pendientes:
            open(FILE_ENVIADAS, "w").close()
            pendientes = fotos
        foto = random.choice(pendientes)
        ruta = os.path.join(carpeta, foto)
        txt = "✅ *¡SEÑAL EXITOSA!* 🚀\n\nResultados confirmados en **Acciones Vip**. Seguimos sumando en equipo. 💰📈\n\n_Contacta con @nabil para más info._"
        with open(ruta, 'rb') as p:
            msg = bot.send_photo(GRUPO_ID, p, caption=txt, parse_mode="Markdown")
            bot.pin_chat_message(GRUPO_ID, msg.message_id)
        with open(FILE_ENVIADAS, "a") as f: f.write(foto + "\n")
    except Exception as e: print(f"Error señal: {e}")

def enviar_p_frase():
    try:
        bot.unpin_all_chat_messages(GRUPO_ID)
        vistas = []
        if os.path.exists(FILE_FRASES_VISTAS):
            with open(FILE_FRASES_VISTAS, "r") as f: vistas = f.read().splitlines()
        disponibles = [fr for fr in frases_motivadoras if fr not in vistas]
        if not disponibles:
            open(FILE_FRASES_VISTAS, "w").close()
            disponibles = frases_motivadoras
        frase = random.choice(disponibles)
        msg = bot.send_message(GRUPO_ID, f"✨ *MENSAJE DEL DÍA - ACCIONES VIP*\n\n{frase}\n\n💪 ¡Vamos con todo equipo!", parse_mode="Markdown")
        bot.pin_chat_message(GRUPO_ID, msg.message_id)
        with open(FILE_FRASES_VISTAS, "a") as f: f.write(frase + "\n")
    except Exception as e: print(f"Error frase: {e}")

# ==========================================
# 5. HORARIOS (10 FRASES + 2 SEÑALES)
# ==========================================
horas_frases = ["08:30", "10:00", "11:30", "13:00", "15:30", "17:00", "19:30", "20:30", "22:00", "23:00"]
for h in horas_frases:
    schedule.every().day.at(h).do(enviar_p_frase)

schedule.every().day.at("14:30").do(enviar_p_senal)
schedule.every().day.at("18:30").do(enviar_p_senal)

# ==========================================
# 6. COMANDOS (TEST, LINK, REGISTRO)
# ==========================================
@bot.message_handler(commands=['test'])
def test_all(m):
    if m.from_user.id == ADMIN_ID:
        enviar_p_frase()
        bot.reply_to(m, "✅ BOT NABIL ACTIVO. Frase enviada y fijada en el grupo.")

@bot.message_handler(commands=['link'])
def link_command(m):
    txt = "🔗 *ACCESO OFICIAL ACCIONES VIP:*\n\nPulsa aquí para entrar: [TU_LINK_AQUÍ]\n\n¡Te esperamos dentro! 🚀"
    bot.send_message(m.chat.id, txt, parse_mode="Markdown")

@bot.message_handler(commands=['registro'])
def registro_command(m):
    txt = "📝 *PASOS PARA TU REGISTRO:*\n\n1. Regístrate en el enlace oficial.\n2. Completa tu perfil.\n3. Habla con @nabil para activar tu cuenta VIP. 📈"
    bot.send_message(m.chat.id, txt, parse_mode="Markdown")

@bot.message_handler(content_types=['new_chat_members'])
def bienvenida(m):
    try: bot.delete_message(m.chat.id, m.message_id)
    except: pass
    for u in m.new_chat_members:
        if not u.is_bot:
            try: bot.send_message(u.id, f"¡Hola {u.first_name}! 👋 Bienvenido a **Acciones Vip**. Si quieres ganar dinero con nosotros, contacta con @nabil 📈💰", parse_mode="Markdown")
            except: pass

# ==========================================
# 7. BUCLE DE EJECUCIÓN
# ==========================================
def scheduler_loop():
    while True:
        schedule.run_pending()
        time.sleep(30)

Thread(target=scheduler_loop, daemon=True).start()

print("🚀 BOT NABIL PRO TOTALMENTE ACTUALIZADO")
bot.infinity_polling(timeout=20, long_polling_timeout=10)
