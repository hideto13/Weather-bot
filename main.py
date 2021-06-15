import telebot, bs4, requests
from telebot import types
from pyowm.owm import OWM
from pyowm.utils import config as cfg

config = cfg.get_default_config()
config['language'] = 'ru'

owm = OWM('YOUR_WEATHER_TOKEN', config)
bot = telebot.TeleBot('YOUR_TELEBOT_TOKEN')


def getcity():
    z = ''
    s = requests.get('https://randstuff.ru/city/')
    b = bs4.BeautifulSoup(s.text, "html.parser")
    p = b.select('.city-name')
    for x in p:
        s = (x.getText().strip())
        z = z + s + '\n\n'
    return s

def send_message(message):

    try:
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(message.text)
        weather = observation.weather
        temp = weather.temperature("celsius")["temp"]
        temp = round(temp, 1)

        answer = "В городе " + message.text + " сейчас " + weather.detailed_status + "." + "\n"
        answer += "Температура около: " + str(temp) + " С"

    except Exception:
        answer = "Не найден город или что-то пошло не так, попробуйте ввести название снова. Перейти к описанию => /help\n"
    return answer


@bot.message_handler(commands=["help"])
def help_message(message):
    mainmenu = types.InlineKeyboardMarkup()
    catalog = types.InlineKeyboardButton(text="Случайный город", callback_data="Randomcity")
    mainmenu.add(catalog, )
    bot.send_message(message.chat.id,
                     "Этот бот показывает погоду в текущее время в выбранном городе. Введите название города:",
                     reply_markup=mainmenu)


@bot.callback_query_handler(func=lambda a: True)
def inline_a(a):
    class message:
        text = str(getcity())
    answer = send_message(message)
    bot.send_message(a.message.chat.id, answer)


@bot.message_handler(content_types=['text'])
def send_message_1(message):
    answer = send_message(message)
    bot.send_message(message.chat.id, answer)

if __name__ == '__main__':
    bot.infinity_polling()
