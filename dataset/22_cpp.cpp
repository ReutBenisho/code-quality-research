#include <iostream>
#include <string>

class Test {
public:
    void hasArguments(const std::string* name) {
        int length = name->length();
        std::cout << "Length: " + std::to_string(length) << std::endl;
    }

    static void main() {
        const std::string* name = nullptr;
        Test mnp;
        mnp.hasArguments(name);
    }
};