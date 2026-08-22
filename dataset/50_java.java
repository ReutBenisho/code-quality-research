
package Test;

public class Main {

    static class Pointer<T> {
        public T value;
        public Pointer(T value) {
            this.value = value;
        }
    }

    static void func1(Pointer<Integer> dataRef) {
        dataRef.value = Integer.MAX_VALUE;
    }

    static void func2() {
        Pointer<Integer> data = new Pointer<>(0);
        func1(data);
        
        if (data.value < Integer.MAX_VALUE) {
            int result = data.value + 1;
            System.out.println(result);
        }
    }

    public static void main(String[] args) {
        func2();
    }
}