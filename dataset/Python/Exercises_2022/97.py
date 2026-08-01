def factorSum(num):
    """
  the funcation get number and return the sum of the the prime numbers
    """
    temp = num
    if temp % 2 == 0:
        sum = 2
        while temp % 2 == 0:
            temp = temp / 2
    else:
        sum = 0

    if temp % 3 == 0:
        sum = sum + 3
        while temp % 3 == 0:
            temp = temp / 3
    else:
        pass

    if temp != 1:
        for i in range(5, num + 1):
            if i % 2 != 0 and i % 3 != 0:
                if temp % i == 0:
                    sum = sum + i
                    while temp % i == 0:
                        temp = temp / i
                        if temp == 1:
                            return sum
    else:
        return sum

