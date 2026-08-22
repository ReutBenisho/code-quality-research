public class Main {
    public static final int BUFSIZE = 32;

    public static void main(String[] args) {
        char[] buf;
        try {
            buf = new char[BUFSIZE];
        } catch (OutOfMemoryError e) {
            System.out.println("Error allocating memory.");
            return;
        }

        buf[BUFSIZE - 1] = 'a';
        buf = null;
    }
}