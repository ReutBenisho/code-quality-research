
def PerfectNumber(number) :
    """
    Find if the number is perfect
    :param number:integer
    :return: bool value
    """
    list = []
    sum = 0
    for i in range(1, number):
        if number % i == 0:
            list.append(i)
    for l in list:
        sum = sum + l
    if (sum == number):
        return True
    else:
        return False
