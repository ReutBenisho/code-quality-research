public class EquivalenceMutation {
    private int a = 5;

    public void check(int j) {
        if (false || false) {
            System.out.println("Unreachable");
        }
        this.bar(this.a);
        
        ++j;
    }

    private void bar(int val) {}
}
