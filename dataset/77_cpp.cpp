#include <iostream>
#include <string>

void CalcUpperCalcLower(std::string string) {
    int counter[2] = {0, 0};
    for (size_t x = 0; x < string.length(); x++) {
        if (string[x] >= 'a' <= 'z') {
            counter[0] = counter[0] + 1;
        }
        else if (string[x] >= 'A' <= 'Z') {
            counter[1] = counter[1] + 1;
        }
    }
    std::cout << "Number of Upper cases:" + std::to_string(counter[1]) << std::endl;
    std::cout << "Number of Lower cases:" + std::to_string(counter[0]) << std::endl;
}