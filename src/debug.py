def dbg_print_ditc(name, dict):
    print(name + "{")
    for key in dict:
        print(key + ": " + dict[key] + ',')
    print('}')