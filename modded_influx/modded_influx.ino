#include "my_headers.h"

WiFiMulti wifiMulti;
#define PZEM_RX 18
#define PZEM_TX 19

#define PIR_IN 13
#define PIR_OUT 14

float voltage;
float current;
float power;
float energy;
float frequency;
int people_inside = 0;

PZEM004Tv30 pzem(Serial1, PZEM_RX, PZEM_TX);
InfluxDBClient client(INFLUXDB_URL, INFLUXDB_ORG, INFLUXDB_BUCKET, INFLUXDB_TOKEN, InfluxDbCloud2CACert);

void wifi_setup(){
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

void setup() {
  pinMode(PIR_IN, INPUT);
  pinMode(PIR_OUT, INPUT);
  Serial.begin(115200);
  wifi_setup();
}

void loop() {
    voltage = pzem.voltage();
    current = pzem.current();
    power = pzem.power();
    energy = pzem.energy();
    frequency = pzem.frequency();

    int pir_in_state = digitalRead(PIR_IN);
    int pir_out_state = digitalRead(PIR_OUT);
    
  if (pir_in_state == HIGH && people_inside<255)
    people_inside ++;

  if (pir_out_state == HIGH && people_inside>0) 
    people_inside --;

  if (isnan(voltage) || isnan(current) || isnan(power) || isnan(energy) || isnan(frequency))
      Serial.println("Error reading sensor data!");
  else {
      send_to_cloud(client, voltage, current, power, energy, frequency, people_inside);
      send_to_serial(voltage, current, power, energy, frequency, people_inside);
      send_to_file(voltage, current, power, energy, frequency, people_inside);
  }
  delay(3000);
}
