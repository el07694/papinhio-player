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

def import_station_logos():
	station_logos = ["ΑΓΙΑ ΣΚΕΠΗ","ΑΓΙΟΣ ΑΝΔΡΕΑΣ","τη Υπερμάχω"]
	position = 0
	for station_logo in station_logos:
		position+= 1
		sound_file_item = sqlite3_functions.search_sound_files(station_logo)[0]
		description = sound_file_item["description"]
		rating = sound_file_item["rating"]
		duration_milliseconds = sound_file_item["duration_milliseconds"]
		duration_human = sound_file_item["duration_human"]
		original_path = sound_file_item["original_path"]
		filename = Path(sound_file_item["saved_path"]).stem
		station_logos_saved_path = os.path.abspath("../../disket-box/station-logos/"+filename+".mp3")
		shutil.copyfile(sound_file_item["saved_path"],station_logos_saved_path)
		station_logo = {
			"type":"sound_clips",
			"title":station_logo,
			"position":position,
			"description":description,
			"rating":rating,
			"volume":sound_file_item["volume"],
			"normalize":sound_file_item["normalize"],
			"pan":sound_file_item["pan"],
			"low_frequency":sound_file_item["low_frequency"],
			"high_frequency":sound_file_item["high_frequency"],
			"duration_milliseconds":duration_milliseconds,
			"duration_human":duration_human,
			"original_path":original_path,
			"saved_path":station_logos_saved_path
		}
		sqlite3_functions.import_station_logo(station_logo,1)