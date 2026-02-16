import telebot
import schedule
import time
import pytz
import http.server
import socketserver
from datetime import datetime
from threading import Thread

# ==========================================
# 1. CONFIGURACIÓN (Tus datos)
# ==========================================
TOKEN = "8375170883:AAGUhVAyyu1lvnx42RscIEuw9opknbKIBX8"
GRUPO_ID = -1003716695186  # ID de tu grupo
ADMIN_ID = 212466214       # Tu ID personal
ZONA_HORARIA = 'Europe/Madrid'

bot = telebot.TeleBot(TOKEN)
madrid_tz = pytz.timezone(ZONA_HORARIA)

# ==========================================
# 2. TRUCO PARA RENDER (SERVIDOR WEB)
# ==========================================
# Esto evita el error de "Timed Out" y mantiene el bot vivo
def run_dummy_server():
    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot esta vivo!")

    port = 8080
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"Servidor de mantenimiento activo en puerto {port}")
        httpd.serve_forever()

# Iniciamos el servidor en un hilo aparte
Thread(target=run_dummy_server, daemon=True).start()

# ==========================================
# 3. CONTENIDO Y LÓGICA
# ==========================================
frases = [
    "🚀 *¡Buenos días equipo!* El éxito no es suerte, es constancia. ¿Ya revisaste tus metas de hoy?",
    "📈 *Recordatorio:* El mercado recompensa la paciencia y castiga la impulsividad. ¡Mantente frío!",
    "💰 *Mentalidad de riqueza:* No trabajes por el dinero, haz que el dinero trabaje para ti.",
    "🔥 *Motivación:* Los límites solo están en tu mente. ¡A por todas!",
    "💎 *Tip del día:* La disciplina es hacer lo que debes, incluso cuando no tienes ganas.",
    "📊 *Análisis:* Antes de entrar en una operación, revisa tu gestión de riesgo. ¡Protege tu capital!"
]

def enviar_mensaje_programado():
    try:
        ahora = datetime.now(madrid_tz)
        # Seleccionamos una frase según la hora para que no se repita igual siempre
        indice = ahora.hour % len(frases)
        mensaje = frases[indice]
        
        bot.send_message(GRUPO_ID, mensaje, parse_mode="Markdown")
        print(f"✅ Mensaje enviado a las {ahora.strftime('%H:%M:%S')}")
    except Exception as e:
        print(f"❌ Error al enviar mensaje: {e}")

# ==========================================
# 4. PROGRAMACIÓN DE HORARIOS
# ==========================================
# Se enviará un mensaje en estas horas exactas (Hora de Madrid)
horarios = ["09:00", "11:00", "13:00", "15:00", "17:00", "19:00", "21:00"]

for hora in horarios:
    schedule.every().day.at(hora).do(enviar_mensaje_programado)

# ==========================================
# 5. COMANDOS DEL BOT
# ==========================================
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Soy el bot de Nabil. Estoy programado para enviar contenido de valor automáticamente.")

@bot.message_handler(commands=['test'])
def test_mensaje(message):
    if message.from_user.id == ADMIN_ID:
        enviar_mensaje_programado()
        bot.reply_to(message, "✅ Prueba enviada al grupo.")
    else:
        bot.reply_to(message, "No tienes permiso para esto.")

# ==========================================
# 6. EJECUCIÓN CONTINUA
# ==========================================
print("🚀 BOT INICIADO Y FUNCIONANDO EN LA NUBE")

def scheduler_loop():
    while True:
        schedule.run_pending()
        time.sleep(30)

# El hilo del scheduler corre en segundo plano
Thread(target=scheduler_loop, daemon=True).start()

# Iniciamos el bot para que responda a comandos (polling)
bot.infinity_polling()
