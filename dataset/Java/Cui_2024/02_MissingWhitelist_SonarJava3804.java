/**
 * Source: Cui et al. 2024, Fig 3(b)
 * Issue: PMD #2976
 * Category: Type Resolution / Multi-threading
 * Ground Truth: False Positive (FP)
 */
import javax.annotation.concurrent.Immutable;
import javax.annotation.concurrent.ThreadSafe;

public class Wrapper {
    @Immutable
    class MyImmutable { }

    @ThreadSafe
    class MyThreadSafe { }

    class Main {
        // PMD flags these as unsafe volatile fields because it misses the class annotations
        private volatile MyImmutable x;
        private volatile MyThreadSafe y;
    }
}