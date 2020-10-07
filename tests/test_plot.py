import configparser
from multiprocessing import Queue

from smartpi.plot.live_plt import live_plt


def test_plot():
    # load the configuration settings
    config = configparser.ConfigParser()
    config.read("settings.ini")
    config_plot = config["plot"]

    print("Loaded the configurations")

    # setup the live plot
    title = str(config_plot["title"])
    y_top_limit = int(config_plot["y_top_limit"])
    y_bottom_limit = int(config_plot["y_bottom_limit"])
    title = str(config_plot["title"])
    x_label = str(config_plot["y_label"])
    y_label = str(config_plot["x_label"])
    x_limit = 1

    print("Setup the live plot")

    queue = Queue()
    queue.put("DONE")

    print("Setup the queue and entered the termination condition")

    live_plt(
        queue, title, x_limit, y_top_limit, y_bottom_limit, x_label, y_label, None, None
    )
    print("Setup and run successfully live_plt")
