import os
import shutil
import sqlite3
from sqlite3 import Error
from pydub import AudioSegment
import sys
sys.path.append("../../")
import importlib
from pathlib import Path

convert_time_function = importlib.import_module("src.python+.lib.convert_time_function")
sqlite3_functions = importlib.import_module("src.python+.lib.sqlite3_functions")


def import_playlist():

	sound_files = sqlite3_functions.read_sound_files()
	playlists = []
	for sound_file in sound_files:
		saved_path = sound_file["saved_path"]
		dir_name = os.path.dirname(os.path.abspath(saved_path))
		album_name = dir_name.split("/")[-1]
		playlist_found = False
		counter = 0
		for playlist in playlists:
			if playlist["name"]==album_name:
				playlists[counter]["sound_file_numbers"].append(sound_file["number"])
				playlist_found = True
			counter += 1

		if playlist_found == False:
			playlists.append({"name":album_name,"sound_file_numbers":[sound_file["number"]]})

	for playlist in playlists:
		title = playlist["name"]
		playlist_sound_file_numbers = playlist["sound_file_numbers"]
		playlist_import = []
		position = 0
		for playlist_sound_file_number in playlist_sound_file_numbers:
			position += 1
			playlist_import.append({"relative_type":"sound_files","relative_number":playlist_sound_file_number,"position":position})

		sqlite3_functions.import_playlist(title,playlist_import)