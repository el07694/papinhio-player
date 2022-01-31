import sys
import pyaudio
sys.path.append("../../")
import importlib
sqlite3_functions = importlib.import_module("src.python+.lib.sqlite3_functions")


def import_settings():

	p = pyaudio.PyAudio()
	info = p.get_host_api_info_by_index(0)
	numdevices = info.get('deviceCount')

	output_devices = [[0,0,"Καμία συσκευή αναπαραγωγής ήχου"]]

	counter = 1
	for i in range (0,numdevices):
		if p.get_device_info_by_host_api_device_index(0,i).get('maxOutputChannels')>0:
			output_devices.append([counter,i,str(p.get_device_info_by_host_api_device_index(0,i).get('name'))])
			counter += 1
	if len(output_devices)>1:
		primary_output_device = output_devices[1][2]
		primary_output_device_index = output_devices[1][1]
		secondary_output_device = output_devices[1][2]
		secondary_output_device_index = output_devices[1][1]
	else:
		primary_output_device = output_devices[0][2]
		primary_output_device_index = output_devices[0][1]
		secondary_output_device = output_devices[0][2]
		secondary_output_device_index = output_devices[0][1]

	input_devices = [[0,0,"Καμία συσκευή μικροφώνου"]]
	counter = 1
	for i in range (0,numdevices):
		if p.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')>0:
			input_devices.append([counter,i,p.get_device_info_by_host_api_device_index(0,i).get('name')])
			counter += 1
	if len(input_devices)>1:
		input_device = input_devices[1][2]
		input_device_index = input_devices[1][1]
	else:
		input_device = input_devices[0][2]
		input_device_index = input_devices[0][1]

	system_sound_volume = 50

	#default_font = "Times New Roman"
	default_font = "Calibri"
	default_font_size = 26
	default_font_color = "#000000"
	default_background_color = "#F1F1F1"
	default_buttons_background = "#F5F5F5"
	default_buttons_font_color = "#000000"
	#default_style = "WindowsVista"
	default_style = "Fusion"

	sql = """ INSERT INTO `settings` (`keyword`, `current_value`) VALUES ( ?, ?) """
	settings = []

	settings.append(("primary_output_device_name",primary_output_device))
	settings.append(("primary_output_device_number",primary_output_device_index))
	settings.append(("secondary_output_device_name",secondary_output_device))
	settings.append(("secondary_output_device_number",secondary_output_device_index))
	
	settings.append(("input_device_name",input_device))
	settings.append(("input_device_number",input_device_index))
	settings.append(("input_device_sound_volume",100))
	settings.append(("input_device_normalize",0))
	settings.append(("input_device_pan",0))
	settings.append(("input_device_low_frequency",20))
	settings.append(("input_device_high_frequency",20000))
	
	settings.append(("general_deck_sound_volume",50))
	settings.append(("general_deck_normalize",0))
	settings.append(("general_deck_pan",0))
	settings.append(("general_deck_low_frequency",20))
	settings.append(("general_deck_high_frequency",20000))
	
	settings.append(("player_list_display","Προβολή λίστας"))
	
	
	settings.append(("deck_1_relative_type",""))
	settings.append(("deck_1_relative_number",0))
	settings.append(("deck_1_current_duration_milliseconds",0))
	settings.append(("deck_1_repeats",0))
	settings.append(("deck_1_status",0))
	settings.append(("deck_1_total_time_milliseconds",0))

	settings.append(("deck_2_relative_type",""))
	settings.append(("deck_2_relative_number",0))
	settings.append(("deck_2_current_duration_milliseconds",0))
	settings.append(("deck_2_repeats",0))
	settings.append(("deck_2_status",0))
	settings.append(("deck_2_total_time_milliseconds",0))
	
	settings.append(("music_clip_deck_relative_type",""))	 
	settings.append(("music_clip_deck_relative_number",0))	  
	settings.append(("music_clip_deck_current_duration_milliseconds",0))	   
	settings.append(("music_clip_deck_repeats",0))	 
	settings.append(("music_clip_deck_status",0))
	settings.append(("music_clip_deck_total_time_milliseconds",0))
	
	
	settings.append(("default_font",default_font))
	settings.append(("default_font_size",default_font_size))
	settings.append(("default_font_color",default_font_color))
	settings.append(("default_background_color",default_background_color))
	settings.append(("default_button_background",default_buttons_background))
	settings.append(("default_button_font_color",default_buttons_font_color))
	settings.append(("default_style",default_style))
	
	settings.append(("player_field_change_position","1"))
	settings.append(("player_field_play","1"))
	settings.append(("player_field_title","1"))
	settings.append(("player_field_last_play","1"))
	settings.append(("player_field_next_play","1"))
	settings.append(("player_field_image","1"))
	settings.append(("player_field_prepare","1"))
	settings.append(("player_field_play_now","1"))
	settings.append(("player_field_remove","1"))
	settings.append(("player_field_duration","1"))
	settings.append(("player_field_artist","1"))
	settings.append(("player_field_album","1"))
	settings.append(("player_field_author","1"))
	settings.append(("player_field_composer","1"))
	settings.append(("player_field_year","1"))
	settings.append(("player_field_description","1"))
	settings.append(("player_field_from","1"))
	settings.append(("player_field_rating","1"))
	settings.append(("player_field_volume","1"))
	settings.append(("player_field_normalize","1"))
	settings.append(("player_field_pan","1"))
	settings.append(("player_field_frequencies","1"))
	settings.append(("player_field_repeat","1"))
	settings.append(("player_field_open_file","1"))
	
	settings.append(("program_component_time_lines","1"))
	settings.append(("program_component_general_deck","1"))
	settings.append(("program_component_deck_1","1"))
	settings.append(("program_component_deck_2","1"))
	settings.append(("program_component_music_clip_deck","1"))
	settings.append(("program_component_speackers_deck","1"))
	settings.append(("program_component_ip_calls","0"))
	settings.append(("program_component_player_list","1"))
	settings.append(("program_component_web_sites","1"))
	
	settings.append(("repeat_player_list","1"))
	settings.append(("auto_dj","1"))
			
	for setting in settings:
		sqlite3_functions.import_setting({"keyword":setting[0],"current_value":setting[1]})