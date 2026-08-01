
#include <iostream>
using namespace std;


void function() {
	short *p = 0;
	try {
                p = new short [1000];
            }
 	catch (bad_alloc&)
	{
	  cout << "Error allocating memory." << endl;
	}

	cout<<p;
	return;
}

int main()
{
	int i,j;
	cout<<"Please enter two numbers: "<<endl;
	cin>>i>>j;
	
	while (i==j) function();
	return 0;
}

