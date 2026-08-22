/**
 * The function receives an integer and checks whether
 * the digits in the number form an arithmetic series
 *
 * :param number:Positive number
 * :return:Returns true if the series is an invoice series
 */
bool CheckArithmeticSeries(int number) {
    int counter = number % 10 - (number / 10) % 10;
    while (number > 100) {
        int newcounter = (number / 10) % 10 - (number / 100) % 10;
        if (newcounter != counter) {
            return false;
        }
        else {
            number = number / 10;
        }
    }
    return true;
}