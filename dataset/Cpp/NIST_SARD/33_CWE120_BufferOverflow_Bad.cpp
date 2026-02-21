
#include <iostream>
#include <string>

#define MAXSIZE 40

void process_input() {
    char buffer[MAXSIZE];
    // פגיעות: קריאת קלט ללא הגבלת אורך לתוך חוצץ קבוע
    std::cin >> buffer; 
    std::cout << "Data received: " << buffer << std::endl;
}

int main() {
    process_input();
    return 0;
}