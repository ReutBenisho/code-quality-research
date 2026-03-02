import java.util.ArrayList;

public class LambdaSample {
    Runnable someAction = () -> {
        var foo = new ArrayList<String>(5);
        System.err.println(foo);
    };
}
