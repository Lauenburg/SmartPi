import numpy
import time
import configparser
from multiprocessing import Process, Queue
from mqtt_control.subscribe import mqtt_main
import matplotlib.pyplot as plt
from plot.live_plt import live_plt

if __name__ == '__main__':
    # load the configuration settings 
    config = configparser.ConfigParser() 
    config.read('settings.ini')
    config_mqtt = config["mqtt_client"]
    config_logs = config["logs"]

    # setup the mqtt broker configurations
    broker_address = config_mqtt["address"]  
    port = int(config_mqtt["port"]) 
    topic = str(config_mqtt["topic"]) 

    pqueue = Queue() 

    # configure and start the mqtt service
    subscriber = Process(target=mqtt_main, args=(broker_address, port, topic, pqueue))
    subscriber.daemon = True
    subscriber.start()  
    # start the plot
    live_plt(pqueue)
    # Wait for the reader to finish
    subscriber.join()  
    #result_cubes = pool.apply_async(live_plt, config_logs["dir_log"]) 
    time.sleep(1)
