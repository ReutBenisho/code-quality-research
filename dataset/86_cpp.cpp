#include <string>
#include <algorithm>

/**
 * The function receives two strings and checks whether one is an anagram of the other
 * I.e. do they have exactly the same letters but in a different order.
 *
 * :param string1:Sring
 * :param string2:string
 * :return:The function will return truth if it is an anagram.
 */
bool is_anagram(std::string string1, std::string string2) {
    std::string a = string1;
    std::transform(a.begin(), a.end(), a.begin(), ::toupper);

    std::string b = string2;
    std::transform(b.begin(), b.end(), b.begin(), ::toupper);

    if (a.length() != b.length()) {
        return false;
    }

    std::string sorted_a = a;
    std::string sorted_b = b;
    std::sort(sorted_a.begin(), sorted_a.end());
    std::sort(sorted_b.begin(), sorted_b.end());

    if (sorted_a == sorted_b) {
        return true;
    }
    else {
        return false;
    }
}