import paho.mqtt.client as mqtt
from pathlib import Path
import time


class MqttSubscriber(mqtt.Client):
    ''' Configuration of the mqtt client and it call back
        functions.
    '''
    def __init__(self, topic, queue, **kwargs):
        super(MqttSubscriber, self).__init__(**kwargs)
        self.topic = topic
        self.connected = False
        self.queue = queue


    def on_connect(self, client, userdata, flags, rc):
        ''' Call back function that is processed by the loop function
            of the main thread and triggered when the connection
            is established. 
        
            Args:
                Refer to standard paho-mqtt documentation 
        '''

        print("Connected with result code " + str(rc))
        if rc == 0:
            print("Connected to broker")

            self.connected = True  # Signal connection
            self.subscribe(self.topic)

        else:
            print("Connection failed")


    def on_message(self, client, userdata, message):
        ''' Call back function that is processed by the loop function
            of the main thread and triggered when ever there is the 
            message in the message buffer. 
        
            Args:
                Refer to standard paho-mqtt documentation 
        '''
        print("Message received for topic \"" + message.topic + "\" : " + message.payload.decode("utf-8"))
        # write payload to log file and put it in to the queue
        with open(save_log, 'a+') as f:
            f.write(message.payload.decode("utf-8") + "\n")
            #if message.topic.split('/')[-1] == 'P1' or message.topic.split('/')[-1] == 'F1' or message.topic.split('/')[-1] == 'I1':
            #    self.queue.put({message.topic.split('/')[-1]:message.payload.decode("utf-8")})
            self.queue.put(message.payload.decode("utf-8"))


def mqtt_main(broker_address, port, topic, queue, x_limit, stop_limit, dir_log, file_log):
    ''' Handles the connection to the broker as well as the 
        processing of the messages.

        Args:
            broker_address: IP-Address of the broker
            port: Port of the broker
            topic: Topic to which to subscribe
            queue: Message buffer for the asynchronous exchange 
            stop_limit: Boolean telling mqtt to stop when x_limit is reach.
                        At x_limit the live plot stop plotting.
            dir_log: Directory where the data logs are to be saved.
            file_log: File name of the data log.

    '''
    # make the log file location excisable for the on_message call back function 
    global save_log
    # concatenate the log directory with the log file name
    save_log = str(dir_log) +"/"+ str(file_log)
    # ensure that the directory exists
    Path(dir_log).mkdir(parents=True, exist_ok=True)

    # setup the topic and the call back functions
    mqtt_sub = MqttSubscriber(topic, queue)
    mqtt_sub.on_connect = mqtt_sub.on_connect
    mqtt_sub.on_message = mqtt_sub.on_message
    # connect to broker
    mqtt_sub.connect(broker_address, port=port)  
    # start the loop
    mqtt_sub.loop_start()  

    # save start time to know when to stop
    start_time = time.time()
    
    # wait for connection
    while not mqtt_sub.connected:  
        time.sleep(0.1)

    # run loop till keyboard interrupt or until x_limit is reached
    try:
        while True:
            time.sleep(1)
            if (float(time.time()) >= float(start_time)+float(x_limit)+float(5) 
                and stop_limit):
                break
    except KeyboardInterrupt:
        print("exiting")
        mqtt_sub.disconnect()

    queue.put('DONE')


if __name__ == '__main__':
    print("Nothing is done here. -> Run \'python master.py\'")
