#include <string>
#include <algorithm>

/**
 * The function receives a string and checks if it is a pangram
 *
 * :param str: String parameter
 * :return:Returns true if the string is a pangram else return false
 */
bool IsPangrams(std::string str) {
    std::string alphabet = "AbcdefghiJklmnopqrstuvwXyz";

    std::string str_lower = str;
    std::transform(str_lower.begin(), str_lower.end(), str_lower.begin(), ::tolower);

    std::string str_upper = str;
    std::transform(str_upper.begin(), str_upper.end(), str_upper.begin(), ::toupper);

    for (char c : alphabet) {
        if (str_lower.find(c) == std::string::npos && str_upper.find(c) == std::string::npos) {
            return false;
        }
    }

    return true;
}