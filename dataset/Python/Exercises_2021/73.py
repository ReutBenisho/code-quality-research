def RemoveMinDigit(num):
    """
    Decription
    Take number and remove all the appearance of the minimum digit in the number.
    :param num: positive decimal number.
    :return: the num after we removed all the appearance of the minimum digit in the number.
    """
    if num <= 0:
        print("Error, number must be positive")
        return num

    num = str(num)
    minimum = num[0]
    for i in range(1, len(num)):
        minimum = min(num[i], minimum)
    num = num.replace(minimum, '')
    num = int(num)
    return num
