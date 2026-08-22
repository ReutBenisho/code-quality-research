import sys

def function():
    p = None
    try:
        p = [0] * 1000
        print("Memory allocated at: " + str(p))
    except MemoryError as e:
        print("Error allocating memory: " + str(e), file=sys.stderr)
        return

    del p

if __name__ == "__main__":
    print("Please enter two numbers: ")
    try:
        i = int(input())
        j = int(input())
    except ValueError:
        sys.exit(1)

    while i == j:
        function()
        print("Running again... (Press Ctrl+C to stop or change logic)")