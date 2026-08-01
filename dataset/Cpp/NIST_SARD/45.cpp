
#include <wchar.h>

namespace Test
{

	void Function1(char * &data)
	{
		data = new char[100];
		memset(data, 'A', 100-1);
		data[100-1] = '\0';
		delete [] data;
	}

	void Function2()
	{
		char * data;
		data = NULL;
		Function1(data);
		printLine(data);
	}
}
int main(int argc, char * argv[])
{
	Test::Function2();
	return 0;
}