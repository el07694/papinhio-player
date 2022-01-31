import os
import shutil
import sqlite3
from sqlite3 import Error
from pydub import AudioSegment
import sys
sys.path.append("..")
import importlib
sqlite3_functions = importlib.import_module("Αρχεία πηγαίου κώδικα εφαρμογής (Python).Αρχεία κώδικα python (Python files).Συναρτήσεις sqlite3 (Sqlite3 functions)")

convert_time_function = importlib.import_module("Αρχεία πηγαίου κώδικα εφαρμογής (Python).Βοηθητικές συναρτήσεις (Ηelpful functions).Μετατροπή από milliseconds σε ανθρώπινη μορφή (Convert time function)")

def main():

	#case 1
	time_collection = {
		"type":"time_collection",
		"title":"Ηχητική συλλογή ώρα Ελλάδος (12 αρχεία) (1)",
		"case":1,
		"append":1,
		"append_relative_type":"sound_files",
		"append_relative_number":1
	}
	group_title = "Ηχητική συλλογή ώρα Ελλάδος (12 αρχεία) (1)"
	time_items = []
	original_paths = []
	saved_paths = []
	image_paths = []
	directory_folder = os.path.abspath("../Δισκοθήκη (Disket box)/Συλλογές ώρα Ελλάδος (Greece time files)/"+str(group_title))
	os.makedirs(directory_folder)
	for i in range(1,13):
		original_path = os.path.abspath("../Δισκοθήκη (Disket box)/Πρότυπα αρχεία κατά την εγκατάσταση του προγράμματος (Test install contents)/Συλογές ώρα Ελλάδας (Greece time files)/Συλλογή 1/"+str(i)+".mp3")
		saved_path = directory_folder+"/"+str(i)+".mp3"
		if i<10:
			when_to_play = "0"+str(i)+":00|"+str(i+12)+":00"
			image_path = os.path.abspath("../Δισκοθήκη (Disket box)/Πρότυπα αρχεία κατά την εγκατάσταση του προγράμματος (Test install contents)/Συλογές ώρα Ελλάδας (Greece time files)/Εικόνες Συλλογών ώρα Ελλάδας/clock-0"+str(i)+".png")
		else:
			when_to_play = str(i)+":00|"+str(i+12)+":00"
			image_path = os.path.abspath("../Δισκοθήκη (Disket box)/Πρότυπα αρχεία κατά την εγκατάσταση του προγράμματος (Test install contents)/Συλογές ώρα Ελλάδας (Greece time files)/Εικόνες Συλλογών ώρα Ελλάδας/clock-"+str(i)+".png")			
		original_paths.append(original_path)
		saved_paths.append(saved_path)
		image_paths.append(image_path)
		
		#shutil.copyfile(original_path,saved_path)
		segment = AudioSegment.from_file(original_path,format="mp3")
		duration_milliseconds = len(segment)
		duration_human = convert_time_function.convert_duration_from_milliseconds_to_human(duration_milliseconds)
		segment = segment.set_frame_rate(44800)
		title = "Η ώρα είναι: "+str(i)
		artist = "Χρήστος Παππάς"
		album = group_title
		year = 2021
		file_handle = segment.export(saved_path,format="mp3",tags={"title": title, "artist": artist,"year":2021,"comment":""},cover=image_path)
		time_items.append({
			"type":"time_item",
			"collection_number":1,
			"title":title,
			"when_to_play":when_to_play,
			"rating":5,
			"volume":100,
			"normalize":0,
			"pan":0,
			"low_frequency":20,
			"high_frequency":20000,
			"duration_milliseconds":duration_milliseconds,
			"duration_human":duration_human,
			"original_path":original_path,
			"saved_path":saved_path
		})
	sqlite3_functions.import_time_collection(time_collection,time_items)
		
	#case 2
	time_collection = {
		"type":"time_collection",
		"title":"Ηχητική συλλογή ώρα Ελλάδος (24 αρχεία) (2)",
		"case":2,
		"append":0,
		"append_relative_type":"",
		"append_relative_number":-1
	}
	group_title = "Ηχητική συλλογή ώρα Ελλάδος (24 αρχεία) (2)"
	rating = 5
	case = 2
	append = 0
	append_sound_file_number = -1
	time_items = []

	original_paths = []
	saved_paths = []
	image_paths = []
	directory_folder = os.path.abspath("../Δισκοθήκη (Disket box)/Συλλογές ώρα Ελλάδος (Greece time files)/"+str(group_title))
	os.makedirs(directory_folder)
	for i in range(1,25):
		original_path = os.path.abspath("../Δισκοθήκη (Disket box)/Πρότυπα αρχεία κατά την εγκατάσταση του προγράμματος (Test install contents)/Συλογές ώρα Ελλάδας (Greece time files)/Συλλογή 2/"+str(i)+".mp3")
		saved_path = directory_folder+"/"+str(i)+".mp3"
		if i<10:
			when_to_play = "0"+str(i)+":00"
			image_path = os.path.abspath("../Δισκοθήκη (Disket box)/Πρότυπα αρχεία κατά την εγκατάσταση του προγράμματος (Test install contents)/Συλογές ώρα Ελλάδας (Greece time files)/Εικόνες Συλλογών ώρα Ελλάδας/clock-0"+str(i)+".png")
		else:
			when_to_play = str(i)+":00"
			if i>12:
				j = i-12
			else:
				j = i
			if j<10:
				j = "0"+str(j)
			image_path = os.path.abspath("../Δισκοθήκη (Disket box)/Πρότυπα αρχεία κατά την εγκατάσταση του προγράμματος (Test install contents)/Συλογές ώρα Ελλάδας (Greece time files)/Εικόνες Συλλογών ώρα Ελλάδας/clock-"+str(j)+".png")			
		original_paths.append(original_path)
		saved_paths.append(saved_path)
		image_paths.append(image_path)
		
		#shutil.copyfile(original_path,saved_path)
		segment = AudioSegment.from_file(original_path,format="mp3")
		duration_milliseconds = len(segment)
		duration_human = convert_time_function.convert_duration_from_milliseconds_to_human(duration_milliseconds)
		segment = segment.set_frame_rate(44800)
		title = "Η ώρα είναι: "+str(i)
		artist = "Χρήστος Παππάς"
		album = group_title
		year = 2021
		file_handle = segment.export(saved_path,format="mp3",tags={"title": title, "artist": artist,"year":2021,"comment":""},cover=image_path)
		time_items.append({
			"type":"time_item",
			"collection_number":2,
			"title":title,
			"when_to_play":when_to_play,
			"rating":5,
			"volume":100,
			"normalize":0,
			"pan":0,
			"low_frequency":20,
			"high_frequency":20000,
			"duration_milliseconds":duration_milliseconds,
			"duration_human":duration_human,
			"original_path":original_path,
			"saved_path":saved_path
		})
	sqlite3_functions.import_time_collection(time_collection,time_items)	
	
	#case 3
	time_collection = {
		"type":"time_collection",
		"title":"Ηχητική συλλογή ώρα Ελλάδος (24 αρχεία) (3)",
		"case":3,
		"append":0,
		"append_relative_type":"",
		"append_relative_number":-1
	}
	group_title = "Ηχητική συλλογή ώρα Ελλάδος (24 αρχεία) (3)"
	rating = 5
	case = 3
	append = 0
	append_sound_file_number = -1
	original_paths = []
	saved_paths = []
	image_paths = []
	time_items = []
	directory_folder = os.path.abspath("../Δισκοθήκη (Disket box)/Συλλογές ώρα Ελλάδος (Greece time files)/"+str(group_title))
	os.makedirs(directory_folder)
	for i in range(1,13):
		original_path = os.path.abspath("../Δισκοθήκη (Disket box)/Πρότυπα αρχεία κατά την εγκατάσταση του προγράμματος (Test install contents)/Συλογές ώρα Ελλάδας (Greece time files)/Συλλογή 3/"+str(i)+".mp3")
		saved_path = directory_folder+"/"+str(i)+".mp3"
		if i<10:
			when_to_play = "0"+str(i)+":00|"+str(i+12)+":00"
			image_path = os.path.abspath("../Δισκοθήκη (Disket box)/Πρότυπα αρχεία κατά την εγκατάσταση του προγράμματος (Test install contents)/Συλογές ώρα Ελλάδας (Greece time files)/Εικόνες Συλλογών ώρα Ελλάδας/clock-0"+str(i)+".png")
		else:
			when_to_play = str(i)+":00|"+str(i+12)+":00"
			image_path = os.path.abspath("../Δισκοθήκη (Disket box)/Πρότυπα αρχεία κατά την εγκατάσταση του προγράμματος (Test install contents)/Συλογές ώρα Ελλάδας (Greece time files)/Εικόνες Συλλογών ώρα Ελλάδας/clock-"+str(i)+".png")			
		original_paths.append(original_path)
		saved_paths.append(saved_path)
		image_paths.append(image_path)
		
		#shutil.copyfile(original_path,saved_path)
		segment = AudioSegment.from_file(original_path,format="mp3")
		duration_milliseconds = len(segment)
		duration_human = convert_time_function.convert_duration_from_milliseconds_to_human(duration_milliseconds)
		segment = segment.set_frame_rate(44800)
		title = "Η ώρα είναι: "+str(i)
		artist = "Χρήστος Παππάς"
		album = group_title
		year = 2021
		file_handle = segment.export(saved_path,format="mp3",tags={"title": title, "artist": artist,"year":2021,"comment":""},cover=image_path)
		time_items.append({
			"type":"time_item",
			"collection_number":3,
			"title":title,
			"when_to_play":when_to_play,
			"rating":5,
			"volume":100,
			"normalize":0,
			"pan":0,
			"low_frequency":20,
			"high_frequency":20000,
			"duration_milliseconds":duration_milliseconds,
			"duration_human":duration_human,
			"original_path":original_path,
			"saved_path":saved_path
		})
		
		original_path = os.path.abspath("../Δισκοθήκη (Disket box)/Πρότυπα αρχεία κατά την εγκατάσταση του προγράμματος (Test install contents)/Συλογές ώρα Ελλάδας (Greece time files)/Συλλογή 3/"+str(i)+"-30.mp3")
		saved_path = directory_folder+"/"+str(i)+"-30.mp3"
		if i<10:
			when_to_play = "0"+str(i)+":30|"+str(i+12)+":30"
			image_path = os.path.abspath("../Δισκοθήκη (Disket box)/Πρότυπα αρχεία κατά την εγκατάσταση του προγράμματος (Test install contents)/Συλογές ώρα Ελλάδας (Greece time files)/Εικόνες Συλλογών ώρα Ελλάδας/clock-0"+str(i)+"-30.png")
		else:
			when_to_play = str(i)+":30|"+str(i+12)+":30"
			image_path = os.path.abspath("../Δισκοθήκη (Disket box)/Πρότυπα αρχεία κατά την εγκατάσταση του προγράμματος (Test install contents)/Συλογές ώρα Ελλάδας (Greece time files)/Εικόνες Συλλογών ώρα Ελλάδας/clock-"+str(i)+"-30.png")		   
		original_paths.append(original_path)
		saved_paths.append(saved_path)
		image_paths.append(image_path)
		
		#shutil.copyfile(original_path,saved_path)
		segment = AudioSegment.from_file(original_path,format="mp3")
		duration_milliseconds = len(segment)
		duration_human = convert_time_function.convert_duration_from_milliseconds_to_human(duration_milliseconds)
		segment = segment.set_frame_rate(44800)
		title = "Η ώρα είναι: "+str(i)+":30"
		artist = "Χρήστος Παππάς"
		album = group_title
		year = 2021
		file_handle = segment.export(saved_path,format="mp3",tags={"title": title, "artist": artist,"year":2021,"comment":""},cover=image_path)
		time_items.append({
			"type":"time_item",
			"collection_number":3,
			"title":title,
			"when_to_play":when_to_play,
			"rating":5,
			"volume":100,
			"normalize":0,
			"pan":0,
			"low_frequency":20,
			"high_frequency":20000,
			"duration_milliseconds":duration_milliseconds,
			"duration_human":duration_human,
			"original_path":original_path,
			"saved_path":saved_path
		})
	
	sqlite3_functions.import_time_collection(time_collection,time_items)
	
	#case 4
	time_collection = {
		"type":"time_collection",
		"title":"Ηχητική συλλογή ώρα Ελλάδος (48 αρχεία) (4)",
		"case":4,
		"append":0,
		"append_relative_type":"",
		"append_relative_number":-1
	}

	group_title = "Ηχητική συλλογή ώρα Ελλάδος (48 αρχεία) (4)"
	rating = 5
	case = 4
	append = 0
	append_sound_file_number = -1
	original_paths = []
	saved_paths = []
	image_paths = []
	directory_folder = os.path.abspath("../Δισκοθήκη (Disket box)/Συλλογές ώρα Ελλάδος (Greece time files)/"+str(group_title))
	os.makedirs(directory_folder)
	time_items = []
	for i in range(1,25):
		original_path = os.path.abspath("../Δισκοθήκη (Disket box)/Πρότυπα αρχεία κατά την εγκατάσταση του προγράμματος (Test install contents)/Συλογές ώρα Ελλάδας (Greece time files)/Συλλογή 4/"+str(i)+".mp3")
		saved_path = directory_folder+"/"+str(i)+".mp3"
		if i<10:
			when_to_play = "0"+str(i)+":00"
			image_path = os.path.abspath("../Δισκοθήκη (Disket box)/Πρότυπα αρχεία κατά την εγκατάσταση του προγράμματος (Test install contents)/Συλογές ώρα Ελλάδας (Greece time files)/Εικόνες Συλλογών ώρα Ελλάδας/clock-0"+str(i)+".png")
		else:
			when_to_play = str(i)+":00"
			if i>12:
				j = i-12
			else:
				j = i
			if j<10:
				j = "0"+str(j)
			image_path = os.path.abspath("../Δισκοθήκη (Disket box)/Πρότυπα αρχεία κατά την εγκατάσταση του προγράμματος (Test install contents)/Συλογές ώρα Ελλάδας (Greece time files)/Εικόνες Συλλογών ώρα Ελλάδας/clock-"+str(j)+".png")			
		original_paths.append(original_path)
		saved_paths.append(saved_path)
		image_paths.append(image_path)
		
		#shutil.copyfile(original_path,saved_path)
		segment = AudioSegment.from_file(original_path,format="mp3")
		duration_milliseconds = len(segment)
		duration_human = convert_time_function.convert_duration_from_milliseconds_to_human(duration_milliseconds)
		segment = segment.set_frame_rate(44800)
		title = "Η ώρα είναι: "+str(i)
		artist = "Χρήστος Παππάς"
		album = group_title
		year = 2021
		file_handle = segment.export(saved_path,format="mp3",tags={"title": title, "artist": artist,"year":2021,"comment":""},cover=image_path)
		time_items.append({
			"type":"time_item",
			"collection_number":4,
			"title":title,
			"when_to_play":when_to_play,
			"rating":5,
			"volume":100,
			"normalize":0,
			"pan":0,
			"low_frequency":20,
			"high_frequency":20000,
			"duration_milliseconds":duration_milliseconds,
			"duration_human":duration_human,
			"original_path":original_path,
			"saved_path":saved_path
		})
		
		original_path = os.path.abspath("../Δισκοθήκη (Disket box)/Πρότυπα αρχεία κατά την εγκατάσταση του προγράμματος (Test install contents)/Συλογές ώρα Ελλάδας (Greece time files)/Συλλογή 4/"+str(i)+"-30.mp3")
		saved_path = directory_folder+"/"+str(i)+"-30.mp3"
		if i<10:
			when_to_play = "0"+str(i)+":30"
			image_path = os.path.abspath("../Δισκοθήκη (Disket box)/Πρότυπα αρχεία κατά την εγκατάσταση του προγράμματος (Test install contents)/Συλογές ώρα Ελλάδας (Greece time files)/Εικόνες Συλλογών ώρα Ελλάδας/clock-0"+str(i)+"-30.png")
		else:
			when_to_play = str(i)+":30"
			if i>12:
				j = i-12
			else:
				j = i
			if j<10:
				j = "0"+str(j)
			image_path = os.path.abspath("../Δισκοθήκη (Disket box)/Πρότυπα αρχεία κατά την εγκατάσταση του προγράμματος (Test install contents)/Συλογές ώρα Ελλάδας (Greece time files)/Εικόνες Συλλογών ώρα Ελλάδας/clock-"+str(j)+"-30.png")		   
		original_paths.append(original_path)
		saved_paths.append(saved_path)
		image_paths.append(image_path)

		#shutil.copyfile(original_path,saved_path)
		segment = AudioSegment.from_file(original_path,format="mp3")
		duration_milliseconds = len(segment)
		duration_human = convert_time_function.convert_duration_from_milliseconds_to_human(duration_milliseconds)
		segment = segment.set_frame_rate(44800)
		title = "Η ώρα είναι: "+str(i)+":30"
		artist = "Χρήστος Παππάς"
		album = group_title
		year = 2021
		file_handle = segment.export(saved_path,format="mp3",tags={"title": title, "artist": artist,"year":2021,"comment":""},cover=image_path)
		time_items.append({
			"type":"time_item",
			"collection_number":4,
			"title":title,
			"when_to_play":when_to_play,
			"rating":5,
			"volume":100,
			"normalize":0,
			"pan":0,
			"low_frequency":20,
			"high_frequency":20000,
			"duration_milliseconds":duration_milliseconds,
			"duration_human":duration_human,
			"original_path":original_path,
			"saved_path":saved_path
		})
	sqlite3_functions.import_time_collection(time_collection,time_items)
main()