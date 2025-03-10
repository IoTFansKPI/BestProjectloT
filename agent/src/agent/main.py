from paho.mqtt import client as mqtt_client
import time
import config
from schema.aggregated_data_schema import AggregatedDataSchema
from file_datasource import FileDatasource


def connect_mqtt():
    """Manually connect to MQTT broker"""
    print(
        f'Attempting to connect to MQTT broker at {config.MQTT_BROKER_HOST}:{config.MQTT_BROKER_PORT}'
    )

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(
                f'Connected to MQTT Broker at {config.MQTT_BROKER_HOST}:{config.MQTT_BROKER_PORT}'
            )
        else:
            print(f'Failed to connect to MQTT Broker. Return code: {rc}')
            exit(rc)

    client = mqtt_client.Client()
    client.on_connect = on_connect
    try:
        client.connect(config.MQTT_BROKER_HOST, config.MQTT_BROKER_PORT)
    except Exception as e:
        print(f'Connection failed: {e}')
        exit(1)

    client.loop_start()
    return client


def publish(client, topic, datasource, delay):
    """Publish data to MQTT topic"""
    datasource.startReading()
    while True:
        try:
            time.sleep(delay)
            data = datasource.read()
            msg = AggregatedDataSchema().dumps(data)
            result = client.publish(topic, msg)
            if result.rc == 0:
                print(f'Sent `{msg}` to topic `{topic}`')
            else:
                print(f'Failed to send message to topic {topic}')
        except KeyboardInterrupt:
            print('Publishing stopped.')
            break
        except Exception as e:
            print(f'Error during publishing: {e}')


def run():
    client = connect_mqtt()
    datasource = FileDatasource('accelerometer.csv', 'gps.csv')
    publish(client, config.MQTT_TOPIC, datasource, config.DELAY)


if __name__ == '__main__':
    run()
