#include <vector>

bool PerfectNumber(int number) {
    /**
     * Find if the number is perfect
     * :param number:integer
     * :return: bool value
     */
    std::vector<int> list;
    int sum = 0;
    for (int i = 1; i < number; i++) {
        if (number % i == 0) {
            list.push_back(i);
        }
    }
    for (int l : list) {
        sum = sum + l;
    }
    if (sum == number) {
        return true;
    }
    else {
        return false;
    }
}