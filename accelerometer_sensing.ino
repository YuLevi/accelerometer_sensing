#include <DFRobot_WT61PC.h>
#include <SoftwareSerial.h>

SoftwareSerial accLeft (10,11);
SoftwareSerial accRight (5,6);
DFRobot_WT61PC sensorLeft(&accLeft);
DFRobot_WT61PC sensorRight(&accRight);

void setup ()
{
  Serial.begin(9600);
  accLeft.begin(9600);
  accRight.begin(9600);

  sensorLeft.modifyFrequency(FREQUENCY_0_1HZ);
  sensorRight.modifyFrequency(FREQUENCY_0_1HZ);
}

void loop()
{
  if (sensorLeft.available()){
    Serial.print("Acc\t"); Serial.print(sensorLeft.Acc.X); Serial.print("\t"); Serial.print(sensorLeft.Acc.Y); Serial.print("\t"); Serial.print(sensorLeft.Acc.Z); Serial.print("\n");
    Serial.print("Gyro\t"); Serial.print(sensorLeft.Gyro.X); Serial.print("\t"); Serial.print(sensorLeft.Gyro.Y); Serial.print("\t"); Serial.print(sensorLeft.Gyro.Z); Serial.print("\n");
    Serial.print("Angle\t"); Serial.print(sensorLeft.Angle.X); Serial.print("\t"); Serial.print(sensorLeft.Angle.Y); Serial.print("\t"); Serial.print(sensorLeft.Angle.Z); Serial.print("\n");
    Serial.print("\n");

    Serial.print("Acc\t"); Serial.print(sensorRight.Acc.X); Serial.print("\t"); Serial.print(sensorRight.Acc.Y); Serial.print("\t"); Serial.print(sensorRight.Acc.Z); Serial.print("\n");
    Serial.print("Gyro\t"); Serial.print(sensorRight.Gyro.X); Serial.print("\t"); Serial.print(sensorRight.Gyro.Y); Serial.print("\t"); Serial.print(sensorRight.Gyro.Z); Serial.print("\n");
    Serial.print("Angle\t"); Serial.print(sensorRight.Angle.X); Serial.print("\t"); Serial.print(sensorRight.Angle.Y); Serial.print("\t"); Serial.print(sensorRight.Angle.Z); Serial.print("\n");
    Serial.print("\n");
    
  }
}