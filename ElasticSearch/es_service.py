from elasticsearch import Elasticsearch
from confluent_kafka import Consumer
from Kafka.kafka_service import connect_kafka_consumer
import threading

def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print('Connected')
    else:
        print('Could not connect!')
    return _es

def store_data(data):
    res = es.index(index='bSocial',doc_type='employee',id=1,body=e1)

def poll_messages_loop(c):
    try:
        while True:
            msg = c.poll(0.1)
            if msg is None:
                continue
            elif not msg.error():
                print('Received message in {0} : {1}'
                    .format(msg.topic(), msg.value()))
            elif msg.error().code() == KafkaError._PARTITION_EOF:
                print('End of partition reached {0}/{1}'
                    .format(msg.topic(), msg.partition()))
            else:
                print('Error occured: {0}'.format(msg.error().str()))

    except KeyboardInterrupt:
        pass

    finally:
        c.close()

def start_consuming_thread(topic):
    c = connect_kafka_consumer(topic,"es")
    th = threading.Thread(target=poll_messages_loop, args=(c, ))
    th.start()
    return th


