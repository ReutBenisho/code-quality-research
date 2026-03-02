import javax.annotation.concurrent.Immutable;
import javax.annotation.concurrent.ThreadSafe;

public class Wrapper {
    @Immutable
    class MyImmutable { }

    @ThreadSafe
    class MyThreadSafe { }

    class Main {
        private volatile MyImmutable x;
        private volatile MyThreadSafe y;
    }
}
