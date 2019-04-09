import random
from DEcoding.hemming.math_funcs import *

if __name__ == '__main__':
    message = "\nType string for coding (for example your initials), but only one type of symbols " \
              "(for example numbers, letters of one alphabet): "
    input_string = str(input(message))
    symbols_codes_list = []

    add = None
    while add != "" and add != "Y" and add != "N":
        add = str(input("\nAdd a random error in message? ('y'/'n' or 'enter' for 'n')"))
        if add == "":
            add = "N"
        add = add.upper()
        print(add)

    for symbol in input_string:
        symbols_codes_list.append(bin(ord(symbol))[2:])

    symbols_length = len(symbols_codes_list[0])
    bin_str = ""

    for code in symbols_codes_list:
        bin_str += code

    print(f"\nMessage in binary code: {int(bin_str)}\n")

    bin_list = list(bin_str)
    bin_list = list(map(int, bin_list))
    ret, powers = hamming_coding(bin_list)

    if add == "Y":
        random_error = random.randint(0, len(ret)-1)

        print(f"Error in byte with number: {random_error+1}\n")

        if ret[random_error] == 1:
            ret[random_error] = 0
        else:
            ret[random_error] = 1

        print("After adding error:")
        print_list(ret)
        print("\n")

    decoded = hamming_decoding(ret, powers)
    decoded_str = ""
    byte_str = ""

    print("Message after decoding and fix error:")
    print_list(decoded)
    print("\n")

    for byte in decoded:
        byte_str += str(byte)
        if len(byte_str) == symbols_length:
            decoded_str += chr(int(byte_str, 2))
            byte_str = ""

    print("Decoded message:")
    print(decoded_str)
