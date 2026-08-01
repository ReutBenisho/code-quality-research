
#include <iostream>

namespace Test {
    void process() {
        long * data;
        long * &dataRef = data;
        
        data = nullptr;
        
        {
            long * localData = dataRef;
            if (localData != nullptr) {
                std::cout << *localData << std::endl;
            } else {
                std::cout << "Data is null" << std::endl;
            }
        }
    }
}

int main() {
    Test::process();
    return 0;
}
