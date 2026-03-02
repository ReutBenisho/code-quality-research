
public class SecureStorage {
    private byte[] buf;

    private SecureStorage(final byte[] buf) {
        this.buf = buf; 
    }

    public static SecureStorage of(final byte[] buf) {
        return new SecureStorage(buf.clone());
    }
}
