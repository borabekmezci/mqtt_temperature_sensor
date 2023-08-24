import paho.mqtt.client as mqtt
import time

mqttBroker = 'broker.emqx.io'
port = '1883'
#List of topics to subscribe to (using a wildcard)
topics = 'home/groundfloor/#'

def on_message(client , userdata , message):
    print("Received mesage : Temperature is ", str(message.payload.decode("UTF-8")) + ". Topic is " + topics)

client = mqtt.Client("Smartphone")
print ("Client is " + str((client._client_id.decode("utf-8"))))
client.connect (mqttBroker)

client.loop_start()
client.subscribe(topics)
client.on_message = on_message

time.sleep(120)

client.loop_stop()