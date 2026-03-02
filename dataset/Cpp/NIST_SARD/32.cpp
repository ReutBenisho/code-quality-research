
#include <iostream>

namespace CWE476_33_Fixed {
    void process() {
        long * data;
        long * &dataRef = data;
        
        data = nullptr;
        
        {
            long * localData = dataRef;
            // התיקון: בדיקה לפני שימוש
            if (localData != nullptr) {
                std::cout << *localData << std::endl;
            } else {
                std::cout << "Data is null" << std::endl;
            }
        }
    }
}

int main() {
    CWE476_33_Fixed::process();
    return 0;
}