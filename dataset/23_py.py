import secrets

class TestClass:
    def func(self):
        if IO.STATIC_FINAL_TRUE:
            min_val = -32768
            max_val = 32767
            data = min_val + secrets.randbelow(max_val - min_val + 1)
        else:
            data = 0

        if IO.STATIC_FINAL_TRUE:
            data += 1
            data = (data + 32768) % 65536 - 32768
            result = data
            IO.writeLine("result: " + str(result))