import pywin
import paho.mqtt.client as mqtt
import platform
import uuid
import json
import sys


def on_connect(client, userdata, flags, rc):
    client.subscribe("cslab/pc/2/on")
    client.subscribe("cslab/pc/2/off")
    data = {'status':'online','uuid':hex(uuid.getnode()),'name':platform.node()}
    client.publish("cslab/pc/2/status",payload=json.dumps(data,indent=3), qos=0, retain=True)

   

def on_message(client, userdata, msg):
    if(msg.topic == "cslab/pc/2/on"):
        print("Internet on ")
        print(msg.payload)
    elif(msg.topic == "cslab/pc/2/off"):
        print("Internet off ")
        print(msg.payload)
    else:
        print("Wrong Command")

print("Arg:",sys.argv[1]);

print(hex(uuid.getnode()));
print (platform.node())
print (platform.machine());


client = mqtt.Client()
data = {'status':'offline','uuid':hex(uuid.getnode()),'name':platform.node()}
client.will_set("cslab/pc/2/status", payload=json.dumps(data,indent=3), qos=0, retain=True)

client.on_connect = on_connect
client.on_message = on_message

while(True):
    try:
        client.connect("localhost",1883,60)
        print("Connected!")
        break;
    except ConnectionRefusedError:
        print("Trying to Reconnect")

client.loop_forever();
