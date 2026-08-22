#include <iostream>
#include <string>
#include <algorithm>

int RemoveMinDigit(int num) {
    /**
     * Decription
     * Take number and remove all the appearance of the minimum digit in the number.
     * :param num: positive decimal number.
     * :return: the num after we removed all the appearance of the minimum digit in the number.
     */
    if (num <= 0) {
        std::cout << "Error, number must be positive" << std::endl;
        return num;
    }

    std::string num_str = std::to_string(num);
    char minimum = num_str[0];
    for (size_t i = 1; i < num_str.length(); i++) {
        minimum = std::min(num_str[i], minimum);
    }
    
    std::string result = "";
    for (char c : num_str) {
        if (c != minimum) {
            result += c;
        }
    }
    
    int num_res = std::stoi(result);
    return num_res;
}