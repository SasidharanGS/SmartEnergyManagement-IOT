#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "New day";
const char* password = "team1234";
const char* mqttServer = "localhost";
const int mqttPort = 1883; // MQTT default port

WiFiClient espClient;
PubSubClient client(espClient);

char clientId[20]; // To hold the generated client ID

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Generating a random number to add as part of the client ID
    int clientIdRandom = random(0, 1000);
    snprintf(clientId, sizeof(clientId), "ESP32Client-%d", clientIdRandom);
    
    if (client.connect(clientId)) {
      Serial.print("connected as ");
      Serial.println(clientId);
      client.subscribe("esp32/test"); // Subscribe to a topic
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
  setup_wifi();
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);

  // Initialize random number generator with a seed
  randomSeed(analogRead(0)); // You can use a different pin for analogRead if needed
}
  
void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
