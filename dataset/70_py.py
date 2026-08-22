def RemoveMinDigit(n):
    dig = [int(x) for x in str(n)]#make a list from the number
    min_dig = min(dig)#find the min dig
    new=list(filter(lambda a: a != min_dig,dig))#removing the min dig
    s = [str(i) for i in new]
    res = int("".join(s))
    return res
