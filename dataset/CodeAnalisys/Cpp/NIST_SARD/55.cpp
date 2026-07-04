bool OpenFile(const std::string& path, std::ifstream& fileToOpen)
{
    if (fileToOpen.is_open()) {
        fileToOpen.close();
    }

	fileToOpen.clear();

    fileToOpen.open(path);

    return fileToOpen.is_open();
}