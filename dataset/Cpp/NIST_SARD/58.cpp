
void assignData(std::string &data)
{
    std::cin >> data;
}

int main()
{
    std::string data1;
    std::string data2;
    assignData(data1);
    assignData(data2);
	std::cout << data1 <<std::endl;
	std::cout << data2 <<std::endl;
}