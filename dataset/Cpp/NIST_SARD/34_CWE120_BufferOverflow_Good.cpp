
#include <iostream>
#include <iomanip>

#define MAXSIZE 40

void process_input_safe() {
    char buffer[MAXSIZE];
    std::cin >> std::setw(MAXSIZE) >> buffer; 
    std::cout << "Data received safely: " << buffer << std::endl;
}

int main() {
    process_input_safe();
    return 0;
}
