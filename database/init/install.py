import sys

from delete_database import *
from clear_disket_box import *
from create_database import *
from settings import *
from sound_files import *
from station_logos import *
from Greece_time_collections import *
from sound_clips import *
from retransmitions import *
from playlist import *
from player_list import *
from radio_stations import *
from scheduled_transmitions import *

print("1. Διαγραφή υπάρχουσας βάσης δεδομένων.")
delete_database_file()

print("2. Άδειασμα δισκοθήκης.")
empty_disket_box()

print("3. Δημιουργία βάσης δεδομένων και πινάκων.")
create_database_file()

print("4. Εισαγωγή αρχικών ρυθμίσεων.")
import_settings()

print("5. Εισαγωγή αρχείων ήχου.")
import_sound_files()

print("6. Εισαγωγή σημάτων σταθμών.")
import_station_logos()

print("7. Εισαγωγή συλλογών ώρα Ελλάδας.")
import_Greece_time_collections()

print("8. Εισαγωγή ηχητικών clips.")
import_sound_clips()

print("9. Εισαγωγή αναμεταδόσεων.")
import_retransmitions()

print("10. Εισαγωγή λιστών αναπαραγωγής.")
import_playlist()

print("11. Εισαγωγή δεδομένων player list.")
import_player_list_data()

print("12. Εισαγωγή ραδιοφωνικών συνδέσεων.")
import_radio_stations()

print("13. Εισαγωγή προγραμματισμένων μεταδόσεων.")
import_scheduled_transmitions()

sys.exit()