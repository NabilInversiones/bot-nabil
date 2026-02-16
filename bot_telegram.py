import telebot
import time
import schedule
from threading import Thread
import pytz
from datetime import datetime

# CONFIGURACIÓN
TOKEN = '8375170883:AAH7qQnL6lOq_DEx_Q885D96u0_7-kR5A_Q'
CHAT_ID = '-1002347313886'
MADRID_TZ = pytz.timezone('Europe/Madrid')

bot = telebot.TeleBot(TOKEN)

frases = [
    "✅ Señal confirmada. ¡Vamos a por ello!",
    "📈 Tendencia alcista detectada. Operación en curso.",
    "💰 Objetivo alcanzado. ¡Felicidades a todos!",
    "🚀 El mercado está respondiendo bien. Seguimos.",
    "📊 Analizando próximas entradas. Estén atentos.",
    "🎯 Punto de entrada perfecto. ¡No lo dejes pasar!",
    "💎 Paciencia y disciplina son las claves hoy.",
    "🔥 ¡Día de ganancias! Seguimos sumando.",
    "⚡️ Ejecución rápida recomendada para esta señal.",
    "🏆 Somos el equipo ganador. ¡A por más!"
]

def enviar_frase():
    try:
        ahora = datetime.now(MADRID_TZ)
        frase = frases[ahora.day % len(frases)]
        bot.send_message(CHAT_ID, frase)
    except Exception as e:
        print(f"Error: {e}")

def enviar_publicidad():
    try:
        bot.send_message(CHAT_ID, "📢 ¡Únete a nuestro canal VIP para señales exclusivas! Escríbeme aquí: @NabilInversiones")
    except Exception as e:
        print(f"Error: {e}")

# Horarios: cada 2 horas (08:00, 10:00, 12:00, etc.)
for h in range(8, 28, 2):
    hora_str = f"{h%24:02d}:00"
    schedule.every().day.at(hora_str).do(enviar_frase)

schedule.every(2).hours.do(enviar_publicidad)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    print("Bot activo en Render (Sin Proxy)...")
    Thread(target=run_schedule, daemon=True).start()
    bot.infinity_polling()
