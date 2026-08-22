def factorsum(num):
    """

    The function returns the sum of all factorial numbers of num
    :param num: integer number
    :return: Sum of all factorial numbers of num

    """
    factorial_divisors = set()
    for i in range(2, num):
        if num % i == 0:
            factorial_divisors.add(i)
        while num % i == 0:
            num = num / i
    return sum(factorial_divisors)

