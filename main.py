from cgitb import text
from requests import request
import config
import logging
from aiogram.utils.callback_data import CallbackData
from aiogram import Bot, Dispatcher, executor,types
from pars import parse

rating = 0.0
places = []
city1 = "/{}"
city2 = ""
deliverytime = 0

callBackInfo = CallbackData("city","kitchen")

bot = Bot(token = config.TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
deliverytime = 0.0

@dp.message_handler(commands = "special_buttons")
async def comandSpecialButtons(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(types.KeyboardButton(text = "Запросить геолокацию", request_location = True))
    await message.answer("Выберите действие:", reply_markup = keyboard)


@dp.message_handler(commands = "start")
async def welcome(message: types.Message ):
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton(text = "Оформить доставку 🐢",callback_data='order')
    markup.add(item1)
    sti = open('/Users/fedorbulygin/Desktop/Project/sticker.webp','rb') 
    await message.answer_sticker(sti)   
    await message.answer(text = "Здравствуйте! Вас приветствует телеграм бот МИФИ по доставке еды!",reply_markup=markup)

@dp.callback_query_handler(text = "order")
async def callBackProcess(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    geoKey = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
    geoKey.add(types.KeyboardButton(text = "Отправить геолокацию", request_location = True))
    buttons=[ 
        types.InlineKeyboardButton(text = "Москва",callback_data = 'city_moscow'),
        types.InlineKeyboardButton(text = "Санкт-Петербург",callback_data = 'city_spb'),
        types.InlineKeyboardButton(text = "Екатеринбург",callback_data = 'city_ekb'),
    ]
    cityKeyboard = types.InlineKeyboardMarkup(row_width=2) 
    cityKeyboard.add(*buttons)
    await callback_query.message.answer(text = "Выберите город:",reply_markup = cityKeyboard)
    await callback_query.message.answer(text = "Я могу сделать все за тебя. Ты можешь нажать на кнопку и передать мне свое местоположение",reply_markup = geoKey)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('city_'))
async def callbacks_city(callback_query: types.CallbackQuery ):
    #Ответили на callback
    await bot.answer_callback_query(callback_query.id)
    global city1
    global city2
    city2 = callback_query.data[5:len(callback_query.data)]
    city1 = city1.format(city2)
    callback_query_id = callback_query.id
    parse(city1,places)
    
    rateKey = types.InlineKeyboardMarkup(row_width=2,resize_keyboard=True)
    buttons = [
        types.InlineKeyboardButton(text = "От 4.0", callback_data='_r4.0'),
        types.InlineKeyboardButton(text = "От 4.1", callback_data='_r4.1'),
        types.InlineKeyboardButton(text = "От 4.2", callback_data='_r4.2'),
        types.InlineKeyboardButton(text = "От 4.3", callback_data='_r4.3'),
        types.InlineKeyboardButton(text = "От 4.4", callback_data='_r4.4'),
        types.InlineKeyboardButton(text = "От 4.5", callback_data='_r4.5'),
        types.InlineKeyboardButton(text = "От 4.6", callback_data='_r4.6'),
        types.InlineKeyboardButton(text = "От 4.7", callback_data='_r4.7'),
        types.InlineKeyboardButton(text = "От 4.8", callback_data='_r4.8'),
        types.InlineKeyboardButton(text = "От 4.9", callback_data='_r4.9'),
        types.InlineKeyboardButton(text = "От 5.0", callback_data='_r5.0')
    ]
    rateKey.add(*buttons)
    await callback_query.message.answer(text = "Какой минимальный рейтинг должен быть у ресторана?",reply_markup = rateKey)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('_r'))
async def setRating(callback_query: types.CallbackQuery ):
    global rating
    rating = float(callback_query.data[2:])
    print(rating)
    timeKey = types.InlineKeyboardMarkup(row_width=2,resize_keyboard=True)
    buttons = [
        types.InlineKeyboardButton(text = "До 30 минут",callback_data='_t40'),
        types.InlineKeyboardButton(text = "До 45 минут",callback_data='_t55'),
        types.InlineKeyboardButton(text = "До 1 часа",callback_data='_t95'),
        types.InlineKeyboardButton(text = "До 90 минут",callback_data='_t120'),
        types.InlineKeyboardButton(text = "До 2 часов",callback_data='_t240')
    ]
    timeKey.add(*buttons)
    await callback_query.message.answer(text = "Сколько времени вы готовы ждать доставку?",reply_markup= timeKey)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('_t'))
async def setRating(callback_query: types.CallbackQuery):
    global deliverytime
    global places
    deliverytime = int(callback_query.data[2:])
    print(deliverytime)
    if (city2 == "moscow"):
        await callback_query.message.answer(text = "Список ресторанов в Москве: ")
        for place in places:
            if (place['rate'] == "Мало оценок"):
                break
            if ( rating <= (float(place['rate'])  ) and (  deliverytime >= int(place['time'][3:5])) ):
                print("|",place['title'],"|",place['link'],"|","|",place['rate'],"|",place['time'])
                await callback_query.message.answer(text = (place['title']+'\n'+"Рейтинг: "+place['rate']+'\n'+"Время доставки: ~"+place['time']+'\n'+place['link']) )


    elif (city2 == "spb"):
        await callback_query.message.answer(text = "Список ресторанов в Санкт-Петербурге:")
        for place in places:
            if (place['rate'] == "Мало оценок"):
                break
            if ( rating <= (float(place['rate'])  ) and (  deliverytime >= int(place['time'][3:5])) ):
                print("|",place['title'],"|",place['link'],"|","|",place['rate'],"|",place['time'])
                await callback_query.message.answer(text = (place['title']+'\n'+"Рейтинг: "+place['rate']+'\n'+"Время доставки: ~"+place['time']+'\n'+place['link']) )

    elif (city2 == "ekb"):
        await callback_query.message.answer(text = "Список ресторанов в Екатеринбурге: ")
        for place in places:
            if (place['rate'] == "Мало оценок"):
                break
            if ( rating <= (float(place['rate'])  ) and (  deliverytime >= int(place['time'][3:5])) ):
                print("|",place['title'],"|",place['link'],"|","|",place['rate'],"|",place['time'])
                await callback_query.message.answer(text = (place['title']+'\n'+"Рейтинг: "+place['rate']+'\n'+"Время доставки: ~"+place['time']+'\n'+place['link']) )

@dp.message_handler(content_types = ["location"])
async def location(message):
    if message.location is not None:
        print("latitude: %s; longitude: %s" % (message.location.latitude, message.location.longitude))
        if ( (message.location.latitude > 55.0 and message.location.latitude < 65.0) and ( message.location.longitude > 35 and message.location.longitude < 45) ):
            print("СЗАО")
            await message.answer(text = "Ваш город Москва, округ СЗАО")

executor.start_polling(dp, skip_updates=True)
