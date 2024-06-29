from confluent_kafka import Producer

class KafkaProducer:
    def __init__(self, config):
        self.producer = Producer(config)

    def delivery_report(err, msg):
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

    def send_message(self, topic, message):
        self.producer.produce(topic, value=message)
        self.producer.flush()