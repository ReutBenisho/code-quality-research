
def IsPangrams (x):

    """ 
       Checks if a string is a pangram
       Parameters: String
       Returns: Boolean parameter: Returns true if it is an pangram and false number or not
            
    """
    
    x.lower()
    l = 'a'
    for i in range (26):
        if (l in x):
            l = chr(ord(l) + 1) 
        else:
            return False

    return True