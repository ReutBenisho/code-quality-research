class Test:
    def closeConnection(self, c):
        if c is not None:
            c.close()

    def process(self, pool):
        c = pool.getConnection()
        try:
            # Business logic
            pass
        finally:
            self.closeConnection(c)

    class Pool:
        def getConnection(self):
            pass