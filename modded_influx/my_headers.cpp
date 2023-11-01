#include "my_headers.h"
#define DEVICE "ESP32"

void send_to_cloud(InfluxDBClient &client, float voltage, float current, float power, float energy, float frequency, int count) {
    Point sensor("sensor_data");
    
    sensor.addTag("device", DEVICE);
    sensor.addTag("SSID", WIFI_SSID);
    sensor.addField("voltage", voltage);
    sensor.addField("current", current);
    sensor.addField("power", power);
    sensor.addField("energy", energy);
    sensor.addField("frequency", frequency);
    sensor.addField("people_inside", count);
    
    if (wifiMulti.run() != WL_CONNECTED) {
        Serial.println("Wifi connection lost");
    }
    
    if (!client.writePoint(sensor)) {
        Serial.print("InfluxDB write failed: ");
        Serial.println(client.getLastErrorMessage());
    }
    Serial.println("Data sent to cloud");
}

void send_to_serial(float voltage, float current, float power, float energy, float frequency, int count) {
  Serial.print("Voltage: ");
  Serial.print(voltage);
  Serial.print(" V, Current: ");
  Serial.print(current);
  Serial.print(" A, Power: ");
  Serial.print(power);
  Serial.print(" W, Energy: ");
  Serial.print(energy);
  Serial.print(" Wh, Frequency: ");
  Serial.print(frequency);
  Serial.print(" Hz, People Inside:");
  Serial.println(count);
}
