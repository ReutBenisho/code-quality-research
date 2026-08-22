import java.util.Objects;

public class StandardLibrarySample {
    public void processResource(AutoCloseable resource) throws Exception {
        if (Objects.nonNull(resource)) {
            resource.close(); 
        }
    }
}
