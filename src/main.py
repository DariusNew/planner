from timeit import default_timer as timer
from algorithm import aStarPlanner
from world import World
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation

if __name__ == "__main__":

    world = World()
    world.vis()
    start = timer()
    print(aStarPlanner(world))
    end = timer()
    print("time taken: ", end-start)
    world.vis()

    print("looking inside")

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