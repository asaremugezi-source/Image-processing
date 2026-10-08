from mathematics import gcd, lcm
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
                new_grid[i//old_height][j//old_width][k] += grid[i//new_height][j//new_width][k]
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
