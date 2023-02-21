# Raspberry_Pi
Raspberry Pi Codes


for Calculating Heart Rate and SPO2 download 
hrcalc.py
hrdump.py
max30102.py
testMAX30102.py 
and now run all files in python and in last execute testMAX30102 file to get the HR and SPO2 values in terminal.


for Temperature values download
mlx90614.py
testmlx.py
and run mlx90614 to execute and after that run testmlx for checking output



***for audio files to record and play or draw graph install following libraries---- some files can show error so ignore those files because new updates removes few older features and requirements....
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-pip
sudo apt-get install idle3
sudo pip3 install --upgrade adafruit-python-shell
cd ~
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/i2smic.py
sudo python3 i2smic.py
sudo reboot
sudo pip3 install PyAudio
sudo pip3 install TIME-python
sudo pip3 install DateTime
sudo pip3 install matplotlib
sudo pip3 install os-win
sudo pip3 install Py-OS
sudo pip3 install wavefile
sudo pip3 install PyWave
sudo pip3 install python-csv
sudo apt-get install libatlas-base-dev libportaudio2 libsound-dev libportaudio0 libportaudioccp0 libportaudio19-dev
python3 -m pip install --user sounddevice
python3 -m pip install --user scipy 
sudo pip3 install numpy
**** if numpy error occurs then use ****
sudo pip3 install numpy --upgrade --ignore-installed

*** for MQTT 
sudo pip3 install paho-mqtt
sudo pip3 install hashlib
sudo pip3 install TIME-python


**** for Tkinter
sudo apt-get install python3-tk


*** for i2s bus usage in temprature and HR sensor
sudo pip3 install smbus2
