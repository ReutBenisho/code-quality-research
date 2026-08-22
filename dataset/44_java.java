public class Main {
    public static void main(String[] args) {
        if (args.length < 1)
            return;

        int i = 0;
        char[] buff = new char[128];
        String arg1 = args[0] + "\0";

        while (arg1.charAt(i) != '\0' && i < 127) {
            buff[i] = arg1.charAt(i);
            i++;
        }
        buff[i] = '\0';

        System.out.println("buff = " + new String(buff, 0, i));
    }
}