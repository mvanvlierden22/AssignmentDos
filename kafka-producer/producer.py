from kafka import KafkaProducer
import json
from bson import json_util
import time


def kafka_python_producer_sync(producer, msg, topic):
    producer.send(topic, json.dumps(msg, default=json_util.default).encode("utf-8"))
    print(msg)
    producer.flush(timeout=60)


def success(metadata):
    print(metadata.topic)


def error(exception):
    print(exception)


def kafka_python_producer_async(producer, msg, topic):
    producer.send(
        topic, json.dumps(msg, default=json_util.default).encode("utf-8")
    ).add_callback(success).add_errback(error)
    producer.flush()


if __name__ == "__main__":
    producer = KafkaProducer(
        bootstrap_servers="127.0.0.1:9092"
    )  # use your VM's external IP Here!
    with open(
        "/home/jads/DataEngineering/AssignmentDos/schiphol_api_connections/flight_data/2023-10-01.json"
    ) as f:  # change this path to the path in your laptop
        flights = json.load(f)

    for flight in flights:
        kafka_python_producer_sync(producer, flight, "flights")
        time.sleep(5)

    f.close()
