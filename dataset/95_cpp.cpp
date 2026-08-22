#include <iostream>
#include <unordered_set>
#include <numeric>

void factorSum(double x) {
    /**
     * sum all the divide prime numbers
     *
     * :param x:the number from the user
     * :return:the sum
     */
    if (x <= 1) {
        std::cout << "error" << std::endl;
        return;
    }
    double d = 2;
    std::unordered_set<double> gruop;
    while (d < x) {
        if (static_cast<long long>(x) % static_cast<long long>(d) == 0) {
            gruop.insert(d);
            x = x / d;
        }
        else {
            d += 1;
        }
    }
    if (d == x) {
        gruop.insert(d);
    }
    
    double sum = std::accumulate(gruop.begin(), gruop.end(), 0.0);
    std::cout << sum << std::endl;
}