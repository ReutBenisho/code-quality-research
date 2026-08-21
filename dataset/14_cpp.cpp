#include <string>

class Test {
public:
    bool compareStrings() {
        std::string s1 = "str1";
        const std::string s2 = "str2";
        return &s1 == &s2;
    }
};