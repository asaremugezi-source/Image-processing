import BMP_io
import general_io
import main
import mathematics
import transformations
import random
f = lambda :random.randint(0,255)
start = 2
end = 7
failed = 0
for g in (transformations.rescale, transformations.rescale_slow):
    for i in range(start, end):
        for j in range(start, end):
            grid = [[[f(),f(),f()] for x in range(i)] for y in range(j)]
            for k in range(start, end):
                for l in range(start, end):
                    if grid != g(g(grid, i*k, j*l),i,j):
                        print("test failed for grid: ")
                        print(grid)
                        print(k, l)
                        failed += 1
print(str(failed) + " tests failed.")
failed = 0
start = 1
end = 7
for i in range(start, end):
    for j in range(start, end):
        for _ in range(10):
            grid = [[[f(),f(),f()] for x in range(i)] for y in range(j)]
            for k in range(start, end):
                for l in range(start, end):
                    if transformations.rescale(grid,k,l) != transformations.rescale_slow(grid,k,l):
                        print("test failed for grid: ")
                        print(grid)
                        print()
                        print(transformations.rescale(grid,k,l))
                        print()
                        print(transformations.rescale_slow(grid,k,l))
                        failed += 1
print(str(failed) + " tests failed.")


                
