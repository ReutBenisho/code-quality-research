#include <string>
#include <algorithm>

bool is_anagram(std::string s1, std::string s2) {
    // the sorted strings are checked
    std::string str1 = s1;
    std::transform(str1.begin(), str1.end(), str1.begin(), ::tolower);
    
    std::string str2 = s2;
    std::transform(str2.begin(), str2.end(), str2.begin(), ::tolower);
    
    std::sort(str1.begin(), str1.end());
    std::sort(str2.begin(), str2.end());
    
    if (str1 == str2) {
        return true;
    }
    else {
        return false;
    }
}