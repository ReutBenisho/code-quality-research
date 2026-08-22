
def XNor(num1,num2):
    if num1==False and num2==False: #Checking conditions
        return True
    elif num1==False and num2==True:
        return False
    elif num1==True and num2==False:
        return False
    elif num1==True and num2==True:
        return True
