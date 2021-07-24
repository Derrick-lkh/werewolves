import os
import telebot
from telebot import types
from dotenv import load_dotenv
import random
import requests
import time

load_dotenv()
token = os.getenv('AUT_TOKEN')
bot = telebot.TeleBot(token)


Users = {376517278: {'user_name': 'Derrick_lkh'}, 620331844: {'user_name': 'Valentino'}, 33540344: {'user_name': 'Mant'}, 341249922: {'user_name': 'AaronPeh'}}
room_id = ""
Roles = ["Hacker", "FBI", "FBI", "Sage", "Shield", "Civilian", "Civilian", "Civilian", "Civilian"]
Roles1 = ["FBI", "Hacker", "FBI", "Sage", "Shield", "Civilian", "Civilian", "Civilian", "Civilian"]
reset_markup = types.ReplyKeyboardRemove(selective=False)

# Game Var
hacker_target = []


# Define Game functions
def start_game():
    return True


def add_to_game(user_name, chat_id):
    print("add to game", chat_id in Users)
    if chat_id in Users:
        return False
    else:
        Users[chat_id] = {"user_name": user_name}
        return True


def random_roles():
    # random.shuffle(Roles)
    print(Roles)
    count = 0
    for i in Users:
        Users[i].update({"roles": Roles[count]})
        msg = "You are the " + Roles[count]
        bot.send_message(i, msg, reply_markup=reset_markup)
        count += 1
    print(Users)


def night_actions():
    markup = types.ReplyKeyboardMarkup(row_width=1)
    action_list = []
    for i in Users:
        if Users[i]["roles"] != "Hacker":
            option = Users[i]["user_name"]
            print(option)
            markup.row(types.KeyboardButton(option))
    for t in Users:
        if Users[t]["roles"] == "Hacker":
            print("Hacker found")
            msg = bot.send_message(t, "Choose your target:", reply_markup=markup)
            bot.register_next_step_handler(msg, hack)


def collate_night_actions():
    msg = "During the night,\n"
    try:
        for i in Users:
            if Users[i]["user_name"] in hacker_target:
                Users[i].update({"dead": True})
                msg = msg + str(Users[i]["user_name"]) + " was killed in action \U0001f480\n"
    except:
        pass
    bot.send_message(room_id, msg)


def voting_phase():
    markup = types.ReplyKeyboardMarkup(row_width=2)
    print("voting phase")
    for i in Users:
        if "dead" in Users[i].keys():
            print(Users[i]["dead"])
            pass
        else:
            option = Users[i]["user_name"]
            markup.row(types.KeyboardButton(option))
    msg = bot.send_message(room_id, "Please vote:", reply_markup=markup)
    bot.register_next_step_handler(msg, collate_votes)


collated_votes = []


def collate_votes(message):
    collated_votes.append(message.text)
    msg = str(message.from_user.username) + " voted for " + str(message.text)
    bot.reply_to(message, msg)


# Hacker actions
def hack(message):
    global hacker_target
    hacker_target.append(str(message.text))
    msg = "You have selected to hack " + str(message.text)
    bot.reply_to(message, msg, reply_markup=reset_markup)


@bot.message_handler(commands=['start'])
def init_room(message):
    global room_id
    room_id = message.chat.id
    msg = '''**C4X Werewolves Started**\nUse /join to enter the game'''
    bot.reply_to(message, msg)


# Join game
@bot.message_handler(commands=['join'])
def join_game(message):
    msg = ''''''
    chat_id = message.from_user.id
    user_name = str(message.from_user.username)
    if add_to_game(user_name, chat_id):
        msg = user_name + " Joined the game"
    else:
        msg = user_name + " Already in the game"
    print(Users)
    bot.reply_to(message, msg)


# Starts game
@bot.message_handler(commands=['start_game'])
def start_game(message):
    msg = '''Starting Game ... ...'''
    bot.reply_to(message, msg)
    random_roles()

    night_actions()
    time.sleep(20)
    collate_night_actions()
    voting_phase()



@bot.message_handler(commands=['pm'])
def pm(message):
    chat_id = str(message.from_user.id)
    msg = ''' This is a PM '''
    bot.send_message(chat_id, msg)


def test():
    for i in Users:
        if "dead" in Users[i].keys():
            print("dead")


def main():
    while True:
        try:
            bot.polling(none_stop=False, interval=0, timeout=0)
        except:
            pass


if __name__ == '__main__':
    # test()
    main()
