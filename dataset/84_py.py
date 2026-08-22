def is_anagram(s1, s2):
    # the sorted strings are checked
    str1 = s1.lower()
    str2 = s2.lower()
    if (sorted(str1) == sorted(str2)):
        return True
    else:
        return False
