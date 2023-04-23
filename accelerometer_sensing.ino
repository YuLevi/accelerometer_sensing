#include <DFRobot_WT61PC.h>
#include <SoftwareSerial.h>

// Create SoftwareSerial object for connected accelerometers
SoftwareSerial accLeft (10,11);
SoftwareSerial accRight (5,6);

// Create DFRobot_WT61PCs object for accelerometers
DFRobot_WT61PC sensorLeft(&accLeft);
DFRobot_WT61PC sensorRight(&accRight);

void setup (){
  // Initialize serial communications
  Serial.begin(115200);
  accLeft.begin(9600);
  accRight.begin(9600);

  // Set frequency of data acquisition
  sensorLeft.modifyFrequency(FREQUENCY_0_1HZ);
  sensorRight.modifyFrequency(FREQUENCY_0_1HZ);
}

void loop(){
  if (sensorLeft.available() && sensorRight.available()){
    sendData(sensorLeft, "left");
    sendData(sensorRight, "right");
  }
}

// Log collected data with time
void sendData(DFRobot_WT61PC sensorData, String ID){
  unsigned long currentTime = millis();
  Serial.println(currentTime);
  Serial.println("Acc\t"+ID+"\t"+sensorData.Acc.X+"\t"+sensorData.Acc.Y+"\t"+sensorData.Acc.Z);
  Serial.println("Gyro\t"+ID+"\t"+sensorData.Gyro.X+"\t"+sensorData.Gyro.Y+"\t"+sensorData.Gyro.Z);
  Serial.println("Angle\t"+ID+"\t"+sensorData.Angle.X+"\t"+sensorData.Angle.Y+"\t"+sensorRight.Angle.Z);
}
