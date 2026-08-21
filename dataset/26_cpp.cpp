#include <iostream>
#include <random>

class TestClass {
public:
    void func() {
        switch (7) {
        case 7: {
            int x;
            std::random_device rd;
            std::mt19937 gen(rd());
            std::uniform_int_distribution<int> dist;
            x = dist(gen);
            if (x == 0) {
                IO::writeLine("Inside the if statement");
            } else {
            }
            IO::writeLine("Hello from func()");
            break;
        }
        default:
            IO::writeLine("Benign, fixed string");
            break;
        }
    }
};