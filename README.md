# FingerPrint project

# Tools:
Python 3.8 - PyQt5(for creat desktop app) - MySQL Workbench .

# About Data :
Data are fingerprint images(bmp) [train & test] (Look at src/data).

## some hint:

Open Pythone project in terminal :

	§source/
	source bin/activat
	
	
# Create DATABASE in MYSQL 

## Using Terminal :
	
	sudo mysql -u root -p

	CREATE DATABASE (name);

	GRANT ALL PRIVILEGES ON (name_of_db).* TO '(root)'@'localhost';	




# PyQt5 -------to--------> Python:

To Convert from main.ui(pyqt5) to main.py(python) in terminal write : 
	
	pyuic5 -x main.ui -o main.py



