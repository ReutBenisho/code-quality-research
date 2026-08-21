
public class Test {
    public void hasArguments(String name) {
        int length = name.length();
        System.out.println("Length: " + length);
    }

    public static void main(String[] args) {
        String name = null;
        Test mnp = new Test();
        mnp.hasArguments(name); 
    }
}
