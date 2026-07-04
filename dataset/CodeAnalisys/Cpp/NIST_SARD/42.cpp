#include <iostream>
using namespace std;

#define BUFSIZE 32

int main() {
	char *buf;
	try {
                buf = new char[BUFSIZE];
            }
 	catch (bad_alloc&)
	{
	  cout << "Error allocating memory." << endl;
	  return 0;
	}

	buf[BUFSIZE-1]='a';
	delete [] buf;
	return 0;
}