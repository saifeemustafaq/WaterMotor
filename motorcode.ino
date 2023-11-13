#include <WiFi.h>
#include <PubSubClient.h>
#include <ESP32Servo.h>

// Network and MQTT configurations
const char* ssid = "TOP_Floor";
const char* password = "Batman@359517";
const char* mqtt_server = "broker.hivemq.com";
const char* control_topic_servo1 = "home/saifeevilla288786/esp32/servo1";
const char* control_topic_servo2 = "home/saifeevilla288786/esp32/servo2";
String client_id_str = "ESP32Client_" + String(random(0xffff), HEX);
const char* client_id = client_id_str.c_str();

WiFiClient espClient;
PubSubClient client(espClient);
Servo myservo1;
Servo myservo2;

// Setup WiFi connection
void setup_wifi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}

// Callback for incoming MQTT messages
void callback(char* topic, byte* message, unsigned int length) {
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    messageTemp += (char)message[i];
  }

  if (String(topic) == control_topic_servo1) {
    if (messageTemp == "ON") {
      myservo1.write(100); // Adjust as needed for your servo
    } else if (messageTemp == "OFF") {
      myservo1.write(0);
    }
  } else if (String(topic) == control_topic_servo2) {
    if (messageTemp == "ON") {
      myservo2.write(100); // Adjust as needed for your servo
    } else if (messageTemp == "OFF") {
      myservo2.write(0);
    }
  }
}

// Reconnect to MQTT broker with exponential backoff
void reconnect() {
  unsigned long reconnectTime = 5000; // Initial reconnect time
  while (!client.connected()) {
    if (client.connect(client_id)) {  // Corrected line
      client.subscribe(control_topic_servo1);
      client.subscribe(control_topic_servo2);
    } else {
      delay(reconnectTime);
      reconnectTime = min(reconnectTime * 2, (unsigned long)120000); // Cap at 2 minutes
    }
  }
}


void setup() {
  myservo1.attach(14); // ESP32 pin connected to the first servo signal
  myservo2.attach(27); // ESP32 pin connected to the second servo signal, use another PWM-capable pin
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  reconnect(); // Make sure to connect and subscribe to topics on setup
}

void loop() {
  client.loop(); // Process incoming messages and maintain connection
  if (!client.connected()) {
    reconnect();
  }
}
