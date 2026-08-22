import java.util.Collections;
import java.util.stream.Collectors;

public class Main {
    public static int RemoveMinDigit(int x) {
        /** 
         * The function gets a number and drops all occurrences of the minimum digit
         *  
         * Parameters: Integer positive number
         *             
         * Returns: 
         *     Integer positive number: Without the minimum digit
         */
        String strX = String.valueOf(x);
        char minChar = Collections.min(strX.chars().mapToObj(c -> (char) c).collect(Collectors.toList()));
        String minStr = String.valueOf(minChar);

        int count = 0;
        for (char c : strX.toCharArray()) {
            if (c == minChar) {
                count++;
            }
        }

        String new_number = "";
        for (int n = 0; n < count; n++) {
            new_number = strX.replace(minStr, "");
        }
        return Integer.parseInt(new_number);
    }
}