def dbg_print_dict(name, dict):
    print(name + "{")
    for key in dict:
        print(key + ": " + dict[key] + ',')
    print('}')