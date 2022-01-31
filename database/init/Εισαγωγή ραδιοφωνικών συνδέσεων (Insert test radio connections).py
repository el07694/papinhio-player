import os
import shutil
import sqlite3
from sqlite3 import Error
from pydub import AudioSegment
import sys
sys.path.append("..")
import importlib
sqlite3_functions = importlib.import_module("Αρχεία πηγαίου κώδικα εφαρμογής (Python).Αρχεία κώδικα python (Python files).Συναρτήσεις sqlite3 (Sqlite3 functions)")

def main():
	
	radio_connection_images = []
	radio_connection_images.append("radio_clip_art.png")
	radio_connection_images.append("radio_clip_art.png")
	radio_connection_images.append("radio_clip_art.png")
	
	for radio_connection_image in radio_connection_images:
		original_path = os.path.abspath("../Δισκοθήκη (Disket box)/Πρότυπα αρχεία κατά την εγκατάσταση του προγράμματος (Test install contents)/Εικόνες ραδιοφωνικών συνδέσων (Radio connection images)/"+radio_connection_image)
		saved_path = os.path.abspath("../Δισκοθήκη (Disket box)/Εικόνες ραδιοφωνικών σταθμών (Radio connection images)/"+radio_connection_image)
		if os.path.exists(original_path):
			if os.path.exists(saved_path)==False:	   
				shutil.copyfile(original_path,saved_path)	   
		else:
			print("Wrong image path: "+radio_connection_image)
			print("Installation terminated due the above error")
			sys.exit()
	
	radio_connections = []
	
	#Local connection 1 (icecast - mp3)
	radio_connections.append(("Δοκιμαστική ραδιοφωνική σύνδεση 1 (Icecast - mp3)", "Αιθαλίδου 18-20", os.path.abspath("../Δισκοθήκη (Disket box)/Εικόνες ραδιοφωνικών σταθμών (Radio connection images)/"+radio_connection_images[0]), "Χρήστος Παππάς", "6981017788", "", "el07694@gmail.com", "http://localhost", "Δοκιμαστικός ραδιοφωνικός σταθμός (Icecast 2 - mp3)","Other","localhost","ftp_username","ftp_password","localhost","mysql_username","mysql_password","mysql_database_name","$artist - $title","http://localhost/radio.php", "http", "localhost", "8000", "/listen.mp3", "icecast_username", "icecast_password", "128", "1", "2"))
	
	#Local connection 2 (icecast - ogg)
	radio_connections.append(("Δοκιμαστική ραδιοφωνική σύνδεση 2 (Icecast - ogg)", "Αιθαλίδου 18-20", os.path.abspath("../Δισκοθήκη (Disket box)/Εικόνες ραδιοφωνικών σταθμών (Radio connection images)/"+radio_connection_images[1]), "Χρήστος Παππάς", "6981017788", "", "el07694@gmail.com", "http://localhost", "Δοκιμαστικός ραδιοφωνικός σταθμός (Icecast 2 - ogg)","Other","localhost","ftp_username","ftp_password","localhost","mysql_username","mysql_password","mysql_database_name","$artist - $title","http://localhost/radio.php", "http", "localhost", "8000", "/listen.ogg", "icecast_username", "icecast_password", "128", "1", "2"))
	
	#Local connection 3 (aiortc)
	radio_connections.append(("Δοκιμαστική ραδιοφωνική σύνδεση 3 (Aiortc)", "Αιθαλίδου 18-20", os.path.abspath("../Δισκοθήκη (Disket box)/Εικόνες ραδιοφωνικών σταθμών (Radio connection images)/"+radio_connection_images[2]), "Χρήστος Παππάς", "6981017788", "", "el07694@gmail.com", "http://localhost", "Δοκιμαστικός ραδιοφωνικός σταθμός (Aiortc)","Other","localhost","ftp_username","ftp_password","localhost","mysql_username","mysql_password","mysql_database_name","$artist - $title","http://localhost/radio.php", "aiortc", "localhost", "8000", "", "icecast_username", "icecast_password", "128", "1", "2"))
	
	
	for radio_connection in radio_connections:
		radio_connection_item = {
			"title":radio_connection[0],
			"address":radio_connection[1],
			"image_path":radio_connection[2],
			"director":radio_connection[3],
			"telephone":radio_connection[4],
			"fax":radio_connection[5],
			"email":radio_connection[6],
			"site":radio_connection[7],
			"description":radio_connection[8],
			"genre":radio_connection[9],
			"web_server_hostname":radio_connection[10],
			"ftp_username":radio_connection[11],
			"ftp_password":radio_connection[12],
			"mysql_hostname":radio_connection[13],
			"mysql_username":radio_connection[14],
			"mysql_password":radio_connection[15],
			"mysql_database":radio_connection[16],
			"metadata":radio_connection[17],
			"radio_page_url":radio_connection[18],
			"radio_type":radio_connection[19],
			"radio_hostname":radio_connection[20],
			"radio_port":radio_connection[21],
			"radio_mount":radio_connection[22],
			"radio_username":radio_connection[23],
			"radio_password":radio_connection[24],
			"bit_rate":radio_connection[25],
			"mp3_stream":radio_connection[26],
			"channels":radio_connection[27]
		}
		sqlite3_functions.import_radio_connection(radio_connection_item)
		
main()