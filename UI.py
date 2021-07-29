narrative_para = {}
narrative_rules = '''WELCOME TO ELANGO'S NIGHTMARE\n\nRULES OF THE GAME ARE SIMPLE:\n\n1. There are hackers among your group and the end-goal is to identify and eliminate all hackers, or be eliminated.\u26A0\uFE0F\n\n2. Take your time in the lobby phase to familiarise yourself with the game and the respective roles (/list_role).\U0001f4cb\n\n3. Your role will be kept a secret from others. Do not share your roles with your friend or enemy.\U0001f645\u200D\u2642\uFE0F\n\n4. Night phase will come afterwards, where the most intense actions take place.\U0001f60f\n\n5. A disccusion board will take place for 90 seconds where every player will come together to discuss who are the hackers.\U0001f4ad\n\n6. Voting phase allows every player to vote for who they think are hackers. Be careful who you vote for and keep it a secret.\U0001f64a\n\n7. You will not be able to vote if you are dead. Stay dead.\u26B0\uFE0F\n\n8. The player that receives the most votes will be eliminated from the game.\U0001f44b\n\n9. Night phase repeats itself again until either all hackers are eliminated or everyone dies in the hands of the hackers.\U0001f608\n\n10. Stay alive and Goodluck!\U0001f369\n\nBefore we begin, please click and send any message to this link: https://t.me/AaronTestWerewolf_bot'''
role_list = '''/FBI_Role - The detective of the game\U0001f575\uFE0F\n\n/hacker_Role - Try to hack as many victims without getting caught\U0001f480\n\n/sage_Role - Your duty is not over! sage\U0001f489\n\n/shield_Role - Protect the innocent from the hackers!\U0001f6e1\uFE0F\n\n civilian_Role - Stay alive!\U0001f607\n'''
fbi_Role = "Role of the FBI:\nThe FBI is to find the hackers and convince the civilians to vote against them.\n\nAbility of the FBI:\n The FBI is able to check on a player's identity every round, and will not be disclosed to the other players he/she decides to state verbally. "
hacker_Role = "Role of the Hacker:\nThe hackers are to team up with his partner-in-crime and eliminate the rest of the players before they get eliminated.\n\nAbility of the hacker:\n The hacker is able to choose and hack a player and eliminate him out of the game provided the victim is not shielded"
sage_Role = "Role of the Sage:\nThe sage is to ensure the least casualty throughout the game until the hacker is eliminated.\n\nAbility of the Sage:\n The sage is able to revive any players that has been eliminated from the game (including hackers) provided they were not revived before"
shield_Role = "Role of the Shield:\nThe shield is able to protect any players that he trusts.\n\nAbility of the Shield:\nThe Shield is capable in putting up a shield on a selected play to prevent him from being hacked"
civilian_Role = "Role of the Civilian:\nThe civilian has to stay alive as long as possible. \n\nAbility of the Civilian:\n-No ability-\n\nTips:\nPlaying mind games helps you to survive and manipulate the situation to your advantage\U0001f609. Goodluck!"

# Assign UI
narrative_para["civilian_Role"] = civilian_Role
narrative_para["shield_Role"] = shield_Role 
narrative_para["sage_Role"] = sage_Role
narrative_para["hacker_Role"] = hacker_Role
narrative_para["FBI_Role"] = fbi_Role
narrative_para["list_role"] = role_list
narrative_para["rules"] = narrative_rules
# GIF
narrative_para["sage_Role_gif"] = "sage"
narrative_para["hacker_Role_gif"] = "reyna"
narrative_para["FBI_Role_gif"] = "fbiopenup"
narrative_para["shield_Role_gif"] = "shield"


def narrate():
  return narrative_para
