import java.util.Arrays;

public class Main {
    public static boolean is_anagram(String s1, String s2) {
        // the sorted strings are checked
        String str1 = s1.toLowerCase();
        String str2 = s2.toLowerCase();
        
        char[] charArray1 = str1.toCharArray();
        char[] charArray2 = str2.toCharArray();
        
        Arrays.sort(charArray1);
        Arrays.sort(charArray2);
        
        if (Arrays.equals(charArray1, charArray2)) {
            return true;
        }
        else {
            return false;
        }
    }
}