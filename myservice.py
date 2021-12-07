import pywin
import paho.mqtt.client as mqtt
import platform
import uuid
import json


def on_connect(client, userdata, flags, rc):
    client.subscribe("cslab/pc1/on")
    client.subscribe("cslab/pc1/off")

    data = {'status':'online','uuid':hex(uuid.getnode()),'name':platform.node()}
 
    client.publish("cslab/pc1/status",payload=json.dumps(data,indent=3), qos=0, retain=True)

#    client.publish("cslab/pc1/status",payload="Online", qos=0, retain=True)
   

def on_message(client, userdata, msg):
    if(msg.topic == "cslab/pc1/on"):
        print("Internet on ")
        print(msg.payload)
    elif(msg.topic == "cslab/pc1/off"):
        print("Internet off ")
        print(msg.payload)
    else:
        print("Wrong Command")

print(hex(uuid.getnode()));
print (platform.node())
print (platform.machine());


client = mqtt.Client()
data = {'status':'offline','uuid':hex(uuid.getnode()),'name':platform.node()}
client.will_set("cslab/pc1/status", payload=json.dumps(data,indent=3), qos=0, retain=True)

client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost",1883,60)
client.loop_forever();
