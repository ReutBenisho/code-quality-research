#include <string>
#include <algorithm>

bool is_anagram(std::string s1, std::string s2) { //A function that gets two strings and checks if one is An anagram of the second
    std::transform(s1.begin(), s1.end(), s1.begin(), ::toupper); //Convert all letters to uppercase
    std::transform(s2.begin(), s2.end(), s2.begin(), ::toupper);

    std::sort(s1.begin(), s1.end()); //sort
    std::sort(s2.begin(), s2.end()); //sort

    return s1 == s2; //Check if the strings are equal
}