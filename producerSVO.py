from confluent_kafka import Producer
from random import choice
from time import sleep
import json

"""
don't forget to create a topic to post to!
    kafka-topics --bootstrap-server localhost:29092 --create --topic svo --partitions 4 --replication-factor 1

Initialize your Python environment!
    python3 -m venv .venv
    source .venv/bin/activate
"""

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

#declare producer
p = Producer({'bootstrap.servers': 'localhost:29092'})

#initialize lists to append to
lstSubject = []
lstVerb = []
lstObject = []

#read in txt files
with open('subject.txt') as txtSubject:
    for subject in txtSubject:
        lstSubject.append(subject.replace('\n',''))

with open('verb.txt') as txtVerb:
    for verb in txtVerb:
        lstVerb.append(verb.replace('\n',''))

with open('object.txt') as txtObject:
    for varObject in txtObject:
        lstObject.append(varObject.replace('\n',''))

#produce random sentences until you stop the stream and post them to the topic svo
while True:
    randSVO = f'SVO: {choice(lstSubject)} {choice(lstVerb)} {choice(lstObject)}'
    p.poll(0)
    p.produce('svo', randSVO.encode('utf-8'), callback=delivery_report)
    #wait 3 seconds between producing sentences
    sleep(5)

#idk what this does but I know it needs to exist
p.flush()