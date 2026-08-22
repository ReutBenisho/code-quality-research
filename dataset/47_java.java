package Test;

public class Main {

    static class Pointer<T> implements AutoCloseable {
        public T value;
        private boolean isFreed = false;

        public Pointer(T value) {
            this.value = value;
        }

        @Override
        public void close() {
            if (isFreed) {
                throw new IllegalStateException("Double Free Error: Memory/Resource already freed!");
            }
            this.value = null;
            this.isFreed = true;
        }
    }

    public static void function1(Pointer<char[]> dataRef) {
        dataRef.value = new char[100];
        java.util.Arrays.fill(dataRef.value, 'A');
        dataRef.value[99] = '\0';
        
        dataRef.close(); 
    }

    public static void function2() {
        Pointer<char[]> data = new Pointer<>(null);
        function1(data);
        
        data.close(); 
    }

    public static void main(String[] args) {
        function2();
    }
}