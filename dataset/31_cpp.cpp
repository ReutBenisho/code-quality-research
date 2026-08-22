
#include <iostream>

namespace Test {
    void process() {
        long * data;
        long * &dataRef = data;
        
        data = nullptr;
        
        {
            long * localData = dataRef;
            std::cout << *localData << std::endl; 
        }
    }
}

int main() {
    Test::process();
    return 0;
}
