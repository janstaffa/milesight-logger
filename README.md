## Milesight® logger

Simple cross platform application for logging and displaying temperature and humidity data from Milesight® sensors 

<div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 10px">
	<img src="/assets/app1.png" style="min-width: 250px; max-width: 600px"/>
	<img src="/assets/app1.png"style="min-width: 250px; max-width: 600px"/>
</div>


### Server
The server application listens for LoRaWAN® Gateway Messages. More information available [here](https://docs.loriot.io/space/NMS/6032911/Gateway+Message). 
The logged data is then made available to client applications using a simple rest API. Collected data is the temperature, humidity and sensor battery state.