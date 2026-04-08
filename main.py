import telebot
from games import game_stone_scissors_paper, game_guess_number, game_towns

from config import TOKEN
import random
from telebot import types

bot = telebot.TeleBot(token=TOKEN)

pet_info = {
    'name': None,
    'age': None,
    'gender': None,
    'energy': 100,
    'satiety': 100,
    'happiness': 100
}

emotions = {
    'VERY_HAPPY': '😁',
    'HAPPY': '😀',
    'SAD': '😕',
    'DIE': '😵',
    'HUNGRY': '😋',
    'SLEEPPY': '😴',
    'PLAY': '🕹',
    'DREAM': '🥱😴',
    'EAT': '🍽😋'
}


def set_name(new_name):
    new_name = new_name.strip()
    alphabet = 'qwertyuiopasdfghjklzxcvbnmйцукенгшщзхъфывапролджэячсмитьбю'
    if new_name != '' and not new_name.isdigit() and new_name[0].lower() in alphabet:
        pet_info['name'] = new_name
        return True
    return False


def set_age(new_age):
    new_age = new_age.strip()
    if new_age != '' and new_age.isdigit():  # '23'
        pet_info['age'] = int(new_age)
        return True
    return False


def set_gender(new_gender):
    new_gender = new_gender.strip()
    if new_gender != '' and new_gender.lower() in 'мж' and len(new_gender) == 1:
        pet_info['gender'] = new_gender.upper()
        return True
    return False


def set_energy(new_energy):
    if new_energy >= 100:
        new_energy = 100
        info_energy = f'У {pet_info['name']} очень много энергии! {emotions['VERY_HAPPY']}'
    elif new_energy >= 70 and new_energy < 100:
        info_energy = f'У {pet_info['name']} есть энергия! {emotions['HAPPY']}'
    elif new_energy >= 30 and new_energy < 70:
        info_energy = f'{pet_info['name']} хочет спать! {emotions['SLEEPPY']}'
    elif new_energy >= 1 and new_energy < 30:
        info_energy = f'{pet_info['name']} очень сильно хочет спать!!! {emotions['SAD']} {emotions['SLEEPPY']}'
    else:
        new_energy = 0
        info_energy = f'{pet_info['name']} умер от недостатка энергии. {emotions['DIE']}'
    pet_info['energy'] = new_energy
    return info_energy


def set_satiety(new_satiety):
    if new_satiety >= 100:
        new_satiety = 100
        info_satiety = f'У {pet_info['name']} очень много голода! {emotions['VERY_HAPPY']}'
    elif new_satiety >= 70 and new_satiety < 100:
        info_satiety = f'У {pet_info['name']} есть голод! {emotions['HAPPY']}'
    elif new_satiety >= 30 and new_satiety < 70:
        info_satiety = f'{pet_info['name']} хочет кушать! {emotions['HUNGRY']}'
    elif new_satiety >= 1 and new_satiety < 30:
        info_satiety = f'{pet_info['name']} очень сильно хочет кушать!!! {emotions['SAD']} {emotions['HUNGRY']}'
    else:
        new_satiety = 0
        info_satiety = f'{pet_info['name']} умер от недостатка голода. {emotions['DIE']}'
    pet_info['satiety'] = new_satiety
    return info_satiety


def set_happiness(new_happiness):
    if new_happiness >= 100:
        new_happiness = 100
        info_happiness = f'У {pet_info['name']} очень весёлый! {emotions['VERY_HAPPY']}'
    elif new_happiness >= 70 and new_happiness < 100:
        info_happiness = f'{pet_info['name']} весёлый! {emotions['HAPPY']}'
    elif new_happiness >= 30 and new_happiness < 70:
        info_happiness = f'{pet_info['name']} хочет играть! {emotions['PLAY']}'
    elif new_happiness >= 1 and new_happiness < 30:
        info_happiness = f'{pet_info['name']} очень сильно хочет играть!!! {emotions['SAD']} {emotions['PLAY']}'
    else:
        new_happiness = 0
        info_happiness = f'{pet_info['name']} умер от скуки. {emotions['DIE']}'
    pet_info['happiness'] = new_happiness
    return info_happiness


def user_actions_menu():
    menu = '----------Выберите варианты действий----------\n'
    menu += (f'1) Играть с {pet_info['name']}\n'
             f'2) Кормить {pet_info['name']}\n'
             f'3) Уложить спать {pet_info['name']}\n'
             f'4) Получить информацию о состоянии {pet_info['name']}\n'
             f'5) Выйти из игры\n'
             f'Выберите цифру действия')

    return menu


def start_game_stone_scissors_paper(message):
    bot.send_message(chat_id=message.chat.id, text='Введите камень, ножницы или бумага')
    bot.register_next_step_handler(message, process_game_stone_scissors_paper)


def process_game_stone_scissors_paper(message):
    current_satiety = pet_info['satiety']
    current_happiness = pet_info['happiness']
    current_energy = pet_info['energy']
    if current_energy - 25 == 0 or current_satiety - 40 == 0:
        bot.send_message(chat_id=message.chat.id,
                         text='Питомец умер😵. Чтобы начать играть нажмите "/start"')
        return
    keyboard_action = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_continue = types.KeyboardButton(text='🟢Продолжить игру🟢')
    btn_stop = types.KeyboardButton(text='⛔Завершить игру⛔')
    keyboard_action.add(btn_continue, btn_stop)
    user_answer = message.text.lower().strip()
    res = game_stone_scissors_paper(user_answer)
    bot.send_message(chat_id=message.chat.id, text=f"{res['game_res']}\nОтвет бота: {res['game_choose_bot']}")
    bot.send_message(chat_id=message.chat.id, text='Выберите дальнейшее действие: \n'
                                                   '- Продолжить игру\n'
                                                   '- Завершить игру\n'
                                                   'Введите цифру:', reply_markup=keyboard_action)

    info_energy = set_energy(current_energy - 25)
    info_happiness = set_happiness(current_happiness + 30)
    info_satiety = set_satiety(current_satiety - 40)

    bot.send_message(chat_id=message.chat.id, text=f'{info_energy}\n{info_happiness}\n{info_satiety}')
    bot.register_next_step_handler(message, repit_game_stone_scissors_paper)


def repit_game_stone_scissors_paper(message):
    text = message.text
    if text == '🟢Продолжить игру🟢':
        bot.register_next_step_handler(message, process_game_stone_scissors_paper)
    elif text == '⛔Завершить игру⛔':
        play_handler(message)


def start_game_guess_number(message):
    bot.send_message(chat_id=message.chat.id,
                     text=f'Введите случайное число в диапазоне от 5 до 15: ')
    bot.register_next_step_handler(message, process_game_guess_number)


def process_game_guess_number(message):
    current_satiety = pet_info['satiety']
    current_happiness = pet_info['happiness']
    current_energy = pet_info['energy']
    if current_energy - 25 == 0 or current_satiety - 40 == 0:
        bot.send_message(chat_id=message.chat.id,
                         text='Питомец умер😵. Чтобы начать играть нажмите "/start"')
        return
    keyboard_action = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_continue = types.KeyboardButton(text='🟢Продолжить игру🟢')
    btn_stop = types.KeyboardButton(text='⛔Завершить игру⛔')
    keyboard_action.add(btn_continue, btn_stop)
    user_number = message.text.lower().strip()
    res = game_guess_number(user_number)
    bot.send_message(chat_id=message.chat.id, text=f"{res['game_res']}\nОтвет бота: {res['game_choose_bot']}")
    bot.send_message(chat_id=message.chat.id, text='Выберите дальнейшее действие: \n'
                                                   '- Продолжить игру\n'
                                                   '- Завершить игру\n'
                                                   'Введите цифру:', reply_markup=keyboard_action)
    info_energy = set_energy(current_energy - 25)
    info_happiness = set_happiness(current_happiness + 30)
    info_satiety = set_satiety(current_satiety - 40)
    bot.send_message(chat_id=message.chat.id, text=f'{info_energy}\n{info_happiness}\n{info_satiety}')
    bot.register_next_step_handler(message, repit_game_guess_number)


def repit_game_guess_number(message):
    text = message.text
    if text == '🟢Продолжить игру🟢':
        bot.register_next_step_handler(message, process_game_guess_number)
    elif text == '⛔Завершить игру⛔':
        play_handler(message)

def start_game_towns(message):
    bot.send_message(chat_id=message.chat.id, text='Введите название города:')
    bot.register_next_step_handler(message, process_game_towns)

def process_game_towns(message):
    current_satiety = pet_info['satiety']
    current_happiness = pet_info['happiness']
    current_energy = pet_info['energy']
    if current_energy - 25 == 0 or current_satiety - 40 == 0:
        bot.send_message(chat_id=message.chat.id,
                         text='Питомец умер😵. Чтобы начать играть нажмите "/start"')
        return
    keyboard_action = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_continue = types.KeyboardButton(text='🟢Продолжить игру🟢')
    btn_stop = types.KeyboardButton(text='⛔Завершить игру⛔')
    keyboard_action.add(btn_continue, btn_stop)
    user_city = message.text.lower().strip()
    res = game_towns(user_city)
    bot.send_message(chat_id=message.chat.id, text=f"{res['game_res']}\nОтвет бота: {res['game_choose_bot']}")
    bot.send_message(chat_id=message.chat.id, text='Выберите дальнейшее действие: \n'
                                                   '- Продолжить игру\n'
                                                   '- Завершить игру\n'
                                                   'Введите цифру:', reply_markup=keyboard_action)
    info_energy = set_energy(current_energy - 25)
    info_happiness = set_happiness(current_happiness + 30)
    info_satiety = set_satiety(current_satiety - 40)
    bot.send_message(chat_id=message.chat.id, text=f'{info_energy}\n{info_happiness}\n{info_satiety}')
    bot.register_next_step_handler(message, repit_game_towns)

def repit_game_towns(message):
    text = message.text
    if text == '🟢Продолжить игру🟢':
        bot.register_next_step_handler(message, process_game_towns)
    elif text == '⛔Завершить игру⛔':
        play_handler(message)


@bot.message_handler(commands=['start'])
def pet_start(message):
    chat_id = message.chat.id
    pet_info['energy'] = 100
    pet_info['satiety'] = 100
    pet_info['happiness'] = 100
    bot.send_message(chat_id=chat_id, text='Добро пожаловать в игру с питомцем\nВведите имя питомца:')
    bot.register_next_step_handler(message, process_name)


def process_name(message):
    chat_id = message.chat.id
    name: str = message.text
    if name.startswith('/start'):
        pet_start(message)
        return
    check_name = set_name(name)
    if check_name:
        bot.send_message(chat_id=chat_id, text='Имя сохранено')
        bot.send_message(chat_id=chat_id, text='Введите возраст вашего питомца (целое число лет)')
        bot.register_next_step_handler(message, process_age)
    else:
        bot.send_message(chat_id=chat_id, text='Некорректное значение имени!\nВведите имя питомца:')
        bot.register_next_step_handler(message, process_name)
        return


def process_age(message):
    chat_id = message.chat.id
    age = message.text
    check_age = set_age(age)
    if check_age:
        bot.send_message(chat_id=chat_id, text='Возраст сохранён')
        bot.send_message(chat_id=chat_id, text='Введите пол вашего питомца (М / Ж)')
        bot.register_next_step_handler(message, process_gender)
    else:
        bot.send_message(chat_id=chat_id, text='Некорректное значение возраста!\nВведите возраст питомца:')
        bot.register_next_step_handler(message, process_age)


def process_gender(message):
    chat_id = message.chat.id
    gender = message.text
    check_gender = set_gender(gender)
    if check_gender:
        bot.send_message(chat_id=chat_id, text='Пол сохранён')
        bot.send_message(chat_id=chat_id, text=user_actions_menu())

    else:
        bot.send_message(chat_id=chat_id, text='Некорректное значение пола!\nВведите пол питомца:')
        bot.register_next_step_handler(message, process_gender)


@bot.message_handler(func=lambda message: message.text == '1')
def play_handler(message):

    if pet_info['name'] is None:
        bot.send_message(chat_id=message.chat.id,
                         text='При попытке поиграть питомца возникли ошибки. Чтобы начать играть нажмите "/start"')
        return
    if pet_info['energy'] == 0 or pet_info['satiety'] == 0 or pet_info['happiness'] == 0:
        bot.send_message(chat_id=message.chat.id,
                         text='Питомец умер😵. Чтобы начать играть нажмите "/start"')
        return
    chat_id = message.chat.id
    keyboard_game = types.InlineKeyboardMarkup(row_width=1)
    btn_game_stone_scissors_paper = types.InlineKeyboardButton(text='Камень-Ножницы-Бумага',
                                                               callback_data='btn_game_stone_scissors_paper')
    btn_game_guess_number = types.InlineKeyboardButton(text='Угадай число', callback_data='btn_game_guess_number')
    btn_game_towns = types.InlineKeyboardButton(text='Игра в города', callback_data='btn_game_towns')
    btn_leave = types.InlineKeyboardButton(text='Выйти из секции игр', callback_data='btn_leave')
    keyboard_game.add(btn_game_stone_scissors_paper, btn_game_guess_number, btn_game_towns, btn_leave)
    bot.send_message(chat_id=chat_id,
                     text=f'--------------Добро пожаловать в секцию с играми--------------\nВыберите игру:',
                     reply_markup=keyboard_game)


@bot.callback_query_handler(func=lambda callback: True)
def callback_game(callback):
    bot.answer_callback_query(callback_query_id=callback.id, text='Запрос в обработке')
    if callback.data == 'btn_game_stone_scissors_paper':
        welcome_game('Камень-Ножницы-Бумага', start_game_stone_scissors_paper, callback.message)
    elif callback.data == 'btn_game_guess_number':
        welcome_game('Угадай число', start_game_guess_number, callback.message)
    elif callback.data == 'btn_game_towns':
        welcome_game('Города', start_game_towns, callback.message)
    elif callback.data == 'btn_leave':
        bot.send_message(chat_id=callback.message.chat.id,
                         text=f'Всего доброго! Приходите к нам по чаще {emotions['PLAY']}')
        bot.send_message(chat_id=callback.message.chat.id,
                         text=user_actions_menu())
    else:
        bot.send_message(chat_id=callback.chat.id,
                         text=f'Неизвестная команда {emotions['SAD']}. Выберите предложенные варианты.')


@bot.message_handler(func=lambda message: message.text == '2')
def eat_handler(message):
    if pet_info['energy'] == 0 or pet_info['satiety'] == 0 or pet_info['happiness'] == 0:
        bot.send_message(chat_id=message.chat.id,
                         text='Питомец умер😵. Чтобы начать играть нажмите "/start"')
        return
    if pet_info['name'] is None:
        bot.send_message(chat_id=message.chat.id,
                         text='При попытке накормить питомца возникли ошибки. Чтобы начать играть нажмите "/start"')
        return
    current_happiness = pet_info['happiness']
    current_energy = pet_info['energy']

    if pet_info['satiety'] == 100:
        bot.send_message(chat_id=message.chat.id, text=f'{pet_info['name']} не голоден {emotions['VERY_HAPPY']}')
    else:
        set_satiety(100)
        info_happiness = set_happiness(current_happiness - 20)
        info_energy = set_energy(current_energy - 25)
        bot.send_message(chat_id=message.chat.id, text=f'{pet_info['name']} ест {emotions['EAT']}')
        bot.send_message(chat_id=message.chat.id, text=info_happiness)
        bot.send_message(chat_id=message.chat.id, text=info_energy)


@bot.message_handler(func=lambda message: message.text == '3')
def sleep_handler(message):
    if pet_info['energy'] == 0 or pet_info['satiety'] == 0 or pet_info['happiness'] == 0:
        bot.send_message(chat_id=message.chat.id,
                         text='Питомец умер😵. Чтобы начать играть нажмите "/start"')
        return
    if pet_info['name'] is None:
        bot.send_message(chat_id=message.chat.id,
                         text='При попытке сна питомца возникли ошибки. Чтобы начать играть нажмите "/start"')
        return
    current_satiety = pet_info['satiety']
    current_happiness = pet_info['happiness']

    if pet_info['energy'] == 100:
        bot.send_message(chat_id=message.chat.id, text=f'{pet_info['name']} не хочет спать {emotions['VERY_HAPPY']}')
    else:
        set_energy(100)
        info_satiety = set_satiety(current_satiety - 40)
        info_happiness = set_happiness(current_happiness - 30)
        bot.send_message(chat_id=message.chat.id, text=f'{pet_info['name']} спит {emotions['DREAM']}')
        bot.send_message(chat_id=message.chat.id, text=info_happiness)
        bot.send_message(chat_id=message.chat.id, text=info_satiety)


@bot.message_handler(func=lambda message: message.text == '4')
def info_handler(message):
    if pet_info['energy'] == 0 or pet_info['satiety'] == 0 or pet_info['happiness'] == 0:
        bot.send_message(chat_id=message.chat.id,
                         text='Питомец умер😵. Чтобы начать играть нажмите "/start"')
        return
    if pet_info['name'] is None:
        bot.send_message(chat_id=message.chat.id,
                         text='При попытке узнать информацию о питомце возникли ошибки. Чтобы начать играть нажмите "/start"')
        return
    name = pet_info['name']
    age = pet_info['age']
    gender = pet_info['gender']
    energy = pet_info['energy']
    satiety = pet_info['satiety']
    happiness = pet_info['happiness']

    info = (f'Имя: {name}\n'
            f'Возраст: {age}\n'
            f'Пол: {gender}\n'
            f'-----Характеристики-----\n'
            f'Уровень энергии: {energy} / 100\n'
            f'Уровень сытости: {satiety} / 100\n'
            f'Уровень счастья: {happiness} / 100')

    bot.send_message(chat_id=message.chat.id, text=info)


@bot.message_handler(func=lambda message: message.text == '5')
def end_game_handler(message):
    pet_info['name'] = None
    pet_info['age'] = None
    pet_info['gender'] = None
    pet_info['energy'] = 100
    pet_info['satiety'] = 100
    pet_info['happiness'] = 100
    bot.send_message(message.chat.id, text=f'До скорых встреч! {emotions['HAPPY']}')


@bot.message_handler(func=lambda message: True)
def welcome_game(game_name, game_func, message):
    bot.send_message(chat_id=message.chat.id, text=f'Добро пожаловать в игру "{game_name}"')
    game_func(message)
print(111)

bot.infinity_polling()
