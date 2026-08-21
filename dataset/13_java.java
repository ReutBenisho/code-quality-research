import java.util.ArrayList;

public class Test {
    Runnable someAction = () -> {
        var foo = new ArrayList<String>(5);
        System.err.println(foo);
    };
}
