# Time Warp Advanced IoT & Robotics Features

## Overview
Time Warp now includes comprehensive IoT (Internet of Things) and advanced robotics capabilities, making it perfect for educational projects involving smart homes, sensor networks, and intelligent robots.

## New Classes Added

### 1. IoTDeviceManager
Manages multiple IoT devices with automatic discovery and connection.
- Device discovery and connection
- Device grouping for batch operations
- Automation rules (if-then logic)
- Data history tracking

### 2. SmartHomeHub  
Complete smart home automation system.
- Environmental monitoring and control
- Scene management (lighting, temperature, etc.)
- Scheduling and automation
- Energy monitoring

### 3. SensorNetwork
Advanced sensor network with data analytics.
- Multi-sensor data collection
- Trend analysis and prediction
- Threshold monitoring and alerts
- Data visualization

### 4. AdvancedRobotInterface
Intelligent robotics with AI features.
- Path planning and navigation
- Obstacle avoidance
- Environment mapping (SLAM)
- Mission execution with waypoints

## New PILOT Commands (R: prefix)

### IoT Device Management
- `R:IOT DISCOVER` - Discover IoT devices on network
- `R:IOT CONNECT [device_id]` - Connect to device(s)
- `R:IOT READ device_id` - Read data from device
- `R:IOT SEND device_id command` - Send command to device
- `R:IOT GROUP group_name CREATE device1,device2` - Create device group
- `R:IOT GROUP group_name command` - Control device group

### Smart Home Automation
- `R:SMARTHOME SETUP` - Initialize smart home system
- `R:SMARTHOME SCENE CREATE scene_name` - Create automation scene
- `R:SMARTHOME SCENE scene_name` - Activate scene
- `R:SMARTHOME TARGET parameter value tolerance` - Set environmental target
- `R:SMARTHOME MONITOR` - Check environmental status

### Sensor Network
- `R:SENSOR ADD sensor_id type location` - Add sensor to network
- `R:SENSOR COLLECT` - Collect data from all sensors
- `R:SENSOR ANALYZE sensor_id parameter` - Analyze trends
- `R:SENSOR PREDICT sensor_id parameter steps` - Predict future values

### Advanced Robotics
- `R:ROBOT PLAN start_x start_y goal_x goal_y` - Plan path
- `R:ROBOT MISSION x1,y1 x2,y2 x3,y3` - Execute multi-waypoint mission
- `R:ROBOT SCAN` - Scan environment with sensors
- `R:ROBOT AVOID` - Enable obstacle avoidance
- `R:ROBOT LEARN` - Learn and map environment
- `R:ROBOT GOTO x y z` - Move to specific position

## New Logo Commands

### IoT Commands
- `IOTDISCOVER` - Discover IoT devices (sets IOT_DEVICES variable)
- `IOTCONNECT [device_id]` - Connect to devices (sets IOT_CONNECTED)
- `IOTREAD device_id` - Read device data (sets IOT_* variables)
- `SMARTHOME` - Setup smart home (sets SMART_DEVICES)

### Robotics Commands
- `ROBOTPLAN start_x start_y goal_x goal_y` - Plan path (sets PATH_STEPS)
- `ROBOTSCAN` - Scan environment (sets SCAN_RANGE, OBJECTS_COUNT)
- `ROBOTAVOID` - Obstacle avoidance (sets AVOID_RESULT)
- `ROBOTLEARN` - Environment mapping (sets MAP_OBSTACLES)

### Sensor Commands
- `SENSORCOLLECT` - Collect sensor data (sets SENSORS_ACTIVE)
- `SENSORPREDICT sensor_id parameter` - Predict values (sets PREDICTION)

## Example Programs

### Smart Home Control
```pilot
T:Setting up smart home...
R:SMARTHOME SETUP
R:SMARTHOME TARGET temperature 22.0 1.0
R:IOT DISCOVER
R:IOT CONNECT
R:IOT READ temp_01
T:Current temperature: *TEMP_01_TEMPERATURE*°C
```

### Robot Navigation
```pilot
T:Robot navigation demo...
R:ROBOT PLAN 0 0 10 15
T:Path planned with *PATH_LENGTH* steps
R:ROBOT SCAN
T:Objects detected: *OBJECTS_DETECTED*
R:ROBOT MISSION 5,5 10,10 15,15
T:Mission status: *MISSION_STATUS*
```

### Sensor Analytics
```pilot
R:SENSOR ADD temp_office temperature Office
R:SENSOR COLLECT
R:SENSOR ANALYZE temp_office temperature
R:SENSOR PREDICT temp_office temperature 5
T:Prediction: *PREDICTION*
```

### Logo IoT Demo
```logo
IOTDISCOVER
IOTCONNECT
REPEAT 5 [
  IOTREAD temp_01
  FORWARD IOT_TEMPERATURE
  RIGHT 72
]
```

## Variables Set by Commands

### IoT Variables
- `IOT_DEVICES` - Number of discovered devices
- `IOT_CONNECTED` - Number of connected devices
- `IOT_TEMPERATURE`, `IOT_HUMIDITY`, etc. - Device readings
- `SMART_DEVICES` - Smart home devices connected

### Robotics Variables
- `PATH_LENGTH`, `PATH_STEPS` - Path planning results
- `SCAN_RANGE` - LIDAR scan range
- `OBJECTS_COUNT`, `OBJECTS_DETECTED` - Object detection
- `MAP_OBSTACLES` - Number of mapped obstacles
- `MISSION_STATUS` - Current mission status
- `ROBOT_X`, `ROBOT_Y` - Robot position

### Sensor Variables
- `SENSORS_ACTIVE` - Number of active sensors
- `SENSOR_[ID]_[PARAM]` - Individual sensor readings
- `TREND_[PARAM]` - Trend analysis results
- `PREDICTION` - Predicted values

## Educational Applications

1. **Smart Home Projects**: Learn about IoT, automation, and environmental control
2. **Robotics Education**: Path planning, navigation, and AI concepts
3. **Data Science**: Sensor data collection, analysis, and prediction
4. **Systems Integration**: Combining multiple technologies
5. **Environmental Monitoring**: Real-world data collection and analysis

## Simulation Features

All IoT and robotics features work in simulation mode, making them perfect for educational use without requiring physical hardware. The system generates realistic simulated data and responses for all devices and sensors.