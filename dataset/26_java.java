
public class TestClass
{
    public void func() throws Throwable
    {
        switch (7)
        {
        case 7:
            int x;
            x = (new SecureRandom()).nextInt();
            if (x == 0)
            {
                IO.writeLine("Inside the if statement");
            }
            else
            {
            }
            IO.writeLine("Hello from func()");
            break;
        default:
            IO.writeLine("Benign, fixed string");
            break;
        }
    }
}