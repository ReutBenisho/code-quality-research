class Pointer:
    def __init__(self, value=None):
        self.value = value

def process():
    data = Pointer(None)
    data_ref = data
    
    data = None
    data_ref = data

    local_data = data_ref
    print(local_data.value)

if __name__ == "__main__":
    process()