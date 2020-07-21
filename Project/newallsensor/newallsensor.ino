#include <ESP8266HTTPClient.h>


const int refresh=3;

#include "DHT.h"
#define DHTPIN 2     
#define DHTTYPE DHT11   
DHT dht(DHTPIN, DHTTYPE);
const char* host = "tesingplace.tech";

#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

#ifndef STASSID
#define STASSID "Hidden Network" 
#define STAPSK  "&&double_and"
#endif

int sense_Pin = 0; // Soil Sensor input at Analog PIN A0
int value = 0;

const char* ssid = STASSID;
const char* password = STAPSK;





void setup(void) {
  
   dht.begin();
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  if (WiFi.status() == WL_CONNECTED)
  {
    uint8_t macAddr[6];
    WiFi.macAddress(macAddr);
    Serial.printf("Connected, mac address: %02x:%02x:%02x:%02x:%02x:%02x", macAddr[0], macAddr[1], macAddr[2], macAddr[3], macAddr[4], macAddr[5]);
  }  
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  }

void loop(void) {
 
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity(); 
  value = analogRead(sense_Pin); 
  if(isnan(temperature) || isnan(humidity)){
    Serial.println("Failed to read DHT11");
  }else{
    Serial.print("Humidity: ");
    Serial.print(humidity);
    Serial.print(" %\t");
    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.println(" *C");
    Serial.print("MOISTURE LEVEL : ");
    Serial.print(value);
    delay(10000);
  }
   
    Serial.print("connecting to ");
    Serial.println(host);

   HTTPClient http;  //Declare an object of class HTTPClient
 
http.begin("http://testingplace.tech/testdisplay.php?&temperature="+ String(temperature) +"&humidity="+ String(humidity) +"&moisture="+String(value));  //Specify request destination
int httpCode = http.GET();                                                                  //Send the request
delay(10000); 

if (httpCode > 0) { //Check the returning code
 
String payload = http.getString();   //Get the request response payload
Serial.println(payload);                     //Print the response payload
 
}
 
http.end();   //Close connection
 
}
 
    
 
