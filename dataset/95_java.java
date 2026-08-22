import java.util.HashSet;
import java.util.Set;

public class Main {
    public static void factorSum(double x) {
        /**
         * sum all the divide prime numbers
         *
         * :param x:the number from the user
         * :return:the sum
         */
        if (x <= 1) {
            System.out.println("error");
            return;
        }
        double d = 2;
        Set<Double> gruop = new HashSet<>();
        while (d < x) {
            if ((long) x % (long) d == 0) {
                gruop.add(d);
                x = x / d;
            }
            else {
                d += 1;
            }
        }
        if (d == x) {
            gruop.add(d);
        }

        double sum = 0;
        for (double val : gruop) {
            sum += val;
        }
        System.out.println(sum);
    }
}