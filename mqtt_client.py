import argparse
import os
import numpy as np
import speech_recognition as sr

from datetime import datetime, timedelta
from queue import Queue
from time import sleep
from sys import platform

import random
import time

from flask import json
from paho.mqtt import client as mqtt_client

broker = '192.168.200.250'
port = 1883
topic = "llava"
# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'


# username = 'emqx'
# password = 'public'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
