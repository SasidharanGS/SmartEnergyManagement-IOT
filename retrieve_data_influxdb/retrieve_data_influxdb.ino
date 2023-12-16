#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <string.h>

const char* ssid = "New day";
const char* password = "team1234";
const char* server = "https://us-east-1-1.aws.cloud2.influxdata.com/api/v2/query?org=5d772333248db5a7&bucket=current-voltage&precision=s&q="; 
// e.g. https://us-west-2-1.aws.cloud2.influxdata.com/api/v2/query?org=YOUR_ORG&bucket=YOUR_BUCKET&precision=s
const char* token = "Kg2101Yx5EPdblFv8zNhfTZIh_ZKO287Bv33pCenGvGg5JrK6GW3_C4wHEhQNei2WA7ugObG5J-RjmOW98ZQSg=="; 
const char* query = "SELECT%20%2A%20FROM%20%22sensor_data%22%20WHERE%20time%20%3E%3D%20now()%20-%2030d";


void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi!");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    
    char url[100];
    strcpy(url, server);
    strcat(url, "/");
    strcat(url, query);
    http.begin(url);

    http.addHeader("Authorization", "Token " + String(token));
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(query);
    if (httpResponseCode == 200) {
      String response = http.getString();
      DynamicJsonDocument doc(1024);
      deserializeJson(doc, response);
      JsonArray results = doc["results"][0]["series"][0]["values"];
      for (JsonArray::iterator it = results.begin(); it != results.end(); ++it) {
        String timestamp = (*it)[0].as<String>();
        float value = (*it)[1].as<float>();
        Serial.print("Timestamp: ");
        Serial.print(timestamp);
        Serial.print(", Value: ");
        Serial.println(value);
      }
    } else {
      Serial.print("Error retrieving data. HTTP response code: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  } else {
    Serial.println("WiFi not connected.");
  }
  delay(5000);
}



// curl --request POST \
//   https://us-east-1-1.aws.cloud2.influxdata.com/api/v2/query?orgID=5d772333248db5a7  \
//   --header 'Authorization: Token Kg2101Yx5EPdblFv8zNhfTZIh_ZKO287Bv33pCenGvGg5JrK6GW3_C4wHEhQNei2WA7ugObG5J-RjmOW98ZQSg==' \
//   --header 'Accept: application/csv' \
//   --header 'Content-type: application/vnd.flux' \
//   --data 'from(bucket:"current-voltage")
//         |> range(start: -30d)
//         |> filter(fn: (r) => r._measurement == "sensor_data")
//         |> aggregateWindow(every: 1h, fn: mean)'