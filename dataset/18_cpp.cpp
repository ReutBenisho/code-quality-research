#include <iostream>

class Test {
private:
    int a = 5;

    void bar(int val) {}

public:
    void check(int j) {
        if (false || false) {
            std::cout << "Text" << std::endl;
        }
        this->bar(this->a);
        
        ++j;
    }
};