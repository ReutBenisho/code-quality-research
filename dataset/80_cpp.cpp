/**
 * The function receives an integer and checks if a number is perfect
 * :param number:Integer
 * :return:Returns True if the number Perfect otherwise False
 */
bool PerfectNumber(int number) {
    int sum = 0;
    for (int i = 1; i < number; i++) {
        if ((number % i) == 0) {
            sum = sum + i;
        }
    }
    if (sum == number) {
        return true;
    }
    else {
        return false;
    }
}