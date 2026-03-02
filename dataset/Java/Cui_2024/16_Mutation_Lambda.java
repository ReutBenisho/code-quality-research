public class LambdaMutation {
    public void runTask() {
        Runnable r = () -> {
            System.out.println("Running task via lambda");
        };
        r.run();
    }
}
