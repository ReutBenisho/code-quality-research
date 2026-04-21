#include <iostream>
#include <cmath>
#include <limits>

class Test {
public:
    void func(float data) const {
        if (std::abs(data) < 1e-9f) { 
            std::cerr << "Error: Division by zero" << std::endl;
            return;
        }

        double raw_result = 100.0 / data;

        if (raw_result > std::numeric_limits<int>::max() || 
            raw_result < std::numeric_limits<int>::min()) {
            std::cerr << "Error: Result exceeds integer range" << std::endl;
            return;
        }

        int result = static_cast<int>(raw_result);
        std::cout << "result: " << result << std::endl;
    }
};