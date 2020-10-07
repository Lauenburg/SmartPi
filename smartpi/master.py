import configparser
import time
from multiprocessing import Process
from multiprocessing import Queue

from smartpi.mqtt_control.subscribe import mqtt_main
from smartpi.plot.live_plt import live_plt


def subscribe_and_live_plot(
    broker_address,
    port,
    topic,
    dir_log,
    file_log,
    dir_fig,
    file_fig,
    x_limit,
    time_stop,
    y_top_limit,
    y_bottom_limit,
    title,
    x_label,
    y_label,
):
    # create a queue instance for the data exchange
    queue = Queue()

    # configure and start the mqtt service
    subscriber = Process(
        target=mqtt_main,
        args=(
            broker_address,
            port,
            topic,
            queue,
            x_limit,
            time_stop,
            dir_log,
            file_log,
        ),
    )
    subscriber.daemon = True
    subscriber.start()

    live_plot = Process(
        target=live_plt,
        args=(
            queue,
            title,
            x_limit,
            y_top_limit,
            y_bottom_limit,
            x_label,
            y_label,
            dir_fig,
            file_fig,
        ),
    )

    # start the plotting thread
    live_plot.start()

    # Wait for the reader to finish
    subscriber.join()

    # Wait for the plotter to finish
    live_plot.join()

    time.sleep(1)


if __name__ == "__main__":
    # load the configuration settings
    config = configparser.ConfigParser()
    config.read("settings.ini")
    config_mqtt = config["mqtt_client"]
    config_logs = config["logs"]
    config_plot = config["plot"]

    # setup the mqtt broker configurations
    broker_address = config_mqtt["address"]
    port = int(config_mqtt["port"])
    topic = str(config_mqtt["topic"])
    # time at which the live plot stops plotting
    x_limit = float(config_plot["x_limit"])
    # boolean that tells the mqtt thread to stop
    # when the live plot stops e.i. when x_limit is reached
    time_stop = bool(config_mqtt["stop_broker_at_x_limit"])
    # directory and file where to save the plot.
    dir_log = str(config_logs["dir_log"])
    file_log = str(config_logs["file_log"])

    # setup the live plot
    title = str(config_plot["title"])
    y_top_limit = int(config_plot["y_top_limit"])
    y_bottom_limit = int(config_plot["y_bottom_limit"])
    title = str(config_plot["title"])
    x_label = str(config_plot["y_label"])
    y_label = str(config_plot["x_label"])
    # directory and file where to save the plot.
    dir_fig = str(config_logs["dir_fig"])
    file_fig = str(config_logs["file_fig"])

    subscribe_and_live_plot(
        broker_address,
        port,
        topic,
        dir_log,
        file_log,
        dir_fig,
        file_fig,
        x_limit,
        time_stop,
        y_top_limit,
        y_bottom_limit,
        title,
        x_label,
        y_label,
    )
