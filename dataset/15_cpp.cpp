#include <iostream>

class NestedMutation {
public:
    void outerMethod() {
        class NestedClass {
        public:
            void foo() {
                std::cout << "Inner logic execution." << std::endl;
            }
        };
        NestedClass().foo();
    }
};