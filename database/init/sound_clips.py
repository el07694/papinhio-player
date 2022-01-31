import os
import shutil
import sqlite3
from sqlite3 import Error
from pydub import AudioSegment
import sys
sys.path.append("../..")
import importlib
convert_time_function = importlib.import_module("src.python+.lib.convert_time_function")
sqlite3_functions = importlib.import_module("src.python+.lib.sqlite3_functions")

def import_sound_clips():
	sound_clips_names = []
	sound_clips_names.append("airplane landing daniel simion.mp3")
	sound_clips_names.append("baby music box daniel simion.mp3")
	sound_clips_names.append("cartoon birds 2 daniel simion.mp3")
	sound_clips_names.append("cartoon telephone daniel simion.mp3")
	sound_clips_names.append("funny voices daniel simon.mp3")
	sound_clips_names.append("News Intro Maximilien 1801238420.mp3")
	sound_clips_names.append("old car engine daniel simion.mp3")
	sound_clips_names.append("old school bell daniel_simon.mp3")
	sound_clips_names.append("sms alert 5 daniel simon.mp3")
	sound_clips_names.append("Sony Battery AM Radio Tuning 1 SailorMoonFan 222190110.mp3")	
	
	for sound_clip_name in sound_clips_names:
		shutil.copyfile(os.path.abspath("../../disket-box/test-contents/sound-clips/"+sound_clip_name), os.path.abspath("../../disket-box/sound-clips/"+sound_clip_name))

	sql = """ INSERT INTO `sound_clips` (`title`, `position`, `description`, `rating`, `duration_milliseconds`, `duration_human`, `original_path`, `saved_path`) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?) """
	songs = []
	
	songs.append((r'airplane landing daniel simion',1,'airplane landing daniel simion',10,0,'',os.path.abspath("../../disket-box/test-contents/sound-clips/"+sound_clips_names[0]), os.path.abspath("../../disket-box/sound-clips/"+sound_clips_names[0])))
	songs.append((r'baby music box daniel simion',2,'baby music box daniel simion',10,0,'',os.path.abspath("../../disket-box/test-contents/sound-clips/"+sound_clips_names[1]), os.path.abspath("../../disket-box/sound-clips/"+sound_clips_names[1])))
	songs.append((r'cartoon birds 2 daniel simion',3,'cartoon birds 2 daniel simion',10,0,'',os.path.abspath("../../disket-box/test-contents/sound-clips/"+sound_clips_names[2]), os.path.abspath("../../disket-box/sound-clips/"+sound_clips_names[2])))
	songs.append((r'cartoon telephone daniel simion',4,'cartoon telephone daniel simion',10,0,'',os.path.abspath("../../disket-box/test-contents/sound-clips/"+sound_clips_names[3]), os.path.abspath("../../disket-box/sound-clips/"+sound_clips_names[3])))
	songs.append((r'funny voices daniel simon',5,'funny voices daniel simon',10,0,'',os.path.abspath("../../disket-box/test-contents/sound-clips/"+sound_clips_names[4]), os.path.abspath("../../disket-box/sound-clips/"+sound_clips_names[4])))
	songs.append((r'News Intro Maximilien 1801238420',6,'News Intro Maximilien 1801238420',10,0,'',os.path.abspath("../../disket-box/test-contents/sound-clips/"+sound_clips_names[5]), os.path.abspath("../../disket-box/sound-clips/"+sound_clips_names[5])))
	songs.append((r'old car engine daniel simion',7,'old car engine daniel simion',10,0,'',os.path.abspath("../../disket-box/test-contents/sound-clips/"+sound_clips_names[6]), os.path.abspath("../../disket-box/sound-clips/"+sound_clips_names[6])))
	songs.append((r'old school bell daniel_simon',8,'old school bell daniel_simon',10,0,'',os.path.abspath("../../disket-box/test-contents/sound-clips/"+sound_clips_names[7]), os.path.abspath("../../disket-box/sound-clips/"+sound_clips_names[7])))
	songs.append((r'sms alert 5 daniel simon',9,'sms alert 5 daniel simon',10,0,'',os.path.abspath("../../disket-box/test-contents/sound-clips/"+sound_clips_names[8]), os.path.abspath("../../disket-box/sound-clips/"+sound_clips_names[8])))
	songs.append((r'Sony Battery AM Radio Tuning 1 SailorMoonFan 222190110',10,'Sony Battery AM Radio Tuning 1 SailorMoonFan 222190110',10,0,'',os.path.abspath("../../disket-box/test-contents/sound-clips/"+sound_clips_names[9]), os.path.abspath("../../disket-box/sound-clips/"+sound_clips_names[9])))
	
	counter = 0
	for song in songs:
		song_item = songs[counter]
		counter = counter + 1
		saved_path = song_item[len(song_item)-1]
		sound_item = AudioSegment.from_file(saved_path,format="mp3")
		sound_item = sound_item.set_frame_rate(44800)
		file_handle = sound_item.export(saved_path,format="mp3",tags={"title": song_item[0], "artist": "","album":"","year":"","comment":""})

		duration_in_milliseconds = len(sound_item)
		duration_human = convert_time_function.convert_duration_from_milliseconds_to_human(duration_in_milliseconds)
		song_item = list(song_item)
		song_item[4]= duration_in_milliseconds
		song_item[5]= duration_human
		song_item = tuple(song_item)
		#`title`, `position`, `description`, `rating`, `duration_milliseconds`, `duration_human`, `original_path`, `saved_path`
		sound_clip = {
			"title":song_item[0],
			"position":song_item[1],
			"description":song_item[2],
			"rating":10,
			"volume":100,
			"normalize":0,
			"pan":0,
			"low_frequency":20,
			"high_frequency":20000,
			"duration_milliseconds":song_item[4],
			"duration_human":song_item[5],
			"original_path":song_item[6],
			"saved_path":song_item[7]
		}
		sound_clip = sqlite3_functions.import_sound_clip(sound_clip)