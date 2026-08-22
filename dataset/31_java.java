package Test;

public class Main {

    static class Pointer<T> {
        public T value;
        public Pointer(T value) {
            this.value = value;
        }
    }

    public static void process() {
        Pointer<Long> data;
        Pointer<Long> dataRef;

        data = null;
        dataRef = data;

        {
            Pointer<Long> localData = dataRef;
            System.out.println(localData.value);
        }
    }

    public static void main(String[] args) {
        process();
    }
}