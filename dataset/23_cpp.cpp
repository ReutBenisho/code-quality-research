#include <iostream>
#include <random>
#include <limits>
#include <cstdint>

class TestClass {
public:
    void func() {
        int16_t data;
        if (IO::STATIC_FINAL_TRUE) {
            std::random_device rd;
            std::mt19937 gen(rd());
            std::uniform_int_distribution<int> dist(std::numeric_limits<int16_t>::min(), std::numeric_limits<int16_t>::max());
            data = static_cast<int16_t>(dist(gen));
        } else {
            data = 0;
        }

        if (IO::STATIC_FINAL_TRUE) {
            int16_t result = static_cast<int16_t>(++data);
            IO::writeLine("result: " + std::to_string(result));
        }
    }
};