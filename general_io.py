def read_data(data ,address, num_bytes = 4):
    val = 0
    for i in range(num_bytes):
        val += int(data[address+i])<<(8*i)
    return val

def write_data(data, address, val, num_bytes = 4):
    for i in range(num_bytes):
        data[address+i] = val & 0xFF
        val >>= 8
