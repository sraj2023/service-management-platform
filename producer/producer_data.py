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
TOPIC_NAME = 'order_placed'
def generate_unique_number():
    # Generate a unique 2-digit number
    return random.sample(range(100), 1)[0]
def producer_data():
    customer_ids = ['101', '102', '103', '104', '105', '106']
    options= ['house cleaning','house painting','carpenter','plumbing','electrician']
    contractor_ids = ['2201', '2202', '2203', '2204', '2205','2206']
    data= {
        'job_id': generate_unique_number(),
        'customer_id': random.choice(customer_ids),
        'service_option': random.choice(options),
        'contractor_id': random.choice(contractor_ids),
        'location': dummy.address(),
        'price_quoted': random.randint(1, 2000)
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