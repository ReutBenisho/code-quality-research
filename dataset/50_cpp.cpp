
static void Func1(unsigned int &data)
{
    data = UINT_MAX;
}

void Func2()
{
    unsigned int data;
    data = 0;
    Func1(data);
	if (data < UINT_MAX)
    {
		unsigned int result = data + 1;
		printLine(result);
	}
}

int main()
{
	Func2();
}