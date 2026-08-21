class Test:
    def hasArguments(self, name):
        length = len(name)
        print("Length: " + str(length))

    @staticmethod
    def main(args=None):
        name = None
        mnp = Test()
        mnp.hasArguments(name)