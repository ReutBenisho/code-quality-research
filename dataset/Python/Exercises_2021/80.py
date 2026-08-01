def PerfectNumber(number):
    '''
    The function receives an integer and checks if a number is perfect
    :param number:Integer
    :return:Returns True if the number Perfect otherwise False
    '''
    sum = 0
    for i in range(1, number):
        if(number % i) == 0:
            sum = sum + i
    if sum == number:
        return True
    else:
        return False