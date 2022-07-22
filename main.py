# Импорт нужных библиотек.
import telebot
from telebot import types
from telebot.async_telebot import AsyncTeleBot
import asyncio
from gtts import gTTS
import datetime
import os

# Переменные
lang = None
text = None

token = "твой токен"
client = telebot.TeleBot(token)

# /start /help

@client.message_handler(commands=['help','start'])
def helpcmd(message):
	client.send_message(message.chat.id, "♻️ List:\n\n❗️ /start, /help - help command.\n❗️ /gtts - google text to speech")

# Текст в речь

@client.message_handler(commands=['gtts'])
def gttscmd(message):
	lang1 = client.send_message(message.chat.id, "Choose language. (for example: en, uk)")
	client.register_next_step_handler(lang1, after_lang)

def after_lang(message):
	global lang
	lang = message.text
	text1 = client.send_message(message.chat.id, "Enter text.")
	client.register_next_step_handler(text1, after_text)

def after_text(message):
	try:
		global text
		text = message.text
		audio = 'speech.mp3'
		sp = gTTS(text=text, lang=lang, slow=False)
		sp.save(audio)
		saudio = open(r'speech.mp3', 'rb')
		client.send_voice(message.chat.id, saudio)
		saudio.close()
	except Exception as e:
		client.send_message(message.chat.id, e)

# Запуск

asyncio.run(client.polling())

