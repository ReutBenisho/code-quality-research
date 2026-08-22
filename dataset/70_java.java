import java.util.*;
import java.util.stream.*;

public class Main {
    public static int RemoveMinDigit(int n) {
        List<Integer> dig = String.valueOf(n).chars()
                .mapToObj(x -> Character.getNumericValue((char) x))
                .collect(Collectors.toList()); //make a list from the number

        int min_dig = Collections.min(dig); //find the min dig

        List<Integer> new_list = dig.stream()
                .filter(a -> a != min_dig)
                .collect(Collectors.toList()); //removing the min dig

        List<String> s = new_list.stream()
                .map(i -> String.valueOf(i))
                .collect(Collectors.toList());

        int res = Integer.parseInt(String.join("", s));
        return res;
    }
}