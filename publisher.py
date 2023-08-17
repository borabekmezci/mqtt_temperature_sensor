import os
import glob
import time
import paho.mqtt.client as mqtt

mqttBroker = 'broker.emqx.io'
port = '1883'
topics = 'temperature'

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')



base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


def read_temp_raw():
    f = open(device_file , 'r')
    lines =f.readlines()
    f.close()
    return lines



def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES' :
        time.sleep(1)
        lines = read_temp_raw()

    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string =lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0

        return temp_c

client = mqtt.Client("Temperature Sensor (DS18B20)" , "1")
print("Client is " + str (client._client_id.decode("UTF-8")))
client.connect(mqttBroker)



while True:
        client.publish(topics , read_temp())
        print("Measured temperature value is " + str(read_temp()) + ". Topic is " + topics)
        time.sleep(1)



