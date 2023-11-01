#ifndef MY_HEADERS_H
#define MY_HEADERS_H

#include <WiFiMulti.h>
#include <InfluxDbClient.h>
#include <InfluxDbCloud.h>
#include <PZEM004Tv30.h> 

#define WIFI_SSID "New day"
#define WIFI_PASSWORD "team1234"
#define INFLUXDB_URL "https://us-east-1-1.aws.cloud2.influxdata.com"
#define INFLUXDB_TOKEN "Kg2101Yx5EPdblFv8zNhfTZIh_ZKO287Bv33pCenGvGg5JrK6GW3_C4wHEhQNei2WA7ugObG5J-RjmOW98ZQSg=="
#define INFLUXDB_ORG "5d772333248db5a7"
#define INFLUXDB_BUCKET "current-voltage"
#define TZ_INFO "UTC5.5"
#define DEVICE "ESP32"

extern WiFiMulti wifiMulti;
void send_to_cloud(InfluxDBClient &client, float voltage, float current, float power, float energy, float frequency, int count);
void send_to_serial(float voltage, float current, float power, float energy, float frequency, int count);
void send_to_file(float voltage, float current, float power, float energy, float frequency, int count);

#endif