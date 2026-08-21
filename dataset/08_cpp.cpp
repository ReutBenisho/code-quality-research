class StandardLibrarySample {
public:
    void processResource(AutoCloseable* resource) {
        if (resource != nullptr) {
            resource->close();
        }
    }
};