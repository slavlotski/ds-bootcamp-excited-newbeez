import os

import numpy as np
from coolname import generate
import random
from mlem.api import load
from mlem.runtime.client import HTTPClient
from telegram import Update
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters,CallbackQueryHandler, ConversationHandler
import requests #<--added

# create a telegram bot and paste it here, or use `flyctl secrets set TELEGRAM_TOKEN=token` to set it secretly
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/davanstrien/convnext-tiny-224-wikiart"
WIKI_ART_TOKEN = "Bearer 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"
headers = {"Authorization": WIKI_ART_TOKEN}
# add URL of you REST API app here
client = HTTPClient(host="https://art-expert-excited-newbeez.fly.dev", port=None) 


# Stages
START_ROUTES, END_ROUTES = range(2)
# Callback data
ONE, TWO, THREE, FOUR, FIVE = ['estimate_price','auction','artist', 'courses','help'] #<--------added FIVE courses

f_greeting_path = 'content/greetings.txt'
f_smth_went_wrong_path ='content/smth_went_wrong_errors.txt'
f_auctions_path = 'content/auctions.txt'
f_artists_path = 'content/artists.txt'
f_courses_path = 'content/courses.txt'
f_dates_path = 'content/date.txt' #<--------added 

button_list = [
    [InlineKeyboardButton("Оценить",callback_data='estimate_price'),
    InlineKeyboardButton("Auction",callback_data='auction'),
    InlineKeyboardButton("Artists",callback_data='artists'),
    InlineKeyboardButton('Курсы',callback_data = 'courses'),
    InlineKeyboardButton("Помощь",callback_data='helper')]
]

def get_random_text(path):
    f = open(path, 'r', encoding='UTF-8')
    text = f.read().split('\n')
    f.close()
    return random.choice(text)


async def button(update, _):
    query = update.callback_query
    variant = query.data

    await query.answer()


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')
    


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        f"Привет, {update.effective_user.first_name}! На связи ИИ. (Yes, I mean the ARTIFICIAL INTELLEGENCE). \n\n" #<--------changed msg
        f"Я взял все картины проданные на аукционе sothebys.com и "
        "обучил свою нейросеть, чтобы предсказать их стоимость.\n\n"
        "Отправь мне фотографию своего рисунка и я скажу, how much bucks он может стоить.",
    )


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(f'{update.effective_user.first_name}.\n Введите /start чтобы попасть в главное меню и управлять кнопками. Или воспользуйтесь командами\n'
    '/auction вывести список аукционов\n'
    '/artists рассказать о топ-100 вдохновляющих современных художниках\n'
    '/courses порекомендовать онлайн-курсы\n'
    )

async def get_random_greeting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(f'{update.effective_user.first_name}!\n{get_random_text(f_greeting_path)}\n А ещё я могу порекомендовать аукционы, художественные курсы и рассказать про топ-100 вдохновляющих современных художников.') #<---added f-string
    reply_markup = InlineKeyboardMarkup(button_list)
    await update.message.reply_text('Чего изволите?',reply_markup=reply_markup)
    return START_ROUTES
    

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    reply_markup = InlineKeyboardMarkup(button_list)
    await query.message.reply_text('Чего изволите?',reply_markup=reply_markup)
    return START_ROUTES

#####----------------------
# added
###

def req(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data) #<--- added import requests
    return response.json()

def get_genre(filename):
    predictions = req(filename)
    return predictions[0]['label']
 
#####end#####----------------------

async def photo_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download_to_drive('user_photo.jpg')
    res = client.predict("user_photo.jpg")

    pic_name = " ".join(generate(np.random.randint(2, 5))).capitalize() #<--------changed Date:
    caption = f"""Original Title: {np.random.choice(["Unknown", pic_name])}
    Author: {{author}}
    Date: {get_random_text(f_dates_path)} 
    Estimated price: {{price}} $ [Sothebys auction]
    Style: {np.random.choice(["Surrealism", "Realism", "Abstract Art", "Impressionism"])}
    Genre: {get_genre("user_photo.jpg")}
    Media: {np.random.choice(["oil", "pencil", "photo"])}
    Similar painting: https://www.sothebys.com/en/buy/fine-art/paintings/abstract/_eve-ackroyd-woman-as-still-life-4eb9
        """
        # Price is estimated using Sothebys.com data
        # Other characteristics can be predicted using Wikiart data

    await update.message.reply_photo(
            update.message.photo[-1].file_id,
            caption=caption.format(
                price=res["price"],
                author=update.effective_user.full_name,
            )
        )
    reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Еще",callback_data='estimate_price'),
        InlineKeyboardButton("Auction",callback_data='auction'),]
        ])
    await update.message.reply_text('Хотите узнать, где можно выставить работу для продажи? Или хотите оценить еще одну картину?',reply_markup=reply_markup)
    return START_ROUTES 

async def estimate_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if hasattr(update, 'callback_query'):
        query = update.callback_query
        await query.answer()
        await query.message.reply_text('Загрузите вашу картину')
    return START_ROUTES
        

async def auction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(get_random_text(f_auctions_path))
    reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Да",callback_data='auction'),
        InlineKeyboardButton("Нет",callback_data='artists'),
        InlineKeyboardButton("Завершить",callback_data='bye')] #<----added btn
        ])
    await query.message.reply_text('Показать еще аукционы?',reply_markup=reply_markup)
    return START_ROUTES

async def artists(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(f'Топ-100 современных художников:\n{get_random_text(f_artists_path)}') #<---added f-string
    reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Да",callback_data='artists'),
        InlineKeyboardButton("Меню",callback_data='menu'),
        InlineKeyboardButton("Завершить",callback_data='bye')]
        ])
    await query.message.reply_text('Показать еще художника?',reply_markup=reply_markup)
    return START_ROUTES

async def helper(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    reply_markup = InlineKeyboardMarkup(button_list)
    await query.message.reply_text('Если думаешь, что запутался, ты не писал код этого бота...\nА если серьезно, вбей /start и/или следуй зову кнопок',reply_markup=reply_markup)
    return START_ROUTES    

async def bye(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("Возвращайся за вдохновением и мотивацией!",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Тык',callback_data='end')]]))

    return END_ROUTES

async def courses(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(f'Узнай, где прокачать свои скиллы:\n{get_random_text(f_courses_path)}') #<---added f-string
    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Да',callback_data='courses'),
                                        InlineKeyboardButton('Меню',callback_data='menu')
                                        ]])
    await query.message.reply_text("Показать еще курс?",reply_markup=reply_markup)

    return START_ROUTES

async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="See you next time!")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", get_random_greeting)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(estimate_price,pattern='^'+'estimate_price'+'$'),
                CallbackQueryHandler(auction,pattern='^'+'auction'+'$'),
                CallbackQueryHandler(artists,pattern='^'+'artists'+'$'),
                CallbackQueryHandler(bye,pattern='^'+'bye'+'$'),
                CallbackQueryHandler(menu,pattern='^'+'menu'+'$'),
                CallbackQueryHandler(helper,pattern='^'+'helper'+'$'),
                CallbackQueryHandler(courses,pattern='^'+'courses'+'$')
            ],
            END_ROUTES:[
                CallbackQueryHandler(end,pattern='^'+'end'+'$')
            ]
        },
        fallbacks=[CommandHandler("start", get_random_greeting)]

    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("start", get_random_greeting))
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("auction", auction))
    app.add_handler(CommandHandler("artists", artists))
    app.add_handler(MessageHandler(filters.PHOTO, photo_received))

    app.run_polling()


if __name__ == "__main__":
    main()
