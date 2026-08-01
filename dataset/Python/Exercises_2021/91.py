
def is_anagram(s1, s2): #A function that gets two strings and checks if one is An anagram of the second
    s1, s2 = list(s1.upper()), list(s2.upper()) #Convert all letters to uppercase
    s1.sort() #sort
    s2.sort() #sort
    return s1 == s2 #Check if the strings are equal
