import os
import telebot
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
user_data = {}
@bot.message_handler(commands=['start'])
def start(m):
    user_data[m.chat.id] = {"balance": 0, "initial": 0}
    bot.send_message(m.chat.id, "Mines Helper LIVE 24/7\n\n/balance 100 - set balance\nThen: 3 4 10 (mines gems profit)")
@bot.message_handler(commands=['balance'])
def set_bal(m):
    try:
        bal = float(m.text.split()[1])
        user_data[m.chat.id] = {"balance": bal, "initial": bal}
        bot.send_message(m.chat.id, f"Balance: {bal} GHS OK")
    except:
        bot.send_message(m.chat.id, "Use: /balance 100")
@bot.message_handler(func=lambda m: True)
def calc(m):
    try:
        if m.chat.id not in user_data:
            user_data[m.chat.id] = {"balance": 0, "initial": 0}
        mines, picked = int(m.text.split()[0]), int(m.text.split()[1])
        profit = float(m.text.split()[2]) if len(m.text.split())>2 else 0
        user_data[m.chat.id]["balance"] += profit
        bal = user_data[m.chat.id]["balance"]
        init = user_data[m.chat.id]["initial"]
        next_safe = ((25-mines-picked)/(25-picked)*100) if picked<25 else 0
        msg = f"Balance: {bal:.2f}\n"
        if init>0: msg+=f"P/L: {bal-init:+.2f}\n"
        msg+=f"\nSafe: {next_safe:.1f}% | Risk: {100-next_safe:.1f}%\n"
        msg+= "STOP! CASH OUT!" if next_safe<40 else "Consider cash out" if next_safe<65 else "OK continue"
        bot.send_message(m.chat.id, msg)
    except:
        bot.send_message(m.chat.id, "Format: 3 4 10")
bot.infinity_polling()
