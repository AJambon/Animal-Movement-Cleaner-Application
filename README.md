# Animal Movement Cleaner Application

Bio-logging can be used to study animal movements. However, geolocation technologies are not perfect and can generate unaccurate positions. 
In that way, this application aims at giving an easy way to clean geolocated data thanks to algorithms, but also gives the opportunity to proceed it by hand. 
A 3D visualization is obtained thanks to CesiumJS. 


# How to install it
Prerequisites: 
Nodejs 10.16.0 (https://nodejs.org/en/ ), Python 3.7.3 (https://www.python.org/downloads/ )

Everything can be done from cmde

Installation:

1/ Create a directory for the application : here it will be named ‘application’ 
2/ Go in your new directory and execute $ git clone https://github.com/AJambon/stageNS.git

Back installation: 

2/Still in the same directory, execute $ pip install virtualenv

3/ Go in Back directory C:\application\stageNS\Back and 
-	create virtual environment with python $ -m venv virtualenvironmentname  
-	activate virtual environment with $ .\virtualenvironmentname\Scripts\activate
-	Add the path of the virtual environment folder in the gitignore file

4/ Go in the directory named telemetry2 with $ cd telemetry2
-	Dependencies installation with $ python setup.py develop
-	execute $ pserve development.ini

Front installation: 

5/ Go in src directory with $ cd C:\application\stageNS\Front\stage_front\src
- Open the file config.js
- Replace the apiUrl by your server name
```javascript 
export const myConfig = {
    apiUrl : 'http://localhost:6543'
}
``` 
6/ Go in Front directory with $ cd C:\application\stageNS\Front\stage_front
-	Execute $ npm install
-	Execute $ npm run dev

Then you can open your browser and enter http://localhost:8080


