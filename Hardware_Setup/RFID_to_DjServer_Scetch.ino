#include <WiFi.h>
#include <PubSubClient.h>
#include <SPI.h>
#include <MFRC522.h>
#include <ArduinoJson.h>

#define SS_PIN 10
#define RST_PIN 9
#define SCK_PIN 12
#define MISO_PIN 13
#define MOSI_PIN 11

const char* ssid = "Your_SSID";  // Replace with your WiFi SSID
const char* password = "Your_PASSWORD";  // Replace with your WiFi password

// MQTT settings
const char* mqtt_server = "Your_Broker_System_IP";  // Replace with your Server IP that runs the MQTT broker
const int mqtt_port = 1883;
const char* mqtt_topic = "product/rfid";

WiFiClient espClient;
PubSubClient client(espClient);

MFRC522 rfid(SS_PIN, RST_PIN);

void setup_wifi() {
  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");
  Serial.println("IP Address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 3 seconds");
      delay(3000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  SPI.begin(SCK_PIN, MISO_PIN, MOSI_PIN, SS_PIN);
  rfid.PCD_Init();
  Serial.println("RFID Reader Initialized.");

  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial()) {
    return;
  }

  String uidString = "";
  for (byte i = 0; i < rfid.uid.size; i++) {
    if (rfid.uid.uidByte[i] < 0x10) {
      uidString += "0";
    }
    uidString += String(rfid.uid.uidByte[i], HEX);
  }
  uidString.toUpperCase();

  Serial.print("RFID UID: ");
  Serial.println(uidString);

  // Create JSON payload
  StaticJsonDocument<128> doc;
  doc["rfid_tag"] = uidString;
  char buffer[128];
  serializeJson(doc, buffer);

  // Publish to MQTT
  if (client.publish(mqtt_topic, buffer)) {
    Serial.println("[MQTT] Published RFID tag.");
  } else {
    Serial.println("[MQTT ERROR] Failed to publish.");
  }

  rfid.PICC_HaltA();
  rfid.PCD_StopCrypto1();

  delay(1500);  // Delay to avoid rapid firing
}