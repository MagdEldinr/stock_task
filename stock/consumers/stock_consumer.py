import os

import django

# initialize django setup
basedir = os.path.abspath(".")
from sys import path

path.append(basedir)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thndr.settings")
django.setup()

import paho.mqtt.client as mqtt
from django.conf import settings
from stock.serializers import StockSerializer
from stock.models import Stock
import json

def on_connect(client, userdata, flags, rc):
    client.subscribe("thndr-trading")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    payload = json.loads(msg.payload)
    try:
        instance = Stock.objects.get(stock_id=payload.get("stock_id"))
        serializer = StockSerializer(instance=instance, data=payload, partial=True)
    except Stock.DoesNotExist:
        serializer = StockSerializer(data=payload)

    serializer.is_valid(raise_exception=True)
    serializer.save()

client = mqtt.Client("stock_client")
client.on_connect = on_connect
client.on_message = on_message
client.connect(settings.BROKER_HOST)
client.loop_forever()
