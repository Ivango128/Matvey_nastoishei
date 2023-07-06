from pprint import pprint

import requests
import datetime
from googletrans import Translator
from telebot.async_telebot import AsyncTeleBot


API_KEY = '148d4ca9d8ad4614a711190fa33b1524'
TOKEN = '6286035570:AAGUyK_aRQaZdERTc3ZDYB5fqY-mcH6UWQM'
bot = AsyncTeleBot(TOKEN, parse_mode='HTML')


def translate_ru_to_en(text):
    translator = Translator(service_urls=['translate.google.com'])
    translation = translator.translate(text, src='ru', dest='en')
    return translation.text



def translate_en_to_ru(text):
    translator = Translator(service_urls=['translate.google.com'])
    translation = translator.translate(text, src='en', dest='ru')
    return translation.text

@bot.message_handler(commands=["start"])
async def start_command(message):
    chat_id = message.from_user.id
    await bot.send_message(chat_id,"Привет! Напиши мне индигреенты, который хочешь видеть в рецепте через запятую")


@bot.message_handler(func=lambda message: True)
async def search_recipe(message):
    print(message.text)
    query = translate_ru_to_en(message.text)
    chat_id = message.from_user.id
    url = f'https://api.spoonacular.com/recipes/complexSearch?query={query}&apiKey={API_KEY}&fillIngredients=True'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        pprint(data)
        # Получаем первый рецепт из результатов поиска
        if 'results' in data and len(data['results']) > 0:
            for i in range(0, len(data['results'])):
                if i == 4:
                    break
                recipe_id = data['results'][i]['id']
                recipe_title = data['results'][i]['title']
                recipe_img = data['results'][i]['image']
                recipe_url = f'https://spoonacular.com/recipes/{recipe_title.replace(" ", "-")}-{recipe_id}'

                recipe_title = translate_en_to_ru(recipe_title)
                #await bot.send_message(chat_id, f'Найден рецепт "{recipe_title}": {recipe_url}', disable_web_page_preview=True)
                await bot.send_photo(chat_id, recipe_img, caption=f'Найден рецепт "{recipe_title}": {recipe_url}')
        else:
            await bot.send_message(chat_id,'Рецепт не найден.')

    except requests.exceptions.HTTPError as err:
        await bot.send_message(chat_id,'Рецепт не найден.')

    except:
        await bot.send_message(chat_id,'Рецепт не найден.')


import asyncio

asyncio.run(bot.polling())