bool OpenFile(const std::string& pathStr, std::ifstream& fileToOpen)
{
    std::filesystem::path filePath(pathStr);

    if (!std::filesystem::exists(filePath)) {
        return false;
    }

    if (!std::filesystem::is_regular_file(filePath)) {
        return false;
    }

    if (fileToOpen.is_open()) {
        fileToOpen.close();
    }
    
    fileToOpen.clear();
    fileToOpen.open(filePath);

    return fileToOpen.is_open();
}