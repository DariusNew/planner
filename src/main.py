from timeit import default_timer as timer
from algorithm import aStarPlanner
from world import World
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Planner configuration')
    parser.add_argument('-p', '--planner', dest='planner', type=str, choices=['a*', 'rrt'], default='a*', help='[a*, rrt] (default: a*)')
    parser.add_argument('-v', '--visualise', dest='visualise', type=int, choices=[0,1], default=1, help='[0 for no vis, 1 for vis] (default: 1)')
    args = parser.parse_args()

    world = World(100,100)
    world.vis()
 
    if args.planner == 'a*':
        start = timer()
        aStarPlanner(world)
        end = timer()
        print("time taken: ", end-start)
        world.vis()
    elif args.planner == 'rrt':
        start = timer()
        aStarPlanner(world) #change to rrt
        end = timer()
        print("time taken: ", end-start)
        world.vis()
    if args.visualise == 1:
        cmap = ListedColormap(['w', 'k', 'r', 'b', 'y', 'g'])
        fig = plt.figure()
        plot = plt.matshow(world.frames[0], cmap=cmap, fignum=0)

        def init():
            plot.set_data(world.frames[0])
            return plot

        def update(i):
            plot.set_data(world.frames[i])
            return [plot]
        anim = FuncAnimation(fig, update, init_func=init, frames = len(world.frames), interval = 30)
        plt.show()

    print('exit')