# stageNS
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
-	Dependencies installation with $ python setup.py develop
4/ Go in the directory named telemetry2 with $ cd telemetry2
-	 execute $ pserve development.ini

Front installation: 
5/ Go in Front directory with $ cd C:\stageAJ\stageNS\Front\stage_front
-	Execute $ npm install
-	Execute $ npm run dev

Then you can open your browser and enter http://localhost:8080


