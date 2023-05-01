# BrumEco Accelerometer Sensing

This project is designed to collect and visualise real-time accelerometer data from multiple sensors. The project consists of two main components:

1. A microcontroller program to read data from the accelerometers and transmit it to a computer over a serial connection.
2. A Python program to receive the data, save it to CSV files, and visualize it in real-time using Matplotlib Animation.

## Hardware Requirements

- Arduino Uno or similar microcontroller board
- Two WT61PC accelerometers
- USB cable for connecting the microcontroller to the computer

## Software Requirements

- Arduino IDE or CLI
- Python 3.7+
- Required Python packages: `matplotlib`, `pyserial`
- DFRobot_WT61PC Library for Arduino (https://github.com/DFRobot/DFRobot_WT61PC)

## Usage

1. Upload the `accelerometer_sensing.ino` sketch to the Arduino board.
2. Connect the accelerometers to the Arduino board as follows:
   - Left accelerometer: Connect `TX` pin to Arduino pin `11`, `RX` pin to Arduino pin `10`.
   - Right accelerometer: Connect `TX` pin to Arduino pin `9`, `RX` pin to Arduino pin `8`.
3. Run the Python program `data_capture.py`. The program will automatically detect the Arduino serial port. Once the Arduinno is selected, the program will start collecting and visualising the data in real-time.
4. To stop the script, simply close the plot window.

## Data Format

> Data will be saved to CSV files located in the `captured_accel_data` directory. Each sensor will have its own file, with the filename format `accel_data_<timestamp>_<sensorID>.csv`.

The transmitted data consists of three main components: accelerometer, gyroscope, and angle data. Each data packet is prefixed by a unique identifier indicating which sensor it came from.

The data is formatted as follows:

`<sensorID> <timestamp> <accX> <accY> <accZ> <gyroX> <gyroY> <gyroZ> <angleX> <angleY> <angleZ>`

- `<sensorID>`: The unique identifier for the sensor that generated the data packet.
- `<timestamp>`: The time in milliseconds since the Arduino board was last reset.
- `<accX>`, `<accY>`, `<accZ>`: The X, Y, and Z acceleration values in units of meters per second squared.
- `<gyroX>`, `<gyroY>`, `<gyroZ>`: The X, Y, and Z angular velocity values in units of degrees per second.
- `<angleX>`, `<angleY>`, `<angleZ>`: The X, Y, and Z orientation angles in degrees.
