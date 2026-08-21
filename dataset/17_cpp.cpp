#include <iostream>

class Test {
private:
    int b = 10;

public:
    void b() {
        std::cout << "Method b called. Field b value: " << this->b << std::endl;
    }
};