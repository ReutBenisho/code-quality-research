import ctypes

def function1(data_ref):
    data_ref[0] = ctypes.create_string_buffer(100)
    ctypes.memset(data_ref[0], ord('A'), 100 - 1)
    data_ref[0][100 - 1] = 0
    
    libc = ctypes.CDLL(None)
    libc.free(ctypes.cast(data_ref[0], ctypes.c_void_p))

def function2():
    data_ref = [None]
    function1(data_ref)
    
    libc = ctypes.CDLL(None)
    libc.free(ctypes.cast(data_ref[0], ctypes.c_void_p))

if __name__ == "__main__":
    function2()