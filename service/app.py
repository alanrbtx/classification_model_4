from flask import Flask, request
import pickle
from skimage import io
from skimage.transform import resize
from skimage.color import rgb2gray
import logging
from dotenv import load_dotenv
import os
import redis
from db import Database
import hvac
import argparse
from vault import Vault
from producer import KafkaProducer

parser = argparse.ArgumentParser()
parser.add_argument("--token", default="none")
parser.add_argument("--vault_addr", default="none")

load_dotenv()

host_model = os.getenv("HOST_EXPERIMENTS_PATH")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pkl_path = '/classification/neigh.pkl'
def load_pickle(file_path):
    neigh = pickle.load(open(file_path, 'rb'))
    logger.info("Модель успешно загружена из %s", file_path)
    return neigh

def predict_image(file_path):
    image = io.imread(file_path)
    if len(image.shape) == 4:
        image = image.squeeze(0)
    image = rgb2gray(resize(image, (200,200)))
    image = image.reshape(1, -1)

    neigh = load_pickle(pkl_path)
    res = neigh.predict(image)[0]
    if res == 0:
        print("MODEL PREDICTION: CAT")
        logger.info("Модель предсказала CAT")
        return {"result": "cat"}
    else:
        print("MODEL PREDICTION: DOG")
        logger.info("Модель предсказала DOG")
        return {"result": "dog"}

app = Flask(__name__)

@app.route('/get_test_prediction', methods=['GET'])
def get_test_result():
    res = predict_image("../data/PetImages/Cat/3004.jpg")
    return res


# kafka = Kafka()
@app.route('/get_real_prediction', methods=['POST'])
def get_real_result():

    res = predict_image(request.files["media"])

    namespace = parser.parse_args()

    vault = Vault(namespace.vault_addr, namespace.token)
    read_response = vault.get_secrets()

    password=read_response['data']['data']['PASS']
    host=read_response['data']['data']['HOST']
    port=read_response['data']['data']['PORT']
    kafka_host = read_response['data']['data']['PROD_HOST']

    producer_config = {
        'bootstrap.servers': 'kafka:9092'
    }

    producer = KafkaProducer(producer_config)
    producer.send_message('test_topic', f"Model prediction: {res}")
    logger.info("Result sended by producer")

    db = Database(password, host, port)
    db.connect(res, request)
    
    # kafka.send(res)
    return res

class TestClass():
    def test_load_picke(self):
        assert load_pickle(f'{host_model}/neigh.pkl')

    
if __name__ == '__main__':
    app.run(port=8000, host='0.0.0.0')