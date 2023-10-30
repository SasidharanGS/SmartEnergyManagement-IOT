#include "my_headers.h"

WiFiMulti wifiMulti;
#define PZEM_RX_PIN 18
#define PZEM_TX_PIN 19

float voltage;
float current;
float power;
float energy;
float frequency;

PZEM004Tv30 pzem(Serial1, PZEM_RX_PIN, PZEM_TX_PIN);
InfluxDBClient client(INFLUXDB_URL, INFLUXDB_ORG, INFLUXDB_BUCKET, INFLUXDB_TOKEN, InfluxDbCloud2CACert);

void setup() {
  Serial.begin(115200);
  
  WiFi.mode(WIFI_STA);
  wifiMulti.addAP(WIFI_SSID, WIFI_PASSWORD);

  Serial.print("Connecting to wifi");
  while (wifiMulti.run() != WL_CONNECTED) {
    Serial.print(".");
    delay(100);
  }
  Serial.println();

  timeSync(TZ_INFO, "pool.ntp.org", "time.nis.gov");

  if (client.validateConnection()) {
  Serial.print("Connected to InfluxDB: ");
  Serial.println(client.getServerUrl());
  } else {
  Serial.print("InfluxDB connection failed: ");
  Serial.println(client.getLastErrorMessage());
}
  }

void loop() {
    voltage = pzem.voltage();
    current = pzem.current();
    power = pzem.power();
    energy = pzem.energy();
    frequency = pzem.frequency();

  if (isnan(voltage) || isnan(current) || isnan(power) || isnan(energy) || isnan(frequency))
      Serial.println("Error reading sensor data!");
  else {
      send_to_cloud(client, voltage, current, power, energy, frequency);
      send_to_serial(voltage, current, power, energy, frequency);
  }
  delay(3000);
}
