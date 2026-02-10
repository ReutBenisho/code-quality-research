/**
 * Source: Cui et al. 2024, Fig 5(b)
 * Issue: PMD #3148
 * Category: Java Standard Libraries (Objects.nonNull)
 * Ground Truth: False Positive (FP)
 */
import java.util.Objects;

public class StandardLibrarySample {
    public void processResource(AutoCloseable resource) throws Exception {
        if (Objects.nonNull(resource)) {
            // PMD incorrectly thinks this is unreachable
            resource.close(); 
        }
    }
}