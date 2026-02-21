
#include <iostream>

namespace CWE476_33 {
    void process() {
        long * data;
        long * &dataRef = data;
        
        data = nullptr; // המקור לבעיה
        
        {
            long * localData = dataRef;
            // כאן ה-AI אמור לזהות dereference של null
            std::cout << *localData << std::endl; 
        }
    }
}

int main() {
    CWE476_33::process();
    return 0;
}