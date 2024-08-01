## Milesight® logger

Simple cross platform application for logging and displaying temperature and humidity data from Milesight® sensors 

<div align="center">
	<img src="/assets/app1.png" width="400px"/>
	<img src="/assets/app2.png" width="400px"/>
</div>


### Server
The server application listens for LoRaWAN® Gateway Messages. More information available [here](https://docs.loriot.io/space/NMS/6032911/Gateway+Message). 
The logged data is then made available to client applications using a simple rest API. Collected data is the temperature, humidity and sensor battery state.


### Hardware
The application was tested on the following sensor, but any technology using LoRaWAN® Gateway Messages in the format specified above will work.

<a href="https://www.milesight.com/iot/product/lorawan-sensor/em300-th"><img src="/assets/sensor.png" width="200px"></a>