# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 19:47:14 2022

@author: jestp
"""

#pygame 3
#Conway's game of life
# taken from https://www.geeksforgeeks.org/conways-game-life-python-implementation/

import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Set up variables

ON = 255
OFF = 0
vals = [ON, OFF]

def randomGrid(N):
    
    #returns a random grid of NXN random values
    return np.random.choice(vals, N*N, p = [0.2, 0.8]).reshape (N, N)

def addGlider (i, j, grid):
    # adds a glider with top left cell at (i, j)
    
    glider = np.array([[0, 0, 255],
                      [255, 0, 255],
                     [0, 255, 255]])
    grid[i:i+3, j:j+3] = glider

def update(frameNum, img, grid, N):
    
    #Copies grid
    
    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):
            
            
            #Computer the 8 neighbor sum in torodial
            total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] +
                         grid[(i-1)%N, j] + grid[(i+1)%N, j] +
                         grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
                         grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/255)
            
            #apply conway's rules
            if grid[i, j] == ON:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = OFF
            else:
                if total == 3:
                    newGrid[i, j] = ON
    
    # update the data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

def main():
    
    # Command line args are in sys.argv [1], sys.argv[2]...
    # sys.argv[0] is the script name itself
    # parse arguments
    
    parser = argparse.ArgumentParser(description = "Runs Conway's Game of Life simulation.")
    
    #arguments
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--glider', action='store_true', required=False)
    parser.add_argument('--gosper', action='store_true', required=False)
    args = parser.parse_args()
    
    # set grid size
    N = 100
    if args.N and int(args.N) > 8:
        N =  int(args.N)
        
    # set animation update interval
    
    updateInterval = 50
    if args.interval:
        updateInterval = int(args.interval)
        
    # declare grid
    grid = np.array([])
    
    if args.glider:
        grid = np.zeros(N*N).reshape(N, N)
        addGlider(1, 1, grid)
    elif args.gosper:
        grid = np.zeros(N*N).reshape(N,N)
    else:
        grid = randomGrid(N)
        
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ),
                                  frames = 10,
                                  interval = updateInterval,
                                  save_count=50)
    
    # # of frames
    # set output file
    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])
    
    plt.show()
    
if __name__ == '__main__':
    main()