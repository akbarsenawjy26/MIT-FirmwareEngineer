from flask import Flask, jsonify
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Konfigurasi InfluxDB
influxdb_url = "http://localhost:8086"
influxdb_token = "7rApYAJ4k8vyzYZcqVXvsXFw7HGd-uPmTzTN1aVL9dUrQKMeQJKFhxh2mpL-2LrfvkQnE-S4wqVckFeeOxN5sQ=="
influxdb_org = "MIT"
influxdb_bucket = "mqtt_logging"

# Inisialisasi klien InfluxDB
client = InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)

# Fungsi untuk melakukan query data tegangan (voltage) dari InfluxDB
def query_voltage_data():
    try:
        # Mendapatkan instance query API
        query_api = client.query_api()

        # Membuat query untuk membaca data tegangan (voltage) dari 15 menit yang lalu
        query = f'from(bucket:"{influxdb_bucket}") |> range(start: -15m) |> filter(fn: (r) => r["_measurement"] == "voltage") |> filter(fn: (r) => r["_field"] == "value")'
        
        # Menjalankan query
        result = query_api.query(query=query)

        # Menyiapkan data response dari query
        data = []
        for table in result:
            for row in table.records:
                data.append(row.values)

        return data

    except Exception as e:
        return {"error": str(e)}

# Fungsi untuk melakukan query data arus (current) dari InfluxDB
def query_current_data():
    try:
        # Mendapatkan instance query API
        query_api = client.query_api()

        # Membuat query untuk membaca data arus (current) dari 15 menit yang lalu
        query = f'from(bucket:"{influxdb_bucket}") |> range(start: -15m) |> filter(fn: (r) => r["_measurement"] == "current") |> filter(fn: (r) => r["_field"] == "value")'
        
        # Menjalankan query
        result = query_api.query(query=query)

        # Menyiapkan data response dari query
        data = []
        for table in result:
            for row in table.records:
                data.append(row.values)

        return data

    except Exception as e:
        return {"error": str(e)}

# Endpoint API untuk mendapatkan data tegangan (voltage) dari InfluxDB
@app.route('/api/voltage', methods=['GET'])
def get_voltage():
    # Panggil fungsi untuk melakukan query data tegangan (voltage) dari InfluxDB
    data = query_voltage_data()

    # Kembalikan response dalam format JSON
    return jsonify(data)

# Endpoint API untuk mendapatkan data arus (current) dari InfluxDB
@app.route('/api/current', methods=['GET'])
def get_current():
    # Panggil fungsi untuk melakukan query data arus (current) dari InfluxDB
    data = query_current_data()

    # Kembalikan response dalam format JSON
    return jsonify(data)

# Menjalankan aplikasi Flask
if __name__ == '__main__':
    app.run(debug=True)
