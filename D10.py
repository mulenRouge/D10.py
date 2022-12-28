from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from OneWkBot_credits import bot_token
import requests
from bs4 import BeautifulSoup
def get_weather():
    appid = "5981364656:AAGSx0AIKm_U_84ZF1KxHHUENMNua9L_2Hk"
    city_id = 625144
    res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                       params={'id': city_id, 'units': 'metric', 'lang': 'by', 'APPID': appid})
    data = res.json()
    return data['weather'][0]['description'], data['main']['temp']
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Выберите:',
                              reply_markup=keyboard_main_menu())
def main_menu(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text='Выберите:',
                            reply_markup=keyboard_main_menu())
def keyboard_main_menu():
    keyboard = [
        [InlineKeyboardButton("Погода", callback_data='1'),
         InlineKeyboardButton("Курс доллара", callback_data='2'), ],
    ]
    return InlineKeyboardMarkup(keyboard)

def weather(update: Update, context: CallbackContext) -> None:
    conditions, temp = get_weather()
    conditions = capitalize(conditions)
    conditions = conditions.capitalize()

    keyboard = [[InlineKeyboardButton("Главное меню", callback_data='main')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Погода в Минске: "
                                 f"\n{conditions},\nТемпература: {temp} C",
                            reply_markup=reply_markup)
def dollar(update: Update, context: CallbackContext) -> None:
    data = requests.get('https://myfin.by/currency/usd').json()
    keyboard = [[InlineKeyboardButton("Главное меню", callback_data='main')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Курс ЦБ РБ доллара США: \n"
                                 f"{round(float(data['Valute']['USD']['Value']), 2)} руб.",
                            reply_markup=reply_markup)
def main() -> None:
    updater = Updater(bot_token)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
    updater.dispatcher.add_handler(CallbackQueryHandler(weather, pattern='1'))
    updater.dispatcher.add_handler(CallbackQueryHandler(dollar, pattern='2'))
    updater.start_polling()
    print('started')
if __name__ == '__main__':
    main()