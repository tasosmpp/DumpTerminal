import pywin
import paho.mqtt.client as mqtt
import platform
import uuid
import json
import sys

client_id="-1";
broker="null"

def on_connect(client, userdata, flags, rc):

#   Client actuator commands    
    client.subscribe("cslab/pc/"+client_id+"/internet_on")
    client.subscribe("cslab/pc/"+client_id+"/internet_off")
    client.subscribe("cslab/pc/"+client_id+"/restart")
    client.subscribe("cslab/pc/"+client_id+"/shutdown")

#   Publish Client Info to the Brocker
    data = {'status':'online','uuid':hex(uuid.getnode()),'name':platform.node()}
    client.publish("cslab/pc/"+client_id+"/status",payload=json.dumps(data,indent=3), qos=0, retain=True)

   

def on_message(client, userdata, msg):
    if(msg.topic == "cslab/pc/"+client_id+"/internet_on"):
        print("Internet on ")
        print(msg.payload)
    elif(msg.topic == "cslab/pc/"+client_id+"/internet_off"):
        print("Internet off ")
        print(msg.payload)
    elif(msg.topic == "cslab/pc/"+client_id+"/restart"):
        print("Restart")
        print(msg.payload)
    elif(msg.topic == "cslab/pc/"+client_id+"/shutdown"):
        print("Shutting down ")
        print(msg.payload)
    else:
        print("Wrong Command")



def __main__():
    print(hex(uuid.getnode()))
    print (platform.node())
    print (platform.machine())


    client = mqtt.Client()
    data = {'status':'offline','uuid':hex(uuid.getnode()),'name':platform.node()}
    client.will_set("cslab/pc/"+client_id+"/status", payload=json.dumps(data,indent=3), qos=0, retain=True)

    client.on_connect = on_connect
    client.on_message = on_message

    while(True):
        try:
            client.connect(broker,1883,60)
            print("Connected!")
            break
        except ConnectionRefusedError:
            print("Trying to Reconnect")
    
    client.loop_forever();


print("Arg:",sys.argv[1]);
client_id = sys.argv[1];
broker = sys.argv[2];
print(client_id);
__main__()