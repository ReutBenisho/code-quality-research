public class Test {
    private int a = 5;

    public void check(int j) {
        if (false || false) {
            System.out.println("Text");
        }
        this.bar(this.a);
        
        ++j;
    }

    private void bar(int val) {}
}
