#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <numeric>

int RemoveMinDigit(int n) {
    std::string s_n = std::to_string(n);
    std::vector<int> dig;
    for (char x : s_n) {
        dig.push_back(x - '0'); //make a list from the number
    }
    int min_dig = *std::min_element(dig.begin(), dig.end()); //find the min dig
    
    std::vector<int> new_vec;
    std::copy_if(dig.begin(), dig.end(), std::back_inserter(new_vec), [min_dig](int a) {
        return a != min_dig;
    }); //removing the min dig
    
    std::vector<std::string> s;
    for (int i : new_vec) {
        s.push_back(std::to_string(i));
    }
    
    std::string joined = "";
    for (const auto& str : s) {
        joined += str;
    }
    int res = std::stoi(joined);
    return res;
}