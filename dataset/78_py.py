def CalcUpperCalcLower(s):
    """
    printing number of upper and lower letters in the string that been given:
    :param s: string
    :return: none
    """
    upper_count, lower_count = 0, 0  # counters of upper and lower letters
    for i in s:
        if i.isupper():  # if the char is upper increase upper_count
            upper_count += 1
        elif i.islower():  # if the char is lower increase lower_count
            lower_count += 1
    print("Number of Upper cases: {0} \nNumber of Lower cases: {1}".format(upper_count, lower_count))
