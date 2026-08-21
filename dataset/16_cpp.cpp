#include <iostream>
#include <functional>

class Test {
public:
    void runTask() {
        std::function<void()> r = []() {
            std::cout << "Running task via lambda" << std::endl;
        };
        r();
    }
};