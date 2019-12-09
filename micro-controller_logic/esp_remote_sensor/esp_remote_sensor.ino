/*
  Semester Project
  CS 235 Computer Architecture and Assembly Language

  Detection of speedbreakers and Road quality Measurement

  This file contains the code to read Accelerometer and Gyroscope reading from MPU-6050 sensor module over IIC
  and creates a web socket to send data over wifi
*/


#include <WiFiClientSecure.h>
#include <WebSocketsServer.h>
#include <Ticker.h>
#include <stdlib.h>
#include <time.h>
#include <Wire.h>


// // // Set SSID and Password for the Network here.
char* ssid = "Spectre x360";
char* password = "zxcvbnml";

WebSocketsServer webSocket = WebSocketsServer(80);
float sampleRate = 1;
Ticker timer;

// MPU6050 Slave Device Address
const uint8_t MPU6050SlaveAddress = 0x68;

// Select SDA and SCL pins for I2C communication
const uint8_t scl = D6;
const uint8_t sda = D7;

const uint8_t leftLED = D2;
const uint8_t rightLED = D3;
const uint8_t upLED = D1;
const uint8_t downLED = D0;

// sensitivity scale factor respective to full scale setting provided in datasheet
const uint16_t AccelScaleFactor = 16384;
const uint16_t GyroScaleFactor = 131;

// MPU6050 few configuration register addresses
const uint8_t MPU6050_REGISTER_SMPLRT_DIV   =  0x19;
const uint8_t MPU6050_REGISTER_USER_CTRL    =  0x6A;
const uint8_t MPU6050_REGISTER_PWR_MGMT_1   =  0x6B;
const uint8_t MPU6050_REGISTER_PWR_MGMT_2   =  0x6C;
const uint8_t MPU6050_REGISTER_CONFIG       =  0x1A;
const uint8_t MPU6050_REGISTER_GYRO_CONFIG  =  0x1B;
const uint8_t MPU6050_REGISTER_ACCEL_CONFIG =  0x1C;
const uint8_t MPU6050_REGISTER_FIFO_EN      =  0x23;
const uint8_t MPU6050_REGISTER_INT_ENABLE   =  0x38;
const uint8_t MPU6050_REGISTER_ACCEL_XOUT_H =  0x3B;
const uint8_t MPU6050_REGISTER_SIGNAL_PATH_RESET  = 0x68;

int16_t AccelX, AccelY, AccelZ, Temperature, GyroX, GyroY, GyroZ;


void setup() {

  // Start Serial port
  Serial.begin(115200);

  srand(time(NULL));

  Wire.begin(sda, scl);
  MPU6050_Init();

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

  double Ax, Ay, Az, T, Gx, Gy, Gz;
  // Read values from sensor
  Read_RawValue(MPU6050SlaveAddress, MPU6050_REGISTER_ACCEL_XOUT_H);

  //divide each with their sensitivity scale factor
  Ax = (double)AccelX/AccelScaleFactor;
  Ay = (double)AccelY/AccelScaleFactor;
  Az = (double)AccelZ/AccelScaleFactor;
  T = (double)Temperature/340+36.53; //temperature formula
  Gx = (double)GyroX/GyroScaleFactor;
  Gy = (double)GyroY/GyroScaleFactor;
  Gz = (double)GyroZ/GyroScaleFactor;

  // Build JSON string here which will be sent to the client

  json = "{\"Ax\":";
  json += Ax;
  json += ", \"Ay\":";
  json += Ay;
  json += ", \"Az\":";
  json += Az;
  json += ", \"T\":";
  json += T;
  json += ", \"Gx\":";
  json += Gx;
  json += ", \"Gy\":";
  json += Gy;
  json += ", \"Gz\":";
  json += Gz;
  json += "}";
  webSocket.broadcastTXT(json.c_str(), json.length());

  // webSocket.sendTXT(c_numb, json); // Sending data to the web-socket connection through python

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

//configure MPU6050
void MPU6050_Init(){
  delay(150);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_SMPLRT_DIV, 0x07);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_PWR_MGMT_1, 0x01);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_PWR_MGMT_2, 0x00);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_CONFIG, 0x00);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_GYRO_CONFIG, 0x00);//set +/-250 degree/second full scale
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_ACCEL_CONFIG, 0x00);// set +/- 2g full scale
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_FIFO_EN, 0x00);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_INT_ENABLE, 0x01);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_SIGNAL_PATH_RESET, 0x00);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_USER_CTRL, 0x00);
}

// read all 14 register
void Read_RawValue(uint8_t deviceAddress, uint8_t regAddress){
  Wire.beginTransmission(deviceAddress);
  Wire.write(regAddress);
  Wire.endTransmission();
  Wire.requestFrom(deviceAddress, (uint8_t)14);
  AccelX = (((int16_t)Wire.read()<<8) | Wire.read());
  AccelY = (((int16_t)Wire.read()<<8) | Wire.read());
  AccelZ = (((int16_t)Wire.read()<<8) | Wire.read());
  Temperature = (((int16_t)Wire.read()<<8) | Wire.read());
  GyroX = (((int16_t)Wire.read()<<8) | Wire.read());
  GyroY = (((int16_t)Wire.read()<<8) | Wire.read());
  GyroZ = (((int16_t)Wire.read()<<8) | Wire.read());
}

void I2C_Write(uint8_t deviceAddress, uint8_t regAddress, uint8_t data){
  Wire.beginTransmission(deviceAddress);
  Wire.write(regAddress);
  Wire.write(data);
  Wire.endTransmission();
}
