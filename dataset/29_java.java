import org.junit.Test;
import static org.junit.Assert.assertThrows;

public class TestUrlLoading {

    public static byte[] get_url_to_bytes(String url, boolean allow_file_url) {
        if (!allow_file_url && url.startsWith("file://")) {
            throw new IllegalArgumentException("File URL not explicitly allowed: " + url);
        }
        return "fake_data".getBytes();
    }

    public static byte[] get_url_to_bytes(String url) {
        return get_url_to_bytes(url, false);
    }

    @Test
    public void test_file_url_not_allowed() {
        String fake_file_url = "file://fake_image.png";
        assertThrows(IllegalArgumentException.class, () -> {
            get_url_to_bytes(fake_file_url, false);
        });
    }
}