from datetime import datetime

def find_when_to_play(Greece_time_case):
	now = datetime.now()
	now_hour = now.hour
	now_minute = now.minute
	if Greece_time_case == 1:
		next_hour_time_clip = now_hour+1
		if next_hour_time_clip>24:
			next_hour_time_clip = 1
		if next_hour_time_clip<=12:
			hour_1 = next_hour_time_clip
			hour_2 = hour_1 + 12
		else:
			hour_2 = next_hour_time_clip
			hour_1 = hour_2 - 12
			
		if hour_1<10:
			hour_1 = "0"+str(hour_1)
		if hour_2<10:
			hour_2 = "0"+str(hour_2)
			
		when_to_play = str(hour_1)+":00|"+(str(hour_2))+":00"
	elif Greece_time_case == 2:
		next_hour_time_clip = now_hour+1
		if next_hour_time_clip>24:
			next_hour_time_clip = 1
		if next_hour_time_clip<10:
			next_hour_time_clip = "0"+str(next_hour_time_clip)
			when_to_play = str(next_hour_time_clip)+":00"
	elif Greece_time_case == 3:
		if now_minute<30:
			next_hour_time_clip = now_hour
			if next_hour_time_clip>24:
				next_hour_time_clip = 1
			if next_hour_time_clip<12:
				hour_1 = next_hour_time_clip
				hour_2 = next_hour_time_clip+12
			else:
				hour_2 = next_hour_time_clip
				hour_1 = next_hour_time_clip-12
			if hour_1<10:
				hour_1 = "0"+str(hour_1)
			if hour_2<10:
				hour_2 = "0"+str(hour_2)
			when_to_play = str(hour_1)+":30|"+(str(hour_2))+":30"
		else:
			next_hour_time_clip = now_hour+1
			if next_hour_time_clip>24:
				next_hour_time_clip = 1
			if next_hour_time_clip<=12:
				hour_1 = next_hour_time_clip
				hour_2 = next_hour_time_clip+12
			else:
				hour_2 = next_hour_time_clip
				hour_1 = next_hour_time_clip-12
			if hour_1<10:
				hour_1 = "0"+str(hour_1)
			if hour_2<10:
				hour_2 = "0"+str(hour_2)
				when_to_play = str(hour_1)+":00|"+(str(hour_2))+":00"
	elif Greece_time_case == 4:
		if now_minute<30:
			next_hour_time_clip = now_hour
			if next_hour_time_clip>24:
				next_hour_time_clip = 1
			hour_1 = next_hour_time_clip
			if hour_1<10:
				hour_1 = "0"+str(hour_1)
			when_to_play = str(hour_1)+":30"
		else:
			next_hour_time_clip = now_hour+1
			if next_hour_time_clip>24:
				next_hour_time_clip = 1
			hour_1 = next_hour_time_clip
			if hour_1<10:
				hour_1 = "0"+str(hour_1) 
			
			when_to_play = str(hour_1)+":00"
	return when_to_play