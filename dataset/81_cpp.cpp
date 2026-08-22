#include <iostream>
#include <string>
#include <unordered_set>
#include <cctype>

bool IsPangrams(std::string s) {
    /**
     * check if a string IsPangrams:
     * :param s: string
     * :return: bool, True if al abc.. exist in it, False otherwise
     */
    std::unordered_set<auto> seen;
    for (char i : s) {
        if (isalpha(i) && seen.find(i.upper) == seen.end()) {
            seen.insert(toupper(i)); // add up each alpha char ass upper
        }
    }
    return seen.size() == 26; // check condition
}