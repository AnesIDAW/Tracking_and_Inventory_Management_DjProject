#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <TinyGPS++.h>
#include <HardwareSerial.h>

// WiFi Credentials and Django api URL
const char* ssid = "Redmi";  
const char* password = "anes2909";  
const char* serverUrl = "http://192.168.43.209:8000/tracking/api/vehicle-locations/";

// GPS Pins RX and TX
#define RXD2 16
#define TXD2 17 

#define GPS_BAUD 9600

HardwareSerial gpsSerial(1);
TinyGPSPlus gps;

// GPS Coordonates Retreving Function ----------------------------------------------------------------------------
void get_gps_location(double &latitude, double &longitude){

  while (gpsSerial.available() > 0) {
        gps.encode(gpsSerial.read());
  }

  if (gps.location.isValid()){
    latitude = gps.location.lat();
    longitude = gps.location.lng();
  }
  else{
    Serial.println("⚠️ No valid GPS fix yet.");
  }

}
// --------------------------------------------------------------------------------------------------------------


// WiFi Connection Checking Function ----------------------------------------------------------------------------
void ensureWiFiConnected() {
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("⚠️ WiFi Disconnected! Reconnecting...");
        WiFi.begin(ssid, password);
        int attempts = 0;
        while (WiFi.status() != WL_CONNECTED && attempts < 10) {  // Limit retries
            delay(1000);
            Serial.print(".");
            attempts++;
        }
        if (WiFi.status() == WL_CONNECTED) {
            Serial.println("\n✅ Reconnected to WiFi!");
        } else {
            Serial.println("\n❌ Failed to reconnect!");
        }
    }
}
// ---------------------------------------------------------------------------------------


void setup() {
    //Serial Monitor begin Baud rate
    Serial.begin(115200);

    // Start Serial connection with GPS Module with the defined RX and TX
    gpsSerial.begin(GPS_BAUD, SERIAL_8N1, RXD2, TXD2);
    Serial.println("Serial 2 Start at 9600 Baud Rate ..");

    // Start WiFi Connection 
    WiFi.begin(ssid, password);
    Serial.print("Connecting to WiFi...");
    
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.print(".");
    }

    Serial.println("\n✅ Connected to WiFi!");
}

void loop() {
    ensureWiFiConnected();

    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        http.begin(serverUrl);  
        http.addHeader("Content-Type", "application/json");

        // Get GPS Data
        double latitude = 0.0, longitude = 0.0;
        get_gps_location(latitude, longitude);

        // Create JSON object
        StaticJsonDocument<200> jsonDoc;
        jsonDoc["plate_number"] = 123014;


        if (gps.location.isValid()){  // Change this ID for different vehicles
        jsonDoc["latitude"] = latitude;
        jsonDoc["longitude"] = longitude;
        } else {
          Serial.println("🚫 GPS Fix Not Available - Skipping Data Upload.");
          return;  // Exit loop() early if GPS is not ready
        }
        
        String jsonData;
        serializeJson(jsonDoc, jsonData);  // Convert JSON object to string

        Serial.println("\n📡 Sending Data to Server:");
        Serial.println(jsonData);  // Debugging: Show JSON before sending

        // Send HTTP POST request
        int httpResponseCode = http.POST(jsonData);

        // Read response
        Serial.print("🔹 Response Code: ");
        Serial.println(httpResponseCode);

        if (httpResponseCode > 0) {
            String response = http.getString();
            Serial.print("🔹 Server Response: ");
            Serial.println(response);
        } else {
            Serial.println("❌ HTTP Request failed!");
        }
        http.end();

    } else {
        Serial.println("⚠️ WiFi Disconnected! Retrying...");
    }

    delay(3000);  // Send data every 3 seconds

}

