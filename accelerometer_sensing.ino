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
  Serial.println(String(millis())+"\t"+ID);
  Serial.println("Acc\t"+String(sensorData.Acc.X)+"\t"+String(sensorData.Acc.Y)+"\t"+String(sensorData.Acc.Z));
  Serial.println("Gyro\t"+String(sensorData.Gyro.X)+"\t"+String(sensorData.Gyro.Y)+"\t"+String(sensorData.Gyro.Z));
  Serial.println("Angle\t"+String(sensorData.Angle.X)+"\t"+String(sensorData.Angle.Y)+"\t"+String(sensorRight.Angle.Z));
}
