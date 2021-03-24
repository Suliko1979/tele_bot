import telebot
import requests
from bs4 import BeautifulSoup


token = '1700307370:AAFisNKNsymLLGMtX2Li-qEK_ayWvmuaaRA'

bot = telebot.TeleBot(token)
welcome_text = """
	Приветствую тебя на нашем онлайн магазине!
	Выбери супермаркет!
"""
error_msg = """
	Введите правильно привет!
"""
list_product_category_names = """
	Список категорий продуктов
"""

shop_list = [
	{'name': 'Globus'},
	{'name': 'Фрунзе'},
]
globus_url = 'https://globus-online.kg/catalog/'
frunze_url = 'https://online.gipermarket.kg/'

@bot.message_handler(content_types=['text'])
def send_welcome(message):
	chat_id = message.chat.id
	markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
	markup.row(
		shop_list[0].get('name'),
		shop_list[1].get('name'),
	)

	if message.text.lower() == 'привет':
		bot.reply_to(message=message,
					 text=welcome_text,
					 reply_markup=markup)
	elif shop_list[0].get('name') == message.text:
		markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
		response = requests.get(globus_url)
		soup = BeautifulSoup(response.text, 'lxml')
		soup = soup.find_all('a', class_='parent')
		for s in soup[2:]:
			markup.add(s.text)
		bot.send_message(chat_id=chat_id,
						 text=list_product_category_names,
						 reply_markup=markup)

	elif shop_list[1].get('name') == message.text:
		markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
		response = requests.get(frunze_url)
		soup = BeautifulSoup(response.text, 'lxml')
		soup = soup.find_all('div', class_='advanced-container-medium catalog-category-grid main-catalog')
		for s in soup:
			markup.add(s.text)
		bot.send_message(chat_id=chat_id,
						 text=list_product_category_names,
						 reply_markup=markup)

	else:
		bot.send_message(chat_id=message.chat.id,
						 text=error_msg)


bot.polling()
