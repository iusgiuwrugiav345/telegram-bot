import requests
import asyncio
from telegram import Bot
import time

# 🔹 API-ключи (замени на свои)
MISTRAL_API_KEY = "sJOjVrVsFcfKjU5tMDbZvCU162V7DtSk"
UNSPLASH_API_KEY = "253PNYg85795iHWG8RiCLXkUPzDnKhm-35n1XwZWU2Q"
TELEGRAM_BOT_TOKEN = "7801508703:AAEfVX21WfcMe5R4r-jhPZV91KmZXbvPvO8"
CHANNEL_ID = "@insideuzbekistan24"

# 🔹 Настройки
NUM_NEWS = 3  # Сколько новостей отправлять за раз

# Создаём Telegram-бота
bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def send_news_with_image(news_text, image_url):
    """Отправляет новость с изображением в Telegram"""
    message = f"{news_text}\n\n📢 Не пропустите важные события: @insideuzbekistan24"

    try:
        if image_url:
            await bot.send_photo(chat_id=CHANNEL_ID, photo=image_url, caption=message)
        else:
            await bot.send_message(chat_id=CHANNEL_ID, text=message)
    except Exception as e:
        print(f"Ошибка отправки: {e}")

def get_news():
    """Генерирует новости через Mistral API"""
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "mistral-medium",
        "messages": [{"role": "system", "content": "Сгенерируй 3 свежие новости мира подробно. Раздели их пустыми строками. А также не ставь нумерацию"}]
    }

    response = requests.post(url, json=data, headers=headers).json()
    return response.get("choices", [{}])[0].get("message", {}).get("content", "").split("\n\n")

def get_image(query):
    """Ищет изображение по теме через Unsplash API"""
    url = f"https://api.unsplash.com/photos/random?query={query}&client_id={UNSPLASH_API_KEY}"
    response = requests.get(url).json()
    return response.get("urls", {}).get("regular", None)

async def main():
    while True:
        print("🔹 Генерация новостей...")
        news_list = get_news()

        for news in news_list[:NUM_NEWS]:
            if news.strip():
                image_url = get_image(news[:30])  # Берём первые 30 символов как тему
                await send_news_with_image(news, image_url)
        
        print("✅ Новости отправлены. Ждём 1 час...")
        time.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
