
def isPolindrome(x): #A function that checks if the polynomial number
    reverse = 0
    temp=x
    while (x != 0): # reversing the given number
        xtemp = x % 10
        reverse = reverse * 10 + xtemp
        x = int(x / 10)
    if (temp == reverse):
        return True
    else:
        return False
