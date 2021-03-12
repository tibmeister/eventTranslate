#!/usr/bin/python3

import paho.mqtt.client as mqtt
import json
import time

localBroker = "localhost"
subscribeTopic = "zoneminder/1/#"
remoteBroker = "remote_broker"
hbTopic = "homebridge/front_yard/motion"

## Create callbacks ##
def on_connect(client, userdata, flags, rc):
    if rc==0:

        # A little debugging is good for the soul
        print("Client connected: ", client.client_name)
        print("Connected with result code {0}".format(str(rc)))

        # We've got a good return code, so flip the connected_flag so we stop the loop
        client.connected_flag=True

        # Check which client we've called, and do the appropriate action
        if client.client_name == "localClient":
            # Verbosity anyone
            print("Subscribing to topic ", subscribeTopic)
            # Subscribe to the topic
            client.subscribe(subscribeTopic)
    else:
        # More verbosity
        print("Connection failed with result code {0}".format(str(rc)))
        # Things went sideways, so flip the flag so the program will self-terminate
        client.bad_connection_flag=True

def on_message(client, userdata, message):
    time.sleep(1)
    # Some verbosity
    print("received message =",str(message.payload.decode("utf-8")))

    # Deserialize the JSON data
    json_data = json.loads(str(message.payload.decode("utf-8")))

    # Just some debugging junk
    sTopic = "zoneminder/%s/%s/eventtype" % (json_data["monitor"], json_data["state"])
    print("Topic ", sTopic)
    print("Message ", json_data["eventtype"])

    # check the eventtype and publish the proper message
    if json_data["eventtype"] == "event_start":
        rclient.publish(hbTopic,payload="ON", qos=1)

    if json_data["eventtype"] == "event_end":
        rclient.publish(hbTopic,payload="OFF",qos=1)

def on_subscribe(client, userdata, mid, granted_qos):
    # Just for debugging
    print("Client ", client.client_name, " is subscribed to ", str(mid), " ", str(granted_qos))

def on_disconnect(client, userdata, rc):
    # More debugging
    print("Disconnected with return code = ",rc)

def on_publish(client, userdata, result):
    # You guessed it, just for debugging
    print("Published to ", client.client_name, " with result ", result)

## Start of main code ##

# Create a flag in the class to use later
mqtt.Client.connected_flag=False
mqtt.Client.bad_connection_flag=False

# Create an attribute to keep track of which client we are working with in the callbacks
mqtt.Client.client_name=""

# Create the local client
lclient = mqtt.Client("localClient")
lclient.client_name = "localClient"

# Setup the callbacks
lclient.on_message = on_message
lclient.on_connect = on_connect
lclient.on_subscribe = on_subscribe
lclient.on_disconnect = on_disconnect

# Connect and start the loop
lclient.connect(localBroker)
lclient.loop_start()

# Wait in the loop for the connection
while not lclient.connected_flag and not lclient.bad_connection_flag:
    print("Waiting for connection to ",localBroker)
    time.sleep(1)

# If we can't connect to the local client, then die
if lclient.bad_connection_flag:
    lclient.loop_stop()
    sys.exit()

# Create the remote client
rclient = mqtt.Client("remoteClient")
rclient.client_name="remoteClient"

# Setup the callbacks
rclient.on_connect = on_connect
rclient.on_publish = on_publish
lclient.on_disconnect = on_disconnect

# Connect and start the loop
rclient.connect(remoteBroker)
rclient.loop_start()

# Wait in the loop for the connection
while not rclient.connected_flag and not lclient.bad_connection_flag:
    print("Waiting for connection to ",remoteBroker)
    time.sleep(1)

# If we can't connect to the remote, then die
if rclient.bad_connection_flag:
    rclient.loop_stop()
    sys.exit()

# Start an infinite wait loop
while lclient.connected_flag and rclient.connected_flag:
    time.sleep(1)
