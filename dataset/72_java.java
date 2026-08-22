import java.util.*;
import java.util.stream.*;

public class Main {
    public static int RemoveMinDigit(int num) {
        /**
         * remove all min digit from the number:
         * :param num: int, positive integer
         * :return:int, the number without the smallest digit
         */
        if (num <= 0) {
            System.out.println("number is negative!");
            return num;
        }
        
        List<Integer> numList = String.valueOf(num).chars()
                .mapToObj(i -> Character.getNumericValue((char) i))
                .collect(Collectors.toList()); // turn the number into list of digits
                
        int minVal = Collections.min(numList);
        numList = numList.stream()
                .filter(i -> i != minVal)
                .collect(Collectors.toList()); // arrange the list with out the min digit
                
        if (numList.isEmpty()) { // in case the number is made by 1 digit only: x, xxx, xxx ...
            return 0;
        }
        
        String joined = numList.stream()
                .map(String::valueOf)
                .collect(Collectors.joining(""));
        return Integer.parseInt(joined); // join all digits left into int
    }
}