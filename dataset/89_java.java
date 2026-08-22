import java.util.Arrays;

public class Main {
    public static boolean is_anagram(String s1, String s2) {
        /**
         * :param s1: string
         * :param s2: string
         * :return: true if s1 is anagram of s2, false otherwise
         */
        s1 = s1.replace(" ", ""); // delete all spaces
        s2 = s2.replace(" ", "");

        s1 = s1.toLowerCase(); // turn all letters lower
        s2 = s2.toLowerCase();

        char[] s1Array = s1.toCharArray();
        char[] s2Array = s2.toCharArray();

        Arrays.sort(s1Array); // sort the string
        Arrays.sort(s2Array);

        s1 = new String(s1Array);
        s2 = new String(s2Array);

        return s1.equals(s2); // the condition
    }
}