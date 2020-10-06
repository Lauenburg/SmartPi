import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy


def live_plt(
    queue,
    title,
    x_limit,
    y_top_limit,
    y_bottom_limit,
    x_label,
    y_label,
    dir_fig,
    file_fig,
):
    """ Plots the data from the queue. If the queue is empty
        the function waits for new input.

        Args:
            queue: Queue with the data that is to be plotted
            title: Title for the Plot
            x_limit: Time till end of the live plotting
            y_top_limit: Top limit of the y axes
            y_bottom_limit: Bottom limit of the y axes
            x_label: Label for the x axes
            y_label: Label for the y axes
            dir_fig: Directory where to save the figure
            file_fig: Name under which to save the figure

    """

    # configuring the plot
    fig, ax = plt.subplots(1, 1)
    current_time = float(time.time())
    ax.set_xlim(current_time, current_time + x_limit)
    ax.set_ylim(y_top_limit, y_bottom_limit)
    plt.ylabel(y_label, fontsize=11)
    plt.xlabel(x_label, fontsize=11)
    plt.title(title)
    plt.show(block=False)

    # set up the plot to be live
    fig.canvas.draw()
    background = fig.canvas.copy_from_bbox(ax.bbox)
    time_list = [float(time.time())]
    point_list = [0]
    points = ax.plot(time_list, point_list, "-", animated=True)[0]

    # draw the plot
    while True:
        data = queue.get()
        if data == "DONE":
            break
        if float(time.time()) >= current_time + int(x_limit):
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
        print("AVG: " + str(numpy.average(point_list)))

    if dir_fig is not None and file_fig is not None:
        # concatenate figure directory and file name
        save_fig = str(dir_fig) + "/" + str(file_fig)
        # ensure the directory exists and create it if it does not
        Path(str(dir_fig)).mkdir(parents=True, exist_ok=True)
        # save and close the figure
        fig.savefig(save_fig)
    plt.close("all")
