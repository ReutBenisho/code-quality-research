#include <unordered_set>
#include <numeric>

/**
 * The function returns the sum of all factorial numbers of num
 * :param num: integer number
 * :return: Sum of all factorial numbers of num
 */
double factorsum(double num) {
    std::unordered_set<int> factorial_divisors;
    for (int i = 2; i < num; i++) {
        if (static_cast<long long>(num) % i == 0) {
            factorial_divisors.insert(i);
        }
        while (static_cast<long long>(num) % i == 0) {
            num = num / i;
        }
    }
    return std::accumulate(factorial_divisors.begin(), factorial_divisors.end(), 0.0);
}