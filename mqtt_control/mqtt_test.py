import paho.mqtt.client as mqtt #import the client1
import configparser
import random
import time

def on_message(client, userdata, message):
    ''' Call back function that is processed by the loop function
        of the main thread and triggered when the connection
        is established.

        Args:
            Refer to standard paho-mqtt documentation
    '''
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

def mqtt_client(instance_name, address, topic):
    ''' Configures a basic publisher.

        Args:
            instance_name: Name of the mqtt client instance
            address: IP address of the broker
            topic: Topic to which the client publishes 
    '''
    print("Creating new instance")
    client = mqtt.Client(instance_name) #create new instance
    client.on_message=on_message #attach function to callback
    print("Connecting to broker")
    client.connect(broker_address) #connect to broker
    client.loop_start() #start the loop
    print("Subscribing to topic",topic)
    client.subscribe(topic)
    return client
 

if __name__ == '__main__':
    # load mqtt settings from settings.ini
    config = configparser.ConfigParser()
    config.read('settings.ini')
    config_mqtt = config["mqtt_client"]    
    # retrieve the relevant settings 
    broker_address=str(config_mqtt["address"])
    topic = str(config_mqtt["topic"])

    # create an mqtt client instance
    client = mqtt_client("P1", broker_address, topic)

    # estimate how long to generate data
    config_plot = config["plot"]
    gen_limit = float(config_plot["x_limit"]) * 1.5
    
    # generate an publish sample data 
    for i in range(0, int(gen_limit)):
        time.sleep(0.8)
        n = random.random()
        print("Publishing message to topic","smartpi/P1")
        client.publish(topic, n*150*pow(-1,i))

    # wait and stop loop
    time.sleep(4) 
    client.loop_stop() 
