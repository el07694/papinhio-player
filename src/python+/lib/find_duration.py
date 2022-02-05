from pydub import AudioSegment
import os
import sys

path = os.path.abspath("")

for filename in os.listdir(path):
	if "find_duration.py" not in filename:
		file_path = os.path.join(path, filename)
		mp3 = AudioSegment.from_mp3(file_path)
		duration = len(mp3)
		os.rename(filename, filename.replace(".mp3","_"+str(duration)+".mp3"))