public class Main {

    public static class Ref<T> {
        public T value;
        public Ref(T value) { this.value = value; }
    }

    public static void printLine(char[] data) {
        System.out.println(new String(data));
    }

    public static void function1(Ref<char[]> dataRef) {
        dataRef.value = new char[100];
        java.util.Arrays.fill(dataRef.value, 0, 100 - 1, 'A');
        dataRef.value[100 - 1] = '\0';
    }

    public static void function2() {
        Ref<char[]> dataRef = new Ref<>(null);
        function1(dataRef);

        if (dataRef.value != null) {
            printLine(dataRef.value);
            dataRef.value = null;
        }
    }

    public static void main(String[] args) {
        function2();
    }
}