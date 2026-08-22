#include <iostream>
#include <limits>

class TestClass {
private:
    static const int PRIVATE_STATIC_FINAL_FIVE = 5;

public:
    static void func() {
        int data;

        if (PRIVATE_STATIC_FINAL_FIVE == 5) {
            data = std::numeric_limits<short>::max();
        } else {
            data = 0;
        }

        if (PRIVATE_STATIC_FINAL_FIVE == 5) {
            int result = ++data;
            std::cout << "result: " << result << std::endl;
        }
    }

    static void main(int argc, char* argv[]) {
        func();
    }
};