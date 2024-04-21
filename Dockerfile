# HiveMQ service
FROM hivemq/hivemq4
ENV HIVEMQ_BIND_ADDRESS=0.0.0.0
EXPOSE 1883 8000 8080

# InfluxDB service
FROM influxdb:latest
ENV INFLUXDB_DB=mqtt-logging
ENV INFLUXDB_ADMIN_USER=akbarsenawjy
ENV INFLUXDB_ADMIN_PASSWORD=403201aa
EXPOSE 8086

# Python middleware service
FROM python:3.9-alpine as python_middleware
WORKDIR /middleware
COPY middleware/mqtt_middleware.py .
COPY middleware/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Python backend service
FROM python:3.9-alpine as python_backend
WORKDIR /backend
COPY backend/api.py .
COPY backend/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Frontend
FROM node:lts-alpine as nodejs_frontend
WORKDIR /frontEnd
COPY frontEnd/package.json .
COPY frontEnd/server.js .
COPY frontEnd/index.html .
RUN npm install
EXPOSE 3000


# Root directory
COPY . .

CMD python3 /middleware/mqtt_middleware.py && python3 /backend/api.py && node server.js