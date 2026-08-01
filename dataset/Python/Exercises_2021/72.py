def RemoveMinDigit(num):
    """
    remove all min digit from the number:
    :param num: int, positive integer
    :return:int, the number without the smallest digit
    """
    if num <= 0:
        print("number is negative!")
        return num
    num = [int(i) for i in str(num)]  # turn the number into list of digits
    num = [i for i in num if i != min(num)]  # arrange the list with out the min digit
    if not len(num):  # in case the number is made by 1 digit only: x, xxx, xxx ...
        return 0
    return int("".join(str(i) for i in num))  # join all digits left into int
