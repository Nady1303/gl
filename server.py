import logging
import random

import requests
import io

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters
from telegram_config import TOKEN
import json

reply_keyboard1 = [['/Lets_cook', '/Search_for_ingredients'],
                   ['/Film_recipe', '/Cuisine', "/Add_recipe"],
                   ["/start", "/help"]]
markup1 = ReplyKeyboardMarkup(reply_keyboard1, one_time_keyboard=False)


# Запускаем логгирование
async def help(update, context):
    await update.message.reply_text(
        "Я бот кулинарный справочник." + '\n'
                                         "Я найду для вас рецепт мечты." + '\n'
                                                                           "У нас вы можете найти:" + '\n'
                                                                                                      "-блюдо по вашим ингредиентам" + '\n'
                                                                                                                                       "-варианты блюд вашей любимой кухни" + '\n'
                                                                                                                                                                              "-рецепты для любого для приёма пищи" + '\n'
                                                                                                                                                                                                                      "-и даже блюда из ваших любимых фильмов и мультфильмов!" + '\n'
                                                                                                                                                                                                                                                                                 "Начните работу, нажав на /start")


async def start(update, context):
    global chat_id
    chat_id = update.message.chat_id
    await update.message.reply_text(f'Для дальнейшей '
                                    f'навигации воспользуйтесь кнопками! Удачи вам и помните: готовить может каждый!',
                                    reply_markup=markup1)


async def film(update, context):
    with open('recipes.json', encoding="utf8") as f:
        d = json.load(f)
        a = ''
        for dish in d:
            if dish['reference'] != '':
                a += ('\N{black star}' + '`' + dish['name'] + '`' + 2 * '\n')
                # await update.message.reply_text(
                #     dish['name'], sendImageRemoteFile(dish['img']))

        await update.message.reply_text(a, parse_mode='MarkdownV2')


async def lets_cook(update, context):
    await update.message.reply_text("Напишите " + "/cook" + "  *Название блюда*", parse_mode='MarkdownV2')


async def cook(update, context):
    dish_name = update.message.text[6::]
    k = 0
    recipe = ''
    recipe += '\N{white star}' + '  Ингредиенты  ' + '\N{white star}' + 2 * "\n"
    if dish_name:
        with open('recipes.json', encoding="utf8") as f:
            d = json.load(f)
            for dish in d:
                if dish["name"].lower() == dish_name.lower():
                    recipe += dish["ing_desc"] + 2 * "\n"
                    recipe += '\N{white star}' + '  Способ приготовления  ' + '\N{white star}' + 2 * "\n"
                    recipe += dish["desc"]
                    image = dish["img"]
                    print(image)
                    k = 1
                    await update.message.reply_text(recipe, sendImageRemoteFile(dish["img"]))
                    # await update.message.reply_text(recipe)
    if k == 0:
        await update.message.reply_text(f'К сожалению, не удалось найти блюдо по названию "{dish_name}", ' \
                                        'но вы можете добавить его рецепт самостоятельно!', reply_markup=markup1)


async def cuisine(update, context):
    with open('recipes.json', encoding="utf8") as f:
        d = json.load(f)
        cuisine_dict = {}
        a = ''
        for dish in d:
            if dish['name']:
                if dish['kitchen'] not in cuisine_dict.keys():
                    cuisine_dict[dish['kitchen']] = []
                    cuisine_dict[dish['kitchen']].append(('`' + dish['name'] + '`' + 2 * '\n'))
                else:
                    cuisine_dict[dish['kitchen']].append(('`' + dish['name'] + '`' + 2 * '\n'))
        for e in cuisine_dict:
            a += (2 * '\n' + '*' + e + '*' + 2 * '\n')
            for element in cuisine_dict[e]:
                a += element
        await update.message.reply_text(a, parse_mode='MarkdownV2')


async def search_for_ingredients(update, context):
    dish_name = update.message.text[24::]
    k = 0
    recipe = ''
    recipe += '\N{white star}' + '  Название  ' + '\N{white star}' + 2 * "\n"
    if dish_name:
        with open('recipes.json', encoding="utf8") as f:
            d = json.load(f)
            for dish in d:
                for ing in dish["ingredients"]:
                    if ing.lower() == dish_name.lower():
                        recipe += dish["name"] + 2 * "\n"
                        recipe += '\N{white star}' + '  Ингредиенты  ' + '\N{white star}' + 2 * "\n"
                        recipe += dish["ing_desc"] + 2 * "\n"
                        recipe += '\N{white star}' + '  Способ приготовления  ' + '\N{white star}' + 2 * "\n"
                        recipe += dish["desc"]
                        image = dish["img"]
                        k = 1
                        await update.message.reply_text(recipe, sendImageRemoteFile(dish["img"]))
                        recipe = '\N{white star}' + '  Название  ' + '\N{white star}' + 2 * "\n"

    if k == 0:
        await update.message.reply_text(f'К сожалению, не удалось найти блюдо с ингредиентом"{dish_name}", ' \
                                        'можете добавить блюдо с таким ингредиентом. ', reply_markup=markup1)


def sendImageRemoteFile(img_url):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    remote_image = requests.get(img_url)
    photo = io.BytesIO(remote_image.content)
    photo.name = 'img.png'
    files = {'photo': photo}
    data = {'chat_id': chat_id}
    r = requests.post(url, files=files, data=data)
    print(r.status_code, r.reason, r.content)


async def paschalka(update, context):
    await update.message.reply_text(sendImageRemoteFile("https://resizer.mail.ru/p/21045944-7c5a-5582-a4d1-463" +
                                                        "cea456dac/AQAK40ZUFwV_ffXklzkbrs3L8n0eZXMOM8NGvoY29oThTdZ9" +
                                                        "g099tr4AG3xjHsn5rA05LR_Hcjdaicn5XjAUy3Nj_zU.jpg"))


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


async def Add_recipe(update, context):
    await update.message.reply_text(
        "Введите name своего dish\n"
        "Вы можете прервать это, послав команду /stop.")

    # Число-ключ в словаре states —
    # втором параметре ConversationHandler'а.
    return 1


async def first_response(update, context):
    context.user_data["name"] = update.message.text
    await update.message.reply_text(
        f"Какая классификация у {context.user_data['name']}?(Пример: горячее блюдо, закуска)")
    return 2


async def second_response(update, context):
    context.user_data["class"] = update.message.text
    await update.message.reply_text(
        f"К какому виду блюд относится {context.user_data['name']}?")
    return 3


async def third_response(update, context):
    context.user_data["type"] = update.message.text
    await update.message.reply_text(
        f"Относится ли {context.user_data['name']} к какому-нибудь фильму? Если да, то напишите название фильма, "
        f"если нет - напишите 'нет'")
    return 4


async def fourth_response(update, context):
    context.user_data["reference"] = update.message.text
    await update.message.reply_text(
        f"К какой cuisine относится {context.user_data['name']}?")
    return 5


async def fifth_response(update, context):
    context.user_data["kitchens"] = update.message.text
    await update.message.reply_text(
        f"Какие ингредиенты у {context.user_data['name']}? Через ', ', please")
    return 6


async def sixth_response(update, context):
    context.user_data["ingredients"] = update.message.text.split(', ')
    await update.message.reply_text(
        f"Крайно опишите ингредиенты в {context.user_data['name']}")
    return 7


async def seventh_response(update, context):
    context.user_data["ing_desc"] = update.message.text
    await update.message.reply_text(
        f"Напишите рецепт {context.user_data['name']}?")
    return 8


async def eighth_response(update, context):
    context.user_data["desc"] = update.message.text
    await update.message.reply_text(
        f"Пришлите ссылку на изображение вашего {context.user_data['name']}")
    return 9


async def last_response(update, context):
    context.user_data["img"] = update.message.text
    await update.message.reply_text(
        f"Спасибо за ваше блюдо!")
    print(context.user_data)

    data = json.load(open('recipes.json', encoding='utf8'))
    data.append(context.user_data)
    print(data)
    with open('recipes.json', 'w', encoding='utf8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    context.user_data.clear()
    return ConversationHandler.END


def main():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("Add_recipe", Add_recipe)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, third_response)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, fourth_response)],
            5: [MessageHandler(filters.TEXT & ~filters.COMMAND, fifth_response)],
            6: [MessageHandler(filters.TEXT & ~filters.COMMAND, sixth_response)],
            7: [MessageHandler(filters.TEXT & ~filters.COMMAND, seventh_response)],
            8: [MessageHandler(filters.TEXT & ~filters.COMMAND, eighth_response)],
            9: [MessageHandler(filters.TEXT & ~filters.COMMAND, last_response)],
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )
    application = Application.builder().token(TOKEN).build()
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("Search_for_ingredients", search_for_ingredients))
    application.add_handler(CommandHandler("Film_recipe", film))
    application.add_handler(CommandHandler("Lets_cook", lets_cook))
    application.add_handler(CommandHandler("Cat", paschalka))
    application.add_handler(CommandHandler("Cuisine", cuisine))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("cook", cook))
    application.run_polling()


d = {
    "name": "ывалплпавадилд",
    "class": "ччмиа",
    "type": "ывфвавыааы",
    "reference": "ывавиааи",
    "kitchen": "ывааыввасм",
    "ingredients": ["ваыыва", "аыва"],
    "ing_desc": "ывавывы",
    "desc": "выа",
    "img": "https://images.squarespace-cdn.com/content/v1/590be7fd15d5dbc6bf3e22d0/1569957049182-7WL6TUFOYZTIWGW892KK/Screen+Shot+2019-10-01+at+9.29.16+AM.png?format=2500w"
}
# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
