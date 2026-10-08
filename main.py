import BMP_io
import transformations

def embed(grid1, grid2, top, bottom, left, right):
    x = transformations.rescale(grid2, right-left, bottom-top)
    a = [[grid1[i][j] for j in range(len(grid1[0]))] for i in range(len(grid1))]
    for i in range(right-left):
        for j in range(bottom-top):
            a[j+top][i+left] = x[j][i]
    return a

def main():
    x = BMP_io.read_image("drake_meme")
    y = BMP_io.read_image("bell_curve_meme")
    for i in range(20):
        print(i)
        y = embed(y, x, 180, 280, 50, 150)
        y = embed(y, x, 180, 280, 450, 550)
        y = embed(y, y, 0, 100, 250, 350)
        x = embed(x, y, 0, 600,600,1200)
        x = embed(x, x, 600, 1200,600,1200)
        BMP_io.write_image(x, "drake_meme2")
    return

if __name__ == "__main__":
    main()

    
