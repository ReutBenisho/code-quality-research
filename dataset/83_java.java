public class Main {
    /**
     * Returns true if num is palindrome
     */
    public static boolean isPalindrome(int num) {
        int temp = num;
        int rev = 0;
        while (num > 0) {
            int dig = num % 10;
            rev = rev * 10 + dig;
            num = num / 10;
        }
        if (temp == rev) {
            return true;
        }
        else {
            return false;
        }
    }
}