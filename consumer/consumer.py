from confluent_kafka import Consumer, KafkaException
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


config = {
    'bootstrap.servers': 'kafka:9092',  # Указываем имя сервиса Kafka в Docker Compose сети
    'group.id': 'mygroup',              # Идентификатор группы потребителей
    'auto.offset.reset': 'earliest'     # Начальная точка чтения ('earliest' или 'latest')
}

consumer = Consumer(config)
consumer.subscribe(['test_topic'])

try:
    while True:
        msg = consumer.poll(timeout=1.0)  # ожидание сообщения
        if msg is None:                   # если сообщений нет
            continue
        if msg.error():                   # обработка ошибок
            raise KafkaException(msg.error())
        else:
            # действия с полученным сообщением
            logging.info(f"Received message: {msg.value().decode('utf-8')}")
except KeyboardInterrupt:
    pass
finally:
    consumer.close()