def isPalindrome(num):
    '''Returns true if num is palindrome'''
    temp = num
    rev = 0
    while (num > 0):
        dig = num % 10
        rev = rev * 10 + dig
        num = num // 10
    if (temp == rev):
        return Truebool isPalindrome(int num) {
    /**
     * Returns true if num is palindrome
     */
    int temp = num;
    int rev = 0;
    while (num > 0) {
        int dig = num % 10;
        rev = rev * 10 + dig;
        num = num / 10;
    }
    if (temp == rev) {
        return true;
    }
    else {
        return false;
    }
}