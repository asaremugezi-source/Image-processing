TEMPLATE = bytearray([66, 77, 70, 0, 0, 0, 0, 0, 0, 0, 54, 0, 0, 0, 40, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 1, 0, 24, 0, 0, 0, 0, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

def read_data(data ,address, num_bytes = 4):
    val = 0
    for i in range(num_bytes):
        val += data[address+i]<<(8*i)
    return val

def write_data(data, address, val, num_bytes = 4):
    for i in range(num_bytes):
        data[address+i] = val & 0xFF
        val >>= 8

SIZE_ADDRESS = 0x02
OFFSET_ADDRESS = 0x0A
WIDTH_ADDRESS = 0x12
HEIGHT_ADDRESS = 0x16


def write_image(grid, name = "example", template = TEMPLATE):
    file = template.copy()
    width = len(grid[0])
    height = len(grid)
    offset = read_data(file, OFFSET_ADDRESS)
    write_data(file, WIDTH_ADDRESS, width)
    write_data(file, HEIGHT_ADDRESS, height)
    extra_bytes_per_row = (4-(((width & 0b11) * 3) & 0b11))&0b11
    size = (width * 3 + extra_bytes_per_row)*height
    write_data(file, SIZE_ADDRESS, size)
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
    file = list(x.read())
    x.close()
    width = read_data(file, WIDTH_ADDRESS)
    height = read_data(file, HEIGHT_ADDRESS)
    extra_bytes_per_row = (4-(((width & 0b11) * 3) & 0b11))&0b11
    grid = [[[0,0,0] for i in range(width)] for j in range(height)]
    index = read_data(file, OFFSET_ADDRESS)
    for i in range(height):
        for j in range(width):
            for k in range(3):
                grid[height-i-1][j][2-k] = file[index]
                index += 1
        index += extra_bytes_per_row
    return grid


def gcd(a,b):
    while a != 0:
        r = b % a
        b = a
        a = r
    return b

def lcm(a,b):
    return a*b//gcd(a,b)

def rescale_slow(grid, new_width, new_height):
    #deprecated function used to debug rescale during coding, conceptially simpler expression of same algorithm.
    old_width = len(grid[0])
    old_height = len(grid)
    w = old_width*new_width
    h = old_height*new_height
    new_grid = [[[0,0,0] for i in range(new_width)] for j in range(new_height)]
    for i in range(h):
        for j in range(w):
            for k in range(3):
                new_grid[i//old_width][j//old_height][k] += grid[i//new_height][j//new_width][k]
    for i in range(new_height):
        for j in range(new_width):
            for k in range(3):
                new_grid[i][j][k] += ((w//new_width)*(h//new_height))//2
                new_grid[i][j][k] //= (w//new_width)*(h//new_height)
    return new_grid
            
def rescale(grid, new_width, new_height):
    new_grid = [[[0,0,0] for i in range(new_width)] for j in range(new_height)]
    old_width = len(grid[0])
    old_height = len(grid)
    w = lcm(old_width, new_width)
    h = lcm(old_height, new_height)
    new_square_dimensions = [w//new_width, h//new_height]
    old_square_dimensions = [w//old_width, h//old_height]
    for i in range(new_width):
        left_edge = new_square_dimensions[0]*i
        right_edge = left_edge + new_square_dimensions[0]
        for j in range(new_height):
            top_edge = new_square_dimensions[1]*j
            bottom_edge = new_square_dimensions[1] + top_edge
            for x in range(left_edge//old_square_dimensions[0], (right_edge-1)//old_square_dimensions[0] + 1):
                width = -max(left_edge, x*old_square_dimensions[0]) + min(right_edge, (x+1)*old_square_dimensions[0])
                for y in range(top_edge//old_square_dimensions[1], (bottom_edge-1)//old_square_dimensions[1] + 1):
                    height = -max(top_edge, y*old_square_dimensions[1]) + min(bottom_edge, (y+1)*old_square_dimensions[1])
                    for k in range(3):
                        new_grid[j][i][k] += grid[y][x][k] * width * height
            for k in range(3):
                new_grid[j][i][k] += (new_square_dimensions[0]*new_square_dimensions[1])//2
                new_grid[j][i][k] //= new_square_dimensions[0]*new_square_dimensions[1]
    return new_grid

def embed(grid1, grid2, top, bottom, left, right):
    x = rescale(grid2, right-left, bottom-top)
    a = grid1.copy()
    for i in range(right-left):
        for j in range(bottom-top):
            a[j+top][i+left] = x[j][i]
    return a

x = read_image("drake_meme")
y = read_image("bell_curve_meme")
for i in range(20):
    print(i)
    y = embed(y, x, 180, 280, 50, 150)
    y = embed(y, x, 180, 280, 450, 550)
    y = embed(y, y, 0, 100, 250, 350)
    x = embed(x, y, 0, 600,600,1200)
    x = embed(x, x, 600, 1200,600,1200)
    
    write_image(x, "drake_meme2")
    
