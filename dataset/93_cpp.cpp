#include <string>
#include <algorithm>

int RemoveMinDigit(int x) {
    /** 
     * The function gets a number and drops all occurrences of the minimum digit
     *  
     * Parameters: Integer positive number
     *             
     * Returns: 
     *     Integer positive number: Without the minimum digit
     */
    std::string s = std::to_string(x);
    char min_char = *std::min_element(s.begin(), s.end());

    std::string new_number = "";
    for (int n = 0; n < std::count(s.begin(), s.end(), min_char); n++) {
        std::string temp = s;
        temp.erase(std::remove(temp.begin(), temp.end(), min_char), temp.end());
        new_number = temp;
    }
    return std::stoi(new_number);
}