#include <stdio.h>

int main(int argc, char *argv[])
{
	if (argc < 2) 
		return 1;

	int i = 0;
	char buff[128];
	char *arg1 = argv[1];

	while (arg1[i] != '\0' && i < 127)
	{
		buff[i] = arg1[i];
		i++;
	}
	buff[i] = '\0';

	printf("buff = %s\n", buff);
	
	return 0;
}