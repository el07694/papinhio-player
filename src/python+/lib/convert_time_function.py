def convert_duration_from_milliseconds_to_human(duration_milliseconds):
	total_seconds = int(duration_milliseconds/1000)
	#1. find how much hours total_seconds are
	hours = int(total_seconds/(60*60))
	#2. calculate seconds remaining
	seconds_remaining = total_seconds-(hours*60*60)
	#3. find how much minutes seconds_remaining are
	minutes = int(seconds_remaining/60)
	#4. recalculate seconds remaining
	seconds = seconds_remaining-(minutes*60)
	
	#add leading zero
	if(seconds<10):
		seconds = "0"+str(seconds)
	if(minutes<10):
		minutes = "0"+str(minutes)
	if(hours<10):
		hours = "0"+str(hours)
	
	return str(hours)+":"+str(minutes)+":"+str(seconds)
