def IsPangrams(str):
    '''
    The function receives a string and checks if it is a pangram

    :param str: String parameter
    :return:Returns true if the string is a pangram else return false
    '''
    alphabet = "AbcdefghiJklmnopqrstuvwXyz"
    for char in alphabet:
        if char not in str.lower() and char not in str.upper():
            return False

    return True
