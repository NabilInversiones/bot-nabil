import telebot
import time
import pytz
import random
import os
from datetime import datetime
from threading import Thread
from flask import Flask
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ==========================================
# 1. SERVIDOR FLASK PARA RENDER (KEEP-ALIVE)
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "Bot Nabil Inversiones Online"

def run_server():
    # Render usa el puerto que le asigna el sistema
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# ==========================================
# 2. CONFIGURACIÓN DEL BOT
# ==========================================
TOKEN = "8375170883:AAEo82_IKNHs9jBErXUhA2BUyH0pMkxV04E"
GRUPO_ID = -1003716695186
ZONA_HORARIA = 'Europe/Madrid'

# threaded=False evita errores de conexión en servidores gratuitos
bot = telebot.TeleBot(TOKEN, threaded=False)
madrid_tz = pytz.timezone(ZONA_HORARIA)

TEXTO_SISTEMA_VIP = (
    "🏆 *SISTEMA NABIL INVERSIONES*\n\n"
    "✅ *Tasa de éxito:* 100% Garantizado.\n"
    "✅ *Mercado:* Acciones de Empresas (Seguridad Total).\n"
    "✅ *Capital:* Protegido y respaldado.\n\n"
    "💰 *PARA GANAR DINERO DEBES REGISTRARTE Y CONTACTAR CON NABIL*"
)

def botones_vip():
    markup = InlineKeyboardMarkup()
    enlace_qvse = "https://qvselp.com/#/pages/auth-signup/index?inviteCode=3LVZ"
    btn_registro = InlineKeyboardButton("🚀 REGISTRO EN QVSE", url=enlace_qvse)
    btn_ganar = InlineKeyboardButton("💰 GANAR DINERO", url="https://t.me/NabilInversiones?text=Buenas%20Nabil,%20quiero%20empezar%20a%20ganar%20dinero")
    btn_info = InlineKeyboardButton("ℹ️ INFORMACIÓN", url="https://t.me/NabilInversiones?text=Buenas%20Nabil,%20quiero%20informacion")
    markup.add(btn_registro)
    markup.add(btn_ganar, btn_info) 
    return markup

# ==========================================
# 3. LAS 100 FRASES MOTIVADORAS
# ==========================================
frases_motivadoras = [
    "El éxito es la suma de pequeños esfuerzos repetidos día tras día.",
    "Opera con el plan, no con la emoción. ¡Disciplina ante todo!",
    "No busques el dinero, busca la habilidad y el dinero te seguirá.",
    "Los ganadores no son los que nunca fallan, sino los que nunca se rinden.",
    "Gestiona tu riesgo. Perder una batalla no es perder la guerra.",
    "La paciencia es la clave del éxito en el trading.",
    "Un mal día de trading no define tu carrera. ¡Sigue adelante!",
    "Tu mente es tu activo más valioso. Entrénala bien.",
    "La constancia separa a los amateurs de los profesionales.",
    "Aprende de tus errores y nunca dejarás de ganar.",
    "Haz del trading un negocio, no un juego de azar.",
    "La libertad financiera comienza con una decisión hoy.",
    "El mejor indicador técnico es tu propia psicología.",
    "Sé humilde cuando ganes y resiliente cuando pierdas.",
    "El trading es 10% técnica y 90% mentalidad.",
    "Tu único competidor es la persona que fuiste ayer.",
    "No operes por necesidad, opera por oportunidad.",
    "La disciplina es hacer lo que debes, incluso cuando no quieres.",
    "Protege tu capital como si fuera tu vida.",
    "Los gráficos no mienten, las emociones sí.",
    "Si no puedes controlar tus emociones, no puedes controlar tu dinero.",
    "La mejor inversión que puedes hacer es en ti mismo.",
    "Simplifica tu estrategia. Menos es más.",
    "La confianza viene de la preparación.",
    "No persigas el precio, deja que el precio venga a ti.",
    "Una pérdida es una lección pagada.",
    "Mantén tu mente fría y tu corazón enfocado.",
    "Opera lo que ves, no lo que piensas.",
    "Ganar es genial, pero sobrevivir es vital.",
    "Sé un maestro de una estrategia, no un aprendiz de cien.",
    "Visualiza tu éxito y trabaja por él.",
    "Riqueza rápida desaparece rápido. Construye con base.",
    "Tu plan de trading es tu mapa en la tormenta.",
    "Acepta el riesgo o no operes.",
    "El ego es el asesino de cuentas más grande.",
    "Trata el trading como una profesión y te pagará como tal.",
    "Rendirse no es una opción.",
    "La calidad de tus entradas define la calidad de tu vida.",
    "Cree en ti mismo cuando nadie más lo haga.",
    "El volumen confirma, el precio manda.",
    "La consistencia es el resultado de la disciplina.",
    "Mantente enfocado en el largo plazo.",
    "Corta tus pérdidas y deja correr tus ganancias.",
    "El conocimiento es poder, pero la acción es resultados.",
    "Los sueños no se cumplen, se trabajan.",
    "Sé agresivo con tus metas y paciente con tus trades.",
    "El mercado siempre tiene la razón.",
    "Domina tus demonios internos antes de dominar el mercado.",
    "La suerte no existe en el trading, existe la probabilidad.",
    "Hazlo hoy, mañana podría ser tarde.",
    "Una cuenta pequeña se cuida igual que una grande.",
    "No trabajes por dinero, haz que el dinero trabaje por ti.",
    "Tu disciplina determinará tu destino.",
    "Analiza, opera, aprende y repite.",
    "Tu cuenta bancaria refleja tu nivel de disciplina.",
    "No te compares con otros, compárate con tu ayer.",
    "La excelencia no es un acto, es un hábito.",
    "Piensa en grande, opera con inteligencia.",
    "Invierte en conocimiento y nunca serás pobre.",
    "Solo fallas cuando dejas de intentar.",
    "Mantén tu estrategia simple y tu ejecución perfecta.",
    "Escucha lo que el mercado te dice, no lo que quieres oír.",
    "Cada operación es una nueva oportunidad.",
    "Controla el riesgo y el beneficio vendrá solo.",
    "Sé un francotirador, no un ametrallador.",
    "La perseverancia vence a la inteligencia.",
    "No te enamores de una operación.",
    "Aprender a no operar es tan importante como operar.",
    "Los campeones se hacen en los días difíciles.",
    "El trading es un maratón, no un sprint.",
    "Tu futuro depende de lo que hagas hoy.",
    "Los retrocesos son oportunidades disfrazadas.",
    "La gratitud atrae la abundancia.",
    "No dejes que un trade defina tu felicidad.",
    "Lee libros, estudia gráficos, mejora siempre.",
    "La disciplina es el puente entre metas y logros.",
    "El trading te enseña quién eres realmente.",
    "El éxito es inevitable si no te rindes.",
    "¡Vamos equipo, hoy es un gran día para ganar!"
]

# ==========================================
# 4. FUNCIONES DE ENVÍO
# ==========================================
def enviar_solo_frase(chat_id):
    try:
        frase = random.choice(frases_motivadoras)
        bot.send_message(chat_id, f"✨ *{frase}*", parse_mode="Markdown")
    except Exception as e: print(f"Error frase: {e}")

def enviar_solo_sistema(chat_id):
    try:
        msg = bot.send_message(chat_id, TEXTO_SISTEMA_VIP, parse_mode="Markdown", reply_markup=botones_vip())
        if chat_id == GRUPO_ID:
            bot.unpin_all_chat_messages(GRUPO_ID)
            bot.pin_chat_message(GRUPO_ID, msg.message_id)
    except Exception as e: print(f"Error sistema: {e}")

# ==========================================
# 5. MANEJO DE MENSAJES
# ==========================================
@bot.message_handler(commands=['start', 'link'])
def comando_inteligente(m):
    enviar_solo_sistema(m.chat.id)

@bot.message_handler(content_types=['new_chat_members'])
def bienvenida_discreta(m):
    try:
        bot.delete_message(m.chat.id, m.message_id)
    except: pass
    
    for user in m.new_chat_members:
        try:
            texto_privado = (
                f"👋 *¡Hola {user.first_name}! Bienvenido al equipo de Nabil Inversiones.*\n\n"
                "Para empezar a ganar dinero hoy mismo con nosotros, sigue estos pasos:\n\n"
                "1️⃣ *REGÍSTRATE* en QVSE con el botón de abajo.\n"
                "2️⃣ *DEPÓSITA* el capital que quieras invertir.\n"
                "3️⃣ *ENVÍAME* captura de tu perfil para darte acceso al VIP.\n\n"
                "¡Nos vemos dentro! 🚀📈"
            )
            bot.send_message(user.id, texto_privado, parse_mode="Markdown", reply_markup=botones_vip())
        except: pass

# ==========================================
# 6. RELOJ MAESTRO (TAREAS AUTOMÁTICAS ACTUALIZADAS)
# ==========================================
def scheduler_loop():
    horas_frases = ["08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00", "21:30", "22:30", "23:30"]
    horas_sistema = ["09:00", "11:00", "13:00", "15:00", "17:00", "19:00", "21:00"]

    while True:
        try:
            ahora = datetime.now(madrid_tz).strftime("%H:%M")
            
            if ahora in horas_frases:
                enviar_solo_frase(GRUPO_ID)
                time.sleep(61)
                
            if ahora in horas_sistema:
                enviar_solo_sistema(GRUPO_ID)
                time.sleep(61)

            # --- CICLO DE SEÑALES (PROFESIONAL) ---
            
            # Mensaje 1 (30 min): Aviso de Código
            if ahora == "14:30" or ahora == "18:30":
                bot.send_message(GRUPO_ID, "🚨 *ATENTOS A LA SEÑAL...* \nTenemos el código listo para operar. Abrid QVSE ahora mismo. 🔥", parse_mode="Markdown")
                time.sleep(61)

            # Mensaje 2 (35 min): Confirmación de ejecución
            if ahora == "14:35" or ahora == "18:35":
                bot.send_message(GRUPO_ID, "✅ *SISTEMA ENVIADO* \nCódigo aplicado con éxito. El equipo ya está dentro de la operación. ⏳", parse_mode="Markdown")
                time.sleep(61)

            # Mensaje 3 (40 min): Beneficios y Crecimiento
            if ahora == "14:40" or ahora == "18:40":
                bot.send_message(GRUPO_ID, "💰 *¡SESIÓN COMPLETADA!* \nObjetivo cumplido con éxito. El capital sigue creciendo y sumando beneficios a vuestras cuentas. ¡Otra victoria para el equipo! 💸📈", parse_mode="Markdown", reply_markup=botones_vip())
                time.sleep(61)
                
        except: pass
        time.sleep(30)

# ==========================================
# 7. EJECUCIÓN FINAL
# ==========================================
if __name__ == "__main__":
    # Iniciar servidor Flask para Render en segundo plano
    Thread(target=run_server, daemon=True).start()
    
    # Iniciar reloj de mensajes en segundo plano
    Thread(target=scheduler_loop, daemon=True).start()
    
    print("🚀 Sistema Nabil Inversiones ONLINE")
    
    try:
        bot.remove_webhook()
        time.sleep(2)
    except: pass

    while True:
        try:
            # Polling infinito para recibir mensajes
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Reinicio por error: {e}")
            time.sleep(15)
