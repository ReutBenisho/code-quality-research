#include <iostream>
#include <climits>

static void Func1(unsigned int &data)
{
    data = UINT_MAX;
}

void Func2()
{
    unsigned int data;
    data = 0;
    Func1(data);
    unsigned int result = data + 1;
    std::cout << result << std::endl;
}

int main()
{
    Func2();
    return 0;
}