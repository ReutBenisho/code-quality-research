def IsPangrams(s):
    """
    check if a string IsPangrams:
    :param s: string
    :return: bool, True if al abc.. exist in it, False otherwise
    """
    seen = set()
    for i in s:
        if i.isalpha() and i.upper not in seen:
            seen.add(i.upper())  # add up each alpha char ass upper
    return len(seen) == 26  # check condition
