#include <wchar.h>

namespace Test
{
    void Function1(char * &data)
    {
        data = new char[100];
        memset(data, 'A', 100-1);
        data[100-1] = '\0';
    }

    void Function2()
    {
        char * data = NULL;
        Function1(data);
        
        if (data != NULL)
        {
            delete [] data;
            data = NULL;
        }
    }
}

int main(int argc, char * argv[])
{
    Test::Function2();
    return 0;
}