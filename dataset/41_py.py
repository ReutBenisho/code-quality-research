BUFSIZE = 32

def main():
    try:
        buf = [None] * BUFSIZE
    except MemoryError:
        print("Error allocating memory.")
        return

    buf[33] = 'a'
    del buf

if __name__ == "__main__":
    main()