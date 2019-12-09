#include <WiFiClientSecure.h>
#include <WebSocketsServer.h>
#include <Ticker.h>
#include <stdlib.h>
#include <time.h>

// // // Set SSID and Password for the Network here. 
char* ssid = "Internet";
char* password = "chiron99";

WebSocketsServer webSocket = WebSocketsServer(80);
float sampleRate = 1;
Ticker timer;


void setup() {
 
  // Start Serial port
  Serial.begin(115200);

  srand(time(NULL));

  // Connect to access point
  Serial.println("Connecting");
  WiFi.begin(ssid, password);
  while ( WiFi.status() != WL_CONNECTED ) {
  delay(500);
  Serial.print(".");
  }

  // Print our IP address
  Serial.println("Connected!");
  Serial.print("My IP address: ");
  Serial.println(WiFi.localIP());

  // Start WebSocket server and assign callback
  webSocket.begin();
  webSocket.onEvent(onWebSocketEvent);

  timer.attach(sampleRate, getData);

}

// Defining variables globally to transmit to python connection
String json; // for json
uint8_t c_numb; // for storing device num (connection device) to send data

void getData() {

  // Build JSON string here which will be sent to the client

  json = "{\"Temperature\":";
  json += rand() % 10;
  json += ", \"Water\":";
  json += rand() % 10;
  //json += ", \"data_point_3\":";
  //json += rand() % 10;
  //Serial.print(rand() % 10);
  json += "}";
  webSocket.broadcastTXT(json.c_str(), json.length());
  
  webSocket.sendTXT(c_numb, json); // Sending data to the web-socket connection through python

}


// Called when receiving any WebSocket message
void onWebSocketEvent(uint8_t num,
            WStype_t type,
            uint8_t * payload,
            size_t length) {

  // Figure out the type of WebSocket event
  switch(type) {

  // Client has disconnected
  case WStype_DISCONNECTED:
    Serial.printf("[%u] Disconnected!\n", num);
    break;

  // New client has connected
  case WStype_CONNECTED:
      {
      IPAddress ip = webSocket.remoteIP(num);
      Serial.printf("[%u] Connection from ", num);
      Serial.println(ip.toString());
      break;
      }
  // Echo text message back to client
  case WStype_TEXT:
    {
      c_numb = num;
      sampleRate = (float) atof((const char *) &payload[0]);
      timer.detach();
      timer.attach(sampleRate, getData);
      
      //webSocket.sendTXT(num, payload);
      break;
    }
  // For everything else: do nothing
  default:
    break;
  }
}


void loop() {
 
  // Look for and handle WebSocket data
  webSocket.loop();

}
