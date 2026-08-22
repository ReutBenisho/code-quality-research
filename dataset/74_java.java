import java.util.*;
import java.util.stream.*;

public class Main {
    public static int RemoveMinDigit(int num) {
        int num1 = num;
        List<Integer> Nlist = String.valueOf(num1).chars()
                .mapToObj(x -> Character.getNumericValue((char) x))
                .collect(Collectors.toList()); //Creating list
        int min = 9;
        while (num != 0) { //Finding a minimum
            int digit = num % 10;
            num = (int)(num / 10);
            if (digit < min) {
                min = digit;
            }
        }

        List<Integer> a = Nlist.stream()
                .filter(x -> x != min)
                .collect(Collectors.toList()); //Leave only what is not a minimum

        String joined = a.stream()
                .map(String::valueOf)
                .collect(Collectors.joining(""));
        int res = Integer.parseInt(joined); //Back from list
        return res;
    }
}