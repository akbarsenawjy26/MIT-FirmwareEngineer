## Panduan Pengaturan Proyek

Panduan ini akan memandu Anda melalui pengaturan komponen yang diperlukan untuk menjalankan proyek.

### 1. Persyaratan
- Python v3
- NodeJS v20

### 2. Firmware
- Konfigurasi Platform.ini:
Pastikan konten berikut ada di dalam `platform.ini`:
```ini lib_deps = knolleary/PubSubClient@^2.8```

- Konfigurasi WiFi:
    const char* ssid = "TMU"; // Ganti dengan SSID Anda
    const char* password = "BambangDjaja"; // Ganti dengan Password Anda
- Konfigurasi MQTT:
    const char* mqtt_server = "192.168.137.1"; // Ganti dengan IP Localhost Anda
- Unggah Firmware ke ESP32


### 3. Menjalankan Docker-Compose
- Buka terminal di vscode:
    - docker-compose up -d
    - Pastikan eksekusi berhasil.
![Teks Alternatif](https://github.com/akbarsenawjy26/MIT-FirmwareEngineer/blob/main/img/docker1.png)
- Buka browser dan periksa Hivemq dan InfluxDB:

### Langkah-langkah:

- Buka browser dan akses Hivemq: [localhost:8080](http://localhost:8080)
![Teks Alternatif](https://github.com/akbarsenawjy26/MIT-FirmwareEngineer/blob/main/img/docker2.png)

- Buka browser dan akses InfluxDB: [localhost:8086](http://localhost:8086)
![Teks Alternatif](https://github.com/akbarsenawjy26/MIT-FirmwareEngineer/blob/main/img/docker3.png)

- Ikuti langkah-langkah berikut:

    - Klik "Get Started"
![Teks Alternatif](https://github.com/akbarsenawjy26/MIT-FirmwareEngineer/blob/main/img/docker4.png)
    
    - Isi informasi awal:
        - Nama Pengguna: `akbarsenawjy`
        - Kata Sandi: `403201aa`
        - Nama Organisasi Awal: `MIT`
        - Nama Bucket Awal: `mqtt_logging`
![Teks Alternatif](https://github.com/akbarsenawjy26/MIT-FirmwareEngineer/blob/main/img/docker5.png)

    - Klik "Configure Later"
![Teks Alternatif](https://github.com/akbarsenawjy26/MIT-FirmwareEngineer/blob/main/img/docker6.png)

    - Klik "Python"
![Teks Alternatif](https://github.com/akbarsenawjy26/MIT-FirmwareEngineer/blob/main/img/docker7.png)

    - Klik "Get Token", dan salin token setelah `=`
![Teks Alternatif](https://github.com/akbarsenawjy26/MIT-FirmwareEngineer/blob/main/img/docker8.png)

    - Tempelkan token ke dalam bidang `influxdb_token` di `api.py` dan `mqtt_middleware.py`:
      ```python
      influxdb_token = "tW-EN6DLekedgQW91Ck5mVKEHuq_surGAR9Y3xV8B_Jh965dsZbPP7Br5kzy30NlId2lyimA8KOFt8MYvqW_1w==" # Ganti dengan Token
      ```
    - Klik "Write Data", pilih `mqtt_logging` di bawah bucket
![Teks Alternatif](https://github.com/akbarsenawjy26/MIT-FirmwareEngineer/blob/main/img/docker9.png)

    - Biarkan terbuka, akan dibuka kembali setelah middleware berjalan


### 4. Middleware
- Konfigurasi MQTT:
    - mqtt_broker = "192.168.1.10"  # Alamat IP atau hostname broker MQTT
    - mqtt_port = 1883
    - mqtt_topic_voltage = "home/sensor/voltage"
    - mqtt_topic_current = "home/sensor/current"
    - mqtt_topic_alarm_voltage = "home/actuator/alarmVoltage"
    - mqtt_topic_alarm_current = "home/actuator/alarmCurrent"

- Konfigurasi InfluxDB:
    - influxdb_url = "http://localhost:8086"
    - influxdb_token = "4inUUjaMJ3VfY4gFxvaou3ru4GOAs2EYvNuw2bl8xaX64YXoKMnWS89B7qqB4NEm5sYosuapEHypRMZiE8yoMQ=="  # Ganti dengan Token
    - influxdb_org = "MIT"
    - influxdb_bucket = "mqtt_logging"

- Jalankan di terminal:
    ```bash
   cd middleware
    ```
    ```bash
   mqtt_middleware.py
   ```

- Kembali ke InfluxDB sebelumnya dan pastikan koneksi ditemukan

### 5. Backend
- Jalankan di terminal:
    ```bash
    cd backend
    ```
    ```bash
    python api.py
    ```

- Akses localhost:5000/api/voltage dan localhost:5000/api/current

### 6. Frontend
- Jalankan di terminal:
    ```bash
    cd frontend
    ```
    ```bash
    npm install
    ```
    ```bash
    node server.js
    ```
- Akses localhost:3000