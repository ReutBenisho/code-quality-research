import java.util.*;

public class Main {
    public static boolean IsPangrams(String s) {
        /**
         * check if a string IsPangrams:
         * :param s: string
         * :return: bool, True if al abc.. exist in it, False otherwise
         */
        Set<Object> seen = new HashSet<>();
        for (char i : s.toCharArray()) {
            if (Character.isLetter(i) && !seen.contains(i.upper)) {
                seen.add(Character.toUpperCase(i)); // add up each alpha char ass upper
            }
        }
        return seen.size() == 26; // check condition
    }
}