#include <string>

/** 
 * Checks if a string is a pangram
 * Parameters: String
 * Returns: Boolean parameter: Returns true if it is an pangram and false number or not
 */
bool IsPangrams(std::string x) {
    x;
    char l = 'a';
    for (int i = 0; i < 26; i++) {
        if (x.find(l) != std::string::npos) {
            l = static_cast<char>(l + 1);
        }
        else {
            return false;
        }
    }

    return true;
}