#include <DFRobot_WT61PC.h>
#include <SoftwareSerial.h>

SoftwareSerial accLeft (10,11);
SoftwareSerial accRight (5,6);
DFRobot_WT61PC sensorLeft(&accLeft);
DFRobot_WT61PC sensorRight(&accRight);

void setup (){
  Serial.begin(115200);
  accLeft.begin(9600);
  accRight.begin(9600);

  sensorLeft.modifyFrequency(FREQUENCY_0_1HZ);
  sensorRight.modifyFrequency(FREQUENCY_0_1HZ);
}

void loop(){
  if (sensorLeft.available() && sensorRight.available()){
    sendData(sensorLeft, "Left");
    sendData(sensorRight, "Right");
  }
}

void sendData(DFRobot_WT61PC sensorData, String ID){
  unsigned long currentTime = millis();
  Serial.print(currentTime);

  Serial.print("Acc"+ID+"\t"); Serial.print(sensorData.Acc.X); Serial.print("\t"); Serial.print(sensorData.Acc.Y); Serial.print("\t"); Serial.print(sensorData.Acc.Z); Serial.print("\n");
  Serial.print("Gyro"+ID+"\t"); Serial.print(sensorData.Gyro.X); Serial.print("\t"); Serial.print(sensorData.Gyro.Y); Serial.print("\t"); Serial.print(sensorData.Gyro.Z); Serial.print("\n");
  Serial.print("Angle"+ID+"\t"); Serial.print(sensorData.Angle.X); Serial.print("\t"); Serial.print(sensorData.Angle.Y); Serial.print("\t"); Serial.print(sensorRight.Angle.Z); Serial.print("\n");
  Serial.print("\n");
}