import copy
import argparse
import os
from multiprocessing import Process

from timeit import default_timer as timer
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter

from astar import AStarPlanner
from rrt import rrtPlanner
from genetic import geneticPlanner
from world import World

plt.rcParams['animation.ffmpeg_path'] ='C:\\Users\\ndarius\\Downloads\\ffmpeg-2024-03-18-git-a32f75d6e2-full_build\\bin\\ffmpeg.exe'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Planner configuration')
    parser.add_argument('-p', '--planner', dest='planner', type=str, choices=['a*', 'rrt', 'compare', 'gen'], default='compare', help='[a*, rrt, compare, gen] (default: compare)')
    parser.add_argument('-v', '--visualise', dest='visualise', type=int, choices=[0,1], default=1, help='[0 for no vis, 1 for vis] (default: 1)')
    parser.add_argument('-s', '--save', dest='save', type=int, choices=[0,1], default=0, help='[0 to not save, 1 for save] (default: 0)')
    args = parser.parse_args()

    world = World(30,30)
    world.vis()
    cmap = ListedColormap(['w', 'k', 'r', 'b', 'y', 'c' ,'g'])
 
    if args.planner == 'a*':
        planner = AStarPlanner(world)
        start = timer()
        visFrames = planner.solve()
        end = timer()
        print("time taken: ", end-start)

        if args.visualise == 1:
            fig = plt.figure()
            plot = plt.matshow(visFrames[0], cmap=cmap, fignum=0)

            def init():
                plot.set_data(visFrames[0])
                return plot

            def update(i):
                plot.set_data(visFrames[i])
                return [plot]
            anim = FuncAnimation(fig, update, init_func=init, frames = len(visFrames), interval = 30, repeat=False)

            if args.save == 1:
                filepath = os.path.join(os.getcwd(), "video", "astar.mp4")
                writerVideo = FFMpegWriter(fps=60)
                anim.save(filepath, writer=writerVideo)
            else:
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

            if args.save == 1:
                filepath = os.path.join(os.getcwd(), "video", "rrts.mp4")
                writerVideo = FFMpegWriter(fps=60)
                anim.save(filepath, writer=writerVideo)
            else:
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
            anim = FuncAnimation(fig, update, init_func=init, frames = len(world.frames), interval = 200, repeat=False)
            if args.save == 1:
                filepath = os.path.join(os.getcwd(), "video", "gen.mp4")
                writerVideo = FFMpegWriter(fps=60)
                anim.save(filepath, writer=writerVideo)
            else:
                plt.show()

    elif args.planner == 'compare':
        planner = AStarPlanner(world)
        start = timer()
        visAStarFrames = planner.solve()
        end = timer()
        print("time taken: ", end-start)

        if args.visualise == 1:
            fig1 = plt.figure(1)
            plot1 = plt.matshow(visAStarFrames.frames[0], cmap=cmap, fignum=0)

            def init1():
                plot1.set_data(visAStarFrames.frames[0])
                return plot1

            def update1(i):
                plot1.set_data(visAStarFrames.frames[i])
                return [plot1]
            anim1 = FuncAnimation(fig1, update1, init_func=init1, frames = len(visAStarFrames.frames), interval = 30, repeat=False)
            
            fig2 = plt.figure(2)
            plot2 = plt.matshow(rrtWorld.frames[0], cmap=cmap, fignum=0)

            def init2():
                plot2.set_data(rrtWorld.frames[0])
                return plot2

            def update2(i):
                plot2.set_data(rrtWorld.frames[i])
                return [plot2]
            anim2 = FuncAnimation(fig2, update2, init_func=init2, frames = len(rrtWorld.frames), interval = 30, repeat=False)

            fig3 = plt.figure(3)
            plot3 = plt.matshow(genWorld.frames[0], cmap=cmap, fignum=0)

            def init3():
                plot3.set_data(genWorld.frames[0])
                return plot3

            def update3(i):
                plot3.set_data(genWorld.frames[i])
                return [plot3]
            anim3 = FuncAnimation(fig3, update3, init_func=init3, frames = len(genWorld.frames), interval = 30, repeat=False)
            if args.save == 1:
                filepath1 = os.path.join(os.getcwd(), "video", "astar.mp4")
                filepath2 = os.path.join(os.getcwd(), "video", "rrt.mp4")
                filepath3 = os.path.join(os.getcwd(), "video", "gen.mp4")
                writerVideo = FFMpegWriter(fps=60)
                anim1.save(filepath1, writer=writerVideo)
                anim2.save(filepath2, writer=writerVideo)
                anim3.save(filepath3, writer=writerVideo)
            else:
                plt.show()

    print('exit')