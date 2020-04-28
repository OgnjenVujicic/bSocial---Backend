from elasticsearch import Elasticsearch
from confluent_kafka import Consumer
from Kafka.kafka_service import connect_kafka_consumer
import threading
import json

def connect_elasticsearch():
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print('Connected')
    else:
        print('Could not connect!')
        _es = None
    return _es

def create_index(es,index_name,mappings):
    if not es.indices.exists(index_name):
            es.indices.create(index=index_name, ignore=400, body=mappings)
            print('Created Index ',index_name)

def store_data(es,data,topic):
    print("storing...")
    my_json = data.decode("utf-8").replace("'", '"')
    data = json.loads(my_json)
    res = es.index(index=topic,body=data)

def poll_messages_loop(c,es):
    try:
        while True:
            msg = c.poll(0.1)
            if msg is None:
                continue
            elif not msg.error():
                print('Received message in {0} : {1}'
                    .format(msg.topic(), msg.value()))
                store_data(es,msg.value(),msg.topic())
            elif msg.error().code() == KafkaError._PARTITION_EOF:
                print('End of partition reached {0}/{1}'
                    .format(msg.topic(), msg.partition()))
            else:
                print('Error occured: {0}'.format(msg.error().str()))

    except KeyboardInterrupt:
        pass

    finally:
        c.close()

def start_consuming_thread(topic,es):
    c = connect_kafka_consumer(topic,"es")
    th = threading.Thread(target=poll_messages_loop, args=(c,es, ))
    th.start()
    return th


