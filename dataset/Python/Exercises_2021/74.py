def RemoveMinDigit(num):
    num1 = num
    Nlist = [int(x) for x in str(num1)] #Creating list
    min = 9;
    while (num != 0): #Finding a minimum
        digit = num % 10
        num = int(num / 10)
        if digit < min:
            min = digit

    a = [x for x in Nlist if x != min] #Leave only what is not a minimum
    res = int("".join(map(str, a))) #Back from list
    return res
