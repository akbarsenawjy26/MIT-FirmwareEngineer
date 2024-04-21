import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

globalVoltage = 0.0
globalCurrent = 0

# Konfigurasi MQTT
mqtt_broker = "192.168.1.10"  # Alamat IP atau hostname broker MQTT
mqtt_port = 1883
mqtt_topic_voltage = "home/sensor/voltage"
mqtt_topic_current = "home/sensor/current"
mqtt_topic_alarm_voltage = "home/actuator/alarmVoltage"
mqtt_topic_alarm_current = "home/actuator/alarmCurrent"

# Konfigurasi InfluxDB
influxdb_url = "http://localhost:8086"
influxdb_token = "4inUUjaMJ3VfY4gFxvaou3ru4GOAs2EYvNuw2bl8xaX64YXoKMnWS89B7qqB4NEm5sYosuapEHypRMZiE8yoMQ=="
influxdb_org = "MIT"
influxdb_bucket = "mqtt_logging"

# Inisialisasi klien InfluxDB
influxdb_client = InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)

def transferData():
    return {
        "Voltage": globalVoltage,
        "Current": globalCurrent
    }
    
# Fungsi untuk menulis data ke InfluxDB
def write_to_influxdb(sensor_type, value):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    
    point = Point(sensor_type).field("value", value)
    write_api.write(bucket=influxdb_bucket, record=point)

# Fungsi yang dipanggil saat klien MQTT terhubung ke broker
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    # Subscribe ke topik tegangan (voltage) dan arus (current)
    client.subscribe([(mqtt_topic_voltage, 0), (mqtt_topic_current, 0)])

# Fungsi yang dipanggil saat menerima pesan MQTT
def on_message(client, userdata, msg):
    print("Received message on topic " + msg.topic + ": " + str(msg.payload))

    # Memproses data tegangan (voltage) dan arus (current)
    if msg.topic == mqtt_topic_voltage:
        process_voltage_data(msg.payload.decode())
    elif msg.topic == mqtt_topic_current:
        process_current_data(msg.payload.decode())

# Fungsi untuk memproses data tegangan (voltage)
def process_voltage_data(payload):
    voltage = float(payload)
    globalVoltage = voltage
    print("Voltage received: " + str(voltage))
    # Menulis data tegangan ke InfluxDB
    write_to_influxdb("voltage", voltage)

    # Cek apakah tegangan (voltage) melebihi batas
    if voltage > 230:
        # Mempublikasi pesan "over voltage alarm" ke topik MQTT
        status = "Alarm"
        client.publish(mqtt_topic_alarm_voltage, status)
        # Menulis data tegangan ke InfluxDB
        write_to_influxdb("voltage", voltage)
    else:
        status = "Safe"
        client.publish(mqtt_topic_alarm_voltage, status)


# Fungsi untuk memproses data arus (current)
def process_current_data(payload):
    current = int(payload)
    globalCurrent = current
    print("Current received: " + str(current))
    # Menulis data arus ke InfluxDB
    write_to_influxdb("current", current)

    # Cek apakah arus (current) melebihi batas
    if current > 100:
        # Mempublikasi pesan "over current alarm" ke topik MQTT
        status = "Alarm"
        client.publish(mqtt_topic_alarm_current, status)
        # Menulis data arus ke InfluxDB
        write_to_influxdb("current", current)
        write_to_influxdb("current", current)
    else:
        staus = "Safe"
        client.publish(mqtt_topic_alarm_voltage, "Safe")


# Inisialisasi klien MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

# Daftarkan fungsi callback ke klien MQTT
client.on_connect = on_connect
client.on_message = on_message

# Hubungkan klien MQTT ke broker
client.connect(mqtt_broker, mqtt_port, 60)

# Loop berkelanjutan untuk menangani pesan MQTT
client.loop_forever()
