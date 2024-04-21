#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>

// Forward declaration of mqttCallback function
void mqttCallback(char* topic, byte* payload, unsigned int length);

// WiFi config
const char* ssid = "TMU"; //changes with ur SSID
const char* password = "BambangDjaja"; //changes with ur Password

// MQTT config
const char* mqtt_server = "192.168.137.1"; // Ganti dengan IP Localhost
const int mqtt_port = 1883;
const char* mqtt_topic_voltage = "home/sensor/voltage";
const char* mqtt_topic_current = "home/sensor/current";
const char* mqtt_topic_alarm_voltage = "home/actuator/alarmVoltage";
const char* mqtt_topic_alarm_current = "home/actuator/alarmCurrent";
const char* mqtt_topic_alarm_state = "home/actuator/alarmState";


WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

// Function setupWifi
void setupWiFi() {
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi!");
}

// Function setupMQTT
void setupMQTT() {
    mqttClient.setServer(mqtt_server, mqtt_port);
    mqttClient.setCallback(mqttCallback);
}

// Function to connect, reconnect, & subcribeTopic
void reconnectMQTT() {
    while (!mqttClient.connected()) {
        Serial.println("Connecting to MQTT...");
        if (mqttClient.connect("ArduinoClient")) {
            Serial.println("Connected to MQTT broker!");
            mqttClient.subscribe(mqtt_topic_alarm_voltage);
            mqttClient.subscribe(mqtt_topic_alarm_current);
        } else {
            Serial.print("Failed to connect, rc=");
            Serial.print(mqttClient.state());
            Serial.println(" Retrying in 5 seconds...");
            delay(5000);
        }
    }
}

// Function callbackPayloadTopic
void mqttCallback(char* topic, byte* payload, unsigned int length) {
    Serial.print("Message received on topic: ");
    Serial.println(topic);

    // Convert payload to string
    payload[length] = '\0';
    String message = String((char*)payload);

    Serial.print("Message payload: ");
    Serial.println(message);

    if (strcmp(topic, mqtt_topic_alarm_voltage) == 0 || strcmp(topic, mqtt_topic_alarm_current) == 0) {
        if (message.equalsIgnoreCase("Alarm")) {
            digitalWrite(LED_BUILTIN, HIGH); // Turn on LED
            Serial.println("LED turned ON");
            mqttClient.publish(mqtt_topic_alarm_state, "On");

        } else {
            digitalWrite(LED_BUILTIN, LOW); // Turn off LED
            Serial.println("LED turned OFF");
            mqttClient.publish(mqtt_topic_alarm_state, "Off");
        }
    }
}

void setup() {
    Serial.begin(9600);
    pinMode(LED_BUILTIN, OUTPUT); // Set LED_BUILTIN pin as output
    setupWiFi();
    setupMQTT();
}

void loop() {
    if (!mqttClient.connected()) {
        reconnectMQTT();
    }

    mqttClient.loop(); // MQTT connection and handle incoming messages

    // Generate dummy data (voltage & current)
    float voltage = random(225, 235); // Random voltage between 225 to 235
    int current = random(0, 105);     // Random current between 0 to 105

    // Convert float and int to string
    char voltageStr[10];
    dtostrf(voltage, 4, 2, voltageStr);
    char currentStr[10];
    itoa(current, currentStr, 10);

    // Publish voltage and current to MQTT topics
    mqttClient.publish(mqtt_topic_voltage, voltageStr);
    mqttClient.publish(mqtt_topic_current, currentStr);

    // Print the sent data to serial monitor
    Serial.print("Voltage: ");
    Serial.println(voltage);
    Serial.print("Current: ");
    Serial.println(current);
    delay(5000); // Delay before checking MQTT connection and sending data
}
