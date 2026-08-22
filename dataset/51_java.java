package testcases.javatestcases.t51;


public class TestClass
{
    private static final int PRIVATE_STATIC_FINAL_FIVE = 5;

    public static void func()
    {
        short data;
        if (PRIVATE_STATIC_FINAL_FIVE==5)
        {
            data = Short.MAX_VALUE;
        }
        else
        {
            data = 0;
        }

        if (PRIVATE_STATIC_FINAL_FIVE==5)
        {
            short result = (short)(++data);
            System.out.println("result: " + result);
        }
    }

    public static void main(String[] args)
    {
        func();
    }
}
