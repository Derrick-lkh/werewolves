import os
import dotenv
import telebot
from telebot import types
from dotenv import load_dotenv
import random
# import requests
import time
from UI import narrative_para
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


load_dotenv()
token = os.getenv('AUT')
bot = telebot.TeleBot(token)
# Admin
reset_markup = types.ReplyKeyboardRemove(selective=False)
# Admin
host_id = ""
joined_msg_id = ""
joined_msg = ""
Users = {}
room_id = ""
# Game Var
shieldTarget = ""
hacker_target = []
collated_votes = []
voting_options = []
Roles = []
Init_game = True
night_actions_allowed = False
night_actions_message = ""


def reset_game():
    global Users, room_id, hacker_target, Init_game, collated_votes, shieldTarget, night_actions_message, sentJoinMsg, joined_msg_id, joined_msg
    sentJoinMsg = []
    nameList = []
    Users = {}
    room_id = ""
    # Game Var
    shieldTarget = ""
    night_actions_message = ""
    joined_msg_id = ""
    joined_msg = ""
    Init_game = True
    hacker_target = []
    collated_votes = []


# Define Game functions
def add_to_game(user_name, chat_id):
    if chat_id in Users:
        msg = user_name + " Already in the game"
        bot.send_message(room_id, msg)
        return False
    else:
        if len(Users) > 9:
            bot.send_message(room_id, "Room is full")
            return False
        else:
            Users[chat_id] = {"user_name": user_name, "dead":False, "revived": False}
            return True


def roles_quantity():
    Prefix_roles = ["FBI", "Hacker","Sage","Shield"]
    if 4 <= len(Users) <= 7:
        cv_counter = len(Users) - 4
        for i in range(0, cv_counter):
            Prefix_roles.append("Civilian")
    elif 8 <= len(Users) <= 10:
        cv_counter = len(Users) - 6
        Prefix_roles.append("Hacker")
        Prefix_roles.append("FBI")
        for i in range(0, cv_counter):
            Prefix_roles.append("Civilian")
    return Prefix_roles


def random_roles():
    global Roles
    Roles = roles_quantity()
    random.shuffle(Roles)
    count = 0
    for i in Users:
        Users[i].update({"roles": Roles[count]})
        msg = "You are the " + Roles[count]
        bot.send_message(i, msg, reply_markup=reset_markup)
        count += 1
    print(Users)


def night_actions():
    global shieldTarget, hacker_target
    hacker_target = []
    has_dead = False
    shieldTarget = ""
    # gif_animation(room_id ,"granny")
    bot.send_message(room_id, "\U0001f4a4 Night is falling in SAFTI. Everyone is going to sleep. Shut your eyes and don't peek \U0001f648")
    markupHacker = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard = True)
    markupAlive = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard = True)
    markupSage = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard = True)
    action_list = []
    for i in Users:
        option = Users[i]["user_name"]
        if Users[i]["dead"] == False:
            markupAlive.row(types.KeyboardButton(option))
            if Users[i]["roles"] != "Hacker":
                markupHacker.row(types.KeyboardButton(option))
        else:
            markupSage.row(types.KeyboardButton(option))
            has_dead = True
    for t in Users:
        if Users[t]["dead"] == False:
            if Users[t]["roles"] == "Hacker":
                print("Hacker found")
                msg = bot.send_message(t, "Please select your target \U0001f3af ", reply_markup=markupHacker)
                bot.register_next_step_handler(msg, hack)
            elif Users[t]["roles"] == "FBI":
                print("FBI found")
                msg = bot.send_message(t, "Who do you think is sus? \U0001f50d", reply_markup=markupAlive)
                bot.register_next_step_handler(msg, FBIDetect)
            elif Users[t]["roles"] == "Sage":
                if has_dead is True:
                    msg = bot.send_message(t, "Who do you want to save? \U0001f691", reply_markup=markupSage)
                    bot.register_next_step_handler(msg, sage_res)
                else:
                    bot.send_message(t, "There is no one to save \U0001f634")
            elif Users[t]["roles"] == "Shield":
                msg = bot.send_message(t, "Choose player to shield: ", reply_markup=markupAlive)
                bot.register_next_step_handler(msg, shield_prot)
                


def collate_night_actions():
    global night_actions_message
    if len(hacker_target) == 0:
        night_actions_message = night_actions_message + "no one was killed \U0001f480"
    else:
        for i in Users:
            if Users[i]["user_name"] in hacker_target:
                if Users[i]["user_name"] != shieldTarget:
                    Users[i].update({"dead": True})
                    night_actions_message = night_actions_message + "@" + str(Users[i]["user_name"]) + " was killed in action \U0001f480\n"
                    gif_animation(room_id, "killer")
                else:
                    night_actions_message = night_actions_message + "Shield prevented an attack \U0001f481\n"
                    gif_animation(room_id, "shield")
    bot.send_message(room_id, night_actions_message)


def voting_phase():
    global collated_votes, voting_options
    collated_votes = []
    voting_options = []
    print("voting phase")
    for i in Users:
        if Users[i]["dead"]:
            print(Users[i]["dead"])
            pass
        else:
            option = str(Users[i]["user_name"])
            voting_options.append(option)
    bot.send_poll(room_id, question = "Place your votes \U0001f47d",options= voting_options, is_anonymous=False, open_period=20, timeout=20)

        
def vote_result():
    print(collated_votes)
    if len(collated_votes) == 0:
        msg = "TIED! No one was Yeeted \U0001f90f"
        gif_animation(room_id, "noyeet")
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
                gif_animation(room_id, "noyeet")
                bot.send_message(room_id, msg)
                return
        else:
            highest_count = count
            highest_count_user = i
    Users[highest_count_user].update({"dead": True})
    msg = "@" + Users[highest_count_user]["user_name"] + " was Yeeted! \U0001f918\n"
    gif_animation(room_id, "yeet")
    bot.send_message(room_id, msg)


# Win condition
noOfHackers = 0


def checkCondition():
    global Init_game
    if Init_game:
        Init_game = False
        return True
    global noOfHackers
    noOfHackers = 0
    noOfSurvivors = 0
    print("Checking win condition")
    for i in Users:
        if Users[i]["dead"] == False:
            noOfSurvivors += 1
            if Users[i]["roles"] == "Hacker":
                noOfHackers += 1
    if noOfHackers / noOfSurvivors > 0.49:
        msg = "Hacker won"
        gif_animation(room_id, "f")
        bot.send_message(room_id, msg)
        return False
    elif noOfHackers == 0:
        msg = "Defenders won"
        gif_animation(room_id, "rick")
        bot.send_message(room_id, msg)
        return False
    else:
        msg = str(noOfHackers) + " hacker(s) remain"
        gif_animation(room_id, "hacker")
        bot.send_message(room_id, msg)
        return True



# Hacker actions
def hack(message):
    global hacker_target
    if night_actions_allowed:
        hacker_target.append(str(message.text))
        msg = "You have selected to attack " + str(message.text)
        bot.reply_to(message, msg, reply_markup=reset_markup)


# FBI actions
def FBIDetect(message):
    if night_actions_allowed:
        target = str(message.text)
        print("FBI selected", target)
        for i in Users:
            if Users[i]["user_name"] == target:
                targetRole = Users[i]["roles"]
                msg = str(target) + " identity is " + str(targetRole)
                bot.reply_to(message, msg, reply_markup=reset_markup)

          
# Sage actions
def sage_res(message):
    global Users, night_actions_message
    if night_actions_allowed:
        sage_target = str(message.text)
        msg = ""
        for i in Users:
            print("sage res", Users[i]["user_name"])
            if Users[i]["user_name"] == sage_target:
                if Users[i]["revived"] is not True:
                    msg = "\U0001f90c You have selected to save " + sage_target
                    Users[i]["dead"] = False
                    Users[i]["revived"] = True
                    print("sage revive", i)
                    night_actions_message = night_actions_message + "Sage revived @" + sage_target + "\U0001f90c\n"
                    gif_animation(i, "sage")
                    bot.send_message(i, "You have been resurrected")
                    bot.reply_to(message, msg, reply_markup=reset_markup)
                    return
                else:
                    msg = sage_target + " have been revived before. Choose another player to revive."
                    bot.reply_to(message, msg)
                    break
            
  
# Shield action
def shield_prot(message):
    global shieldTarget
    if night_actions_allowed:
        shieldTarget = str(message.text)
        msg = "You have selected to protect " + shieldTarget
        bot.reply_to(message, msg, reply_markup=reset_markup)
        

def gif_animation(message ,name):
    file_name = name
    print(file_name)
    photo = open(file_name + '.gif', 'rb')
    bot.send_animation(message, photo)
    time.sleep(1)
    return


def auth(message):
    global host_id
    id = message.from_user.id
    if host_id == "":
        host_id = str(id)
        return False
    elif host_id == str(id):
        return False
    else:
        bot.reply_to(message, "You are not the host \U0001f346\U0001f4a6")
        return True
    

@bot.message_handler(commands=['reset'])
def reset_config(message):
    global host_id
    if auth(message):
        return
    reset_game()
    host_id = ""
    bot.reply_to(message, "@" + message.from_user.username + " gave up as host \U0001f4a9")
    
  
@bot.message_handler(commands=['start'])
def init_room(message):
    global room_id, joined_msg_id, joined_msg, host_id
    if auth(message):
        return
    reset_game()
    room_id = message.chat.id
    print(room_id)
    msg = "Welcome to Elango's Nightmare\U0001f921\U0001f64d\U0001f3ff\u200D\u2642\uFE0F\n @" + str(message.from_user.username) + " is now the host \U0001f48e\U0001f932\n"
    bot.send_message(room_id, msg)


# Starts game
@bot.message_handler(commands=['start_game'])
def start_game(message):
    if auth(message):
        return
    global night_actions_allowed, night_actions_message
    msg = '''Starting Game ... ...'''
    bot.reply_to(message, msg)
    random_roles()

    while checkCondition():
        time.sleep(5)
        night_actions_allowed = True
        night_actions_message = "During the night, \U0001f346\n"
        night_actions()
        time.sleep(25)
        night_actions_allowed = False
        collate_night_actions()
        if checkCondition():
            countdown()
            time.sleep(5)
            voting_phase()
            time.sleep(20)
            vote_result()
        else:
            msg = ''' THANKS FOR PLAYING! Use /start to reset the game \U0001f47b '''
            bot.send_message(room_id, msg)
            return
    msg = ''' THANKS FOR PLAYING! Use /start to reset the game \U0001f47b '''
    bot.send_message(room_id, msg)


@bot.message_handler(commands=['pm'])
def pm(message):
    chat_id = str(message.from_user.id)
    msg = ''' This is a PM '''
    bot.send_message(chat_id, msg)


@bot.message_handler(commands=['rules','list_role','FBI_Role','hacker_Role','sage_Role','shield_Role','civilian_Role'])
def role_handler(message):
    cmd_input = message.text[1:]
    if "rules" in cmd_input:
      cmd_input = "rules"
    elif "list_role" in cmd_input:
      cmd_input = "list_role"
    elif "Role" in cmd_input:
      gif_animation(message.chat.id, narrative_para[cmd_input + "_gif"])
    msg = narrative_para[cmd_input]
    bot.reply_to(message, msg)
  
  
@bot.poll_answer_handler()
def poll_result(msg):
    global collated_votes
    if msg.user.id in Users:
      if Users[msg.user.id]["dead"] != True:
        selected = str(msg.option_ids)
        slice_selected = int(selected[1:-1])
        collated_votes.append(voting_options[slice_selected])
    

def countdown():
  text = "Time remaining for discussion: 60 seconds.\n\n\U0001f95a\U0001f95a\U0001f95a\U0001f95a"
  sent = bot.send_message(room_id, text)
  time.sleep(15)
  bot.edit_message_text(chat_id=room_id, message_id=sent.message_id, text="Time remaining for discussion:45 seconds left\n\n\U0001f423\U0001f95a\U0001f95a\U0001f95a")
  time.sleep(15)
  bot.edit_message_text(chat_id=room_id, message_id=sent.message_id, text="Time remaining for discussion:30 seconds left\n\n\U0001f423\U0001f423\U0001f95a\U0001f95a")
  time.sleep(15)
  bot.edit_message_text(chat_id=room_id, message_id=sent.message_id, text="Time remaining for discussion:15 seconds left\n\n\U0001f423\U0001f423\U0001f423\U0001f95a")
  time.sleep(10)
  bot.edit_message_text(chat_id=room_id, message_id=sent.message_id, text="Time remaining for discussion:5 seconds left\n\n\U0001f423\U0001f423\U0001f423\U0001f423")
  time.sleep(5)
  bot.edit_message_text(chat_id=room_id, message_id=sent.message_id, text="Discussion Phase Over!\n\n\U0001f373\U0001f373\U0001f373\U0001f373")
  time.sleep(3)
  bot.delete_message(chat_id=room_id, message_id= sent.message_id)

@bot.message_handler(commands=['join'])
def join_game(message):
  if auth(message):
        return
  cid = message.chat.id
  uid = str(message.from_user.username)
  markup = types.InlineKeyboardMarkup()
  markup.row(types.InlineKeyboardButton(text='Join game', callback_data=" "))
  bot.send_message(cid, "Do you wish to join the game?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_join_game(call):
  global joined_msg_id, joined_msg
  uid = call.from_user.id
  uname = call.from_user.username
  if add_to_game(uname,uid):
      msg = "@" + uname + " Joined the game"
      joined_msg = joined_msg + uname + " Joined the game\n"
      who_da_boss = str(Users[int(host_id)]["user_name"]) + " is the Host \U0001f48e\U0001f932\n\n \U0001f525 Lobby List:\n"
      msg = who_da_boss + joined_msg
      if joined_msg_id == "":
        send_joined = bot.send_message(chat_id = room_id, text= msg)
        joined_msg_id = send_joined.message_id
      else:
        bot.edit_message_text(chat_id = room_id, message_id = joined_msg_id, text=msg)
  
  
def test():
    voting_phase()


def main():
    while True:
        try:
            bot.polling(none_stop=False, interval=0, timeout=20)
        except:
            pass

    
if __name__ == '__main__':
    # test()
    print("game running")
    main()
