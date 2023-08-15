import time
import random
import json
from confluent_kafka import Producer
from faker import Faker
dummy= Faker()
# Configuration for Confluent Cloud
BOOTSTRAP_SERVERS = ''  # Replace with your Confluent Cloud bootstrap servers
SECURITY_PROTOCOL = 'SASL_SSL'
SASL_MECHANISM = 'PLAIN'
SASL_USERNAME = ''  # Replace with your Confluent Cloud Cluster API key
SASL_PASSWORD = ''  # Replace with your Confluent Cloud Cluster API secret
TOPIC_NAME = 'job_created'
def generate_unique_number():
    # Generate a unique 2-digit number
    return random.sample(range(100), 1)[0]

def producer_data():
    start_date= ['12/08/2023','20/07/2023','31/07/2023','01/08/2023']
    end_date= ['14/08/2023','24/08/2023','30/08/2023']
    data= {
          'job_id': generate_unique_number(),
          'job_start_date': random.choice(start_date),
          'job_end_date': random.choice(end_date),
          'price': random.randint(1, 2000),
          'job_status': 'Yet To Begin'
       }
    return json.dumps(data)
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
def main():
    conf = {
        'bootstrap.servers': BOOTSTRAP_SERVERS,
        'security.protocol': SECURITY_PROTOCOL,
        'sasl.mechanisms': SASL_MECHANISM,
        'sasl.username': SASL_USERNAME,
        'sasl.password': SASL_PASSWORD,
    }
    producer = Producer(conf)
    try:
        while True:
            mock_data = producer_data()
          
            producer.produce(TOPIC_NAME, mock_data.encode('utf-8'), callback=delivery_report)
            producer.flush()
            time.sleep(30)  # Send a new message every 30 second
    except KeyboardInterrupt:
        print("User interrupted, stopping data generation.")
    finally:
        producer.flush()
if __name__ == "__main__":
    main()