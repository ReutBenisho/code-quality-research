#include <string>
#include <algorithm>

bool isPalindrome(int x) {
    /**
     * :param x: int, non-negative
     * :return: bool, true if x is Palindrome, false otherwise
     */
    std::string s = std::to_string(x);
    std::string rev = s;
    std::reverse(rev.begin(), rev.end());
    return s == rev;
}