from confluent_kafka import Producer,Consumer,KafkaError
from flask import json,jsonify

def publish_message(producer_instance, topic_name, key, value):
    if producer_instance is None:
        print("No producer")
        return
    try:
        key_bytes = bytes(key, encoding='utf-8')
        value_bytes = bytes(value, encoding='utf-8')
        producer_instance.produce(topic_name, key=key_bytes, value=value_bytes)
        producer_instance.flush(5)
        print('Message published to kafka successfully.')
    except Exception as ex:
        print('Exception in publishing to kafka message')
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

def connect_kafka_consumer(topic_name,group):
    _consumer = None
    settings = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': group,
    'client.id': 'client-1',
    'enable.auto.commit': True,
    'session.timeout.ms': 6000,
    'default.topic.config': {'auto.offset.reset': 'smallest'}
    }
    try:
        _consumer = Consumer(settings)
        _consumer.subscribe([topic_name])
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        return _consumer


def consume_messages(consumer):
    if consumer is None:
        print("No consumer")
        return
    msgs = consumer.consume(num_messages=1000000,timeout=5)
    json_data_list = []
    for msg in msgs:
        print(msg.value()) 
        my_json = msg.value().decode("utf-8").replace("'", '"')
        data = json.loads(my_json)
        json_data_list.append(data)
    
    consumer.close()

    return jsonify(new_comments=json_data_list)

def poll_messages_loop(c):
    try:
        while True:
            msg = c.poll(0.1)
            if msg is None:
                continue
            elif not msg.error():
                print('Received message: {0}'.format(msg.value()))
            elif msg.error().code() == KafkaError._PARTITION_EOF:
                print('End of partition reached {0}/{1}'
                    .format(msg.topic(), msg.partition()))
            else:
                print('Error occured: {0}'.format(msg.error().str()))

    except KeyboardInterrupt:
        pass

    finally:
        c.close()