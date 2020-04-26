from confluent_kafka import Producer,Consumer,KafkaError
from flask import json,jsonify

def publish_message(producer_instance, topic_name, key, value):
    try:
        key_bytes = bytes(key, encoding='utf-8')
        value_bytes = bytes(value, encoding='utf-8')
        producer_instance.produce(topic_name, key=key_bytes, value=value_bytes)
        producer_instance.flush(30)
        print('Message published successfully.')
    except Exception as ex:
        print('Exception in publishing message')
        print(str(ex))


def connect_kafka_producer():
    _producer = None
    try:
        _producer = Producer({'bootstrap.servers': 'localhost:9092'})
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        return _producer


def consume_messages():
    settings = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'mygroup',
    'client.id': 'client-1',
    'enable.auto.commit': True,
    'session.timeout.ms': 6000,
    'default.topic.config': {'auto.offset.reset': 'smallest'}
    }
    c = Consumer(settings)
    c.subscribe(['comments'])
    msgs = c.consume(num_messages=1000000,timeout=5)

    json_data_list = []
    for msg in msgs:
        print(msg.value()) 
        my_json = msg.value().decode("utf-8").replace("'", '"')
        data = json.loads(my_json)
        json_data_list.append(data)
    
    if c is not None:
        c.close()

    return jsonify(json_data_list)
