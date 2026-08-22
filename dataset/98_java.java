import java.util.HashSet;
import java.util.Set;

public class Main {
    /**
     * The function returns the sum of all factorial numbers of num
     * :param num: integer number
     * :return: Sum of all factorial numbers of num
     */
    public static double factorsum(double num) {
        Set<Integer> factorial_divisors = new HashSet<>();
        for (int i = 2; i < num; i++) {
            if ((long) num % i == 0) {
                factorial_divisors.add(i);
            }
            while ((long) num % i == 0) {
                num = num / i;
            }
        }
        
        double sum = 0;
        for (int val : factorial_divisors) {
            sum += val;
        }
        return sum;
    }
}