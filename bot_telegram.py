import telebot
import time
import datetime
import pytz
import random
from telebot import types, apihelper
import threading

# ==========================================
# CONFIGURACIÓN TÉCNICA Y PARCHE DE PROXY
# ==========================================
TOKEN = '8375170883:AAGUhVAyyu1lvnx42RscIEuw9opknbKIBX8'
CHAT_ID_GRUPO = '-1003716695186'
MI_ENLACE = "https://qvselp.com/#/pages/auth-signup/index?inviteCode=3LVZ"
MI_USUARIO = "NabilInversiones" 

# ESTO ARREGLA EL ERROR 503 EN PYTHONANYWHERE
apihelper.proxy = {'https': 'http://proxy.server:3128'}

bot = telebot.TeleBot(TOKEN)

# ==========================================
# LAS 99 FRASES DE ALTO IMPACTO
# ==========================================
frases_por_bloque = {
    "mañana": [
        "El éxito comienza con la disciplina matutina.", "Tu cuenta bancaria refleja tu nivel de esfuerzo.",
        "No busques suerte, busca consistencia.", "El mercado premia a los que se levantan con un plan.",
        "Hoy es el día para ejecutar, no para dudar.", "La mente clara es tu mejor activo financiero.",
        "Levántate con determinación para acostarte con satisfacción.", "Controla tus emociones o ellas controlarán tu dinero.",
        "El trading es 10% técnica y 90% psicología.", "No cuentes los días, haz que los días cuenten.",
        "Tu futuro se construye hoy, no mañana.", "La paciencia en el mercado es dinero en el bolsillo.",
        "Enfécate en el proceso, el profit vendrá solo.", "La disciplina es el puente entre metas y logros.",
        "Sé el dueño de tu tiempo y serás dueño de tu vida.", "El riesgo viene de no saber lo que estás haciendo.",
        "Gana la mañana y ganarás el día.", "La educación financiera es la mejor inversión.",
        "No trabajes por dinero, haz que el dinero trabaje para ti.", "La constancia vence al talento.",
        "Cada día es una nueva oportunidad de capitalizar.", "El éxito es la suma de pequeños esfuerzos diarios.",
        "Visualiza tus metas antes de abrir la primera señal.", "Sé humilde para aprender y valiente para ganar.",
        "La autodisciplina es el lenguaje del éxito.", "Tu mayor competencia es la persona que ves al espejo.",
        "Aprender a perder es lo que te enseña a ganar.", "No te detengas hasta que estés orgulloso.",
        "El conocimiento paga el mejor interés.", "Planifica tu trade y tradea tu plan.",
        "La mentalidad ganadora no acepta excusas.", "Haz hoy lo que otros no quieren para vivir mañana como otros no pueden.",
        "La riqueza es un estado mental."
    ],
    "tarde": [
        "Mantén el enfoque cuando los demás se distraen.", "La calma en medio del caos define al profesional.",
        "No fuerces el mercado, deja que las señales lleguen.", "El trading real ocurre en los momentos de espera.",
        "Revisa tus resultados de hoy con objetividad.", "Cada error es una lección pagada al mercado.",
        "La gestión de riesgo es lo único que te mantiene vivo.", "No te dejes llevar por la euforia del profit.",
        "Un ganador nunca deja de intentar.", "La disciplina no descansa después del almuerzo.",
        "El mercado es un maestro exigente.", "Enfócate en la calidad, no en la cantidad de operaciones.",
        "Tus hábitos determinan tu futuro financiero.", "El que tiene un porqué fuerte aguanta cualquier proceso.",
        "La libertad financiera empieza con una decisión.", "No mires el reloj, haz lo que él hace: sigue adelante.",
        "La paciencia es amarga, pero su fruto es dulce.", "El trading profesional es aburrido, el emocional es caro.",
        "No arriesgues lo que no estás dispuesto a perder.", "La consistencia es lo que separa a los amateurs de los pros.",
        "Acepta lo que el mercado te dé hoy.", "La confianza se construye con disciplina diaria.",
        "No permitas que un mal trade arruine un buen día.", "Sigue las reglas del sistema sin cuestionar.",
        "El éxito es sobrevivir a los días malos.", "Tu estrategia es tu armadura.",
        "Aprende a estar cómodo estando incómodo.", "El trading es libertad, no una cárcel de gráficos.",
        "La disciplina es hacer lo correcto aunque no quieras.", "Mira el gráfico con ojos de cazador, no de presa.",
        "La rentabilidad es hija de la paciencia.", "Tu plan de trading es tu única guía.",
        "Mantente firme en tu estrategia."
    ],
    "noche": [
        "Analiza tu jornada y prepárate para mañana.", "El descanso es parte del entrenamiento de un trader.",
        "Duerme con metas, despierta con planes.", "La gratitud atrae más abundancia.",
        "Mañana el mercado abrirá con nuevas oportunidades.", "Tu mente necesita resetear para rendir al 100%.",
        "Revisa tu diario de trading antes de dormir.", "La disciplina nocturna es preparar el éxito matutino.",
        "No te dejes llevar por la euforia del profit.", "El éxito requiere sacrificio y noches de estudio.",
        "La paciencia que tuviste hoy es tu ganancia de mañana.", "Cierra el día con un balance positivo en tu mente.",
        "Mañana serás mejor trader que hoy.", "La riqueza se construye mientras duermes si haces bien el trabajo.",
        "Tu compromiso es contigo mismo.", "Mañana es una hoja en blanco para tus ganancias.",
        "El camino es largo, disfruta del proceso.", "Valora lo que has logrado hoy.",
        "La disciplina de hoy es la libertad de mañana.", "Sueña en grande, opera con lógica.",
        "Descansa, el mercado no se va a ninguna parte.", "Tu resiliencia es tu mayor fortaleza.",
        "La mente tranquila toma mejores decisiones.", "Prepárate para la apertura con serenidad.",
        "El trading es una maratón, no un sprint.", "Mañana ejecutaremos con precisión.",
        "La clave es la consistencia a largo plazo.", "Tu futuro yo te agradecerá el esfuerzo de hoy.",
        "Sé agradecido por las oportunidades del mercado.", "La disciplina es el hábito de los campeones.",
        "Duerme sabiendo que diste lo mejor de ti.", "El profit es consecuencia de tu carácter.",
        "Mañana a las 08:00 volvemos a la carga.", "Buenas noches, mañana más y mejor."
    ]
}

# ==========================================
# FUNCIONES DE MENSAJES
# ==========================================
@bot.message_handler(content_types=['new_chat_members'])
def welcome(message):
    for user in message.new_chat_members:
        nombre = user.first_name
        try:
            markup_privado = types.InlineKeyboardMarkup()
            url_contacto = f"https://t.me/{MI_USUARIO}?text=Buenas%20Nabil,%20me%20gustaria%20ganar%20dinero"
            markup_privado.add(types.InlineKeyboardButton("📩 CONTACTAR CON NABIL", url=url_contacto))
            
            txt_privado = (f"¡Hola {nombre}! Bienvenido a <b>ACCIONES VIP</b> 🚀\n\n"
                           f"Para empezar a ganar dinero y activar tu sistema de 100% acierto, "
                           f"necesito que hables directamente conmigo ahora mismo.\n\n"
                           f"👇 Pulsa el botón de abajo para empezar:")
            bot.send_message(user.id, txt_privado, parse_mode='HTML', reply_markup=markup_privado)
        except: pass

@bot.message_handler(commands=['link', 'start', 'registro'])
def info(message):
    markup = types.InlineKeyboardMarkup()
    url_contacto = f"https://t.me/{MI_USUARIO}?text=Buenas%20Nabil,%20me%20gustaria%20ganar%20dinero"
    markup.add(types.InlineKeyboardButton("🥇 REGISTRO VIP", url=MI_ENLACE))
    markup.add(types.InlineKeyboardButton("📩 CONTACTAR CON NABIL", url=url_contacto))
    
    texto = (
        "<b>📊 SISTEMA NABIL INVERSIONES</b>\n\n"
        "✅ <b>Tasa de éxito:</b> 100% Garantizado.\n"
        "✅ <b>Mercado:</b> Acciones de Empresas (Seguridad Total).\n"
        "✅ <b>Capital:</b> Protegido y respaldado.\n\n"
        "⚠️ <b>PARA GANAR DINERO DEBES CONTACTAR CON NABIL</b>\n"
        "<i>Pulsa el botón de abajo para activar tu cuenta ahora mismo.</i>"
    )
    bot.send_message(message.chat.id, texto, parse_mode='HTML', reply_markup=markup)

# ==========================================
# RELOJ DE FRASES (CADA 90 MIN APROX)
# ==========================================
def reloj_frases():
    madrid_tz = pytz.timezone('Europe/Madrid')
    horas = ["08:00", "09:30", "11:00", "12:30", "14:00", "15:30", "17:00", "19:00", "21:00", "23:00"]
    while True:
        try:
            ahora_dt = datetime.datetime.now(madrid_tz)
            ahora_str = ahora_dt.strftime("%H:%M")
            if ahora_str in horas:
                h = ahora_dt.hour
                if 6 <= h < 12: bloque = "mañana"
                elif 12 <= h < 20: bloque = "tarde"
                else: bloque = "noche"
                
                frase = random.choice(frases_por_bloque[bloque])
                msg = f"<b>💎 MENTALIDAD 100% PROFIT</b>\n\n{frase}\n\n📈 <i>Inversiones Seguras con Nabil.</i>"
                bot.send_message(CHAT_ID_GRUPO, msg, parse_mode='HTML')
                time.sleep(61)
        except: pass
        time.sleep(25)

# ==========================================
# RELOJ PUBLICITARIO (CADA 2 HORAS + FIJAR)
# ==========================================
def reloj_publicidad():
    while True:
        time.sleep(7200) # 2 Horas exactas
        try:
            markup = types.InlineKeyboardMarkup()
            url_contacto = f"https://t.me/{MI_USUARIO}?text=Buenas%20Nabil,%20me%20gustaria%20ganar%20dinero"
            markup.add(types.InlineKeyboardButton("🥇 REGISTRO VIP", url=MI_ENLACE))
            markup.add(types.InlineKeyboardButton("📩 CONTACTAR CON NABIL", url=url_contacto))
            
            texto = (
                "<b>📊 SISTEMA NABIL INVERSIONES</b>\n\n"
                "✅ <b>Tasa de éxito:</b> 100% Garantizado.\n"
                "✅ <b>Mercado:</b> Acciones de Empresas (Seguridad Total).\n"
                "✅ <b>Capital:</b> Protegido y respaldado.\n\n"
                "⚠️ <b>PARA GANAR DINERO DEBES CONTACTAR CON NABIL</b>\n"
                "<i>Pulsa el botón de abajo para activar tu cuenta ahora mismo.</i>"
            )
            bot.unpin_all_chat_messages(CHAT_ID_GRUPO)
            sent_msg = bot.send_message(CHAT_ID_GRUPO, texto, parse_mode='HTML', reply_markup=markup)
            bot.pin_chat_message(CHAT_ID_GRUPO, sent_msg.message_id)
        except: pass

# ==========================================
# EJECUCIÓN CON REINTENTO (PARA QUE NO SE CAIGA)
# ==========================================
if __name__ == "__main__":
    threading.Thread(target=reloj_frases, daemon=True).start()
    threading.Thread(target=reloj_publicidad, daemon=True).start()
    
    print("Bot activo en PythonAnywhere con Proxy...")
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(f"Error detectado: {e}. Reintentando en 15 segundos...")
            time.sleep(15)