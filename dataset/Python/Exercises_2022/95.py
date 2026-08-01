def factorSum(x):
    """
    sum all the divide prime numbers

    :param x:the number from the user
    :return:the sum
    """
    if x <= 1:
        print("error")
        return 0
    d = 2
    gruop = set()
    while d < x:
        if x % d == 0:
            gruop.add(d)
            x = x / d
        else:
            d += 1
    if d == x:
        gruop.add(d)
    print(sum(gruop))

