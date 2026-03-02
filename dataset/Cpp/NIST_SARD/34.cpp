
#include <iostream>
#include <iomanip> // עבור setw

#define MAXSIZE 40

void process_input_safe() {
    char buffer[MAXSIZE];
    // תיקון: הגבלת אורך הקלט לגודל החוצץ (מינוס 1 עבור ה-null terminator)
    std::cin >> std::setw(MAXSIZE) >> buffer; 
    std::cout << "Data received safely: " << buffer << std::endl;
}

int main() {
    process_input_safe();
    return 0;
}