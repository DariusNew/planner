import copy
import argparse
from timeit import default_timer as timer
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation

from astar import aStarPlanner
from rrt import rrtPlanner
from genetic import geneticPlanner
from world import World

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Planner configuration')
    parser.add_argument('-p', '--planner', dest='planner', type=str, choices=['a*', 'rrt', 'compare', 'gen'], default='compare', help='[a*, rrt, compare, gen] (default: compare)')
    parser.add_argument('-v', '--visualise', dest='visualise', type=int, choices=[0,1], default=1, help='[0 for no vis, 1 for vis] (default: 1)')
    args = parser.parse_args()

    world = World(30,30)
    world.vis()
    cmap = ListedColormap(['w', 'k', 'r', 'b', 'y', 'c' ,'g'])
 
    if args.planner == 'a*':
        start = timer()
        aStarPlanner(world)
        end = timer()
        print("time taken: ", end-start)
        world.vis()

        if args.visualise == 1:
            fig = plt.figure()
            plot = plt.matshow(world.frames[0], cmap=cmap, fignum=0)

            def init():
                plot.set_data(world.frames[0])
                return plot

            def update(i):
                plot.set_data(world.frames[i])
                return [plot]
            anim = FuncAnimation(fig, update, init_func=init, frames = len(world.frames), interval = 30, repeat=False)
            plt.show()
        
    elif args.planner == 'rrt':
        start = timer()
        rrtPlanner(world) #change to rrt
        end = timer()
        print("time taken: ", end-start)
        world.vis()

        if args.visualise == 1:
            fig = plt.figure()
            plot = plt.matshow(world.frames[0], cmap=cmap, fignum=0)

            def init():
                plot.set_data(world.frames[0])
                return plot

            def update(i):
                plot.set_data(world.frames[i])
                return [plot]
            anim = FuncAnimation(fig, update, init_func=init, frames = len(world.frames), interval = 30, repeat=False)
            plt.show()

    elif args.planner == 'compare':
        aStarWorld = copy.deepcopy(world)
        aStarStart = timer()
        aStarPlanner(aStarWorld)
        aStarEnd = timer()
        print("a*: ", aStarEnd-aStarStart)
        
        rrtWorld = copy.deepcopy(world)
        rrtStart = timer()
        rrtPlanner(rrtWorld)
        rrtEnd = timer()
        print("rrt: ", rrtEnd-aStarStart)

        if args.visualise == 1:
            fig1 = plt.figure(1)
            plot1 = plt.matshow(aStarWorld.frames[0], cmap=cmap, fignum=0)

            def init1():
                plot1.set_data(aStarWorld.frames[0])
                return plot1

            def update1(i):
                plot1.set_data(aStarWorld.frames[i])
                return [plot1]
            anim1 = FuncAnimation(fig1, update1, init_func=init1, frames = len(aStarWorld.frames), interval = 30, repeat=False)
            
            fig2 = plt.figure(2)
            plot2 = plt.matshow(rrtWorld.frames[0], cmap=cmap, fignum=0)

            def init2():
                plot2.set_data(rrtWorld.frames[0])
                return plot2

            def update2(i):
                plot2.set_data(rrtWorld.frames[i])
                return [plot2]
            anim2 = FuncAnimation(fig2, update2, init_func=init2, frames = len(rrtWorld.frames), interval = 30, repeat=False)
            plt.show()

    elif args.planner == 'gen': 
        start = timer()
        geneticPlanner(world)
        end = timer()
        print("time taken: ", end-start)

        if args.visualise == 1:
            fig = plt.figure()
            plot = plt.matshow(world.frames[0], cmap=cmap, fignum=0)
            
            def init():
                plot.set_data(world.frames[0])
                return plot

            def update(i):
                plot.set_data(world.frames[i])
                return [plot]
            anim = FuncAnimation(fig, update, init_func=init, frames = len(world.frames), interval = 200, repeat=True)
            plt.show()

    print('exit')