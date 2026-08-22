public class Main {
    /** 
     * Checks if a string is a pangram
     * Parameters: String
     * Returns: Boolean parameter: Returns true if it is an pangram and false number or not
     */
    public static boolean IsPangrams(String x) {
        x.toLowerCase();
        char l = 'a';
        for (int i = 0; i < 26; i++) {
            if (x.indexOf(l) != -1) {
                l = (char)(l + 1);
            }
            else {
                return false;
            }
        }

        return true;
    }
}