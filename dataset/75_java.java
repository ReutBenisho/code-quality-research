import java.util.*;
import java.util.stream.*;

public class Main {
    public static boolean CheckArithmeticSeries(int Number) {
        List<Integer> num = String.valueOf(Number).chars()
                .mapToObj(x -> Character.getNumericValue((char) x))
                .collect(Collectors.toList()); // make a list from the number
        int n = num.size();
        if (n == 1) {
            return true;
        }
        Collections.sort(num); // Sort list
        int d = num.get(1) - num.get(0);
        for (int i = 2; i < n; i++) {
            if (num.get(i) - num.get(i - 1) != d) {
                return false;
            }
        }
        return true;
    }
}