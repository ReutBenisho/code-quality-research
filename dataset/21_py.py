class Storage:
    def __init__(self, buf):
        self._buf = buf

    @staticmethod
    def of(buf):
        return Storage(buf.copy())