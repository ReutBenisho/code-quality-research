public class Wrapper {
    public byte[] foo(byte[] a1, byte[] a2) {
        if (a1.length != a2.length) {
            return null;
        }
        return a1;
    }
}
