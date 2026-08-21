#include <iostream>
#include <string>
#include <cstdlib>

class TestClass {
public:
    void bad() {
        std::string* data;
        if (IO::STATIC_FINAL_FIVE == 5) {
            const char* env = std::getenv("ADD");
            static std::string envStr = env ? env : "";
            data = env ? &envStr : nullptr;
        } else {
            data = nullptr;
        }

        Class* tempClass = Class::forName(*data);
        Object* tempClassObject = tempClass->newInstance();

        IO::writeLine(tempClassObject->toString());
    }
};