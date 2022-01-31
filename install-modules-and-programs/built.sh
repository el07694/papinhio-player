#!/bin/bash

# This scripts install all the necessary tools to work from scratch with project
# Papinhio player
# created by Chris Pappas
# Contact E-mail: el07694@gmail.com

# This scripts is suitable for Ubuntu Desktop 21.10 LTS fresh install
# It may works for other Ubuntu desktop versions but please check the output to be sure that everything worked well!

# This script needs root priviledges  so change "root-password-here-please" in the above command to the root password, so the script can install the necessary tools without the need to always ask for password.
echo "root-password-here-please" | sudo bash


# Also note that when the icecast2 radio server installation finished, then you will prompt to set up some configuration passwords.

#1. Modifications and installs for python programming language.

#1.1 Install python3.9 if it's not installed
apt-get -y install python3.9

#1.2 Create python alias so you don't nead to type python, use python instead.

echo "alias python='python3.9'" >> ~/.bash_aliases
source ~/.bash_aliases

#1.3 Run auto remove to clean
apt -y autoremove

#1.4 Download and install pip (maybe also pip3)
apt -y install python3-pip

#1.5 Prevent python to create __pycache__ directory
echo "PYTHONPYCACHEPREFIX=\$TMPDIR" >> ~/.bashrc
echo "export PYTHONDONTWRITEBYTECODE=1" >> /etc/environment


#2. Install python modules (with pip command in most cases)

#2.1 Install PyInstaller
pip install pyinstaller

#2.2 Install PyQt5
pip install PyQt5 PyQt5-tools PyQt5-sip PyQtWebEngine

#2.3 Install aiohttp
pip install aiohttp

#2.4 Install aiortc
pip install aiortc

#2.5 Install python-shout
apt-get -y install python3-dev libshout3-dev
pip install python-shout

#2.6 Install Qtdesigner (for PyQt5)
apt-get -y install python3-pyqt5
apt-get -y install qtcreator pyqt5-dev-tools
apt-get -y install qttools5-dev-tools

#2.7 Install python-docx
pip install python-docx

#2.8 Install docx2pdf
pip install docx2pdf

#2.9 Install pydub
pip install pydub

#2.10 Install numpy
pip install numpy

#2.11 Install pyaudio
apt-get -y install portaudio19-dev python-pyaudio
apt-get -y install libasound-dev
mkdir tmp
cd tmp
wget http://files.portaudio.com/archives/pa_stable_v190700_20210406.tgz
tar -zxvf pa_stable_v190700_20210406.tgz
./configure && make
make install
cd ..
rm -r tmp
apt-get -y install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
apt-get -y install ffmpeg
sudo apt-get -y install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
sudo apt-get -y install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
sudo apt-get -y install ffmpeg
sudo apt-get -y install python-pyaudio
sudo apt-get -y install python3-pyaudio
sudo apt-get -y install portaudio19-dev
#sudo apt -y install libpython-dev
mkdir tmp
cd tmp
sudo apt-get -y install git-all
git clone https://people.csail.mit.edu/hubert/git/pyaudio.git
cd pyaudio/
python3.9 setup.py install
cd ../..
rm -rf tmp
python3.9 pyaudio_patch.py

#2.12 Install miniaudio
pip uninstall -y cffi
python3.9 -m pip install cffi
mkdir tmp
cd tmp
git clone https://github.com/irmen/pyminiaudio.git
cd pyminiaudio
python3.9 setup.py build
python3.9 setup.py install
cd ../..
rm -r tmp
pip install miniaudio

#2.13 Install matplotlib
pip install matplotlib

#2.14 install b4s (skipped)
#pip install b4s

#2.15 install eyed3
pip install eyed3

#2.16 install google email service
pip install google-api-python-client
pip install google-auth-oauthlib

#2.17 install pytube
pip install pytube

#2.18 install moviepy
pip install moviepy

#2.19 install m3u_parser
pip install m3u_parser

#2.20 install m3u8
pip install m3u8

#2.21 install pynput (skipped)
#pip install pynput

#2.22 install email_validator
pip install email_validator

#2.23 install psutil
pip install psutil

#2.24 install mutagen
pip install mutagen

#2.25 install tinytag
pip install tinytag

#2.26 install inflect
pip install inflect

#2.27 install translate
pip install translate

#2.28 install mysql connector
python3.9 -m pip install mysql-connector-python

#2.29 install Selenium
pip install selenium
pip install webdriver_manager

#2.30 install comtypes (skipped)
#pip install comtypes

#2.31 install pycaw
pip install pycaw

#2.32 install google_images_search
pip install google_images_search


#3. install icecast-server
apt-get -y install icecast2
#Configuration file located in:
# gedit /etc/icecast2/icecast.xml
# Command for start icecast2 server
#sudo systemctl start icecast2
# Command for restart icecast2 server
#sudo systemctl restart icecast2


#4. Install sublime text editor
apt-get -y update
apt-get -y install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -
add-apt-repository -y "deb https://download.sublimetext.com/ apt/stable/"
apt-get -y update
apt-get -y install sublime-text


#5. Install vim text editor
apt-get -y install vim


#6. Install Anydesk
wget -qO - https://keys.anydesk.com/repos/DEB-GPG-KEY | sudo apt-key add -
echo "deb http://deb.anydesk.com/ all main" | sudo tee /etc/apt/sources.list.d/anydesk-stable.list
sudo apt -y update
sudo apt-get -y install libpangox-1.0-0
sudo apt-get -y install anydesk
CURRENT_WORKING_DIRECTORY=`pwd`
cd ~/.config/
rm -r autostart
mkdir autostart
cd autostart
printf "[Desktop Entry]\n\
Type=Application\n\
Exec="start-anydesk.sh"\n\
Hidden=false\n\
NoDisplay=false\n\
X-GNOME-Autostart-enabled=true\n\
Name[en_IN]=AnyDesk\n\
Name=AnyDesk\n\
Comment[en_IN]=Starts anyDesk remote control application as service\n\
Comment=Starts anyDesk remote control application as service\n" >> anydesk-as-service.sh.desktop
printf "#!/bin/bash\n\
anydesk -service" >> start-anydesk.sh
cd "${CURRENT_WORKING_DIRECTORY}"
#change the above password from anydesk connections
echo p2swex819 | sudo anydesk --set-password

#7. reset terminal (skipped)
#reset
#exec bash --login

#8. install sqlite3
apt-get -y install sqlite3


#9. Run python test script
python3.9 test_modules.py