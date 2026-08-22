public boolean openFile(String path, FileInputStream fileToOpen) {
    if (fileToOpen != null) {
        try {
            fileToOpen.close();
        } catch (IOException e) {
        }
    }

    fileToOpen = new FileInputStream(path);

    return fileToOpen.getChannel().isOpen();
}