public class Main {
    /**
     * The function receives a string and checks if it is a pangram
     *
     * :param str: String parameter
     * :return:Returns true if the string is a pangram else return false
     */
    public static boolean IsPangrams(String str) {
        String alphabet = "AbcdefghiJklmnopqrstuvwXyz";
        for (char c : alphabet.toCharArray()) {
            String chStr = String.valueOf(c);
            if (!str.toLowerCase().contains(chStr) && !str.toUpperCase().contains(chStr)) {
                return false;
            }
        }

        return true;
    }
}