import sys
import ctypes

def main():
    i = 0
    buff = (ctypes.c_char * 128)()
    arg1 = sys.argv[1].encode('utf-8') + b'\0'

    while arg1[i] != 0:
        buff[i] = arg1[i]
        i += 1
    buff[i] = 0

    print("buff = " + buff.value.decode('utf-8'))

if __name__ == "__main__":
    main()