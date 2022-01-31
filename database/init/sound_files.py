import os
import shutil
import sqlite3
from sqlite3 import Error
from pydub import AudioSegment
import sys
sys.path.append("../../")
import importlib
convert_time_function = importlib.import_module("src.python+.lib.convert_time_function")
sqlite3_functions = importlib.import_module("src.python+.lib.sqlite3_functions")
from pathlib import Path

def import_sound_files():
	test_contents_sound_files_mp3_folder = os.path.abspath("../../disket-box/test-contents/sound-files/mp3")
	test_contents_sound_files_images_folder = os.path.abspath("../../disket-box/test-contents/sound-files/images")
	
	read_mp3_directory(test_contents_sound_files_mp3_folder)


def read_mp3_directory(path):
	
	for filename in os.listdir(path):
		file_path = os.path.join(path, filename)
		if os.path.isfile(file_path):
			extension = file_path.split(".")[-1].lower()
			if extension=="mp3":
				filename_stem = Path(file_path).stem
				filename_stem_no_duration = ''.join(filename_stem.split("_")[0:-1])
				image_path = file_path.replace("/mp3/","/images/")
				image_path = os.path.dirname(os.path.abspath(image_path))

				correct_image_filename = ""
				for image_filename in os.listdir(image_path):
					image_file_path = os.path.join(image_path, image_filename)
					image_filename_stem = Path(image_file_path).stem
					if image_filename_stem==filename_stem_no_duration:
						correct_image_filename = image_file_path
						break

				if correct_image_filename=="":
					print("..............Error..............")
					print("mp3: "+str(file_path))
					print("-----------------")
				else:
					#1. copy mp3 to disket-box folder
					original_path = file_path
					filename_stem_no_duration = ' '.join(filename_stem.split("_")[0:-1])
					duration_in_milliseconds = int(filename_stem.split("_")[-1].replace(".mp3",""))

					saved_path = original_path.replace("/test-contents","").replace(filename_stem,filename_stem_no_duration)
					os.makedirs(os.path.dirname(saved_path), exist_ok=True)
					shutil.copyfile(original_path, saved_path)

					#2. copy image to disket-box folder
					image_original_path = correct_image_filename
					image_saved_path = image_original_path.replace("/test-contents","")
					os.makedirs(os.path.dirname(image_saved_path), exist_ok=True)
					shutil.copyfile(image_original_path, image_saved_path)

					sql = """ INSERT INTO `sound_files` (`title`, `artist`, `composer`, `author`, `album`, `year`, `image_path`, `image_title`, `description`, `rating`, `duration_milliseconds`, `duration_human`, `original_path`, `saved_path`) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """

					#sound_item = AudioSegment.from_file(original_path)
					#sound_item = sound_item.set_frame_rate(44800)
					
					if "σπανουδάκης" in original_path.lower() or "σπανουδακης" in original_path.lower() or "σταμάτης" in original_path.lower() or "σταμάτης" in original_path.lower():
						artist = "Σταμάτης Σπανουδάκης"
						year = "2009"
						composer = artist
						author = artist
					else:
						artist = "Άγνωστος καλλιτέχνης"
						year = ""
						composer = "Άγνωστος συνθέτης"
						author = "Άγνωστος στιχουργός"
					album = original_path.split("/")[-2:-1][0]
					comment = str(album)+" "+str(filename_stem)

					
					duration_human = convert_time_function.convert_duration_from_milliseconds_to_human(duration_in_milliseconds)

					#original_path_new = original_path.replace(".mp3","_"+str(duration_in_milliseconds)+".mp3")
					#file_handle = sound_item.export(original_path_new,format="mp3",tags={"title": filename_stem, "artist": artist,"album":album,"year":year,"comment":comment},cover=image_saved_path)
				
					

					sound_file_item = {
					    "type":"sound_files",
					    "title":filename_stem,
					    "artist":artist,
					    "composer":composer,
					    "author":author,
					    "album":album,
					    "year":year,
					    "genre":"Other",
					    "image_path":image_saved_path,
					    "image_title":filename_stem,
					    "description":"",
					    "rating":10,
					    "volume":100,
					    "normalize":0,
					    "pan":0,
					    "low_frequency":20,
					    "high_frequency":20000,
					    "duration_milliseconds":duration_in_milliseconds,
					    "duration_human":duration_human,
					    "original_path":original_path,
					    "saved_path":saved_path
					}
					sqlite3_functions.import_sound_file(sound_file_item)


			else:
				pass
		elif os.path.isdir(file_path):
			read_mp3_directory(file_path)