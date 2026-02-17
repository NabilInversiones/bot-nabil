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
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ==========================================
# 1. CONFIGURACIÓN PRINCIPAL
# ==========================================
TOKEN = "8375170883:AAEo82_IKNHs9jBErXUhA2BUyH0pMkxV04E"
GRUPO_ID = -1003716695186
ADMIN_ID = 212466214
ZONA_HORARIA = 'Europe/Madrid'

bot = telebot.TeleBot(TOKEN)
madrid_tz = pytz.timezone(ZONA_HORARIA)

# TU TEXTO DE INVERSIÓN EXACTO
TEXTO_SISTEMA_VIP = (
    "🏆 *SISTEMA NABIL INVERSIONES*\n\n"
    "✅ *Tasa de éxito:* 100% Garantizado.\n"
    "✅ *Mercado:* Acciones de Empresas (Seguridad Total).\n"
    "✅ *Capital:* Protegido y respaldado.\n\n"
    "💰 *PARA GANAR DINERO DEBES CONTACTAR CON NABIL*\n"
    "Pulsa el botón de abajo para activar tu cuenta ahora mismo."
)

# BOTONES DE ACCIÓN
def botones_vip():
    markup = InlineKeyboardMarkup()
    btn_registro = InlineKeyboardButton("🚀 REGISTRO VIP", url="https://t.me/nabil")
    btn_contacto = InlineKeyboardButton("📩 CONTACTAR CON NABIL", url="https://t.me/nabil")
    markup.add(btn_registro)
    markup.add(btn_contacto)
    return markup

# ==========================================
# 2. LAS 100 FRASES MOTIVADORAS (LISTA COMPLETA)
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
    "El mercado no te quita el dinero, se lo das tú por falta de disciplina.",
    "Haz del trading un negocio, no un juego de azar.",
    "La libertad financiera comienza con una decisión hoy.",
    "No cuentes los días, haz que los días cuenten.",
    "El mejor indicador técnico es tu propia psicología.",
    "Sé humilde cuando ganes y resiliente cuando pierdas.",
    "El trading es 10% técnica y 90% mentalidad.",
    "Tu único competidor es la persona que fuiste ayer.",
    "El éxito llega para quienes trabajan mientras otros descansan.",
    "No operes por necesidad, opera por oportunidad.",
    "La disciplina es hacer lo que debes, incluso cuando no quieres.",
    "El trading es el camino más difícil para hacer dinero fácil.",
    "Protege tu capital como si fuera tu vida.",
    "El miedo y la codicia son los enemigos del trader.",
    "Los gráficos no mienten, las emociones sí.",
    "El éxito no es el destino, es el proceso.",
    "Si no puedes controlar tus emociones, no puedes controlar tu dinero.",
    "El mercado es una transferencia de dinero de los impacientes a los pacientes.",
    "La mejor inversión que puedes hacer es en ti mismo.",
    "Simplifica tu estrategia. Menos es más.",
    "La confianza viene de la preparación.",
    "No persigas el precio, deja que el precio venga a ti.",
    "Una pérdida es una lección pagada.",
    "Mantén tu mente fría y tu corazón enfocado.",
    "Opera lo que ves, no lo que piensas.",
    "El trading profesional es aburrido, el trading emocional es caro.",
    "No intentes predecir, intenta reaccionar.",
    "Ganar es genial, pero sobrevivir es vital.",
    "Sé un maestro de una estrategia, no un aprendiz de cien.",
    "El trading es libertad, pero requiere responsabilidad.",
    "Visualiza tu éxito y trabaja por él.",
    "Cada vela tiene una historia, aprende a leerla.",
    "Riqueza rápida desaparece rápido. Construye con base.",
    "Tu plan de trading es tu mapa en la tormenta.",
    "No hay atajos para la maestría.",
    "Acepta el riesgo o no operes.",
    "El ego es el asesino de cuentas más grande.",
    "Trata el trading como una profesión y te pagará como tal.",
    "Rendirse no es una opción.",
    "La calidad de tus entradas define la calidad de tu vida.",
    "Cree en ti mismo cuando nadie más lo haga.",
    "El volumen confirma, el precio manda.",
    "No arriesgues más de lo que puedes permitirte perder.",
    "La consistencia es el resultado de la disciplina.",
    "El análisis técnico es un mapa, no una bola de cristal.",
    "Mantente enfocado en el largo plazo.",
    "Corta tus pérdidas y deja correr tus ganancias.",
    "El conocimiento es poder, pero la acción es resultados.",
    "Los sueños no se cumplen, se trabajan.",
    "Sé agresivo con tus metas y paciente con tus trades.",
    "Un ganador es un perdedor que lo intentó una vez más.",
    "El mercado siempre tiene la razón.",
    "La riqueza mental precede a la riqueza material.",
    "Domina tus demonios internos antes de dominar el mercado.",
    "La suerte no existe en el trading, existe la probabilidad.",
    "Hazlo hoy, mañana podría ser tarde.",
    "Una cuenta pequeña se cuida igual que una grande.",
    "No trabajes por dinero, haz que el dinero trabaje por ti.",
    "El trading es libertad de tiempo, no solo de dinero.",
    "Tu disciplina determinará tu destino.",
    "El camino al éxito está en construcción permanente.",
    "Analiza, opera, aprende y repite.",
    "Tu cuenta bancaria refleja tu nivel de disciplina.",
    "No te compares con otros, compárate con tu ayer.",
    "El mercado es un maestro cruel pero justo.",
    "La excelencia no es un acto, es un hábito.",
    "Piensa en grande, opera con inteligencia.",
    "Invierte en conocimiento y nunca serás pobre.",
    "Solo fallas cuando dejas de intentar.",
    "Mantén tu estrategia simple y tu ejecución perfecta.",
    "El éxito requiere sacrificio.",
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
    "Deja de buscar el santo grial y busca tu disciplina.",
    "El trading te enseña quién eres realmente.",
    "El éxito es inevitable si no te rindes.",
    "¡Vamos equipo, hoy es un gran día para ganar!"
]

# ==========================================
# 3. LÓGICA DE FIJADO Y ENVÍO
# ==========================================

def gestionar_fijado(nuevo_mensaje):
    """Desfija todo y fija el último mensaje enviado"""
    try:
        bot.unpin_all_chat_messages(GRUPO_ID)
        bot.pin_chat_message(GRUPO_ID, nuevo_mensaje.message_id)
    except:
        pass

def enviar_frase_cada_2h():
    """Envía texto motivador + Sistema Nabil"""
    try:
        frase = random.choice(frases_motivadoras)
        texto = f"✨ *MENSAJE DEL DÍA*\n\n_{frase}_\n\n---\n{TEXTO_SISTEMA_VIP}"
        msg = bot.send_message(GRUPO_ID, texto, parse_mode="Markdown", reply_markup=botones_vip())
        gestionar_fijado(msg)
    except Exception as e:
        print(f"Error en frase: {e}")

def enviar_imagen_vip():
    """Envía imagen + Sistema Nabil a las 14:30 y 18:30"""
    try:
        carpeta = "imagenes"
        if os.path.exists(carpeta):
            fotos = [f for f in os.listdir(carpeta) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
            if fotos:
                foto = random.choice(fotos)
                ruta = os.path.join(carpeta, foto)
                with open(ruta, 'rb') as p:
                    msg = bot.send_photo(
                        GRUPO_ID, p, 
                        caption=f"📈 *RESULTADOS DEL SISTEMA*\n\n{TEXTO_SISTEMA_VIP}", 
                        parse_mode="Markdown", 
                        reply_markup=botones_vip()
                    )
                    gestionar_fijado(msg)
    except Exception as e:
        print(f"Error en imagen: {e}")

# ==========================================
# 4. HORARIOS Y SERVIDOR
# ==========================================

# 10 HORARIOS DE FRASES (CADA 2 HORAS APROX)
horas = ["08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00", "21:00", "22:00", "23:00"]
for h in horas:
    schedule.every().day.at(h).do(enviar_frase_cada_2h)

# IMÁGENES EXACTAS
schedule.every().day.at("14:30").do(enviar_imagen_vip)
schedule.every().day.at("18:30").do(enviar_imagen_vip)

def run_server():
    port = int(os.environ.get("PORT", 10000))
    with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as httpd:
        httpd.serve_forever()

Thread(target=run_server, daemon=True).start()

# ==========================================
# 5. LIMPIEZA DE BASURA Y BIENVENIDA
# ==========================================
@bot.message_handler(content_types=['new_chat_members', 'left_chat_member'])
def limpiar_y_bienvenida(m):
    # Borra "X se unió" o "X salió"
    try: bot.delete_message(m.chat.id, m.message_id)
    except: pass
    
    # Bienvenida VIP si es un usuario nuevo
    if m.content_type == 'new_chat_members':
        for u in m.new_chat_members:
            if not u.is_bot:
                saludo = f"¡Hola {u.first_name}! 👋 Bienvenido al canal oficial.\n\n{TEXTO_SISTEMA_VIP}"
                bot.send_message(m.chat.id, saludo, parse_mode="Markdown", reply_markup=botones_vip())

def scheduler_loop():
    while True:
        schedule.run_pending()
        time.sleep(30)

Thread(target=scheduler_loop, daemon=True).start()
bot.delete_webhook(drop_pending_updates=True)
bot.infinity_polling()
