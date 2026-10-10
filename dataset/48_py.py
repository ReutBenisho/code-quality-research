import ctypes
import sys

if sys.platform == "win32":
    libc = ctypes.CDLL("msvcrt.dll")
else:
    libc = ctypes.CDLL(None)

libc.malloc.restype = ctypes.c_void_p
libc.malloc.argtypes = [ctypes.c_size_t]
libc.free.argtypes = [ctypes.c_void_p]

def function1(data_ref):
    ptr = libc.malloc(100)
    data_ref[0] = ptr
    char_ptr = ctypes.cast(ptr, ctypes.POINTER(ctypes.c_char))
    ctypes.memset(char_ptr, ord('A'), 100 - 1)
    char_ptr[100 - 1] = b'\x00'

def function2():
    data_ref = [None]
    function1(data_ref)
    if data_ref[0] is not None:
        libc.free(data_ref[0])
        data_ref[0] = None

if __name__ == "__main__":
    function2()