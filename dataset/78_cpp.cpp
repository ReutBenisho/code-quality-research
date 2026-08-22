#include <iostream>
#include <string>
#include <cctype>

void CalcUpperCalcLower(std::string s) {
    /**
     * printing number of upper and lower letters in the string that been given:
     * :param s: string
     * :return: none
     */
    int upper_count = 0, lower_count = 0; // counters of upper and lower letters
    for (char i : s) {
        if (isupper(i)) { // if the char is upper increase upper_count
            upper_count += 1;
        }
        else if (islower(i)) { // if the char is lower increase lower_count
            lower_count += 1;
        }
    }
    std::cout << "Number of Upper cases: " << upper_count << " \nNumber of Lower cases: " << lower_count << std::endl;
}