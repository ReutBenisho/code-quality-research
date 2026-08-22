import java.util.Arrays;

public class Main {
    /**
     * The function receives two strings and checks whether one is an anagram of the other
     * I.e. do they have exactly the same letters but in a different order.
     *
     * :param string1:Sring
     * :param string2:string
     * :return:The function will return truth if it is an anagram.
     */
    public static boolean is_anagram(String string1, String string2) {
        String a = string1.toUpperCase();
        String b = string2.toUpperCase();

        if (a.length() != b.length()) {
            return false;
        }

        char[] charArrayA = a.toCharArray();
        char[] charArrayB = b.toCharArray();

        Arrays.sort(charArrayA);
        Arrays.sort(charArrayB);

        if (Arrays.equals(charArrayA, charArrayB)) {
            return true;
        }
        else {
            return false;
        }
    }
}