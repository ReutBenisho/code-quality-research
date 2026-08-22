import sys

def main():
    input_buf = [None] * 100
    l = None
    
    print("How many numbers do you want to type in? ", end="")
    input_str = input()
    i = int(input_str)
    
    try:
        l = [0] * i
    except MemoryError as ba:
        print("Exception:")
        
    if l is None:
        sys.exit(1)
        
    for n in range(0, i):
        print("Enter number: ", end="")
        input_str = input()
        l[n] = int(input_str)
        
    print("You have entered: ", end="")
    for n in range(0, i):
        print(str(l[n]) + ", ", end="")
        
    del l
    return 0

if __name__ == "__main__":
    main()