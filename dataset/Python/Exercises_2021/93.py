
def RemoveMinDigit (x):

    """ 
        The function gets a number and drops all occurrences of the minimum digit
  
        Parameters: Integer positive number
             
        Returns: 
            Integer positive number: Without the minimum digit
    """
    
    for n in range (str(x).count(min(str(x)))):
         new_number = str(x).replace(min(str(x)), "")
    return int (new_number)
