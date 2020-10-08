# SmartPi

This repo is originally based on the SmartPi 2.0 expansion module, which adds interfaces for voltage measurement and non-contact current measurement to the Raspberry Pi, making it a fully-fledged Smart Meter. This project processes and visualizes the data collected by the SmartPi. Although, it can be used for any type of numerical data stream published to an MQTT broker by simply modifying the ```settings.init``` file. 
The script mqtt_control/subscriber.py processes the incoming data and passes it to plot/live_plt.py in an asynchronies way for live visualization.
The script master.py orchestrates both scrips running them as separated processes using pythons multiprocessing library.

### Python dependencies

Dependency management in python is handled via poetry. To install poetry make sure you aren't in a virtual environment so that poetry is available system-wide and run:

```pip3 install poetry```

After activating your environment install all required python dependencies by running:

```poetry install```

### Pre-commit hooks

Install the pre-commit hooks:

```poetry run pre-commit install```

### MQTT

The application uses the MQTT protocol. 
To subscribe to an existing service you can simply edit the settings.ini file.
If you want to run the application locally you have to install and start an MQTT broker.

E.g. on MacOS with brew run:

- Install broker

```brew install mosquitto```

- Start broker

```brew services start mosquitto```

- Monitore the broker (address=127.0.0.1, port=1883,topic=# (all topics))

```mosquitto_sub -v -h 127.0.0.1 -p 1883 -t '#'```

### master.py

To run the application first adapt ```settings.ini``` to your requirements and then run:

```poetry run python smartpi/master.py```

If you simply want to test the application using dummy data you can run:

```poetry run python smartpi/master.py test_run```

By passing the command line argument ```test_run```, master.py will in addition start up the mqtt_control/publisher.py script that publishes dummy data to the broker.
