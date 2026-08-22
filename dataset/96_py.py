def prime(num):
    """
  A function that checks whether a prime number

    :param num: the number we want chack if he prime or not
    :return:if its prime number we return true else false
    """
    for i in range(2,num):
        if(num % i == 0):
            return False

    return True

def factorSum(number):
    """
    The function takes a number and makes the sum of the prim numbers whose product is equal to the parameter

    :param number:the number we want get the sum of prime number
    :return:we return the sum of the prime number
    """
    sum = 0
    for i in range(2,number):
        if(number%i==0):
            if(prime(i)):
                sum+=i
    return sum