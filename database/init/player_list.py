import os
import sqlite3
from sqlite3 import Error
import sys

sys.path.append("..")
import importlib
convert_time_function = importlib.import_module("src.python+.lib.convert_time_function")
sqlite3_functions = importlib.import_module("src.python+.lib.sqlite3_functions")


def import_player_list_data():
    sound_files = sqlite3_functions.read_sound_files()

    position = 0

    for sound_file in sound_files:
        position += 1
        playlist_list_item = {
            "play":1,
            "relative_type":"sound_files",
            "relative_number":sound_file["number"],
            "repeats":0,
            "duration_milliseconds":sound_file["duration_milliseconds"],
            "duration_human":sound_file["duration_human"],
            "position":position
        }
        sqlite3_functions.import_player_list_item(playlist_list_item)
        

    sound_clips = sqlite3_functions.read_sound_clips()

    for sound_clip in sound_clips:
        position += 1
        playlist_list_item = {
            "play":1,
            "relative_type":"sound_clips",
            "relative_number":sound_clip["number"],
            "repeats":0,
            "duration_milliseconds":sound_clip["duration_milliseconds"],
            "duration_human":sound_clip["duration_human"],
            "position":position
        }
        sqlite3_functions.import_player_list_item(playlist_list_item)
    
    retransmitions = sqlite3_functions.read_retransmitions()
    for retransmition in retransmitions:
        position += 1
        playlist_list_item = {
            "play":1,
            "relative_type":"retransmitions",
            "relative_number":retransmition["number"],
            "repeats":0,
            "duration_milliseconds":3600000,
            "duration_human":"01:00:00",
            "position":position
        }
        sqlite3_functions.import_player_list_item(playlist_list_item)
        
        
    position += 1
    playlist_list_item = {
        "play":1,
        "relative_type":"time_collections",
        "relative_number":1,
        "repeats":0,
        "duration_milliseconds":0,
        "duration_human":"00:00:00",
        "position":position
    }
    sqlite3_functions.import_player_list_item(playlist_list_item)
