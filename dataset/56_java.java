public boolean openFile(String pathStr, FileInputStream fileToOpen) {
    Path filePath = Paths.get(pathStr);

    if (!Files.exists(filePath)) {
        return false;
    }

    if (!Files.isRegularFile(filePath)) {
        return false;
    }

    if (fileToOpen != null) {
        try {
            fileToOpen.close();
        } catch (IOException e) {
        }
    }

    try {
        fileToOpen = new FileInputStream(filePath.toFile());
    } catch (FileNotFoundException e) {
        return false;
    }

    return fileToOpen.getChannel().isOpen();
}