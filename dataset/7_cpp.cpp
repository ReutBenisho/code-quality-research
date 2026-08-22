#include <stdexcept>
#include <string>

class CustomException : public std::exception {
private:
    std::string customValue;

public:
    CustomException(std::string customValue) : customValue(customValue) {}

    std::string getCustomValue() const {
        return customValue;
    }
};