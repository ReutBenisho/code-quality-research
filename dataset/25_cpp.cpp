#include <iostream>
#include <string>
#include <vector>
#include <limits>
#include <cstdint>

class TestClass {
public:
    void func(HttpServletRequest& request, HttpServletResponse& response) {
        int data;

        data = std::numeric_limits<int>::min();

        {
            std::vector<Cookie>* cookieSources = request.getCookies();
            if (cookieSources != nullptr) {
                std::string stringNumber = (*cookieSources)[0].getValue();
                try {
                    data = std::stoi(stringNumber);
                } catch (const std::invalid_argument& exceptNumberFormat) {
                    IO::logger.log(Level::WARNING, "Number format exception reading data from cookie", exceptNumberFormat);
                } catch (const std::out_of_range& exceptNumberFormat) {
                    IO::logger.log(Level::WARNING, "Number format exception reading data from cookie", exceptNumberFormat);
                }
            }
        }

        int array[] = { 0, 1, 2, 3, 4 };
        int arrayLength = sizeof(array) / sizeof(array[0]);

        if (data < arrayLength) {
            IO::writeLine(array[data]);
        } else {
            IO::writeLine("Array index out of bounds");
        }
    }
};