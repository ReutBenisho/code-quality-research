import ctypes

MAXSIZE = 40

def process_input():
    buffer = (ctypes.c_char * MAXSIZE)()
    user_input = input().encode('utf-8')
    
    ctypes.memmove(buffer, user_input, len(user_input))
    
    print("Data received: " + buffer.value.decode('utf-8'))

if __name__ == "__main__":
    process_input()