import general_io
TEMPLATE = bytearray([66, 77, 70, 0, 0, 0, 0, 0, 0, 0, 54, 0, 0, 0, 40, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 1, 0, 24, 0, 0, 0, 0, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
SIZE_ADDRESS = 0x02
OFFSET_ADDRESS = 0x0A
WIDTH_ADDRESS = 0x12
HEIGHT_ADDRESS = 0x16


def write_image(grid, name = "example", template = TEMPLATE):
    file = bytearray([template[i] for i in range(len(template))])
    width = len(grid[0])
    height = len(grid)
    offset = general_io.read_data(file, OFFSET_ADDRESS)
    general_io.write_data(file, WIDTH_ADDRESS, width)
    general_io.write_data(file, HEIGHT_ADDRESS, height)
    extra_bytes_per_row = (4-(((width & 0b11) * 3) & 0b11))&0b11
    size = (width * 3 + extra_bytes_per_row)*height
    general_io.write_data(file, SIZE_ADDRESS, size)
    for i in range(height-1,-1,-1):
        for j in range(width):
            for k in range(2,-1,-1):
                file.append(grid[i][j][k])
        for i in range(extra_bytes_per_row):
            file.append(0)
    x = open(name + ".bmp", "wb")
    x.write(file)
    x.close()


def read_image(name):
    x = open(name + ".bmp", "rb")
    file = bytearray(x.read())
    x.close()
    width = general_io.read_data(file, WIDTH_ADDRESS)
    height = general_io.read_data(file, HEIGHT_ADDRESS)
    extra_bytes_per_row = (4-(((width & 0b11) * 3) & 0b11))&0b11
    grid = [[[0,0,0] for i in range(width)] for j in range(height)]
    index = general_io.read_data(file, OFFSET_ADDRESS)
    for i in range(height):
        for j in range(width):
            for k in range(3):
                grid[height-i-1][j][2-k] = file[index]
                index += 1
        index += extra_bytes_per_row
    return grid
