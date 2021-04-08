"""
Python MQTT Subscription client - No Username/Password
Thomas Varnish (https://github.com/tvarnish), (https://www.instructables.com/member/Tango172)
Written for my Instructable - "How to use MQTT with the Raspberry Pi and ESP8266"
"""
import paho.mqtt.client as mqtt
import datetime
import json

# Don't forget to change the variables for the MQTT broker!
mqtt_topic = "room1"
mqtt_topic2 = "room2"
mqtt_broker_ip = "192.168.137.10"   #ip address to connect to raspberry pi basically the ip address of it
now = datetime.datetime.now()
client = mqtt.Client()

# These functions handle what happens when the MQTT client connects
# to the broker, and what happens then the topic receives a message
def on_connect(client, userdata, flags, rc):
    # rc is the error code returned when connecting to the broker
    print ("Connected!", str(rc))
    
    # Once the client has connected to the broker, subscribe to the topic
    client.subscribe(mqtt_topic)
    client.subscribe(mqtt_topic2)
    
def on_message(client, userdata, msg):
    # This function is called everytime the topic is published to.
    # If you want to check each message, and do something depending on
    # the content, the code to do this should be run in this function
    
    print ("Topic: ", msg.topic + "\nMessage: " + str(msg.payload))
    if msg.topic == "room1":
        txt_file = open("data.txt","a")
        txt_file.writelines(msg.topic + " : " + str(msg.payload) + " " + str(now.hour)+ " " + str(now.minute)+ " " + str(now.second) +"\n")
        createjson()
    elif msg.topic == "room2":
        txt_file1 = open("data2.txt","a")
        txt_file1.writelines(msg.topic + " : " + str(msg.payload) + " " + str(now.hour)+ " " + str(now.minute)+ " " + str(now.second) +"\n")
        createjson2()
    
    # The message itself is stored in the msg variable
    # and details about who sent it are stored in userdata

def remove_stuff(x):
    string = x.replace("(","").replace(")","").replace(",","").replace(" ","").replace("'","")   #remove unwanted stuff
    return string

def createjson():
    d = {"records":[]}
    now = datetime.datetime.now()
    with open("data.txt","r") as file:
        #lines = f.read().splitlines()
        for line in file:
            edit = line.split(" ")
            x = edit[-6]
            xx = edit[-5]
            xxx = edit[-4]
            
            count = remove_stuff(x)
            temp = remove_stuff(xx)
            humidity = remove_stuff(xxx)
            
            #print(count)
            #print(temp)
            #print(humidity)
            d["records"].append({"People": int(count),
                                 "Temperature": float(temp),
                                 "Humidity": float(humidity),
                                 "Time":str(now.hour)+":"+str(now.minute)+":"+str(now.second)})
                                 
    out_file = open("roomA1.json", "w")
    json.dump(d, out_file, indent = 4)
    out_file.close()

def createjson2():
    d = {"records":[]}
    now = datetime.datetime.now()
    with open("data2.txt","r") as file:
        #lines = f.read().splitlines()
        for line in file:
            edit = line.split(" ")
            x = edit[-6]
            xx = edit[-5]
            xxx = edit[-4]
            
            count = remove_stuff(x)
            temp = remove_stuff(xx)
            humidity = remove_stuff(xxx)
            
            #print(count)
            #print(temp)
            #print(humidity)
            d["records"].append({"People": int(count),
                                 "Temperature": float(temp),
                                 "Humidity": float(humidity),
                                 "Time":str(now.hour)+":"+str(now.minute)+":"+str(now.second)})
                                 
    out_file = open("roomA2.json", "w")
    json.dump(d, out_file, indent = 4)
    out_file.close()

# Here, we are telling the client which functions are to be run
# on connecting, and on receiving a message
client.on_connect = on_connect
client.on_message = on_message

# Once everything has been set up, we can (finally) connect to the broker
# 1883 is the listener port that the MQTT broker is using
client.connect(mqtt_broker_ip, 1883)

# Once we have told the client to connect, let the client object run itself
client.loop_forever()
client.disconnect()
