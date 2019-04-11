def hamming_coding(bin_list: list):
    """
    :param bin_list: list of bites (binary number represented as list)
    :return: bin_list with control bites (coded)
    """

    powers = get_number_of_control_bites(len(bin_list))

    count_of_control_bites = len(powers)

    print(f"Numbers of control bites: {count_of_control_bites}\nIndexes of control bites: {powers}\n")

    for power in powers:
        bin_list.insert(power - 1, 0)   # power - 1: because indexing start at 0 =)
    r_matrix = create_additional_matrix(count_of_control_bites, len(bin_list))

    print("Message with additional matrix and '0' as code bites (R params):")
    print_list(bin_list)
    print_matrix(r_matrix)
    print("\n")

    r_values = create_r_values(bin_list, r_matrix)

    print(f"R params (first is low order): {r_values}\n")

    index = 0

    for power in powers:
        bin_list[power - 1] = r_values[index]
        index += 1

    print("Message with additional matrix and R-params values as code bites (R params):")
    print_list(bin_list)
    print_matrix(r_matrix)
    print("\n")

    return bin_list


def get_number_of_control_bites(len_message: int):
    """
    :param len_message: count of bites in message
    :return: numbers of controls bites
    """
    count_of_control_bites = 1

    while 2 ** count_of_control_bites < len_message:
        count_of_control_bites += 1

    powers = [power for power in pow_generator(2, count_of_control_bites)]
    print(powers)

    """For understand this strings you need to check "Hamming codes with additional parity (SECDED)" or 
    (in russian) "усеченный код Хемминга" """

    if powers[-1] > len_message and (powers[-1] - 1) != len_message:
        powers[-1] = len_message
    return powers


def get_numbers_of_control_bites_for_decoding(len_message: int):
    list_to_return = []
    for power in pow_generator(2):
        if ((sum(list_to_return) + power) < len_message) or (power <= (len_message - len(list_to_return))):
            list_to_return.append(power)
        elif (len_message - len(list_to_return)) > list_to_return[-1]:
            list_to_return.append((len_message - len(list_to_return))-1)
            return list_to_return
        else:
            return list_to_return


def create_additional_matrix(cols, rows):
    """
    :param cols: number of columns (length of binary code of message with control bites)
    :param rows: number of rows (count of control bites)
    :return: additional matrix (where in cols is binary number of col)
    """
    r_matrix = [[] for col in range(cols)]
    for index in range(rows):
        index = list(bin(index+1)[2:])  # index + 1: range result is [0;rows) and we need [1;rows]
        index.reverse()
        for number_of_control_bite in range(cols):
            try:
                r_matrix[number_of_control_bite].append(int(index[number_of_control_bite]))
            except IndexError:
                r_matrix[number_of_control_bite].append(0)
    return r_matrix


def create_r_values(bin_list: list, r_matrix: list):
    """
    :param bin_list: list of bites (binary number represented as list), with control bites
    :param r_matrix: additional matrix
    :return: list of R (for coding) or S (for decoding) params
    """
    r_list = []
    for row in range(len(r_matrix)):
        r = 0
        for col in range(len(bin_list)):
            r += int(r_matrix[row][col]) * int(bin_list[col])
        r_list.append(r % 2)
    return r_list


def hamming_decoding(bin_list: list):
    """
    :param bin_list: list of bites (binary number represented as list), with control bites and probably error in
                        one bite (one list's element)
    :return: decoded bin_list - list with bites of decoded message
    """

    powers = get_numbers_of_control_bites_for_decoding(len(bin_list))

    s_matrix = create_additional_matrix(len(powers), len(bin_list))

    print("Message before decoding with additional matrix and R-params values as code bites (R params):")
    print_list(bin_list)
    print_matrix(s_matrix)
    print("\n")

    s_values = create_r_values(bin_list, s_matrix)

    print(f"S params (first is low order): {s_values}\n")

    if sum(s_values) != 0:
        bin_str = ""
        s_values_reversed = s_values.copy()
        s_values_reversed.reverse()
        for bite in s_values_reversed:
            bin_str += str(bite)

        print(f"Error in bite with number: {int(bin_str, 2)}\n")

        int_to_change = int(bin_str, 2) - 1
        if bin_list[int_to_change] == 0:
            bin_list[int_to_change] = 1
        else:
            bin_list[int_to_change] = 0

        print("Message before decoding, but after fix a error with additional matrix and R-params:")
        print_list(bin_list)
        print_matrix(s_matrix)
        print("\n")

    powers.reverse()
    for power in powers:
        bin_list.pop(power-1)
    return bin_list


def pow_generator(number=2, max_pow=0, start_pow=0):
    """
    :param number: base of the power
    :param max_pow: max power index, it's max power in generator's output (and final).
                    If this value is 0 - generator will be unlimited.
    :param start_pow: start power index, it's power index of first number in generator's output
    :return: generator object
    """
    if max_pow == 0:
        control_pow = 0
    else:
        control_pow = start_pow
    while control_pow <= max_pow:
        value = number ** start_pow
        start_pow += 1
        if max_pow != 0:
            control_pow += 1
        yield int(value)


def print_list(vector: list):
    row_string = ""
    for col in vector:
        row_string += f" {col}"
    print(row_string)


def print_matrix(matrix: list):
    for row in matrix:
        row_string = ""
        for col in row:
            row_string += f" {col}"
        print(row_string)
    print("\n")
