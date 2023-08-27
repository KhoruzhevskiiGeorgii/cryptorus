import telebot
import requests
import time
from bs4 import BeautifulSoup
import config

token = config.PARSER_TOKEN
channel_id = config.CHANNEL_URL
bot = telebot.TeleBot(token)

@bot.message_handler(content_types=['text'])
def commands(message):
    if message.text == "Старт":
        # bot.send_message(channel_id, "Hello")
        back_post_id = None
        while True:
            post_text = parser(back_post_id)
            back_post_id = post_text[1]

            if post_text[0] != None:
                bot.send_message(channel_id, post_text[0])
                time.sleep(1800)
        print('stop')
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши Старт")

def parser(back_post_id):
    URL = config.NEWS_SOURCE

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    posts = soup.find('div', class_='largeTitle')
    post = posts.find('article')

    post_id = post['data-id']
    if post_id!=back_post_id:
        title = post.find('a', class_='title').text.strip()
        description = post.find('p').text.strip()
        url = config.NEWS + post.find('a', class_='img', href=True)['href'].strip()
        return f'{title}\n\n{description}\n\n{url}', post_id
    else: return None, post_id

bot.infinity_polling(timeout=10, long_polling_timeout = 5)
