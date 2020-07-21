#include <ESP8266HTTPClient.h>



const char* host = "tesingplace.tech";

#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

#ifndef STASSID
#define STASSID "Hidden Network" 
#define STAPSK  "&&double_and"
#endif

const char* ssid = STASSID;
const char* password = STAPSK;



const int relay = 5;
const int relay1 = 4;

void setup(void) {
  
  Serial.begin(115200);
  pinMode(relay, OUTPUT);
  pinMode(relay1, OUTPUT);

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
  digitalWrite(relay, HIGH);
  digitalWrite(relay1, HIGH);

  }
int value=0;
void loop(void) {
  int linecounter=0;
  String actualtemp;
  String actualhum;
  String actualmr;
  String controlt;
  String controlh;
  String controlm;
  float actualtemp1=0.0;
  float actualhum1=0.0;
  float  actualmr1=0.0;
  float controlt1=0.0;
  float controlh1=0.0;
  float controlm1=0.0;
  String line="";
  ++value;
 
  
    Serial.print("connecting to ");
    Serial.println(host);

   HTTPClient http;  //Declare an object of class HTTPClient
 
http.begin("http://testingplace.tech/page4arduino.php");  //Specify request destination
int httpCode = http.GET();                                                                  //Send the request
delay(10000); 

if (httpCode > 0) { //Check the returning code
 
String payload = http.getString();

Serial.println(payload); 
actualtemp=payload.substring(15,17);
Serial.print(actualtemp);
actualhum=payload.substring(17,19);
Serial.print(actualhum);
actualmr=payload.substring(19,21);
Serial.print(actualmr);
controlt=payload.substring(21,23);
Serial.print(controlt);
controlh=payload.substring(23,25);
Serial.print(controlh);
controlm=payload.substring(25,27);
Serial.print(controlm);

actualtemp1=actualtemp.toFloat();
actualhum1=actualhum.toFloat();
actualmr1=actualmr.toFloat();
controlt1=controlt.toFloat();
controlh1=controlh.toFloat();
controlm1=controlm.toFloat();

if(controlt1<=actualtemp1){
  digitalWrite(relay, LOW);
  Serial.print("digital write on");
  digitalWrite(relay1, LOW);
}
else{
  Serial.print("digital write off");
  digitalWrite(relay, LOW);
  digitalWrite(relay1, LOW);
}
delay(2000);
if(controlh1<=actualhum1){
  Serial.print("digital write on");
  digitalWrite(relay, LOW);
  digitalWrite(relay1, LOW);
}
else{
  Serial.print("digital write off");
  digitalWrite(relay, LOW);
  digitalWrite(relay1, LOW);
}
delay(2000);
if(controlm1<=actualmr1){
  Serial.print("digital write on");
  digitalWrite(relay, LOW);
  digitalWrite(relay1, LOW);
}
else{
  Serial.print("digital write off");
  digitalWrite(relay, LOW);
  digitalWrite(relay1, LOW);
}

 
}
 
http.end();   //Close connection
 
}
 
    
 
