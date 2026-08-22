import ctypes

class UnsignedInt:
    def __init__(self, value=0):
        self._val = ctypes.c_uint32(value)

    @property
    def value(self):
        return self._val.value

    @value.setter
    def value(self, val):
        self._val = ctypes.c_uint32(val)

    def __add__(self, other):
        return UnsignedInt(self.value + (other.value if isinstance(other, UnsignedInt) else other))

def print_line(result):
    print(result.value)

def func1(data_ref):
    data_ref[0].value = 4294967295

def func2():
    data = [UnsignedInt(0)]
    func1(data)
    result = data[0] + 1
    print_line(result)

if __name__ == "__main__":
    func2()