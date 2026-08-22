def function():
    p = None
    try:
        p = [0] * 1000
    except MemoryError:
        print("Error allocating memory.")

    print(p, end="")
    return

if __name__ == "__main__":
    print("Please enter two numbers: ")
    i = int(input())
    j = int(input())

    while i == j:
        function()