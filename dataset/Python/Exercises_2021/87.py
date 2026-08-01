
def isPalindrome(x):
    """
    :param x: int, non-negative
    :return: bool, true if x is Palindrome, false otherwise
    """
    return str(x) == str(x)[::-1]
