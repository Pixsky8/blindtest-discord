import discord

def dbg_print_dict(name, dict):
    print(name + "{")
    for key in dict:
        print(key + ": " + dict[key] + ',')
    print('}')

def dbg_print_answer_dict(dict):
    print("anwsers {")
    for message in dict:
        print(str(message.id) + ": " + dict[key].name + ',')
    print('}')

def dbg_print_points_dict(name, dict):
    print(name + " {")
    for user in dict:
        print(user.name + ": " + str(dict[key]) + ',')
    print('}')
