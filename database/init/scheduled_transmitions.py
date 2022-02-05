import os
import json
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
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def import_scheduled_transmitions():
	sound_files = sqlite3_functions.read_sound_files()
	playlists = sqlite3_functions.read_playlists()
	retransmitions = sqlite3_functions.read_retransmitions()

	#1. 22:35 - 07:00 ΣΤΑΜΑΤΗΣ ΣΠΑΝΟΥΔΑΚΗΣ (7 ΣΤΙΓΜΕΣ)
	now = datetime.now()
	start_datetime = str(now.replace(microsecond=0))
	end_datetime = str(now + relativedelta(years=10))

	time_settings = {
		"start_datetime":start_datetime,
		"hour_repeats":"one_time",
		"hour_repeats_information":"22:35:00",
		"end_datetime":end_datetime
	}
	time_settings = json.dumps(time_settings)

	transmition = {
		"title":"22:35 - 07:00 ΣΤΑΜΑΤΗΣ ΣΠΑΝΟΥΔΑΚΗΣ (7 ΣΤΙΓΜΕΣ)",
		"live":json.dumps({"is_live":False}),
		"frequency":"Καθημερινά",
		"time_settings":time_settings,
		"types":"['playlists']",
		"active":1,
		"repeat":1
	}

	transmition_items = []

	for playlist in playlists:
		if "7 στιγμές" in playlist[0]["playlist_title"] or "ΧΑΙΡΕ ΘΑΛΑΣΣΑ ΜΟΥ" in playlist[0]["playlist_title"]:
			transmition_item = {
				"relative_type":"playlists",
				"relative_number":playlist[0]["playlist_number"],
				"relative_time_seconds":"",
				"frequency_type":"one_time",
				"frequency_type_parameters":"",
				"default":0
			}
			transmition_items.append(transmition_item)

	sqlite3_functions.import_transmition(transmition,transmition_items)

	#2. 07:00 - 10:30 ΑΝΑΜΕΤΑΔΟΣΗ ΡΑΔΙΟΦΩΝΙΚΟΥ ΣΤΑΘΜΟΥ ΠΕΙΡΑΙΚΗΣ ΕΚΚΛΗΣΙΑΣ

	now = datetime.now()
	start_datetime = str(now.replace(microsecond=0))
	end_datetime = str(now + relativedelta(years=10))

	time_settings = {
		"start_datetime":start_datetime,
		"hour_repeats":"one_time",
		"hour_repeats_information":"07:00:00",
		"end_datetime":end_datetime
	}
	time_settings = json.dumps(time_settings)

	transmition = {
		"title":"07:00 - 10:30 ΑΝΑΜΕΤΑΔΟΣΗ ΡΑΔΙΟΦΩΝΙΚΟΥ ΣΤΑΘΜΟΥ ΠΕΙΡΑΙΚΗΣ ΕΚΚΛΗΣΙΑΣ",
		"live":json.dumps({"is_live":False}),
		"frequency":"Καθημερινά",
		"time_settings":time_settings,
		"types":"['retransmitions']",
		"active":1,
		"repeat":0
	}

	transmition_items = []
	

	for retransmition in retransmitions:
		if "Πειραϊκή εκκλησία" in retransmition["title"]:
			transmition_item = {
				"relative_type":"retransmitions",
				"relative_number":retransmition["number"],
				"relative_time_seconds":"",
				"frequency_type":"one_time",
				"frequency_type_parameters":"",
				"default":0
			}
			transmition_items.append(transmition_item)

	sqlite3_functions.import_transmition(transmition,transmition_items)

	#3. 10:30:00 - 11:16:43 ΜΙΚΡΟΣ ΠΑΡΑΚΛΗΤΙΚΟΣ ΚΑΝΟΝΑΣ ΕΙΣ ΤΗΝ ΥΠΕΡΑΓΙΑΝ ΘΕΟΤΟΚΟΝ

	now = datetime.now()
	start_datetime = str(now.replace(microsecond=0))
	end_datetime = str(now + relativedelta(years=10))

	time_settings = {
		"start_datetime":start_datetime,
		"hour_repeats":"one_time",
		"hour_repeats_information":"10:30:00",
		"end_datetime":end_datetime
	}
	time_settings = json.dumps(time_settings)

	transmition = {
		"title":"10:30:00 - 11:16:43 ΜΙΚΡΟΣ ΠΑΡΑΚΛΗΤΙΚΟΣ ΚΑΝΟΝΑΣ ΕΙΣ ΤΗΝ ΥΠΕΡΑΓΙΑΝ ΘΕΟΤΟΚΟΝ",
		"live":json.dumps({"is_live":False}),
		"frequency":"Καθημερινά",
		"time_settings":time_settings,
		"types":"['sound_files']",
		"active":1,
		"repeat":0
	}

	transmition_items = []

	for sound_file in sound_files:
		if "Η ΜΙΚΡΗ  ΠΑΡΑΚΛΗΣΗ ΣΤΗΝ ΠΑΝΑΓΙΑ - ΑΓΙΟΝ ΟΡΟΣ" in sound_file["title"]:
			transmition_item = {
				"relative_type":"sound_files",
				"relative_number":sound_file["number"],
				"relative_time_seconds":"",
				"frequency_type":"one_time",
				"frequency_type_parameters":"",
				"default":0
			}
			transmition_items.append(transmition_item)

	transmition, transmition_items = sqlite3_functions.import_transmition(transmition,transmition_items)

	#4. 11:16:43 - 11:30 ΤΟ ΣΥΝΑΞΑΡΙ ΤΗΣ ΗΜΕΡΑΣ (ΖΩΝΤΑΝΗ ΕΚΠΟΜΠΗ)

	now = datetime.now()
	start_datetime = str(now.replace(microsecond=0))
	end_datetime = str(now + relativedelta(years=10))

	time_settings = {
		"start_datetime":start_datetime,
		"start_after_transmitions":"["+str(transmition["number"])+"]",
		"hour_repeats":"one_time",
		"hour_repeats_information":"",
		"end_datetime":end_datetime,
		"duration_seconds":((30-16)*60)+(60-43)
	}
	time_settings = json.dumps(time_settings)

	transmition = {
		"title":"11:16:43 - 11:30 ΤΟ ΣΥΝΑΞΑΡΙ ΤΗΣ ΗΜΕΡΑΣ (ΖΩΝΤΑΝΗ ΕΚΠΟΜΠΗ)",
		"live":json.dumps({"is_live":True,"name":"","telephone":"","email":"","duration_seconds":20*60}),
		"frequency":"start_after_the_end_of_other_transmition",
		"time_settings":time_settings,
		"types":"[]",
		"active":1,
		"repeat":0
	}

	transmition_items = []

	transmition, transmition_items = sqlite3_functions.import_transmition(transmition,transmition_items)

	#5. 11:30 - 12:00 ΠΡΩΙΝΟ ΔΕΛΤΙΟ ΕΙΔΗΣΕΩΝ ΕΚΚΛΗΣΙΑΣΤΙΚΩΝ ΝΕΩΝ ΚΑΙ ΚΑΙΡΟΥ

	now = datetime.now()
	start_datetime = str(now.replace(microsecond=0))
	end_datetime = str(now + relativedelta(years=10))

	time_settings = {
		"start_datetime":start_datetime,
		"start_after_transmitions":"["+str(transmition["number"])+"]",
		"hour_repeats":"one_time",
		"hour_repeats_information":"",
		"end_datetime":end_datetime
	}
	time_settings = json.dumps(time_settings)

	transmition = {
		"title":"ΠΡΩΙΝΟ ΔΕΛΤΙΟ ΕΙΔΗΣΕΩΝ ΕΚΚΛΗΣΙΑΣΤΙΚΩΝ ΝΕΩΝ ΚΑΙ ΚΑΙΡΟΥ",
		"live":json.dumps({"is_live":False}),
		"frequency":"start_after_the_end_of_other_transmition",
		"time_settings":time_settings,
		"types":"['church_news','weather_news']",
		"active":1,
		"repeat":0
	}

	transmition_items = []

	transmition_item = {
		"relative_type":"church_news",
		"relative_number":-1,
		"relative_time_seconds":"00:00:00",
		"frequency_type":"one_time",
		"frequency_type_parameters":"",
		"default":1
	}
	transmition_items.append(transmition_item)

	transmition_item = {
		"relative_type":"weather_news",
		"relative_number":-1,
		"relative_time_seconds":"00:25:00",
		"frequency_type":"one_time",
		"frequency_type_parameters":"",
		"default":1
	}
	transmition_items.append(transmition_item)

	transmition, transmition_items = sqlite3_functions.import_transmition(transmition,transmition_items)


	#6. 12:00 - 15:00 ΑΠΟΛΥΤΙΚΙΑ ΑΓΙΩΝ, ΥΜΝΟΙ, ΨΑΛΜΟΙ, ΤΡΟΠΑΡΙΑ ΤΗΣ ΕΚΚΛΗΣΙΑΣ ΜΑΣ

	now = datetime.now()
	start_datetime = str(now.replace(microsecond=0))
	end_datetime = str(now + relativedelta(years=10))

	time_settings = {
		"start_datetime":start_datetime,
		"start_after_transmitions":"["+str(transmition["number"])+"]",
		"hour_repeats":"one_time",
		"hour_repeats_information":"",
		"end_datetime":end_datetime
	}
	time_settings = json.dumps(time_settings)

	transmition = {
		"title":"12:00 - 15:00 ΑΠΟΛΥΤΙΚΙΑ ΑΓΙΩΝ, ΥΜΝΟΙ, ΨΑΛΜΟΙ, ΤΡΟΠΑΡΙΑ ΤΗΣ ΕΚΚΛΗΣΙΑΣ ΜΑΣ",
		"live":json.dumps({"is_live":False}),
		"frequency":"start_after_the_end_of_other_transmition",
		"time_settings":time_settings,
		"types":"['playlists']",
		"active":1,
		"repeat":1
	}

	transmition_items = []

	for playlist in playlists:
		if "ΑΠΟΛΥΤΙΚΙΑ ΑΓΙΩΝ"==playlist[0]["playlist_title"] or "ΕΟΡΤΕΣ"==playlist[0]["playlist_title"] or "ΥΜΝΟΙ"==playlist[0]["playlist_title"] or "ΑΝΑΣΤΑΣΙΜΑ"==playlist[0]["playlist_title"]:
			transmition_item = {
				"relative_type":"playlists",
				"relative_number":playlist[0]["playlist_number"],
				"relative_time_seconds":"",
				"frequency_type":"one_time",
				"frequency_type_parameters":"",
				"default":0
			}
			transmition_items.append(transmition_item)

	
	transmition, transmition_items = sqlite3_functions.import_transmition(transmition,transmition_items)

	#7. 15:00 - ... ΠΑΡΑΚΛΗΤΙΚΟΣ ΚΑΝΟΝΑΣ ΣΕ ΑΓΙΟΝ Ή ΑΓΙΑ ΤΗΣ ΕΚΚΛΗΣΙΑΣ ΜΑΣ
	transmitions_numbers = []
	for playlist in playlists:
		if playlist[0]["playlist_title"] == "ΠΑΡΑΚΛΗΣΕΙΣ ΜΗΝΙΑΙΕΣ":
			for playlist_item in playlist:
				relative_number = playlist_item["relative_number"]
				for sound_file in sound_files:
					if sound_file["number"] == relative_number:
						title = sound_file["title"]
						day_of_month = title.split(".")[0]

						now = datetime.now()
						start_datetime = str(now.replace(microsecond=0))
						end_datetime = str(now + relativedelta(years=10))

						time_settings = {
							"start_datetime":start_datetime,
							"hour_repeats":"one_time",
							"month_repeats_information":"["+str(day_of_month)+"]",
							"hour_repeats_information":"15:00:00",
							"end_datetime":end_datetime
						}
						time_settings = json.dumps(time_settings)

						transmition = {
							"title":title,
							"live":json.dumps({"is_live":False}),
							"frequency":"month",
							"time_settings":time_settings,
							"types":"['sound_files']",
							"active":1,
							"repeat":0
						}

						transmition_items = []

						transmition_item = {
							"relative_type":"sound_files",
							"relative_number":relative_number,
							"relative_time_seconds":"",
							"frequency_type":"one_time",
							"frequency_type_parameters":"",
							"default":0
						}
						transmition_items.append(transmition_item)

						transmition, transmition_items = sqlite3_functions.import_transmition(transmition,transmition_items)

						transmitions_numbers.append(transmition["number"])

	#8. 15:30 - 19:00 ΟΜΙΛΙΕΣ (ΣΥΛΛΟΓΟΥ ΚΑΙ ΙΕΡΟΚΗΡΥΚΩΝ)
	now = datetime.now()
	start_datetime = str(now.replace(microsecond=0))
	end_datetime = str(now + relativedelta(years=10))

	time_settings = {
		"start_datetime":start_datetime,
		"start_after_transmitions":str(transmitions_numbers),
		"hour_repeats":"one_time",
		"hour_repeats_information":"",
		"end_datetime":end_datetime
	}
	time_settings = json.dumps(time_settings)

	transmition = {
		"title":"ΟΜΙΛΙΕΣ (ΣΥΛΛΟΓΟΥ ΚΑΙ ΙΕΡΟΚΗΡΥΚΩΝ)",
		"live":json.dumps({"is_live":False}),
		"frequency":"start_after_the_end_of_other_transmition",
		"time_settings":time_settings,
		"types":"['playlists']",
		"active":1,
		"repeat":0
	}

	transmition_items = []

	for playlist in playlists:
		if "ΟΜΙΛΙΕΣ"==playlist[0]["playlist_title"]:
			transmition_item = {
				"relative_type":"playlists",
				"relative_number":playlist[0]["playlist_number"],
				"relative_time_seconds":"",
				"frequency_type":"one_time",
				"frequency_type_parameters":"",
				"default":0
			}
			transmition_items.append(transmition_item)

	sqlite3_functions.import_transmition(transmition,transmition_items)

	#9. 19:00 - 21:30 ΖΩΝΤΑΝΕΣ ΕΚΠΟΜΠΕΣ

	#9.1 19:00 - 21:30 ΔΕΥΤΕΡΑ - ΣΥΝΤΡΟΦΙΑ ΜΕ ΤΟΝ ΒΕΛΙΣΑΡΗ
	now = datetime.now()
	start_datetime = str(now.replace(microsecond=0))
	end_datetime = str(now + relativedelta(years=10))

	time_settings = {
		"start_datetime":start_datetime,
		"week_days_selected":"[True,False,False,False,False,False,False]",
		"hour_repeats":"one_time",
		"hour_repeats_information":"19:00:00",
		"end_datetime":end_datetime
	}
	time_settings = json.dumps(time_settings)



	transmition = {
		"title":"19:00 - 21:30 ΔΕΥΤΕΡΑ - ΣΥΝΤΡΟΦΙΑ ΜΕ ΤΟΝ ΒΕΛΙΣΑΡΗ",
		"live":json.dumps({"is_live":False}),
		"frequency":"Εβδομαδιαία",
		"time_settings":time_settings,
		"types":"['retransmitions']",
		"active":1,
		"repeat":0
	}

	transmition_items = []
	

	for retransmition in retransmitions:
		if "Ραδιοφωνικός σταθμός: Συν πάσι τοις Αγίοις" in retransmition["title"]:
			transmition_item = {
				"relative_type":"retransmitions",
				"relative_number":retransmition["number"],
				"relative_time_seconds":"",
				"frequency_type":"one_time",
				"frequency_type_parameters":"",
				"default":0
			}
			transmition_items.append(transmition_item)

	sqlite3_functions.import_transmition(transmition,transmition_items)

	#9.2 19:00 - 21:30 ΤΡΙΤΗ - ΣΥΝΤΡΟΦΙΑ ΜΕ ΤΗΝ ΔΗΜΗΤΡΑ
	
	now = datetime.now()
	start_datetime = str(now.replace(microsecond=0))
	end_datetime = str(now + relativedelta(years=10))

	time_settings = {
		"start_datetime":start_datetime,
		"week_days_selected":"[False,True,False,False,False,False,False]",
		"hour_repeats":"one_time",
		"hour_repeats_information":"19:00:00",
		"end_datetime":end_datetime,
		"duration_seconds":2.5*60
	}

	time_settings = json.dumps(time_settings)

	transmition = {
		"title":"19:00 - 21:30 ΤΡΙΤΗ - ΣΥΝΤΡΟΦΙΑ ΜΕ ΤΗΝ ΔΗΜΗΤΡΑ",
		"live":json.dumps({"is_live":True,"name":"Δήμητρα ΜΠΑΜΠΙΛΗ - ΜΠΟΖΑ","telephone":"","email":"","duration_seconds":2.5*60*60}),
		"frequency":"Εβδομαδιαία",
		"time_settings":time_settings,
		"types":"['ip_calls']",
		"active":1,
		"repeat":1
	}

	transmition_items = []

	ip_call_item = {
		"title":"Τηλεφωνική επικοινωνία με ... ...",
		"name":"...",
		"surname":"...",
		"duration_milliseconds":1000*(2.5*60),
		"duration_human":"02:30:00"
	}

	ip_call_item = sqlite3_functions.import_ip_call_item(ip_call_item)

	transmition_item = {
		"relative_type":"ip_calls",
		"relative_number":ip_call_item["number"],
		"relative_time_seconds":"0",
		"frequency_type":"one_time",
		"frequency_type_parameters":"",
		"default":0
	}

	transmition_items.append(transmition_item)

	sqlite3_functions.import_transmition(transmition,transmition_items)

	#9.3 19:00 - 21:30 ΤΕΤΑΡΤΗ - ΣΥΝΤΡΟΦΙΑ ΜΕ ΤΗΝ ΜΑΓΔΑ

	now = datetime.now()
	start_datetime = str(now.replace(microsecond=0))
	end_datetime = str(now + relativedelta(years=10))

	time_settings = {
		"start_datetime":start_datetime,
		"week_days_selected":"[False,False,True,False,False,False,False]",
		"hour_repeats":"one_time",
		"hour_repeats_information":"19:00:00",
		"end_datetime":end_datetime,
		"duration_seconds":2.5*60
	}
	time_settings = json.dumps(time_settings)

	transmition = {
		"title":"19:00 - 21:30 ΤΕΤΑΡΤΗ - ΣΥΝΤΡΟΦΙΑ ΜΕ ΤΗΝ ΜΑΓΔΑ",
		"live":json.dumps({"is_live":True,"name":"Μάγδαληνή Κόκορη","telephone":"","email":"","duration_seconds":2.5*60*60}),
		"frequency":"Εβδομαδιαία",
		"time_settings":time_settings,
		"types":"[]",
		"active":1,
		"repeat":1
	}

	transmition_items = []

	ip_call_item = {
		"title":"Τηλεφωνική επικοινωνία με ... ...",
		"name":"...",
		"surname":"...",
		"duration_milliseconds":1000*(2.5*60),
		"duration_human":"02:30:00"
	}

	ip_call_item = sqlite3_functions.import_ip_call_item(ip_call_item)

	transmition_item = {
		"relative_type":"ip_calls",
		"relative_number":ip_call_item["number"],
		"relative_time_seconds":"0",
		"frequency_type":"one_time",
		"frequency_type_parameters":"",
		"default":0
	}

	transmition_items.append(transmition_item)

	sqlite3_functions.import_transmition(transmition,transmition_items)


	#9.4 19:00 - 21:30 ΠΕΜΠΤΗ - ΣΥΝΤΡΟΦΙΑ ΜΕ ΤΗΝ ΣΟΦΙΑ
	
	now = datetime.now()
	start_datetime = str(now.replace(microsecond=0))
	end_datetime = str(now + relativedelta(years=10))

	time_settings = {
		"start_datetime":start_datetime,
		"week_days_selected":"[False,False,False,True,False,False,False]",
		"hour_repeats":"one_time",
		"hour_repeats_information":"19:00:00",
		"end_datetime":end_datetime,
		"duration_seconds":2.5*60
	}
	time_settings = json.dumps(time_settings)

	transmition = {
		"title":"19:00 - 21:30 ΠΕΜΠΤΗ - ΣΥΝΤΡΟΦΙΑ ΜΕ ΤΗΝ ΣΟΦΙΑ",
		"live":json.dumps({"is_live":True,"name":"Σοφία Μπεκρή","telephone":"","email":"","duration_seconds":2.5*60*60}),
		"frequency":"Εβδομαδιαία",
		"time_settings":time_settings,
		"types":"[]",
		"active":1,
		"repeat":1
	}

	transmition_items = []

	ip_call_item = {
		"title":"Τηλεφωνική επικοινωνία με ... ...",
		"name":"...",
		"surname":"...",
		"duration_milliseconds":1000*(2.5*60),
		"duration_human":"02:30:00"
	}

	ip_call_item = sqlite3_functions.import_ip_call_item(ip_call_item)

	transmition_item = {
		"relative_type":"ip_calls",
		"relative_number":ip_call_item["number"],
		"relative_time_seconds":"0",
		"frequency_type":"one_time",
		"frequency_type_parameters":"",
		"default":0
	}

	transmition_items.append(transmition_item)

	sqlite3_functions.import_transmition(transmition,transmition_items)


	#9.5 19:00 - 21:30 ΠΑΡΑΣΚΕΥΗ - ΣΥΝΤΡΟΦΙΑ ΜΕ ΤΗΝ ΜΑΚΡΙΝΑ
	now = datetime.now()
	start_datetime = str(now.replace(microsecond=0))
	end_datetime = str(now + relativedelta(years=10))

	time_settings = {
		"start_datetime":start_datetime,
		"week_days_selected":"[False,False,False,False,True,False,False]",
		"hour_repeats":"one_time",
		"hour_repeats_information":"19:00:00",
		"end_datetime":end_datetime,
		"duration_seconds":2.5*60
	}
	time_settings = json.dumps(time_settings)

	transmition = {
		"title":"19:00 - 21:30 ΠΑΡΑΣΚΕΥΗ - ΣΥΝΤΡΟΦΙΑ ΜΕ ΤΗΝ ΜΑΚΡΙΝΑ",
		"live":json.dumps({"is_live":True,"name":"Μακρίνα Ράγκα","telephone":"","email":"","duration_seconds":2.5*60*60}),
		"frequency":"Εβδομαδιαία",
		"time_settings":time_settings,
		"types":"[]",
		"active":1,
		"repeat":1
	}

	transmition_items = []

	ip_call_item = {
		"title":"Τηλεφωνική επικοινωνία με ... ...",
		"name":"...",
		"surname":"...",
		"duration_milliseconds":1000*(2.5*60),
		"duration_human":"02:30:00"
	}

	ip_call_item = sqlite3_functions.import_ip_call_item(ip_call_item)

	transmition_item = {
		"relative_type":"ip_calls",
		"relative_number":ip_call_item["number"],
		"relative_time_seconds":"0",
		"frequency_type":"one_time",
		"frequency_type_parameters":"",
		"default":0
	}

	transmition_items.append(transmition_item)

	sqlite3_functions.import_transmition(transmition,transmition_items)


	#9.6 19:00 - 21:30 ΣΑΒΒΑΤΟ - ΣΥΝΤΡΟΦΙΑ ΜΕ ΤΟΝ ΒΑΣΙΛΕΙΟ ΜΠΑΜΠΙΛΗ
	
	now = datetime.now()
	start_datetime = str(now.replace(microsecond=0))
	end_datetime = str(now + relativedelta(years=10))

	time_settings = {
		"start_datetime":start_datetime,
		"week_days_selected":"[False,False,False,False,False,True,False]",
		"hour_repeats":"one_time",
		"hour_repeats_information":"19:00:00",
		"end_datetime":end_datetime,
		"duration_seconds":2.5*60
	}
	time_settings = json.dumps(time_settings)

	transmition = {
		"title":"19:00 - 21:30 ΣΑΒΒΑΤΟ - ΣΥΝΤΡΟΦΙΑ ΜΕ ΤΟΝ ΒΑΣΙΛΕΙΟ ΜΠΑΜΠΙΛΗ",
		"live":json.dumps({"is_live":True,"name":"Βασίλειος Μπαμπίλης","telephone":"","email":"","duration_seconds":2.5*60*60}),
		"frequency":"Εβδομαδιαία",
		"time_settings":time_settings,
		"types":"[]",
		"active":1,
		"repeat":1
	}

	transmition_items = []

	ip_call_item = {
		"title":"Τηλεφωνική επικοινωνία με ... ...",
		"name":"...",
		"surname":"...",
		"duration_milliseconds":1000*(2.5*60),
		"duration_human":"02:30:00"
	}

	ip_call_item = sqlite3_functions.import_ip_call_item(ip_call_item)

	transmition_item = {
		"relative_type":"ip_calls",
		"relative_number":ip_call_item["number"],
		"relative_time_seconds":"0",
		"frequency_type":"one_time",
		"frequency_type_parameters":"",
		"default":0
	}

	transmition_items.append(transmition_item)

	sqlite3_functions.import_transmition(transmition,transmition_items)



	#9.7 19:00 - 21:30 ΚΥΡΙΑΚΗ - ΣΥΝΤΡΟΦΙΑ ΜΕ ΤΟΝ ΒΑΣΙΛΕΙΟ ΤΣΟΥΠΡΑ
	now = datetime.now()
	start_datetime = str(now.replace(microsecond=0))
	end_datetime = str(now + relativedelta(years=10))

	time_settings = {
		"start_datetime":start_datetime,
		"week_days_selected":"[False,False,False,False,False,False,True]",
		"hour_repeats":"one_time",
		"hour_repeats_information":"19:00:00",
		"end_datetime":end_datetime,
		"duration_seconds":2.5*60
	}
	time_settings = json.dumps(time_settings)

	transmition = {
		"title":"19:00 - 21:30 ΚΥΡΙΑΚΗ - ΣΥΝΤΡΟΦΙΑ ΜΕ ΤΟΝ ΒΑΣΙΛΕΙΟ ΤΣΟΥΠΡΑ",
		"live":json.dumps({"is_live":True,"name":"Βασίλειος Τσούπρας","telephone":"","email":"","duration_seconds":2.5*60*60}),
		"frequency":"Εβδομαδιαία",
		"time_settings":time_settings,
		"types":"[]",
		"active":1,
		"repeat":1
	}

	transmition_items = []

	ip_call_item = {
		"title":"Τηλεφωνική επικοινωνία με ... ...",
		"name":"...",
		"surname":"...",
		"duration_milliseconds":1000*(2.5*60),
		"duration_human":"02:30:00"
	}

	ip_call_item = sqlite3_functions.import_ip_call_item(ip_call_item)

	transmition_item = {
		"relative_type":"ip_calls",
		"relative_number":ip_call_item["number"],
		"relative_time_seconds":"0",
		"frequency_type":"one_time",
		"frequency_type_parameters":"",
		"default":0
	}

	transmition_items.append(transmition_item)

	sqlite3_functions.import_transmition(transmition,transmition_items)


	#10. 21:30 - 22:00 ΒΡΑΔΥΝΟ ΔΕΛΤΙΟ ΕΚΚΛΗΣΙΑΣΤΙΚΩΝ ΝΕΩΝ ΚΑΙ ΚΑΙΡΟΥ
	now = datetime.now()
	start_datetime = str(now.replace(microsecond=0))
	end_datetime = str(now + relativedelta(years=10))

	time_settings = {
		"start_datetime":start_datetime,
		"hour_repeats":"one_time",
		"hour_repeats_information":"21:30:00",
		"end_datetime":end_datetime
	}
	time_settings = json.dumps(time_settings)

	transmition = {
		"title":"21:30 - 22:00 ΒΡΑΔΥΝΟ ΔΕΛΤΙΟ ΕΚΚΛΗΣΙΑΣΤΙΚΩΝ ΝΕΩΝ ΚΑΙ ΚΑΙΡΟΥ",
		"live":json.dumps({"is_live":False}),
		"frequency":"Καθημερινά",
		"time_settings":time_settings,
		"types":"['church_news','weather_news']",
		"active":1,
		"repeat":0
	}

	transmition_items = []

	transmition_item = {
		"relative_type":"church_news",
		"relative_number":-1,
		"relative_time_seconds":"00:00:00",
		"frequency_type":"one_time",
		"frequency_type_parameters":"",
		"default":1
	}
	transmition_items.append(transmition_item)

	transmition_item = {
		"relative_type":"weather_news",
		"relative_number":-1,
		"relative_time_seconds":"00:25:00",
		"frequency_type":"one time",
		"frequency_type_parameters":"",
		"default":1
	}
	transmition_items.append(transmition_item)

	transmition, transmition_items = sqlite3_functions.import_transmition(transmition,transmition_items)


	#11. 22:00 - 22:35 ΑΝΑΜΕΤΑΔΟΣΗ ΜΙΚΡΟΥ ΑΠΟΔΕΙΠΝΟΥ ΑΠΟ ΤΗΝ ΠΕΙΡΑΪΚΗ ΕΚΚΛΗΣΙΑ
	now = datetime.now()
	start_datetime = str(now.replace(microsecond=0))
	end_datetime = str(now + relativedelta(years=10))

	time_settings = {
		"start_datetime":start_datetime,
		"start_after_transmitions":"["+str(transmition["number"])+"]",
		"hour_repeats":"one_time",
		"hour_repeats_information":"22:00:00",
		"end_datetime":end_datetime
	}
	time_settings = json.dumps(time_settings)

	transmition = {
		"title":"ΑΝΑΜΕΤΑΔΟΣΗ ΜΙΚΡΟΥ ΑΠΟΔΕΙΠΝΟΥ ΑΠΟ ΤΗΝ ΠΕΙΡΑΪΚΗ ΕΚΚΛΗΣΙΑ",
		"live":json.dumps({"is_live":False}),
		"frequency":"start_after_the_end_of_other_transmition",
		"time_settings":time_settings,
		"types":"['retransmitions']",
		"active":1,
		"repeat":0
	}

	transmition_items = []
	

	for retransmition in retransmitions:
		if "Πειραϊκή εκκλησία" in retransmition["title"]:
			transmition_item = {
				"relative_type":"retransmitions",
				"relative_number":retransmition["number"],
				"relative_time_seconds":"",
				"frequency_type":"one_time",
				"frequency_type_parameters":"",
				"default":0
			}
			transmition_items.append(transmition_item)

	sqlite3_functions.import_transmition(transmition,transmition_items)

	#12. 22:35 - 24:00 ΣΤΑΜΑΤΗΣ ΣΠΑΝΟΥΔΑΚΗΣ (7 ΣΤΙΓΜΕΣ)
	#(merged with #1. 22:35 - 07:00 ΣΤΑΜΑΤΗΣ ΣΠΑΝΟΥΔΑΚΗΣ (7 ΣΤΙΓΜΕΣ))