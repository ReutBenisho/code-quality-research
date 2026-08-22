class Pointer:
    def __init__(self, value=None):
        self.value = value

def process():
    data = Pointer(None)
    data_ref = data
    
    data = None
    data_ref = data

    local_data = data_ref
    if local_data is not None:
        print(local_data.value)
    else:
        print("Data is null")

if __name__ == "__main__":
    process()