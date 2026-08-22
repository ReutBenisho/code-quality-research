def PerfectNumber(number):
    Sum = 0
    for i in range(1,number):
        if (number% i == 0):
            Sum = Sum + i
    return Sum == number