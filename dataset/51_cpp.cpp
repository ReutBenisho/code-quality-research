package testcases.javatestcases.t51;


public class TestClass
{
    private static final int PRIVATE_STATIC_FINAL_FIVE = 5;

    public static void func()
    {
        short data;#include <iostream>
#include <limits>

class TestClass
{
private:
    static const int PRIVATE_STATIC_FINAL_FIVE = 5;

public:
    static void func()
    {
        short data;
        if (PRIVATE_STATIC_FINAL_FIVE == 5)
        {
            data = std::numeric_limits<short>::max();
        }
        else
        {
            data = 0;
        }

        if (PRIVATE_STATIC_FINAL_FIVE == 5)
        {
            short result = (short)(++data);
            std::cout << "result: " << result << std::endl;
        }
    }

    static void main(int argc, char* argv[])
    {
        func();
    }
};