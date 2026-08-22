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
            if (localData != null) {
                System.out.println(localData.value);
            } else {
                System.out.println("Data is null");
            }
        }
    }

    public static void main(String[] args) {
        process();
    }
}