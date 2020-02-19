from confluent_kafka import Consumer, KafkaError
import time 

c = Consumer({
    'bootstrap.servers': 'localhost:29092',
    'group.id': 'mygroup',
    'auto.offset.reset': 'latest'
})

subs = []
n = "Yet to execute command"
print("\nSelect subscription(s)!\nThen enter 'Run' to start program!") 
print("""0: All
1: SVC
2: SVO
3: SVOC
4: IODO""")

while n.lower() != "RUN".lower():
    n = input("> ")
    if n == "0" and len(subs) == 0:
      subs.append("svc")
      subs.append("svo")
      subs.append("svoc")
      subs.append("iodo")
      print("You subscribed to all topics") 
      break
    if n == "1" and "svc" not in subs:
      subs.append("svc")
      print("You subscribed to SVC")
      
    if n == "2" and "svo" not in subs:
      subs.append("svo")
      print("You subscribed to SVO")
      
    if n == "3" and "svoc" not in subs:
      subs.append("svoc")
      print("You subscribed to SVOC")
      
    if n == "4" and "iodo" not in subs:
      subs.append("iodo")
      print("You subscribed to IODO")
      
      
c.subscribe(subs)

seconds = time.time()

# --config retention.ms=1000
# "/usr/bin/kafka-topics", "--zookeeper", "zookeeper-1:2181", "--delete", "--topic", topic_name

while True:
    msg = c.poll(1.0)
    if time.time() < seconds + 6:
        continue
    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    print('{}'.format(msg.value().decode('utf-8')))

c.close()