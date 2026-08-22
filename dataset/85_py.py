
def Revers(number1):
    '''

    The function will get a number and return the revers number
    :param number: number
    :return: revers number
    :param number1:
    :return:
    '''
    ind = 1
    newnam = 0
    counter2 = counter(number1)
    while counter2 > 1:
        ind = ind * 10
        counter2 = counter2 - 1
    while number1 > 0:
        newnam = newnam + (number1 % 10) * ind
        number1 = number1 // 10
        ind = ind // 10

    return newnam


def isPalindrome(k):
    '''
    A function that accepts a number and returns true if it can be read
     from right to left and from left to right
    :param k: number
    :return: returns true if it can be read
     from right to left and from left to right
    '''
    if k == Revers(k):
        return True
    else:
        return False


