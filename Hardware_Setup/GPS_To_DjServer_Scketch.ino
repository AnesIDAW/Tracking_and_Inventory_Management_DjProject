#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <TinyGPS++.h>
#include <HardwareSerial.h>

// WiFi Credentials
const char* ssid = "Your_SSID";
const char* password = "Your_PASSWORD";

// MQTT Broker Settings
const char* mqtt_server = "Your_Broker_System_IP";  // Change to your Mosquitto host IP or hostname
const int mqtt_port = 1883;
const char* mqtt_topic = "vehicle/gps";

WiFiClient espClient;
PubSubClient client(espClient);

#define RXD2 16
#define TXD2 17
#define GPS_BAUD 9600

HardwareSerial gpsSerial(1);
TinyGPSPlus gps;

void setup_wifi() {
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\n✅ WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect_mqtt() {
  while (!client.connected()) {
    Serial.print("Connecting to MQTT...");
    if (client.connect("ESP32_GPS_Client")) {
      Serial.println(" connected!");
    } else {
      Serial.print(" failed, rc=");
      Serial.print(client.state());
      Serial.println(" retrying in 3 seconds");
      delay(3000);
    }
  }
}

void get_gps_location(double &latitude, double &longitude) {
  while (gpsSerial.available() > 0) {
    gps.encode(gpsSerial.read());
  }

  if (gps.location.isValid()) {
    latitude = gps.location.lat();
    longitude = gps.location.lng();
  } else {
    Serial.println("⚠️ No valid GPS fix yet.");
  }
}

void setup() {
  Serial.begin(115200);
  gpsSerial.begin(GPS_BAUD, SERIAL_8N1, RXD2, TXD2);
  Serial.println("📡 Serial GPS started");

  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  if (!client.connected()) {
    reconnect_mqtt();
  }
  client.loop();

  double latitude = 0.0, longitude = 0.0;
  get_gps_location(latitude, longitude);

  if (gps.location.isValid()) {
    StaticJsonDocument<256> doc;
    doc["plate_number"] = 123014;
    doc["latitude"] = latitude;
    doc["longitude"] = longitude;

    char buffer[256];
    serializeJson(doc, buffer);

    if (client.publish(mqtt_topic, buffer)) {
      Serial.print("📤 Published: ");
      Serial.println(buffer);
    } else {
      Serial.println("❌ MQTT publish failed!");
    }
  }

  delay(3000); // Send every 3 seconds
}
