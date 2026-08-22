import java.util.Arrays;

public class Main {
    public static boolean is_anagram(String s1, String s2) { //A function that gets two strings and checks if one is An anagram of the second
        char[] charArray1 = s1.toUpperCase().toCharArray(); //Convert all letters to uppercase
        char[] charArray2 = s2.toUpperCase().toCharArray();

        Arrays.sort(charArray1); //sort
        Arrays.sort(charArray2); //sort

        return Arrays.equals(charArray1, charArray2); //Check if the strings are equal
    }
}