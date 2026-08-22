#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

bool CheckArithmeticSeries(int Number) {
    std::string s_Num = std::to_string(Number);
    std::vector<int> num;
    for (char x : s_Num) {
        num.push_back(x - '0'); // make a list from the number
    }
    int n = num.size();
    if (n == 1) {
        return true;
    }
    std::sort(num.begin(), num.end()); // Sort list
    int d = num[1] - num[0];
    for (int i = 2; i < n; i++) {
        if (num[i] - num[i - 1] != d) {
            return false;
        }
    }
    return true;
}