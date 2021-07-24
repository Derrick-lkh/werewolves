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

# Users = {376517278: {'user_name': 'Derrick_lkh'}, 620331844: {'user_name': 'Valentino'}, 33540344: {'user_name': 'Mant'}, 341249922: {'user_name': 'AaronPeh'}}
Users = {33540344: {'user_name': 'Mant'}, 341249922: {'user_name': 'AaronPeh'}, 376517278: {'user_name': 'Derrick_lkh'}}
room_id = "-530196332"
Roles = ["Hacker", "FBI", "FBI", "Sage", "Shield", "Civilian", "Civilian", "Civilian", "Civilian"]
Roles1 = ["FBI", "Hacker", "FBI", "Sage", "Shield", "Civilian", "Civilian", "Civilian", "Civilian"]
reset_markup = types.ReplyKeyboardRemove(selective=False)

# Game Var
hacker_target = []
voting_allowed = False


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
    for t in Users:
        if Users[t]["roles"] != "Hacker":
            option = Users[t]["user_name"]
            print(option)
            markup.row(types.KeyboardButton(option))
        if "dead" in Users[t].keys():
            if Users[t]["roles"] == "Hacker":
                print("Hacker found")
                msg = bot.send_message(t, "Choose your target:", reply_markup=markup)
                bot.register_next_step_handler(msg, hack)
            if Users[t]["roles"] == "FBI":
                print("FBI found")
                # msg = bot.send_message(t, "Choose your target:", reply_markup=markup)
                # bot.register_next_step_handler(detection, FBIDetect)


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
            option = "/vote " + str(Users[i]["user_name"])
            markup.row(types.KeyboardButton(option))
    bot.send_message(room_id, "Please vote:", reply_markup=markup)
    # bot.register_next_step_handler(msg, collate_votes)


collated_votes = []


def vote_result():
    bot.send_message(room_id, "End of Voting", reply_markup=reset_markup)
    if len(collated_votes) == 0:
        msg = "TIED! No one was Yeeted \U0001f4a9"
        bot.send_message(room_id, msg)
        return
    collated_votes.sort()
    highest_count_user = 0
    highest_count = 0
    for i in Users:
        print(i)
        count = 0
        for t in collated_votes:
            if Users[i]["user_name"] == t:
                count += 1
                print(t, count)
        if highest_count != 0:
            if count > highest_count:
                highest_count = count
                highest_count_user = i
            elif count == highest_count and highest_count != 0:
                print("Tie")
                msg = "TIED! No one was Yeeted \U0001f4a9"
                bot.send_message(room_id, msg)
                return
        else:
            highest_count = count
            highest_count_user = i
    Users[highest_count_user].update({"dead": True})
    msg = Users[highest_count_user]["user_name"] + " was Yeeted! \U0001f918\n"
    bot.send_message(room_id, msg)


#Win condition
noOfHackers = 0
def checkCondition():
    global noOfHackers
    noOfHackers = 0
    noOfSurvivors = 0
    print("Checking win condition")
    for i in Users:
        print(i)
        if "dead" not in Users[i].keys():
            noOfSurvivors += 1
            if Users[i]["roles"] == "Hacker":
                noOfHackers += 1
    if noOfHackers / noOfSurvivors > 0.49:
        msg = "Hacker won"
    elif noOfHackers == 0:
        msg = "Defenders won"
    else:
        msg = str(noOfHackers)+ "hackers remain"
    print(msg)
    bot.send_message(room_id, msg)
    return msg


@bot.message_handler(commands=['vote'])
def collate_votes(message):
    global collated_votes
    if voting_allowed:
        collated_votes.append(message.text[6:])
        msg = str(message.from_user.username) + " voted for " + str(message.text)
        bot.reply_to(message, msg)


# Hacker actions
def hack(message):
    global hacker_target
    hacker_target.append(str(message.text))
    msg = "You have selected to hack " + str(message.text)
    bot.reply_to(message, msg, reply_markup=reset_markup)


# FBI actions
def FBIDetect(message):
    msg = "You have selected to check " + str(message.text) + " he is a "
    bot.reply_to(message, msg, reply_markup=reset_markup)



@bot.message_handler(commands=['start'])
def init_room(message):
    global room_id
    room_id = message.chat.id
    print(room_id)
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
    print(chat_id)
    bot.reply_to(message, msg)


# Starts game
@bot.message_handler(commands=['start_game'])
def start_game(message):
    print("Started game")
    global voting_allowed
    msg = '''Starting Game ... ...'''
    bot.reply_to(message, msg)
    random_roles()

    night_actions()
    time.sleep(10)
    collate_night_actions()
    checkCondition()
    # Enable voting - initiate voting
    voting_allowed = True
    voting_phase()
    time.sleep(10)
    voting_allowed = False
    vote_result()
    checkCondition()
    # Disable voting - End of voting


@bot.message_handler(commands=['pm'])
def pm(message):
    chat_id = str(message.from_user.id)
    msg = ''' This is a PM '''
    bot.send_message(chat_id, msg)


def test():
    vote_result()


def main():
    while True:
        try:
            bot.polling(none_stop=False, interval=0, timeout=0)
        except:
            pass


if __name__ == '__main__':
    # test()
    main()
