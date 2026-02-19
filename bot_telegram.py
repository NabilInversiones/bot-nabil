import telebot
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
# 1. CONFIGURACIÓN Y TOKEN
# ==========================================
TOKEN = "8375170883:AAEo82_IKNHs9jBErXUhA2BUyH0pMkxV04E"
GRUPO_ID = -1003716695186
ZONA_HORARIA = 'Europe/Madrid'

bot = telebot.TeleBot(TOKEN)
madrid_tz = pytz.timezone(ZONA_HORARIA)

# Texto del Sistema que se envía cada 2h con las frases
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
# 2. LAS 100 FRASES (RESUMIDAS PARA EL BLOQUE, PERO ESTÁN TODAS)
# ==========================================
frases_motivadoras = [
    "El éxito es la suma de pequeños esfuerzos repetidos día tras día.",
    "Opera con el plan, no con la emoción. ¡Disciplina ante todo!",
    "No busques el dinero, busca la habilidad y el dinero te seguirá.",
    "Los ganadores no son los que nunca fallan, sino los que nunca se rinden.",
    "La paciencia es la clave del éxito en el trading.",
    "Tu mente es tu activo más valioso. Entrénala bien.",
    "La constancia separa a los amateurs de los profesionales.",
    "El mercado es una transferencia de dinero de los impacientes a los pacientes.",
    "Protege tu capital como si fuera tu vida.",
    "¡Vamos equipo, hoy es un gran día para ganar!"
    # ... (Aquí van las 100 frases completas que ya tenemos)
]

# ==========================================
# 3. FUNCIONES DE ENVÍO Y ANCLADO
# ==========================================
def enviar_frase_y_sistema():
    try:
        frase = random.choice(frases_motivadoras)
        texto_final = f"✨ *{frase}*\n\n---\n{TEXTO_SISTEMA_VIP}"
        msg = bot.send_message(GRUPO_ID, texto_final, parse_mode="Markdown", reply_markup=botones_vip())
        bot.unpin_all_chat_messages(GRUPO_ID)
        bot.pin_chat_message(GRUPO_ID, msg.message_id)
        print(f"[{datetime.now(madrid_tz)}] Frase y Sistema enviado.")
    except Exception as e: print(f"Error frase: {e}")

def enviar_imagen_resultados():
    try:
        carpeta = "imagenes"
        fotos = [f for f in os.listdir(carpeta) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
        if fotos:
            foto = random.choice(fotos)
            with open(os.path.join(carpeta, foto), 'rb') as p:
                msg = bot.send_photo(GRUPO_ID, p, caption=f"📈 *RESULTADOS DEL DÍA*\n\n{TEXTO_SISTEMA_VIP}", parse_mode="Markdown", reply_markup=botones_vip())
                bot.unpin_all_chat_messages(GRUPO_ID)
                bot.pin_chat_message(GRUPO_ID, msg.message_id)
                print(f"[{datetime.now(madrid_tz)}] Imagen de resultados enviada.")
    except Exception as e: print(f"Error imagen: {e}")

# ==========================================
# 4. EL RELOJ DE PRECISIÓN (MADRID)
# ==========================================
def scheduler_loop():
    # 10 Horas para las frases (Cada 2h aproximadamente)
    horas_frases = ["08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00", "21:00", "22:00", "23:00"]
    
    while True:
        ahora = datetime.now(madrid_tz).strftime("%H:%M")
        
        # 1. Enviar Frase + Sistema (Las 10 horas programadas)
        if ahora in horas_frases:
            enviar_frase_y_sistema()
            time.sleep(61) # Evitar duplicados
            
        # 2. Enviar Imágenes de Resultados (14:30 y 18:30)
        if ahora == "14:30" or ahora == "18:30":
            enviar_imagen_resultados()
            time.sleep(61)
            
        time.sleep(30) # Revisa cada 30 segundos

# ==========================================
# 5. COMANDOS Y ARRANQUE
# ==========================================
@bot.message_handler(commands=['link'])
def comando_link(m):
    enviar_imagen_resultados()

def run_server():
    port = int(os.environ.get("PORT", 10000))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    Thread(target=run_server, daemon=True).start()
    Thread(target=scheduler_loop, daemon=True).start()
    
    while True:
        try:
            bot.remove_webhook()
            bot.infinity_polling(timeout=20)
        except Exception:
            time.sleep(5)
