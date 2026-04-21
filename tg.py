from dotenv import load_dotenv
import os
import telebot
import sqlite3
import time
import threading
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv('/home/ay507291/notacomforta.pl.ua/www/.env')

client = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'), parse_mode="HTML")

ADMIN = 533579836
ROOT = 555116496
DB_PATH = os.getenv('DB_PATH')

# --- Хендлер для старту ---
@client.message_handler(commands=["start"])
def start(message):
    client.send_message(message.chat.id, "✅ Бот запущений і відслідковує нові замовлення.")


# --- Функція для перевірки замовлень ---
def check_orders():
    while True:
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            query = "SELECT * FROM order_order WHERE send=0"
            cursor.execute(query)
            results = cursor.fetchall()

            for row in results:
                order_id = row[0]
                text = (f"📦 <b>Номер замовлення:</b> {row[0]}\n"
                        f"👤 <b>Прізвище та ім'я:</b> {row[1]}\n"
                        f"📞 <b>Телефон:</b> {row[2]}\n"
                        f"💬 <b>Коментар:</b> {row[3]}\n"
                        f"💰 <b>Сума:</b> {row[5]} грн")

                keyboard = InlineKeyboardMarkup()
                keyboard.add(
                    InlineKeyboardButton("🔎 Переглянути на сайті", url=f"https://www.notacomforta.pl.ua/order/track?number={order_id}")
                )
                keyboard.add(
                    InlineKeyboardButton("🛠 Адмін панель", url=f"https://www.notacomforta.pl.ua/admin/order/order/{order_id}/change/")
                )

                # Відправляємо повідомлення ROOT і ADMIN
                client.send_message(ROOT, text, reply_markup=keyboard)
                client.send_message(ADMIN, text, reply_markup=keyboard)

                print("✅ Повідомлення відправлено:", order_id)

                # Оновлюємо статус
                cursor.execute("UPDATE order_order SET send = 1 WHERE id = ?", (order_id,))
                conn.commit()

        except Exception as e:
            print(f"❌ Помилка: {e}")
            try:
                client.send_message(ROOT, f"❌ Помилка: {e}")
            except:
                pass

        finally:
            try:
                conn.close()
            except:
                pass

        time.sleep(10)


# --- Запускаємо цикл перевірки у окремому потоці ---
threading.Thread(target=check_orders, daemon=True).start()


# --- Безкінечний polling з авто-перезапуском ---
while True:
    try:
        client.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print(f"⚠️ Polling впав: {e}. Перезапуск через 5 сек...")
        time.sleep(5)
