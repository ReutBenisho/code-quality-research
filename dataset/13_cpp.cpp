#include <iostream>
#include <vector>
#include <functional>

class Test {
public:
    std::function<void()> someAction = []() {
        std::vector<std::string> foo;
        foo.reserve(5);
        for (const auto& item : foo) {
            std::cerr << item;
        }
    };
};