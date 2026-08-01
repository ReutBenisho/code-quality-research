
def is_anagram(string1, string2):
    '''
    The function receives two strings and checks whether one is an anagram of the other
    I.e. do they have exactly the same letters but in a different order.

    :param string1:Sring
    :param string2:string
    :return:The function will return truth if it is an anagram.
    '''

    a = string1.upper()
    b = string2.upper()
    if len(a) != len(b):
        return False
    elif sorted(a) == sorted(b):
        return True
    else:
        return False

