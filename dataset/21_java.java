
public class Storage {
    private byte[] buf;

    private Storage(final byte[] buf) {
        this.buf = buf; 
    }

    public static Storage of(final byte[] buf) {
        return new Storage(buf.clone());
    }
}
