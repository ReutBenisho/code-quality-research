public FileInputStream openFile(String pathStr, FileInputStream fileToOpen) {
    Path filePath = Paths.get(pathStr);

    if (!Files.exists(filePath)) {
        return null;
    }

    if (!Files.isRegularFile(filePath)) {
        return null;
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
        return null;
    }

    return fileToOpen;
}