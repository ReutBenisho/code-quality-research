#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

int RemoveMinDigit(int num) {
    int num1 = num;
    std::string s_num1 = std::to_string(num1);
    std::vector<int> Nlist;
    for (char x : s_num1) {
        Nlist.push_back(x - '0'); //Creating list
    }
    int min = 9;
    while (num != 0) { //Finding a minimum
        int digit = num % 10;
        num = (int)(num / 10);
        if (digit < min) {
            min = digit;
        }
    }

    std::vector<int> a;
    for (int x : Nlist) { //Leave only what is not a minimum
        if (x != min) {
            a.push_back(x);
        }
    }

    std::string joined = "";
    for (int i : a) {
        joined += std::to_string(i);
    }
    int res = std::stoi(joined); //Back from list
    return res;
}