public class Main {
    /**
     * The function gets a number and checks
     * what the smallest digit is within the number
     * :param number:positive number
     * :return:The function returns the smallest digit within the number.
     */
    public static int findmin(int number) {
        int minimum = (int)(number % 10);
        while (number > 0) {
           if (minimum > (number % 10)) {
               minimum = (number % 10);
           }
           number = number / 10;
        }

        return minimum;
    }

    /**
     * The function receives an integer positive number
     *  and returns the number obtained after downloading all
     *  instances of the minimum digit in the number
     * :param number:positive number
     * :return:Returns the number obtained after downloading all instances of the minimum digit in the number.
     */
    public static int RemoveMinDigit(int number) {
        int a = findmin(number);
        int i = 1;
        int n = 0;
        while (number > 0) {
            if (a != (number % 10)) {
                int digit = number % 10;
                n = n + digit * i;
                i = i * 10;
            }
            number = number / 10;
        }
        return n;
    }
}