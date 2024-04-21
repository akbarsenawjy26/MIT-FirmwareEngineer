## Panduan Pengaturan Proyek

Panduan ini akan memandu Anda melalui pengaturan komponen yang diperlukan untuk menjalankan proyek.

### 1. Persyaratan
- Python v3
- NodeJS v20

### 2. Firmware
a. Konfigurasi Platform.ini:
Pastikan konten berikut ada di dalam `platform.ini`:
```ini lib_deps = knolleary/PubSubClient@^2.8```
b. Konfigurasi WiFi:
const char* ssid = "TMU"; // Ganti dengan SSID Anda
const char* password = "BambangDjaja"; // Ganti dengan Password Anda
c. Konfigurasi MQTT:
const char* mqtt_server = "192.168.137.1"; // Ganti dengan IP Localhost Anda
d. Unggah Firmware ke ESP32\


### 3. Menjalankan Docker-Compose
Buka terminal di vscode:
docker-compose up -d
Pastikan eksekusi berhasil.

Buka browser dan periksa Hivemq dan InfluxDB:

Hivemq: localhost:8080
InfluxDB: localhost:8086
Ikuti langkah-langkah ini:

Klik "Get Started"
Isi penggunaan awal:
Nama Pengguna: akbarsenawjy
Kata Sandi: 403201aa
Nama Organisasi Awal: MIT
Nama Bucket Awal: mqtt_logging
Klik "Configure Later"
Klik "Python"
Klik "Get Token", dan salin token setelah =
Tempelkan ke dalam bidang influxdb_token di api.py dan mqtt_middleware.py
influxdb_token = "tW-EN6DLekedgQW91Ck5mVKEHuq_surGAR9Y3xV8B_Jh965dsZbPP7Br5kzy30NlId2lyimA8KOFt8MYvqW_1w==" # Ganti dengan Token
Klik "Write Data", pilih mqtt_logging di bawah bucket
Biarkan terbuka, akan dibuka kembali setelah middleware berjalan

### 4. Middleware
a. Konfigurasi MQTT:
mqtt_broker = "192.168.1.10"  # Alamat IP atau hostname broker MQTT
mqtt_port = 1883
mqtt_topic_voltage = "home/sensor/voltage"
mqtt_topic_current = "home/sensor/current"
mqtt_topic_alarm_voltage = "home/actuator/alarmVoltage"
mqtt_topic_alarm_current = "home/actuator/alarmCurrent"

b. Konfigurasi InfluxDB:
influxdb_url = "http://localhost:8086"
influxdb_token = "4inUUjaMJ3VfY4gFxvaou3ru4GOAs2EYvNuw2bl8xaX64YXoKMnWS89B7qqB4NEm5sYosuapEHypRMZiE8yoMQ=="  # Ganti dengan Token
influxdb_org = "MIT"
influxdb_bucket = "mqtt_logging"

c. Jalankan di terminal:
cd middleware
python mqtt_middleware.py

d. Kembali ke InfluxDB sebelumnya dan pastikan koneksi ditemukan

### 5. Backend
a. Jalankan di terminal:
cd backend
python api.py

b. Akses localhost:5000/api/voltage dan localhost:5000/api/current

### 6. Frontend
a. Jalankan di terminal:
cd frontend
npm install
node server.js

b. Akses localhost:3000