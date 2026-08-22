import ctypes

UINT_MAX = 4294967295

def print_line(result):
    print(result)

def func1(data_ref):
    data_ref[0] = ctypes.c_uint32(UINT_MAX).value

def func2():
    data = [0]
    func1(data)

    if data[0] < UINT_MAX:
        result = ctypes.c_uint32(data[0] + 1).value
        print_line(result)

if __name__ == "__main__":
    func2()