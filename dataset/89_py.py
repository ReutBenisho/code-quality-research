
def is_anagram(s1, s2):
    """
    :param s1: string
    :param s2: string
    :return: true if s1 is anagram of s2, false otherwise
    """
    s1, s2 = s1.replace(" ", ""), s2.replace(" ", "")  # delete al spaces
    s1, s2 = s1.lower(), s2.lower()  # turn all letters lower
    s1, s2 = "".join(sorted(s1)), "".join(sorted(s2))  # sort the string
    return s1 == s2  # the condition
    
