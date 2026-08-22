#include <string>
#include <algorithm>

bool is_anagram(std::string s1, std::string s2) {
    /**
     * :param s1: string
     * :param s2: string
     * :return: true if s1 is anagram of s2, false otherwise
     */
    // delete all spaces
    s1.erase(std::remove(s1.begin(), s1.end(), ' '), s1.end());
    s2.erase(std::remove(s2.begin(), s2.end(), ' '), s2.end());

    // turn all letters lower
    std::transform(s1.begin(), s1.end(), s1.begin(), ::tolower);
    std::transform(s2.begin(), s2.end(), s2.begin(), ::tolower);

    // sort the string
    std::sort(s1.begin(), s1.end());
    std::sort(s2.begin(), s2.end());

    // the condition
    return s1 == s2;
}