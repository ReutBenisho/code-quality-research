public class Outerclass {
    private int[] arr;
    public int[] getArr() { return arr; } 

    public static class Innerclass {
        private int[] arr2;
        public int[] getArr() { return arr2; } 
    }
}
