#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

int RemoveMinDigit(int num) {
    /**
     * remove all min digit from the number:
     * :param num: int, positive integer
     * :return:int, the number without the smallest digit
     */
    if (num <= 0) {
        std::cout << "number is negative!" << std::endl;
        return num;
    }
    
    std::string num_str = std::to_string(num);
    std::vector<int> num_list;
    for (char i : num_str) {
        num_list.push_back(i - '0'); // turn the number into list of digits
    }
    
    int min_val = *std::min_element(num_list.begin(), num_list.end());
    std::vector<int> filtered_num;
    for (int i : num_list) {
        if (i != min_val) {
            filtered_num.push_back(i);
        }
    }
    num_list = filtered_num; // arrange the list with out the min digit
    
    if (!num_list.size()) { // in case the number is made by 1 digit only: x, xxx, xxx ...
        return 0;
    }
    
    std::string joined = "";
    for (int i : num_list) {
        joined += std::to_string(i);
    }
    return std::stoi(joined); // join all digits left into int
}