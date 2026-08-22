class TestClass:
    _PRIVATE_STATIC_FINAL_FIVE = 5

    @staticmethod
    def func():
        if TestClass._PRIVATE_STATIC_FINAL_FIVE == 5:
            data = 32767
        else:
            data = 0

        if TestClass._PRIVATE_STATIC_FINAL_FIVE == 5:
            data += 1
            result = data
            print("result: " + str(result))

    @staticmethod
    def main(args):
        TestClass.func()