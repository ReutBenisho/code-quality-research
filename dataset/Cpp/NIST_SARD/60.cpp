void func(int * data)
{
	if(data != nullptr)
	{
		data[0] = 5;
		printIntLine(data[0]);
	}
}