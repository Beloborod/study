import random
from DEcoding.hemming.math_funcs import *

if __name__ == '__main__':

    message = "\nType string for coding (for example your initials), but only one type of symbols " \
              "(for example numbers, letters of one alphabet): "

    input_string = str(input(message))  # get message-string

    symbols_codes_list = []

    add = None
    while add != "" and add != "Y" and add != "N":  # add random error in message or no
        add = str(input("\nAdd a random error in message? ('y'/'n' or 'enter' for 'n'): "))
        if add == "":
            add = "N"
        add = add.upper()
        print(add)

    for symbol in input_string:  # get symbol's code, transformation into binary and delete "0b" prefix
        symbols_codes_list.append(bin(ord(symbol))[2:])

    symbols_length = len(symbols_codes_list[0])

    bin_str = ""
    for code in symbols_codes_list:
        bin_str += code

    print(f"\nMessage in binary code: {int(bin_str)}\n")

    bin_list = list(bin_str)    # transform binary message into list and set type of values in list as "int"
    bin_list = list(map(int, bin_list))
    ret = hamming_coding(bin_list)  # get coded message

    if add == "Y":  # add random error
        random_error = random.randint(0, len(ret)-1)

        print(f"Error in bite with number: {random_error+1}\n")

        if ret[random_error] == 1:
            ret[random_error] = 0
        else:
            ret[random_error] = 1

        print("After adding error:")
        print_list(ret)
        print("\n")

    decoded = hamming_decoding(ret)  # get decoded message with fixed error, if it's exist
    decoded_str = ""
    bite_str = ""

    print("Message after decoding and fix error:")
    print_list(decoded)
    print("\n")

    for bite in decoded:
        bite_str += str(bite)
        if len(bite_str) == symbols_length:
            decoded_str += chr(int(bite_str, 2))
            bite_str = ""

    print("Decoded message:")
    print(decoded_str)
    input()
