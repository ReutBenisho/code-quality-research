import java.util.ArrayList;
import java.util.List;

public class Main {
    public static boolean PerfectNumber(int number) {
        /**
         * Find if the number is perfect
         * :param number:integer
         * :return: bool value
         */
        List<Integer> list = new ArrayList<>();
        int sum = 0;
        for (int i = 1; i < number; i++) {
            if (number % i == 0) {
                list.add(i);
            }
        }
        for (int l : list) {
            sum = sum + l;
        }
        if (sum == number) {
            return true;
        }
        else {
            return false;
        }
    }
}