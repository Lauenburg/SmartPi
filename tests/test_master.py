import configparser

from smartpi.master import subscribe_and_live_plot


def test_main():
    # load the configuration settings
    config = configparser.ConfigParser()
    config.read("settings.ini")
    config_mqtt = config["mqtt_client"]
    config_plot = config["plot"]

    # setup the mqtt broker configurations
    broker_address = config_mqtt["address"]
    port = int(config_mqtt["port"])
    topic = str(config_mqtt["topic"])
    # time at which the live plot stops plotting
    x_limit = float(3)
    # boolean that tells the mqtt thread to stop
    # when the live plot stops e.i. when x_limit is reached
    time_stop = True

    # setup the live plot
    title = str(config_plot["title"])
    y_top_limit = int(config_plot["y_top_limit"])
    y_bottom_limit = int(config_plot["y_bottom_limit"])
    title = str(config_plot["title"])
    x_label = str(config_plot["y_label"])
    y_label = str(config_plot["x_label"])

    result = subscribe_and_live_plot(
        broker_address,
        port,
        topic,
        None,
        None,
        None,
        None,
        x_limit,
        time_stop,
        y_top_limit,
        y_bottom_limit,
        title,
        x_label,
        y_label,
    )
    assert result == 0
