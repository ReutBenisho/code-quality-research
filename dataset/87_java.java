public class Main {
    public static boolean isPalindrome(int x) {
        /**
         * :param x: int, non-negative
         * :return: bool, true if x is Palindrome, false otherwise
         */
        String s = String.valueOf(x);
        String rev = new StringBuilder(s).reverse().toString();
        return s.equals(rev);
    }
}