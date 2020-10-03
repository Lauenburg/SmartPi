import numpy
import time
import configparser
from multiprocessing import Process, Queue
import matplotlib.pyplot as plt

def live_plt(queue):
    ''' Plots the data from the queue. If the queue is empty 
        the function waits for new input.

        Args:
            queue: Queue with the data that is to be plotted
    '''
    
    # Load the configuration data
    config = configparser.ConfigParser()
    config.read('settings.ini')
    config_plot = config["plot"]
    config_logs = config["logs"]

    # configuring the plot
    fig, ax = plt.subplots(1, 1)
    current_time = float(time.time())
    ax.set_xlim(current_time, current_time + int(config_plot["x_limit"]))
    ax.set_ylim(int(config_plot["y_top_limit"]), int(config_plot["y_bottom_limit"]))
    plt.ylabel(str(config_plot["y_label"]), fontsize=11)
    plt.xlabel(str(config_plot["x_label"]), fontsize=11)
    plt.title(str(config_plot["title"]))
    plt.show(block=False)

    # set up the plot to be live
    fig.canvas.draw()
    background = fig.canvas.copy_from_bbox(ax.bbox)
    time_list = [float(time.time())]
    point_list = [0]
    points = ax.plot(time_list, point_list, '-', animated=True)[0]

    # draw the plot
    while True:
        data = queue.get()
        if (data == 'DONE'):
            break
        if float(time.time()) >= current_time + int(config_plot["x_limit"]):
            break
        time_list.append(float(time.time()))
        point_list.append(float(data))
        points.set_data(time_list, point_list)
        fig.canvas.restore_region(background)

        # redraw just the points
        ax.draw_artist(points)
        plt.pause(0.01)

        # fill in the axes rectangle
        fig.canvas.blit(ax.bbox)

        print(int(time.time()), int(float(data)))
        print("AVG: "+ str(numpy.average(point_list)))

    # save and close the figure
    fig.savefig(str(config_logs["dir_fig"]))
    plt.close('all')
