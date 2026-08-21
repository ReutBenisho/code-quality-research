#include <iostream>

class Test {
public:
    static const int c = 0;

    static void booleanExpressionMethod() {
        if (c != 0) {
            std::cout << "Text" << std::endl;
        }
    }
};