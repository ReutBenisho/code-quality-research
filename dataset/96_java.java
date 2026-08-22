public class Main {
    /**
     * A function that checks whether a prime number
     *
     * :param num: the number we want chack if he prime or not
     * :return:if its prime number we return true else false
     */
    public static boolean prime(int num) {
        for (int i = 2; i < num; i++) {
            if (num % i == 0) {
                return false;
            }
        }
        return true;
    }

    /**
     * The function takes a number and makes the sum of the prim numbers whose product is equal to the parameter
     *
     * :param number:the number we want get the sum of prime number
     * :return:we return the sum of the prime number
     */
    public static int factorSum(int number) {
        int sum = 0;
        for (int i = 2; i < number; i++) {
            if (number % i == 0) {
                if (prime(i)) {
                    sum += i;
                }
            }
        }
        return sum;
    }
}