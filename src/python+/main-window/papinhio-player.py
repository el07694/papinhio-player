from PyQt5 import QtCore, QtGui, QtWidgets
from qt_material import apply_stylesheet
import subprocess
import sys
import os
import importlib
import ctypes
import traceback
from multiprocessing import freeze_support, Queue
import time

from multiprocessing import Process, Queue, Pipe
from PyQt5.QtCore import pyqtSignal, QThread
from datetime import datetime

sys.path.append("../")
sys.path.append("../../")

### import main ui class ###
papinhio_player_ui = importlib.import_module("compiled-ui.main-window.papinhio-player")

### import database functions ###
database_functions = importlib.import_module("python+.lib.sqlite3_functions")

### import manage processes class ###
manage_processes_class = importlib.import_module("python+.main-window.manage-procceses")

### import manage microphone procces class ###
manage_microphone_class = importlib.import_module("python+.main-window.manage-microphone")

### manage player list table procceses ###
manage_player_list_table_class = importlib.import_module("python+.main-window.manage-player-list")

### import manage decks class ###
manage_decks_class = importlib.import_module("python+.main-window.manage-decks")

### import internet connection error class ###
internet_connection_error_ui = importlib.import_module("compiled-ui.main-window.errors-and-warnings.internet-error")

### import menu 1 ui classes ###

# Παράθυρο για πολλές χρήσεις #
search_scheduled_transmition_ui = importlib.import_module("compiled-ui.menu-3.scheduled-transmitions.search.search")

# Διαχείριση ραδιοφωνικών μεταδόσεων #
manage_radio_connections_ui = importlib.import_module("compiled-ui.menu-1.manage-radio-transmitions.manage-radio-transmitions")

# Αρχεία ήχου #
import_sound_file_ui = importlib.import_module("compiled-ui.menu-1.sound-files.import-sound-file-from-sound-file.import-sound-file-from-sound-file")
#import_sound_file_unsupported_type_error_ui = importlib.import_module("compiled-ui.menu-1.sound-files.Εισαγωγή αρχείου ήχου από αρχείο ήχου (Import sound file from sound file).Λάθος μορφή αρχείου (Wrong file type)")
#import_sound_file_unsupported_image_type_error_ui = importlib.import_module("compiled-ui.menu-1.sound-files.Εισαγωγή αρχείου ήχου από αρχείο ήχου (Import sound file from sound file).Λάθος μορφή αρχείου εικόνας (Wrong image file type)")
#import_sound_file_missing_data_error_ui = importlib.import_module("compiled-ui.menu-1.sound-files.Εισαγωγή αρχείου ήχου από αρχείο ήχου (Import sound file from sound file).Ελλιπή δεδομένα (missing data)")
#import_sound_file_save_question_ui = importlib.import_module("compiled-ui.menu-1.sound-files.Εισαγωγή αρχείου ήχου από αρχείο ήχου (Import sound file from sound file).Ερώτηση αποθήκευσης (Save question)")
import_sound_file_from_video_ui = importlib.import_module("compiled-ui.menu-1.sound-files.import-sound-file-from-video.import-sound-file-from-video")
export_sound_file_ui = importlib.import_module("compiled-ui.menu-1.sound-files.export.export")
edit_sound_file_ui = importlib.import_module("compiled-ui.menu-1.sound-files.edit.edit")
search_sound_file_ui = importlib.import_module("compiled-ui.menu-1.sound-files.search.search")
preview_sound_file_ui = importlib.import_module("compiled-ui.menu-1.sound-files.preview.preview")

# Λίστες αναπαραγωγής #
create_playlist_ui = importlib.import_module("compiled-ui.menu-1.playlists.create.create")
import_playlist_ui = importlib.import_module("compiled-ui.menu-1.playlists.import.import")
#import_playlist_unsupported_type_error_ui = importlib.import_module("compiled-ui.menu-1.playlists.Εισαγωγή λίστας αναπαραγωγής (Import playlist).Λάθος μορφή αρχείου (Wrong file type)")
export_playlist_as_sound_files_ui = importlib.import_module("compiled-ui.menu-1.playlists.export-playlist-as-sound-files.export-playlist-as-sound-files")
export_playlist_as_playlist_ui = importlib.import_module("compiled-ui.menu-1.playlists.export-playlist-as-playlist.export-playlist-as-playlist")
edit_playlist_ui = importlib.import_module("compiled-ui.menu-1.playlists.edit.edit")
search_playlist_ui = importlib.import_module("compiled-ui.menu-1.playlists.search.search")
preview_playlist_ui = importlib.import_module("compiled-ui.menu-1.playlists.preview.preview")

# Ηχητικά clips #
import_sound_clip_ui = importlib.import_module("compiled-ui.menu-1.sound-clips.import.import")
#import_sound_clip_unsupported_type_error_ui = importlib.import_module("compiled-ui.menu-1.sound-clips.Εισαγωγή ηχητικού clip (Import sound clip).Λάθος μορφή αρχείου (Wrong file type)")
export_sound_clip_ui = importlib.import_module("compiled-ui.menu-1.sound-clips.export.export")
edit_sound_clip_ui = importlib.import_module("compiled-ui.menu-1.sound-clips.edit.edit")
search_sound_clip_ui = importlib.import_module("compiled-ui.menu-1.sound-clips.search.search")
preview_sound_clip_ui = importlib.import_module("compiled-ui.menu-1.sound-clips.preview.preview")
classification_sound_clips_ui = importlib.import_module("compiled-ui.menu-1.sound-clips.classification.classification")

# Αναμεταδόσεις #
import_retransmition_ui = importlib.import_module("compiled-ui.menu-1.retransmitions.import.import")
export_retransmition_ui = importlib.import_module("compiled-ui.menu-1.retransmitions.export.export")
edit_retransmition_ui = importlib.import_module("compiled-ui.menu-1.retransmitions.edit.edit")
search_retransmition_ui = importlib.import_module("compiled-ui.menu-1.retransmitions.search.search")
preview_retransmition_ui = importlib.import_module("compiled-ui.menu-1.retransmitions.preview.preview")

# Σήμα σταθμού #
import_station_logo_ui = importlib.import_module("compiled-ui.menu-1.usefull-repeated.station-logos.import.import")
#import_station_logo_unsupported_type_error_ui = importlib.import_module("compiled-ui.menu-1.usefull-repeated.station-logos.Εισαγωγή σήματος σταθμού (Import station logo).Λάθος μορφή αρχείου (Wrong file type)")
export_station_logo_ui = importlib.import_module("compiled-ui.menu-1.usefull-repeated.station-logos.export.export")
edit_station_logo_ui = importlib.import_module("compiled-ui.menu-1.usefull-repeated.station-logos.edit.edit")
search_station_logo_ui = importlib.import_module("compiled-ui.menu-1.usefull-repeated.station-logos.search.search")
preview_station_logo_ui = importlib.import_module("compiled-ui.menu-1.usefull-repeated.station-logos.preview.preview")

# Ώρα Ελλάδας #
import_Greece_time_ui = importlib.import_module("compiled-ui.menu-1.usefull-repeated.Greece-time.import.import")
export_Greece_time_ui = importlib.import_module("compiled-ui.menu-1.usefull-repeated.Greece-time.export.export")
edit_Greece_time_ui = importlib.import_module("compiled-ui.menu-1.usefull-repeated.Greece-time.edit.edit")
search_Greece_time_ui = importlib.import_module("compiled-ui.menu-1.usefull-repeated.Greece-time.search.search")
preview_Greece_time_ui = importlib.import_module("compiled-ui.menu-1.usefull-repeated.Greece-time.preview.preview")

# Δελτίο εκκλησιαστικών ανακοινώσεων #
import_church_news_ui = importlib.import_module("compiled-ui.menu-1.usefull-repeated.church-news.import.import")
export_church_news_ui = importlib.import_module("compiled-ui.menu-1.usefull-repeated.church-news.export.export")
edit_church_news_ui = importlib.import_module("compiled-ui.menu-1.usefull-repeated.church-news.edit.edit")
search_church_news_ui = importlib.import_module("compiled-ui.menu-1.usefull-repeated.church-news.search.search")
preview_church_news_ui = importlib.import_module("compiled-ui.menu-1.usefull-repeated.church-news.preview.preview")

# Δελτίο καιρού #
import_weather_news_ui = importlib.import_module("compiled-ui.menu-1.usefull-repeated.weather-news.import.import")
export_weather_news_ui = importlib.import_module("compiled-ui.menu-1.usefull-repeated.weather-news.export.export")
edit_weather_news_ui = importlib.import_module("compiled-ui.menu-1.usefull-repeated.weather-news.edit.edit")
search_weather_news_ui = importlib.import_module("compiled-ui.menu-1.usefull-repeated.weather-news.search.search")
preview_weather_news_ui = importlib.import_module("compiled-ui.menu-1.usefull-repeated.weather-news.preview.preview")

# Ηχογράφηση #
start_record_ui = importlib.import_module("compiled-ui.menu-1.record.start-record")

# Αναφορές #
week_report_ui = importlib.import_module("compiled-ui.menu-1.reports.weekly-programm-report.weekly-programm-report")
player_history_report_ui = importlib.import_module("compiled-ui.menu-1.reports.player-history-report.player-history-report")
scheduled_transmition_report_ui = importlib.import_module("compiled-ui.menu-1.reports.scheduled-transmition-report.scheduled-transmition-report")
listeners_statistics_report_ui = importlib.import_module("compiled-ui.menu-1.reports.listeners-statistics-report.listeners-statistics-report")

# Διαχείριση συσκευών #
manage_output_devices_ui = importlib.import_module("compiled-ui.menu-1.manage-input-and-output-sound-devices.sound-output-devices-settings.sound-output-devices-settings")
#manage_output_devices_save_question_ui = importlib.import_module("compiled-ui.menu-1.manage-input-and-output-sound-devices.sound-output-devices-settings.Ερώτηση αποθήκευσης (Save question)")
#manage_output_unable_to_open_process_ui = importlib.import_module("compiled-ui.menu-1.manage-input-and-output-sound-devices.sound-output-devices-settings.Αδυναμία έναρξης διεργασίας (Unable to open process)")
manage_input_device_ui = importlib.import_module("compiled-ui.menu-1.manage-input-and-output-sound-devices.microphone-input-device-settings.microphone-input-device-setting")
#manage_input_device_save_question_ui = importlib.import_module("compiled-ui.menu-1.manage-input-and-output-sound-devices.microphone-input-device-settings.Ερώτηση αποθήκευσης (Save question)")

#Διαχείριση διεργασιών #
manage_proccesses_ui = importlib.import_module("compiled-ui.menu-1.manage-procceses.manage-procceses")

### import menu 2 ui classes ###

# Επιλογή θέματος #
choose_theme_ui = importlib.import_module("compiled-ui.menu-2.choose-theme.choose-theme")
change_theme_save_question_ui = importlib.import_module("compiled-ui.menu-2.choose-theme.save-question")

# Ορατά πεδία λίστας αναπαραγωγής #
visible_player_list_fields_ui = importlib.import_module("compiled-ui.menu-2.visible-player-list-fields.visible-player-list-fields")
#visible_player_list_fields_save_question_ui = importlib.import_module("compiled-ui.menu-2.Ορατα πεδία λίστας αναπαραγωγής (Visible player list fields).Ερώτηση αποθήκευσης (Save question)")

# Ορατά πεδία προγράμματος #
visible_programm_components_ui = importlib.import_module("compiled-ui.menu-2.visible-program-components.visible-program-components")
#visible_programm_components_save_question_ui = importlib.import_module("compiled-ui.menu-2.Ορατά πεδία προγράμματος (Visible programm components).Ερώτηση αποθήκευσης (Save question)")

### import menu 3 ui classes ###

# Προγραμματισμένες μεταδόσεις #
import_scheduled_transmition_ui = importlib.import_module("compiled-ui.menu-3.scheduled-transmitions.create.create")
manage_scheduled_transmitions_ui = importlib.import_module("compiled-ui.menu-3.scheduled-transmitions.explore.scheduled-transmitions")

# Ραδιοφωνικοί σταθμοί #
import_radio_station_ui = importlib.import_module("compiled-ui.menu-3.radio-stations.import.import")
edit_radio_stations_ui = importlib.import_module("compiled-ui.menu-3.radio-stations.edit.edit")

### import menu 4 ui classes ###

# Επικοινωνία #
contact_ui = importlib.import_module("compiled-ui.menu-4.contact.contact")

# Λίγα λόγια για το πρόγραμμα #
programm_abstract_information_ui = importlib.import_module("compiled-ui.menu-4.program-abstract-information.program-abstract-information")

### import internet connection error class ###
internet_connection_error_support_ui = importlib.import_module("python+.main-window.errors-and-warnings.internet-error")


### import menu 1 support ui classes ###

# Παράθυρο για πολλές χρήσεις #
search_scheduled_transmition_support_ui = importlib.import_module("python+.menu-3.scheduled-transmitions.search.search")


# Διαχείριση ραδιοφωνικών μεταδόσεων #
manage_radio_connections_support_ui = importlib.import_module("python+.menu-1.manage-radio-transmitions.manage-radio-transmitions")

# Αρχεία ήχου #
import_sound_file_support_ui = importlib.import_module("python+.menu-1.sound-files.import-sound-file-from-sound-file.import-sound-file-from-sound-file")
#import_sound_file_unsupported_type_error_support_ui = importlib.import_module("python+.menu-1.sound-files.Εισαγωγή αρχείου ήχου από αρχείο ήχου (Import sound file from sound file).Λάθος μορφή αρχείου (Wrong file type)")
#import_sound_file_unsupported_image_type_error_support_ui = importlib.import_module("python+.menu-1.sound-files.Εισαγωγή αρχείου ήχου από αρχείο ήχου (Import sound file from sound file).Λάθος μορφή αρχείου εικόνας (Wrong image file type)")
#import_sound_file_missing_data_error_support_ui = importlib.import_module("python+.menu-1.sound-files.Εισαγωγή αρχείου ήχου από αρχείο ήχου (Import sound file from sound file).Ελλιπή δεδομένα (missing data)")
#import_sound_file_save_question_support_ui = importlib.import_module("python+.menu-1.sound-files.Εισαγωγή αρχείου ήχου από αρχείο ήχου (Import sound file from sound file).Ερώτηση αποθήκευσης (Save question)")
import_sound_file_from_video_support_ui = importlib.import_module("python+.menu-1.sound-files.import-sound-file-from-video.import-sound-file-from-video")
export_sound_file_support_ui = importlib.import_module("python+.menu-1.sound-files.export.export")
edit_sound_file_support_ui = importlib.import_module("python+.menu-1.sound-files.edit.edit")
search_sound_file_support_ui = importlib.import_module("python+.menu-1.sound-files.search.search")
preview_sound_file_support_ui = importlib.import_module("python+.menu-1.sound-files.preview.preview")

# Λίστες αναπαραγωγής #
create_playlist_support_ui = importlib.import_module("python+.menu-1.playlists.create.create")
import_playlist_support_ui = importlib.import_module("python+.menu-1.playlists.import.import")
#import_playlist_unsupported_type_error_support_ui = importlib.import_module("python+.menu-1.playlists.Εισαγωγή λίστας αναπαραγωγής (Import playlist).Λάθος μορφή αρχείου (Wrong file type)")
export_playlist_as_sound_files_support_ui = importlib.import_module("python+.menu-1.playlists.export-playlist-as-sound-files.export-playlist-as-sound-files")
export_playlist_as_playlist_support_ui = importlib.import_module("python+.menu-1.playlists.export-playlist-as-playlist.export-playlist-as-playlist")
edit_playlist_support_ui = importlib.import_module("python+.menu-1.playlists.edit.edit")
search_playlist_support_ui = importlib.import_module("python+.menu-1.playlists.search.search")
preview_playlist_support_ui = importlib.import_module("python+.menu-1.playlists.preview.preview")

# Ηχητικά clips #
import_sound_clip_support_ui = importlib.import_module("python+.menu-1.sound-clips.import.import")
#import_sound_clip_unsupported_type_error_support_ui = importlib.import_module("python+.menu-1.sound-clips.import.Λάθος μορφή αρχείου (Wrong file type)")
export_sound_clip_support_ui = importlib.import_module("python+.menu-1.sound-clips.export.export")
edit_sound_clip_support_ui = importlib.import_module("python+.menu-1.sound-clips.edit.edit")
search_sound_clip_support_ui = importlib.import_module("python+.menu-1.sound-clips.search.search")
preview_sound_clip_support_ui = importlib.import_module("python+.menu-1.sound-clips.preview.preview")
classification_sound_clips_support_ui = importlib.import_module("python+.menu-1.sound-clips.classification.classification")

# Αναμεταδόσεις #
import_retransmition_support_ui = importlib.import_module("python+.menu-1.retransmitions.import.import")
export_retransmition_support_ui = importlib.import_module("python+.menu-1.retransmitions.export.export")
edit_retransmition_support_ui = importlib.import_module("python+.menu-1.retransmitions.edit.edit")
search_retransmition_support_ui = importlib.import_module("python+.menu-1.retransmitions.search.search")
preview_retransmition_support_ui = importlib.import_module("python+.menu-1.retransmitions.preview.preview")


# Σήμα σταθμού #
import_station_logo_support_ui = importlib.import_module("python+.menu-1.usefull-repeated.station-logos.import.import")
#import_station_logo_unsupported_type_error_support_ui = importlib.import_module("python+.menu-1.usefull-repeated.station-logos.Εισαγωγή σήματος σταθμού (Import station logo).Λάθος μορφή αρχείου (Wrong file type)")
export_station_logo_support_ui = importlib.import_module("python+.menu-1.usefull-repeated.station-logos.export.export")
edit_station_logo_support_ui = importlib.import_module("python+.menu-1.usefull-repeated.station-logos.edit.edit")
search_station_logo_support_ui = importlib.import_module("python+.menu-1.usefull-repeated.station-logos.search.search")
preview_station_logo_support_ui = importlib.import_module("python+.menu-1.usefull-repeated.station-logos.preview.preview")

# Ώρα Ελλάδας #
import_Greece_time_support_ui = importlib.import_module("python+.menu-1.usefull-repeated.Greece-time.import.import")
export_Greece_time_support_ui = importlib.import_module("python+.menu-1.usefull-repeated.Greece-time.export.export")
edit_Greece_time_support_ui = importlib.import_module("python+.menu-1.usefull-repeated.Greece-time.edit.edit")
search_Greece_time_support_ui = importlib.import_module("python+.menu-1.usefull-repeated.Greece-time.search.search")
preview_Greece_time_support_ui = importlib.import_module("python+.menu-1.usefull-repeated.Greece-time.preview.preview")

# Δελτίο εκκλησιαστικών ανακοινώσεων #
import_church_news_support_ui = importlib.import_module("python+.menu-1.usefull-repeated.church-news.import.import")
export_church_news_support_ui = importlib.import_module("python+.menu-1.usefull-repeated.church-news.export.export")
edit_church_news_support_ui = importlib.import_module("python+.menu-1.usefull-repeated.church-news.edit.edit")
search_church_news_support_ui = importlib.import_module("python+.menu-1.usefull-repeated.church-news.search.search")
preview_church_news_support_ui = importlib.import_module("python+.menu-1.usefull-repeated.church-news.preview.preview")

# Δελτίο καιρού #
import_weather_news_support_ui = importlib.import_module("python+.menu-1.usefull-repeated.weather-news.import.import")
export_weather_news_support_ui = importlib.import_module("python+.menu-1.usefull-repeated.weather-news.export.export")
edit_weather_news_support_ui = importlib.import_module("python+.menu-1.usefull-repeated.weather-news.edit.edit")
search_weather_news_support_ui = importlib.import_module("python+.menu-1.usefull-repeated.weather-news.search.search")
preview_weather_news_support_ui = importlib.import_module("python+.menu-1.usefull-repeated.weather-news.preview.preview")

# Ηχογράφηση #
start_record_support_ui = importlib.import_module("python+.menu-1.record.start-record")

# Αναφορές #
week_report_support_ui = importlib.import_module("python+.menu-1.reports.weekly-programm-report.weekly-programm-report")
player_history_report_support_ui = importlib.import_module("python+.menu-1.reports.player-history-report.player-history-report")
scheduled_transmition_report_support_ui = importlib.import_module("python+.menu-1.reports.scheduled-transmition-report.scheduled-transmition-report")
listeners_statistics_report_support_ui = importlib.import_module("python+.menu-1.reports.listeners-statistics-report.listeners-statistics-report")

# Διαχείριση συσκευών #
manage_output_devices_support_ui = importlib.import_module("python+.menu-1.manage-input-and-output-sound-devices.sound-output-devices-settings.sound-output-devices-settings")
#manage_output_devices_save_question_support_ui = importlib.import_module("python+.menu-1.manage-input-and-output-sound-devices.sound-output-devices-settings.Ερώτηση αποθήκευσης (Save question)")
#manage_output_unable_to_open_process_support_ui = importlib.import_module("python+.menu-1.manage-input-and-output-sound-devices.sound-output-devices-settings.Αδυναμία έναρξης διεργασίας (Unable to open process)")
manage_input_device_support_ui = importlib.import_module("python+.menu-1.manage-input-and-output-sound-devices.microphone-input-device-settings.microphone-input-device-setting")
#manage_input_device_save_question_support_ui = importlib.import_module("python+.menu-1.manage-input-and-output-sound-devices.microphone-input-device-settings.Ερώτηση αποθήκευσης (Save question)")

# Διαχείριση διεργασιών #
manage_proccesses_support_ui = importlib.import_module("python+.menu-1.manage-procceses.manage-procceses")

### import menu 2 support ui classes ###

# Επιλογή θέματος #
choose_theme_support_ui = importlib.import_module("python+.menu-2.choose-theme.choose-theme")
change_theme_save_question_support_ui = importlib.import_module("python+.menu-2.choose-theme.save-question")

# Ορατά πεδία λίστας αναπαραγωγής #
visible_player_list_fields_support_ui = importlib.import_module("python+.menu-2.visible-player-list-fields.visible-player-list-fields")
#visible_player_list_fields_save_question_support_ui = importlib.import_module("python+.menu-2.Ορατα πεδία λίστας αναπαραγωγής (Visible player list fields).Ερώτηση αποθήκευσης (Save question)")

# Ορατά πεδία προγράμματος #
visible_programm_components_support_ui = importlib.import_module("python+.menu-2.visible-program-components.visible-program-components") 
#visible_programm_components_save_question_support_ui = importlib.import_module("python+.menu-2.Ορατά πεδία προγράμματος (Visible programm components).Ερώτηση αποθήκευσης (Save question)")

### import menu 3 support ui classes ###

# Προγραμματισμένες μεταδόσεις #
import_scheduled_transmition_support_ui = importlib.import_module("python+.menu-3.scheduled-transmitions.create.create")
manage_scheduled_transmitions_support_ui = importlib.import_module("python+.menu-3.scheduled-transmitions.explore.scheduled-transmitions")

# Ραδιοφωνικοί σταθμοί #
import_radio_station_support_ui = importlib.import_module("python+.menu-3.radio-stations.import.import")
edit_radio_stations_support_ui = importlib.import_module("python+.menu-3.radio-stations.edit.edit")


### import menu 4 support ui classes ###

# Επικοινωνία #
contact_support_ui = importlib.import_module("python+.menu-4.contact.contact")

# Λίγα λόγια για το πρόγραμμα #
programm_abstract_information_support_ui = importlib.import_module("python+.menu-4.program-abstract-information.program-abstract-information")

class Papinhio_player:

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.app.setStyle("WindowsVista")
        #self.app.addLibraryPath(r"C:/msys64/mingw64/share/qt5/plugins/imageformats")
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = papinhio_player_ui.Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.showMaximized()
        
        self.database_functions = database_functions
        
        

        #decks state is saved (for close Event)
        self.decks_state_saved = False
        
        #manage_processes_class
        self.manage_processes_instance = manage_processes_class.Manage_Processes(self)
        

        #manage microphone class
        self.manage_microphone_instance = manage_microphone_class.Manage_Microphone_Deck(self)
        
        #manage_player_list_table_class
        self.manage_player_list_table_instance = manage_player_list_table_class.Manage_Player_List_Table(self)
        
        #manage_decks_class
        self.manage_decks_instance = manage_decks_class.Manage_Decks(self)
        

        #apply theme settings
        self.apply_theme_settings()
        
        
        #set False to all menu windows
        self.set_windows_boolean_value()
        
        #link menu items with actions (for example: open window)
        self.link_menus()
        '''
        
        #create proccess for program components
        self.programm_components_proccess_number = 21
        self.programm_components_mother_pipe, self.programm_components_child_pipe = Pipe()
        self.programm_components_queue = Queue()
        self.programm_components_emitter = Programm_Components_Emitter(self.programm_components_mother_pipe)
        self.programm_components_emitter.start()
        self.programm_components_child_process = Programm_Components_Child_Proc(self.programm_components_child_pipe, self.programm_components_queue)
        self.programm_components_child_process.start()
        self.programm_components_emitter.programm_components_ready.connect(self.programm_components_ready)
            
        counter = 0
        for process in self.manage_processes_instance.processes:
            if "process_number" in process:
                if process["process_number"]==self.programm_components_proccess_number:
                    self.manage_processes_instance.processes[counter]["pid"] = self.programm_components_child_process.pid
                    self.manage_processes_instance.processes[counter]["start_datetime"] = datetime.now()
                    self.manage_processes_instance.processes[counter]["status"] = "in_progress"
            counter += 1
        
        '''
        
        #close action
        self.MainWindow.closeEvent = lambda event:self.closeEvent(event)
        
        sys.exit(self.app.exec_())

    def programm_components_ready(self,settings):
        if settings["program_component_time_lines"]==1:
            self.ui.graphs_tab.show()
        else:
            self.ui.graphs_tab.hide()
        if settings["program_component_general_deck"]==1:
            self.ui.general_deck_frame.show()
        else:
            self.ui.general_deck_frame.hide()
        if settings["program_component_deck_1"]==1:
            self.ui.deck_1_frame.show()
        else:
            self.ui.deck_1_frame.hide()
        if settings["program_component_deck_2"]==1:
            self.ui.deck_2_frame.show()
        else:
            self.ui.deck_2_frame.hide()
        if settings["program_component_music_clip_deck"]==1:
            self.ui.music_clip_deck_frame.show()
        else:
            self.ui.music_clip_deck_frame.hide()
        if settings["program_component_speackers_deck"]==1:
            self.ui.speackers_deck_frame.show()
        else:
            self.ui.speackers_deck_frame.hide()
        if settings["program_component_ip_calls"]==1:
            self.ui.ip_calls_tabs.show()
        else:
            self.ui.ip_calls_tabs.hide()
        if settings["program_component_player_list"]==1:
            self.ui.player_list_frame.show()
        else:
            self.ui.player_list_frame.hide()
        if settings["program_component_web_sites"]==1:
            self.ui.web_pages.show()
        else:
            self.ui.web_pages.hide()
                     
    def apply_theme_settings(self):
        self.default_font = database_functions.read_setting("default_font")["current_value"]
        #self.default_font_size = database_functions.read_setting("default_font_size")["current_value"]
        self.default_font_size = "14"
        self.default_font_color = database_functions.read_setting("default_font_color")["current_value"]
        self.default_background_color = database_functions.read_setting("default_background_color")["current_value"]
        self.default_buttons_background = database_functions.read_setting("default_button_background")["current_value"]
        self.default_buttons_font_color = database_functions.read_setting("default_button_font_color")["current_value"]
        self.default_style = database_functions.read_setting("default_style")["current_value"]
        self.default_custome_theme = database_functions.read_setting("default_custome_theme")["current_value"]

        if self.default_custome_theme!="":
            apply_stylesheet(self.app, theme=self.default_custome_theme)
        else:
            self.app.setStyle("")
            self.app.setStyleSheet("")
            self.MainWindow.setStyleSheet("")

            #apply theme to mainwindow
            self.app.setStyle(self.default_style)
            self.font = QtGui.QFont(self.default_font, int(self.default_font_size))
            self.MainWindow.setStyleSheet("*{font-family:\""+self.default_font+"\";font-size:"+self.default_font_size+"px;color:\""+self.default_font_color+"\";}QPushButton, QComboBox{background:\""+self.default_buttons_background+"\";color:\""+self.default_buttons_font_color+"\"}QFrame{border:0px;}")
            self.ui.scrollAreaWidgetContents.setStyleSheet("#scrollAreaWidgetContents{background:\""+self.default_background_color+"\"}")
        
        
        self.MainWindow.update()
  
    def set_windows_boolean_value(self): 
        ### Menu 1 ###
        
        # Παράθυρο για πολλές χρήσεις #
        self.search_schedule_transmitions_window_is_open = False
        
        self.internet_error_window_is_open = False
        
        # Διαχείριση ραδιοφωνικών μεταδόσεων #
        self.manage_radio_connections_window_is_open = False

        # Αρχεία ήχου #
        self.import_sound_file_from_sound_file_window_is_open = False
        #self.import_sound_file_unsupported_type_error_window_is_open = False
        #self.import_sound_file_unsupported_image_type_error_window_is_open = False
        #self.import_sound_file_missing_data_error_window_is_open = False
        self.import_sound_file_from_video_window_is_open = False
        #self.import_sound_file_save_question_window_is_open = False
        self.export_sound_file_window_is_open = False
        self.edit_sound_file_window_is_open = False
        self.search_sound_file_window_is_open = False
        self.preview_sound_file_window_is_open = False

        # Λίστες αναπαραγωγής #
        self.create_playlist_window_is_open = False
        self.import_playlist_window_is_open = False
        #self.import_playlist_unsupported_type_error_window_is_open = False
        self.export_playlist_as_sound_files_window_is_open = False
        self.export_playlist_as_playlist_window_is_open = False
        self.edit_playlist_window_is_open = False
        self.search_playlist_window_is_open = False
        self.preview_playlist_window_is_open = False

        # Ηχητικά clips #
        self.import_sound_clip_window_is_open = False
        #self.import_sound_clip_unsupported_type_error_window_is_open = False
        self.export_sound_clip_window_is_open = False
        self.edit_sound_clip_window_is_open = False
        self.search_sound_clip_window_is_open = False
        self.preview_sound_clip_window_is_open = False
        self.classification_sound_clips_window_is_open = False

        # Αναμεταδόσεις #
        self.import_retransmition_window_is_open = False
        self.export_retransmition_window_is_open = False
        self.edit_retransmition_window_is_open = False
        self.search_retransmition_window_is_open = False
        self.preview_retransmition_window_is_open = False

        # Σήμα σταθμού #
        self.import_station_logo_window_is_open = False
        #self.import_station_logo_unsupported_type_error_window_is_open = False
        self.export_station_logo_window_is_open = False
        self.edit_station_logo_window_is_open = False
        self.search_station_logo_window_is_open = False
        self.preview_station_logo_window_is_open = False

        # Ώρα Ελλάδας #
        self.import_Greece_time_window_is_open = False
        self.export_Greece_time_window_is_open = False
        self.edit_Greece_time_window_is_open = False
        self.search_Greece_time_window_is_open = False
        self.preview_Greece_time_window_is_open = False

        # Δελτίο εκκλησιαστικών ανακοινώσεων #
        self.import_church_news_window_is_open = False
        self.export_church_news_window_is_open = False
        self.edit_church_news_window_is_open = False
        self.search_church_news_window_is_open = False
        self.preview_church_news_window_is_open = False

        # Δελτίο καιρού #
        self.import_weather_news_window_is_open = False
        self.export_weather_news_window_is_open = False
        self.edit_weather_news_window_is_open = False
        self.search_weather_news_window_is_open = False
        self.preview_weather_news_window_is_open = False

        # Ηχογράφηση #
        self.start_record_window_is_open = False

        # Αναφορές #
        self.weekly_programm_report_window_is_open = False
        self.player_history_report_window_is_open = False
        self.scheduled_transmition_report_window_is_open = False
        self.listeners_statistics_report_window_is_open = False

        # Διαχείριση συσκευών #
        self.manage_output_devices_window_is_open = False
        #self.manage_output_devices_save_question_window_is_open = False
        #self.manage_output_unable_to_open_process_window_is_open = False
        self.manage_input_device_window_is_open = False
        #self.manage_input_device_save_question_window_is_open = False

        #Διαχείριση διεργασιών #
        self.manage_proccesses_window_is_open = False

        
        ### Menu 2 ###

        # Επιλογή θέματος #
        self.choose_theme_window_is_open = False
        self.change_theme_save_question_window_is_open = False
        
        # Ορατά πεδία λίστας αναπαραγωγής #
        self.visible_player_list_fields_window_is_open = False
        #self.visible_player_list_fields_save_question_window_is_open = False

        # Ορατά πεδία προγράμματος #
        self.visible_program_components_window_is_open = False
        #self.visible_programm_components_save_question_window_is_open = False
        
        ### Menu 3 ###

        # Προγραμματισμένες μεταδόσεις #
        self.create_schedule_transmition_window_is_open = False
        self.explore_scheduled_transmitions_window_is_open = False

        # Ραδιοφωνικοί σταθμοί #
        self.import_radio_station_window_is_open = False
        self.edit_radio_stations_window_is_open = False
        
        ### Menu 4 ###

        # Επικοινωνία #
        self.contact_window_is_open = False

        # Λίγα λόγια για το πρόγραμμα #
        self.programm_abstract_information_window_is_open = False
           
    def link_menus(self):
        ### Menu 1 ###
        
        # Διαχείριση ραδιοφωνικών μεταδόσεων #
        self.ui.menu_manage_transmitions.triggered.connect(lambda checked:self.open_manage_transmitions_window(checked))

        # Αρχεία ήχου #
        self.ui.menu_import_sound_file_from_sound_file.triggered.connect(lambda checked:self.open_import_sound_file_from_sound_file_window(checked))
        self.ui.menu_import_sound_file_from_sound_video.triggered.connect(lambda checked:self.open_import_sound_file_from_video_window(checked))
        self.ui.menu_sound_file_play_now_deck_1.triggered.connect(lambda checked,action="play_from_deck_1":self.open_search_sound_file_window(checked,action))
        self.ui.menu_sound_file_play_now_deck_2.triggered.connect(lambda checked,action="play_from_deck_2":self.open_search_sound_file_window(checked,action))
        self.ui.menu_sound_file_play_when_ready.triggered.connect(lambda checked,action="play_when_ready":self.open_search_sound_file_window(checked,action))
        self.ui.menu_sound_file_add_to_player_list_top.triggered.connect(lambda checked,action="add_to_player_list_top":self.open_search_sound_file_window(checked,action))
        self.ui.menu_sound_file_add_to_player_list_bottom.triggered.connect(lambda checked,action="add_to_player_list_bottom":self.open_search_sound_file_window(checked,action))
        self.ui.menu_sound_file_add_to_new_scheduled_transmition.triggered.connect(lambda checked,action="add_to_new_scheduled_transmition":self.open_search_sound_file_window(checked,action))
        self.ui.menu_sound_file_add_to_existed_scheduled_transmition.triggered.connect(lambda checked,action="add_to_existed_scheduled_transmition":self.open_search_sound_file_window(checked,action))
        self.ui.menu_sound_file_export.triggered.connect(lambda checked,action="export":self.open_search_sound_file_window(checked,action))
        self.ui.menu_sound_file_edit.triggered.connect(lambda checked,action="edit":self.open_search_sound_file_window(checked,action))
        self.ui.menu_sound_file_preview.triggered.connect(lambda checked,action="preview":self.open_search_sound_file_window(checked,action))
        self.ui.menu_sound_file_delete.triggered.connect(lambda checked,action="delete":self.open_search_sound_file_window(checked,action))

        # Λίστες αναπαραγωγής #
        self.ui.menu_playlist_import.triggered.connect(lambda checked:self.open_import_playlist_window(checked))
        self.ui.menu_playlist_create.triggered.connect(lambda checked:self.open_create_playlist_window(checked))
        self.ui.menu_playlist_play_now.triggered.connect(lambda checked,action="play_now":self.open_search_playlist_window(checked,action))
        self.ui.menu_playlist_play_when_ready.triggered.connect(lambda checked,action="play_when_ready":self.open_search_playlist_window(checked,action))
        self.ui.menu_playlist_add_to_playlist_top.triggered.connect(lambda checked,action="add_to_player_list_top":self.open_search_playlist_window(checked,action))
        self.ui.menu_playlist_add_to_playlist_bottom.triggered.connect(lambda checked,action="add_to_player_list_bottom":self.open_search_playlist_window(checked,action))
        self.ui.menu_playlist_add_to_new_scheduled_transmition.triggered.connect(lambda checked,action="add_to_new_scheduled_transmition":self.open_search_playlist_window(checked,action))
        self.ui.menu_playlist_add_to_existed_scheduled_transmition.triggered.connect(lambda checked,action="add_to_existed_scheduled_transmition":self.open_search_playlist_window(checked,action))
        self.ui.menu_playlist_export_as_playlist.triggered.connect(lambda checked,action="export_as_playlist":self.open_search_playlist_window(checked,action))
        self.ui.menu_playlist_export_as_sound_files.triggered.connect(lambda checked,action="export_as_sound_files":self.open_search_playlist_window(checked,action))
        self.ui.menu_playlist_edit.triggered.connect(lambda checked,action="edit":self.open_search_playlist_window(checked,action))
        self.ui.menu_playlist_preview.triggered.connect(lambda checked,action="preview":self.open_search_playlist_window(checked,action))
        self.ui.menu_playlist_delete.triggered.connect(lambda checked,action="delete":self.open_search_playlist_window(checked,action))
        

        # Ηχητικά clips #
        self.ui.menu_sound_clips_import.triggered.connect(lambda checked:self.open_import_sound_clip_window(checked))
        self.ui.menu_sound_clips_play_now.triggered.connect(lambda checked,action="play_now":self.open_search_sound_clip_window(checked,action))
        self.ui.menu_sound_clips_play_when_ready.triggered.connect(lambda checked,action="play_when_ready":self.open_search_sound_clip_window(checked,action))
        self.ui.menu_sound_clips_add_to_playlist_top.triggered.connect(lambda checked,action="add_to_player_list_top":self.open_search_sound_clip_window(checked,action))
        self.ui.menu_sound_clips_add_to_playlist_bottom.triggered.connect(lambda checked,action="add_to_player_list_bottom":self.open_search_sound_clip_window(checked,action))
        self.ui.menu_sound_clips_add_to_new_scheduled_transmition.triggered.connect(lambda checked,action="add_to_new_scheduled_transmition":self.open_search_sound_clip_window(checked,action))
        self.ui.menu_sound_clips_add_to_existed_scheduled_transmition.triggered.connect(lambda checked,action="add_to_existed_scheduled_transmition":self.open_search_sound_clip_window(checked,action))
        self.ui.menu_sound_clips_classification.triggered.connect(lambda checked:self.open_classification_sound_clip_window(checked))
        self.ui.menu_sound_clips_export.triggered.connect(lambda checked,action="export":self.open_search_sound_clip_window(checked,action))
        self.ui.menu_sound_clips_edit.triggered.connect(lambda checked,action="edit":self.open_search_sound_clip_window(checked,action))
        self.ui.menu_sound_clips_preview.triggered.connect(lambda checked,action="preview":self.open_search_sound_clip_window(checked,action))
        self.ui.menu_sound_clips_delete.triggered.connect(lambda checked,action="delete":self.open_search_sound_clip_window(checked,action))

        # Αναμεταδόσεις #
        self.ui.menu_retransmitions_import.triggered.connect(lambda checked:self.open_import_retransmition_window(checked))
        self.ui.menu_retransmitions_play_now_on_deck_1.triggered.connect(lambda checked,action="play_from_deck_1":self.open_search_retransmition_window(checked,action))
        self.ui.menu_retransmitions_play_now_on_deck_2.triggered.connect(lambda checked,action="play_from_deck_2":self.open_search_retransmition_window(checked,action))
        self.ui.menu_retransmitions_play_when_ready.triggered.connect(lambda checked,action="play_when_ready":self.open_search_retransmition_window(checked,action))
        self.ui.menu_retransmitions_add_to_player_list_top.triggered.connect(lambda checked,action="add_to_player_list_top":self.open_search_retransmition_window(checked,action))
        self.ui.menu_retransmitions_add_to_player_list_bottom.triggered.connect(lambda checked,action="add_to_player_list_bottom":self.open_search_retransmition_window(checked,action))
        self.ui.menu_retransmitions_add_to_new_scheduled_transmition.triggered.connect(lambda checked,action="add_to_new_scheduled_transmition":self.open_search_retransmition_window(checked,action))
        self.ui.menu_retransmitions_add_to_existed_scheduled_transmition.triggered.connect(lambda checked,action="add_to_existed_scheduled_transmition":self.open_search_retransmition_window(checked,action))
        self.ui.menu_retransmitions_edit.triggered.connect(lambda checked,action="edit":self.open_search_retransmition_window(checked,action))
        self.ui.menu_retransmitions_preview.triggered.connect(lambda checked,action="preview":self.open_search_retransmition_window(checked,action))
        self.ui.menu_retransmitions_export.triggered.connect(lambda checked,action="export":self.open_search_retransmition_window(checked,action))
        self.ui.menu_retransmitions_delete.triggered.connect(lambda checked,action="delete":self.open_search_retransmition_window(checked,action))

        # Σήμα σταθμού #
        self.ui.menu_station_logos_import.triggered.connect(lambda checked:self.open_import_station_logo_window(checked))
        self.ui.menu_station_logos_play_now_on_deck_1.triggered.connect(lambda checked,action="play_from_deck_1":self.open_search_station_logo_window(checked,action))
        self.ui.menu_station_logos_play_now_on_deck_2.triggered.connect(lambda checked,action="play_from_deck_2":self.open_search_station_logo_window(checked,action))
        self.ui.menu_station_logos_play_when_ready.triggered.connect(lambda checked,action="play_when_ready":self.open_search_station_logo_window(checked,action))
        self.ui.menu_station_logos_add_to_playlist_top.triggered.connect(lambda checked,action="add_to_player_list_top":self.open_search_station_logo_window(checked,action))
        self.ui.menu_station_logos_add_to_playlist_bottom.triggered.connect(lambda checked,action="add_to_player_list_bottom":self.open_search_station_logo_window(checked,action))
        self.ui.menu_station_logos_add_to_new_scheduled_transmition.triggered.connect(lambda checked,action="add_to_new_scheduled_transmition":self.open_search_station_logo_window(checked,action))
        self.ui.menu_station_logos_add_to_existed_scheduled_transmition.triggered.connect(lambda checked,action="add_to_existed_scheduled_transmition":self.open_search_station_logo_window(checked,action))
        self.ui.menu_station_logos_default.triggered.connect(lambda checked,action="select_default":self.open_search_station_logo_window(checked,action))
        self.ui.menu_station_logos_export.triggered.connect(lambda checked,action="export":self.open_search_station_logo_window(checked,action))
        self.ui.menu_station_logos_edit.triggered.connect(lambda checked,action="edit":self.open_search_station_logo_window(checked,action))
        self.ui.menu_station_logos_preview.triggered.connect(lambda checked,action="preview":self.open_search_station_logo_window(checked,action))
        self.ui.menu_station_logos_delete.triggered.connect(lambda checked,action="delete":self.open_search_station_logo_window(checked,action))


        # Ώρα Ελλάδας #
        self.ui.menu_greek_time_import.triggered.connect(lambda checked:self.open_import_Greece_time_window(checked))
        self.ui.menu_greek_time_default.triggered.connect(lambda checked,action="select_default":self.open_search_Greece_time_window(checked,action))
        self.ui.menu_greek_time_add_to_playlist.triggered.connect(lambda checked,action="add_to_player_list":self.open_search_Greece_time_window(checked,action))
        self.ui.menu_greek_time_add_to_new_scheduled_transmition.triggered.connect(lambda checked,action="add_to_new_scheduled_transmition":self.open_search_Greece_time_window(checked,action))
        self.ui.menu_greek_time_add_to_existed_scheduled_transmition.triggered.connect(lambda checked,action="add_to_existed_scheduled_transmition":self.open_search_Greece_time_window(checked,action))
        self.ui.menu_greek_time_export.triggered.connect(lambda checked,action="export":self.open_search_Greece_time_window(checked,action))
        self.ui.menu_greek_time_edit.triggered.connect(lambda checked,action="edit":self.open_search_Greece_time_window(checked,action))
        self.ui.menu_greek_time_preview.triggered.connect(lambda checked,action="preview":self.open_search_Greece_time_window(checked,action))
        self.ui.menu_greek_time_delete.triggered.connect(lambda checked,action="delete":self.open_search_Greece_time_window(checked,action))

        # Δελτίο εκκλησιαστικών ανακοινώσεων #
        self.ui.menu_church_news_import.triggered.connect(lambda checked:self.open_import_church_news_window(checked))
        self.ui.menu_church_news_play_now_on_deck_1.triggered.connect(lambda checked,action="play_from_deck_1":self.open_search_church_news_window(checked,action))
        self.ui.menu_church_news_play_now_on_deck_2.triggered.connect(lambda checked,action="play_from_deck_2":self.open_search_church_news_window(checked,action))
        self.ui.menu_church_news_play_when_ready.triggered.connect(lambda checked,action="play_when_ready":self.open_search_church_news_window(checked,action))
        self.ui.menu_church_news_add_to_playlist_top.triggered.connect(lambda checked,action="add_to_player_list_top":self.open_search_church_news_window(checked,action))
        self.ui.menu_church_news_add_to_playlist_bottom.triggered.connect(lambda checked,action="add_to_player_list_bottom":self.open_search_church_news_window(checked,action))
        self.ui.menu_church_news_add_to_new_scheduled_transmition.triggered.connect(lambda checked,action="add_to_new_scheduled_transmition":self.open_search_church_news_window(checked,action))
        self.ui.menu_church_news_add_to_existed_scheduled_transmition.triggered.connect(lambda checked,action="add_to_existed_scheduled_transmition":self.open_search_church_news_window(checked,action))
        self.ui.menu_church_news_default.triggered.connect(lambda checked,action="select_default":self.open_search_church_news_window(checked,action))
        self.ui.menu_church_news_export.triggered.connect(lambda checked,action="export":self.open_search_church_news_window(checked,action))
        self.ui.menu_church_news_edit.triggered.connect(lambda checked,action="edit":self.open_search_church_news_window(checked,action))
        self.ui.menu_church_news_preview.triggered.connect(lambda checked,action="preview":self.open_search_church_news_window(checked,action))
        self.ui.menu_church_news_delete.triggered.connect(lambda checked,action="delete":self.open_search_church_news_window(checked,action))

        # Δελτίο καιρού #
        self.ui.menu_weather_news_import.triggered.connect(lambda checked:self.open_import_weather_news_window(checked))
        self.ui.menu_weather_news_play_now_on_deck_1.triggered.connect(lambda checked,action="play_from_deck_1":self.open_search_weather_news_window(checked,action))
        self.ui.menu_weather_news_play_now_on_deck_2.triggered.connect(lambda checked,action="play_from_deck_2":self.open_search_weather_news_window(checked,action))
        self.ui.menu_weather_news_play_when_ready.triggered.connect(lambda checked,action="play_when_ready":self.open_search_weather_news_window(checked,action))
        self.ui.menu_weather_news_add_to_player_list_top.triggered.connect(lambda checked,action="add_to_player_list_top":self.open_search_weather_news_window(checked,action))
        self.ui.menu_weather_news_add_to_player_list_bottom.triggered.connect(lambda checked,action="add_to_player_list_bottom":self.open_search_weather_news_window(checked,action))
        self.ui.menu_weather_news_add_to_new_scheduled_transmition.triggered.connect(lambda checked,action="add_to_new_scheduled_transmition":self.open_search_weather_news_window(checked,action))
        self.ui.menu_weather_news_add_to_existed_scheduled_transmition.triggered.connect(lambda checked,action="add_to_existed_scheduled_transmition":self.open_search_weather_news_window(checked,action))
        self.ui.menu_weather_news_default.triggered.connect(lambda checked,action="select_default":self.open_search_weather_news_window(checked,action))
        self.ui.menu_weather_news_export.triggered.connect(lambda checked,action="export":self.open_search_weather_news_window(checked,action))
        self.ui.menu_weather_news_edit.triggered.connect(lambda checked,action="edit":self.open_search_weather_news_window(checked,action))
        self.ui.menu_weather_news_preview.triggered.connect(lambda checked,action="preview":self.open_search_weather_news_window(checked,action))
        self.ui.menu_weather_news_delete.triggered.connect(lambda checked,action="delete":self.open_search_weather_news_window(checked,action))
        
        # Ηχογράφηση #
        self.ui.menu_record_start.triggered.connect(lambda checked:self.open_start_record_window(checked))
        
        # Αναφορές #
        self.ui.menu_report_scheduled_transmition.triggered.connect(lambda checked:self.open_scheduled_transmition_report_window(checked))
        self.ui.menu_report_week_programm.triggered.connect(lambda checked:self.open_week_programm_report_window_window(checked))
        self.ui.menu_report_general_deck_history.triggered.connect(lambda checked:self.open_decks_history_report_window(checked))
        self.ui.menu_report_listeners_statistics.triggered.connect(lambda checked:self.open_listeners_statistics_window(checked))

        # Διαχείριση συσκευών #
        self.ui.menu_manage_output_devices.triggered.connect(lambda checked:self.open_manage_output_devices_window(checked))
        self.ui.menu_manage_input_device.triggered.connect(lambda checked:self.open_manage_input_devices_window(checked))

        #Διαχείριση διεργασιών #
        self.ui.menu_manage_tasks.triggered.connect(lambda checked:self.open_manage_tasks_window(checked))
        
        ### Menu 2 ###

        # Επιλογή θέματος #
        self.ui.menu_choose_theme.triggered.connect(lambda checked:self.open_choose_theme_window(checked))

        # Ορατά πεδία λίστας αναπαραγωγής #
        self.ui.menu_select_player_list_fields.triggered.connect(lambda checked:self.open_select_player_list_fields_window(checked))

        # Ορατά πεδία προγράμματος #
        self.ui.menu_programm_components.triggered.connect(lambda checked:self.open_programm_components_window(checked))
        
        ### Menu 3 ###

        # Προγραμματισμένες μεταδόσεις #
        self.ui.menu_new_scheduled_transmition.triggered.connect(lambda checked:self.open_new_scheduled_transmition_window(checked))
        self.ui.menu_edit_scheduled_transmition.triggered.connect(lambda checked:self.open_review_transmitions_window(checked))
       
        # Ραδιοφωνικοί σταθμοί #
        self.ui.menu_new_radio_station.triggered.connect(lambda checked:self.open_new_radio_connection_window(checked))
        self.ui.menu_edit_radio_station.triggered.connect(lambda checked:self.open_modify_radio_connections_window(checked))
        
        ### Menu 4 ###

        # Επικοινωνία #
        self.ui.menu_abstract_information.triggered.connect(lambda checked:self.open_programm_abstract_information_window(checked))

        # Λίγα λόγια για το πρόγραμμα #
        self.ui.menu_contact.triggered.connect(lambda checked:self.open_contact_window(checked))

    def open_internet_connection_error_window(self):
        if self.internet_connection_error_window_is_open == False:
            self.internet_connection_error_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_internet_connection_error_window = internet_connection_error_ui.Ui_Dialog()
            self.ui_internet_connection_error_window.setupUi(self.internet_connection_error_window)
            self.internet_connection_error_window_is_open = True
            self.internet_connection_error_window_support_code = internet_connection_error_support_ui.Support_Ui_Dialog(self)
            self.internet_connection_error_window.exec()
        
    ### Menu 1 ###
    
    # Παράθυρο για πολλές χρήσεις #
    def open_search_scheduled_transmition_window(self,action,relative_type,relative_number):
        if(self.search_scheduled_transmition_window_is_open==False):    
            self.search_scheduled_transmition_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_search_scheduled_transmition_window = search_scheduled_transmition_ui.Ui_Dialog()
            self.ui_search_scheduled_transmition_window.setupUi(self.search_scheduled_transmition_window)
            self.search_scheduled_transmition_window_is_open = True
            self.search_scheduled_transmition_window_support_code = search_scheduled_transmition_support_ui.Support_Ui_Dialog(self,action,relative_type,relative_number)
            self.search_scheduled_transmition_window.exec()
     
    # Διαχείριση ραδιοφωνικών μεταδόσεων #    
    def open_manage_transmitions_window(self,checked):
        if(self.manage_radio_connections_window_is_open==False):    
            self.manage_radio_connections_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_manage_radio_connections_window = manage_radio_connections_ui.Ui_Dialog()
            self.ui_manage_radio_connections_window.setupUi(self.manage_radio_connections_window)
            self.manage_radio_connections_window_is_open = True
            self.manage_radio_connections_window_support_code = manage_radio_connections_support_ui.Support_Ui_Dialog(self)
            self.manage_radio_connections_window.exec()
         
    # Αρχεία ήχου #
    def open_import_sound_file_from_sound_file_window(self,checked,sound_file_path=None):
        return 1
        if(sound_file_path==None):
            if(self.import_sound_file_window_is_open==False):
                dialog = QtWidgets.QFileDialog(self.MainWindow)
                dialog.setWindowTitle('Άνοιγμα αρχείου ήχου')
                dialog.setNameFilter('All files (*.*);;Mp3 files (*.mp3);;Wav files (*.wav);;Ogg files (*.ogg);;Flv files (*.flv)')
                dialog.setDirectory(QtCore.QDir.currentPath())
                dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
                if dialog.exec_() == QtWidgets.QDialog.Accepted:
                    sound_file_path = str(dialog.selectedFiles()[0])
                    extension = sound_file_path.split(".")[-1].lower()
                    if(extension=="mp3" or extension=="wav" or extension=="wmv" or extension=="flv" or extension=="ogg"):
                        self.import_sound_file_window = QtWidgets.QDialog(self.MainWindow)
                        self.ui_import_sound_file_window = import_sound_file_ui.Ui_Dialog()
                        self.ui_import_sound_file_window.setupUi(self.import_sound_file_window)
                        self.import_sound_file_window_is_open = True
                        self.import_sound_file_window_support_code = import_sound_file_support_ui.Support_Ui_Dialog(self,sound_file_path)
                        self.import_sound_file_window.exec()
                    else:
                        self.import_sound_file_unsupported_type_error_window = QtWidgets.QDialog(self.MainWindow)
                        self.ui_import_sound_file_unsupported_type_error_window = import_sound_file_unsupported_type_error_ui.Ui_Dialog()
                        self.ui_import_sound_file_unsupported_type_error_window.setupUi(self.import_sound_file_unsupported_type_error_window)
                        self.import_sound_file_unsupported_type_error_window_is_open = True
                        self.import_sound_file_unsupported_type_error_window_support_code = import_sound_file_unsupported_type_error_support_ui.Support_Ui_Dialog(self)
                        self.import_sound_file_unsupported_type_error_window.exec()
        else:                
            self.import_sound_file_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_import_sound_file_window = import_sound_file_ui.Ui_Dialog()
            self.ui_import_sound_file_window.setupUi(self.import_sound_file_window)
            self.import_sound_file_window_is_open = True
            self.import_sound_file_window_support_code = import_sound_file_support_ui.Support_Ui_Dialog(self,sound_file_path)
            self.import_sound_file_window.exec()

    def open_import_sound_file_unsupported_image_type_error_window(self):
        pass
            
    def open_import_sound_file_missing_data_error_window(self,error_message):
        pass
         
    def open_import_sound_file_save_question_window(self):
        pass
         
    def open_import_sound_file_from_video_window(self,checked):
        if(self.import_sound_file_from_video_window_is_open==False):    
            self.import_sound_file_from_video_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_import_sound_file_from_video_window = import_sound_file_from_video_ui.Ui_Dialog()
            self.ui_import_sound_file_from_video_window.setupUi(self.import_sound_file_from_video_window)
            self.import_sound_file_from_video_window_is_open = True
            self.import_sound_file_from_video_window_support_code = import_sound_file_from_video_support_ui.Support_Ui_Dialog(self)
            self.import_sound_file_from_video_window.exec()
       
    def open_search_sound_file_window(self,checked,action):
        if(self.search_sound_file_window_is_open==False):   
            self.search_sound_file_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_search_sound_file_window = search_sound_file_ui.Ui_Dialog()
            self.ui_search_sound_file_window.setupUi(self.search_sound_file_window)
            self.search_sound_file_window_is_open = True
            self.search_sound_file_window_support_code = search_sound_file_support_ui.Support_Ui_Dialog(self,action)
            self.search_sound_file_window.exec()
   
    def open_export_sound_file_window(self,sound_file_number):
        if(self.export_sound_file_window_is_open==False):   
            self.export_sound_file_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_export_sound_file_window = export_sound_file_ui.Ui_Dialog()
            self.ui_export_sound_file_window.setupUi(self.export_sound_file_window)
            self.export_sound_file_window_is_open = True
            self.export_sound_file_window_support_code = export_sound_file_support_ui.Support_Ui_Dialog(self,sound_file_number)
            self.export_sound_file_window.exec()
           
    def open_edit_sound_file_window(self,sound_file_number):
        if(self.edit_sound_file_window_is_open==False): 
            self.edit_sound_file_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_edit_sound_file_window = edit_sound_file_ui.Ui_Dialog()
            self.ui_edit_sound_file_window.setupUi(self.edit_sound_file_window)
            self.edit_sound_file_window_is_open = True
            self.edit_sound_file_window_support_code = edit_sound_file_support_ui.Support_Ui_Dialog(self,sound_file_number)
            self.edit_sound_file_window.exec()
  
    def open_preview_sound_file_window(self,sound_file_db_entry):
        if(self.preview_sound_file_window_is_open==False):  
            self.preview_sound_file_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_preview_sound_file_window = preview_sound_file_ui.Ui_Dialog()
            self.ui_preview_sound_file_window.setupUi(self.preview_sound_file_window)
            self.preview_sound_file_window_is_open = True
            self.preview_sound_file_window_support_code = preview_sound_file_support_ui.Support_Ui_Dialog(self,sound_file_db_entry)
            self.preview_sound_file_window.exec()   
    
    # Λίστες αναπαραγωγής #    
    def open_import_playlist_window(self,checked):
        return 1
        if(self.import_playlist_window_is_open==False):
            dialog = QtWidgets.QFileDialog(self.MainWindow)
            dialog.setWindowTitle('Άνοιγμα αρχείου playlist')
            
            self.playlist_formats = ["aimppl","aimppl4","asx","atom","b4s","hypetape","kpl","m3u","m3u8","mpcpl","plc","plist","plp","pls","ram","rmp","rss","smil","vlc","wax","wpl","wvx","xml","xspf","zpl"]
            
            file_formats = "Όλα τα αρχεία (*.*)"
            for file_format in self.playlist_formats:
                file_formats +=";;"+file_format+" αρχεία (*."+file_format+")"
            
            dialog.setNameFilter(file_formats)
            dialog.setDirectory(QtCore.QDir.currentPath())
            dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                playlist_path = str(dialog.selectedFiles()[0])
                file_full_path_split_dot = playlist_path.split(".")
                extension = file_full_path_split_dot[len(file_full_path_split_dot)-1]
                if(extension not in self.playlist_formats):
                    self.import_playlist_unsupported_type_error_window = QtWidgets.QDialog(self.MainWindow)
                    self.ui_import_playlist_unsupported_type_error_window = import_playlist_unsupported_type_error_ui.Ui_Dialog()
                    self.ui_import_playlist_unsupported_type_error_window.setupUi(self.import_playlist_unsupported_type_error_window)
                    self.import_playlist_unsupported_type_error_window_is_open = True
                    self.import_playlist_unsupported_type_error_window_support_code = import_playlist_unsupported_type_error_support_ui.Support_Ui_Dialog(self)
                    self.import_playlist_unsupported_type_error_window.exec()
                else:
                    self.import_playlist_window = QtWidgets.QDialog(self.MainWindow)
                    self.ui_import_playlist_window = import_playlist_ui.Ui_Dialog()
                    self.ui_import_playlist_window.setupUi(self.import_playlist_window)
                    self.import_playlist_window_is_open = True
                    self.import_playlist_window_support_code = import_playlist_support_ui.Support_Ui_Dialog(self,playlist_path)
                    self.import_playlist_window.exec()
     
    def open_create_playlist_window(self,checked):
        if(self.create_playlist_window_is_open==False): 
            self.create_playlist_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_create_playlist_window = create_playlist_ui.Ui_Dialog()
            self.ui_create_playlist_window.setupUi(self.create_playlist_window)
            self.create_playlist_window_is_open = True
            self.create_playlist_window_support_code = create_playlist_support_ui.Support_Ui_Dialog(self)
            self.create_playlist_window.exec()
   
    def open_search_playlist_window(self,checked,action):
        if(self.search_playlist_window_is_open==False): 
            self.search_playlist_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_search_playlist_window = search_playlist_ui.Ui_Dialog()
            self.ui_search_playlist_window.setupUi(self.search_playlist_window)
            self.search_playlist_window_is_open = True
            self.search_playlist_window_support_code = search_playlist_support_ui.Support_Ui_Dialog(self,action)
            self.search_playlist_window.exec()
          
    def open_export_playlist_as_playlist_window(self,playlist_number):
        if(self.export_playlist_as_playlist_window_is_open==False): 
            self.export_playlist_as_playlist_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_export_playlist_as_playlist_window = export_playlist_as_playlist_ui.Ui_Dialog()
            self.ui_export_playlist_as_playlist_window.setupUi(self.export_playlist_as_playlist_window)
            self.export_playlist_as_playlist_window_is_open = True
            self.export_playlist_as_playlist_window_support_code = export_playlist_as_playlist_support_ui.Support_Ui_Dialog(self,playlist_number)
            self.export_playlist_as_playlist_window.exec()
          
    def open_export_playlist_as_sound_files_window(self,playlist_number):
        if(self.export_playlist_as_sound_files_window_is_open==False):  
            self.export_playlist_as_sound_files_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_export_playlist_as_sound_files_window = export_playlist_as_sound_files_ui.Ui_Dialog()
            self.ui_export_playlist_as_sound_files_window.setupUi(self.export_playlist_as_sound_files_window)
            self.export_playlist_as_sound_files_window_is_open = True
            self.export_playlist_as_sound_files_window_support_code = export_playlist_as_sound_files_support_ui.Support_Ui_Dialog(self,playlist_number)
            self.export_playlist_as_sound_files_window.exec()
           
    def open_edit_playlist_window(self,playlist_number):
        if(self.edit_playlist_window_is_open==False):   
            self.edit_playlist_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_edit_playlist_window = edit_playlist_ui.Ui_Dialog()
            self.ui_edit_playlist_window.setupUi(self.edit_playlist_window)
            self.edit_playlist_window_is_open = True
            self.edit_playlist_window_support_code = edit_playlist_support_ui.Support_Ui_Dialog(self,playlist_number)
            self.edit_playlist_window.exec()
            
    def open_preview_playlist_window(self,playlist_number):
        if(self.preview_playlist_window_is_open==False):    
            self.preview_playlist_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_preview_playlist_window = preview_playlist_ui.Ui_Dialog()
            self.ui_preview_playlist_window.setupUi(self.preview_playlist_window)
            self.preview_playlist_window_is_open = True
            self.preview_playlist_window_support_code = preview_playlist_window_support_code.Support_Ui_Dialog(self,playlist_number)
            self.preview_playlist_window.exec()
            
    # Ηχητικά clips #
    def open_import_sound_clip_window(self,checked):
        return 1
        if(self.import_sound_clip_window_is_open==False):
            dialog = QtWidgets.QFileDialog(self.MainWindow)
            dialog.setWindowTitle('Άνοιγμα ηχητικού clip')
            dialog.setNameFilter('All files (*.*);;Mp3 files (*.mp3);;Wav files (*.wav);;Ogg files (*.ogg);;Flv files (*.flv)')
            dialog.setDirectory(QtCore.QDir.currentPath())
            dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                sound_clip_path = str(dialog.selectedFiles()[0])
                extension = sound_clip_path.split(".")[-1].lower()
                if(extension=="mp3" or extension=="wav" or extension=="wmv" or extension=="flv" or extension=="ogg"):
                    self.import_sound_clip_window = QtWidgets.QDialog(self.MainWindow)
                    self.ui_import_sound_clip_window = import_sound_clip_ui.Ui_Dialog()
                    self.ui_import_sound_clip_window.setupUi(self.import_sound_clip_window)
                    self.import_sound_clip_window_is_open = True
                    self.import_sound_clip_window_support_code = import_sound_clip_support_ui.Support_Ui_Dialog(self,sound_clip_path)
                    self.import_sound_clip_window.exec()
                else:
                    self.import_sound_clip_unsupported_type_error_window = QtWidgets.QDialog(self.MainWindow)
                    self.ui_import_sound_clip_unsupported_type_error_window = import_sound_clip_unsupported_type_error_ui.Ui_Dialog()
                    self.ui_import_sound_clip_unsupported_type_error_window.setupUi(self.import_sound_clip_unsupported_type_error_window)
                    self.import_sound_clip_unsupported_type_error_window_is_open = True
                    self.import_sound_clip_unsupported_type_error_window_support_code = import_sound_clip_unsupported_type_error_support_ui.Support_Ui_Dialog(self)
                    self.import_sound_clip_unsupported_type_error_window.exec()
            
    def open_search_sound_clip_window(self,checked,action):
        if(self.search_sound_clip_window_is_open==False):   
            self.search_sound_clip_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_search_playlist_window = search_sound_clip_ui.Ui_Dialog()
            self.ui_search_playlist_window.setupUi(self.search_sound_clip_window)
            self.search_sound_clip_window_is_open = True
            self.search_sound_clip_window_support_code = search_sound_clip_support_ui.Support_Ui_Dialog(self,action)
            self.search_sound_clip_window.exec()
        
    def open_classification_sound_clip_window(self,checked):
        if(self.classification_sound_clips_window_is_open==False):  
            self.classifications_sound_clips_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_classifications_sound_clips_window = classification_sound_clips_ui.Ui_Dialog()
            self.ui_classifications_sound_clips_window.setupUi(self.classifications_sound_clips_window)
            self.classification_sound_clips_window_is_open = True
            self.classification_sound_clip_window_support_code = classification_sound_clips_support_ui.Support_Ui_Dialog(self)
            self.classifications_sound_clips_window.exec()
            
    def open_export_sound_clip_window(self,sound_clip_number):
        if(self.export_sound_clip_window_is_open==False):   
            self.export_sound_clips_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_export_sound_clips_window = export_sound_clip_ui.Ui_Dialog()
            self.ui_export_sound_clips_window.setupUi(self.export_sound_clips_window)
            self.export_sound_clip_window_is_open = True
            self.export_sound_clip_window_support_code = export_sound_clip_support_ui.Support_Ui_Dialog(self,sound_clip_number)
            self.export_sound_clips_window.exec()
            
    def open_edit_sound_clip_window(self,sound_clip_number):
        if(self.edit_sound_clip_window_is_open==False): 
            self.edit_sound_clips_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_edit_sound_clips_window = edit_sound_clip_ui.Ui_Dialog()
            self.ui_edit_sound_clips_window.setupUi(self.edit_sound_clips_window)
            self.edit_sound_clip_window_is_open = True
            self.edit_sound_clip_window_support_code = edit_sound_clip_support_ui.Support_Ui_Dialog(self,sound_clip_number)
            self.edit_sound_clips_window.exec()
            
    def open_preview_sound_clip_window(self,sound_clip_number):
        if(self.preview_sound_clip_window_is_open==False):  
            self.preview_sound_clip_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_preview_sound_clip_window = preview_sound_clip_ui.Ui_Dialog()
            self.ui_preview_sound_clip_window.setupUi(self.preview_sound_clip_window)
            self.preview_sound_clip_window_is_open = True
            self.preview_sound_clip_window_support_code = preview_sound_clip_support_ui.Support_Ui_Dialog(self,sound_clip_number)
            self.preview_sound_clip_window.exec()
            
    # Αναμεταδόσεις #
    def open_import_retransmition_window(self,checked):
        if(self.import_retransmition_window_is_open==False):    
            self.import_retransmition_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_import_retransmition_window = import_retransmition_ui.Ui_Dialog()
            self.ui_import_retransmition_window.setupUi(self.import_retransmition_window)
            self.import_retransmition_window_is_open = True
            self.import_retransmition_window_support_code = import_retransmition_support_ui.Support_Ui_Dialog(self)
            self.import_retransmition_window.exec()
            
    def open_search_retransmition_window(self,checked,action):
        if(self.search_retransmition_window_is_open==False):    
            self.search_retransmition_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_search_retransmition_window = search_retransmition_ui.Ui_Dialog()
            self.ui_search_retransmition_window.setupUi(self.search_retransmition_window)
            self.search_retransmition_window_is_open = True
            self.search_retransmition_window_support_code = search_retransmition_support_ui.Support_Ui_Dialog(self,action)
            self.search_retransmition_window.exec()
            
    def open_edit_retransmition_window(self,retransmition_number):
        if(self.edit_retransmition_window_is_open==False):  
            self.edit_retransmition_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_edit_retransmition_window = edit_retransmition_ui.Ui_Dialog()
            self.ui_edit_retransmition_window.setupUi(self.edit_retransmition_window)
            self.edit_retransmition_window_is_open = True
            self.edit_retransmition_window_support_code = edit_retransmition_support_ui.Support_Ui_Dialog(self,retransmition_number)
            self.edit_retransmition_window.exec()
            
    def open_export_retransmition_window(self,retransmition_number):
        if(self.export_retransmition_window_is_open==False):    
            self.export_retransmition_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_export_retransmition_window = export_retransmition_ui.Ui_Dialog()
            self.ui_export_retransmition_window.setupUi(self.export_retransmition_window)
            self.export_retransmition_window_is_open = True
            self.export_retransmition_window_support_code = export_retransmition_support_ui.Support_Ui_Dialog(self,retransmition_number)
            self.export_retransmition_window.exec()
            
    def open_preview_retransmition_window(self,retransmition_number):
        if(self.preview_retransmition_window_is_open==False):   
            self.preview_retransmition_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_preview_retransmition_window = preview_retransmition_ui.Ui_Dialog()
            self.ui_preview_retransmition_window.setupUi(self.preview_retransmition_window)
            self.preview_retransmition_window_is_open = True
            self.preview_retransmition_window_support_code = preview_retransmition_support_ui.Support_Ui_Dialog(self,retransmition_number)
            self.preview_retransmition_window.exec()
            
    # Σήμα σταθμού #
    def open_import_station_logo_window(self,checked,station_logo_path=None):
        return 1
        if(station_logo_path==None):
            if(self.import_station_logo_window_is_open==False):
                dialog = QtWidgets.QFileDialog(self.MainWindow)
                dialog.setWindowTitle('Άνοιγμα σήματος σταθμού')
                dialog.setNameFilter('All files (*.*);;Mp3 files (*.mp3);;Wav files (*.wav);;Ogg files (*.ogg);;Flv files (*.flv)')
                dialog.setDirectory(QtCore.QDir.currentPath())
                dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
                if dialog.exec_() == QtWidgets.QDialog.Accepted:
                    station_logo_path = str(dialog.selectedFiles()[0])
                    extension = station_logo_path.split(".")[-1].lower()
                    if(extension=="mp3" or extension=="wav" or extension=="wmv" or extension=="flv" or extension=="ogg"):
                        self.import_station_logo_window = QtWidgets.QDialog(self.MainWindow)
                        self.ui_import_station_logo_window = import_station_logo_ui.Ui_Dialog()
                        self.ui_import_station_logo_window.setupUi(self.import_station_logo_window)
                        self.import_station_logo_window_is_open = True
                        self.import_station_logo_window_support_code = import_station_logo_support_ui.Support_Ui_Dialog(self,station_logo_path)
                        self.import_station_logo_window.exec()
                    else:
                        self.import_station_logo_unsupported_type_error_window = QtWidgets.QDialog(self.MainWindow)
                        self.ui_import_station_logo_unsupported_type_error_window = import_station_logo_unsupported_type_error_ui.Ui_Dialog()
                        self.ui_import_station_logo_unsupported_type_error_window.setupUi(self.import_station_logo_unsupported_type_error_window)
                        self.import_station_logo_unsupported_type_error_window_is_open = True
                        self.import_station_logo_unsupported_type_error_window_support_code = import_station_logo_unsupported_type_error_support_ui.Support_Ui_Dialog(self)
                        self.import_station_logo_unsupported_type_error_window.exec()
        else:                
            self.import_station_logo_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_import_station_logo_window = import_station_logo_ui.Ui_Dialog()
            self.ui_import_station_logo_window.setupUi(self.import_station_logo_window)
            self.import_station_logo_window_is_open = True
            self.import_station_logo_window_support_code = import_station_logo_support_ui.Support_Ui_Dialog(self,station_logo_path)
            self.import_station_logo_window.exec()

    def open_search_station_logo_window(self,checked,action):
        if(self.search_station_logo_window_is_open==False): 
            self.search_station_logos_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_search_station_logos_window = search_station_logo_ui.Ui_Dialog()
            self.ui_search_station_logos_window.setupUi(self.search_station_logos_window)
            self.search_station_logo_window_is_open = True
            self.search_station_logo_window_support_code = search_station_logo_support_ui.Support_Ui_Dialog(self,action)
            self.search_station_logos_window.exec()
            
    def open_export_station_logo_window(self,station_logo_number):
        if(self.export_station_logo_window_is_open==False): 
            self.export_station_logo_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_export_station_logos_window = export_station_logo_ui.Ui_Dialog()
            self.ui_export_station_logos_window.setupUi(self.export_station_logo_window)
            self.export_station_logo_window_is_open = True
            self.export_station_logo_window_support_code = export_station_logo_support_ui.Support_Ui_Dialog(self,station_logo_number)
            self.export_station_logo_window.exec()
            
    def open_edit_station_logo_window(self,station_logo_number):
        if(self.edit_station_logo_window_is_open==False):   
            self.edit_station_logo_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_edit_station_logo_window = edit_station_logo_ui.Ui_Dialog()
            self.ui_edit_station_logo_window.setupUi(self.edit_station_logo_window)
            self.edit_station_logo_window_is_open = True
            self.edit_station_logo_window_support_code = edit_station_logo_support_ui.Support_Ui_Dialog(self,station_logo_number)
            self.edit_station_logo_window.exec()

    def open_preview_station_logo_number(self,station_logo_number):
        if(self.preview_station_logo_window_is_open==False):    
            self.preview_station_logo_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_preview_station_logo_window = preview_station_logo_ui.Ui_Dialog()
            self.ui_preview_station_logo_window.setupUi(self.preview_station_logo_window)
            self.preview_station_logo_window_is_open = True
            self.preview_station_logo_window_support_code = preview_station_logo_support_ui.Support_Ui_Dialog(self,station_logo_number)
            self.preview_station_logo_window.exec()
            
    # Ώρα Ελλάδας #
    def open_import_Greece_time_window(self,checked):
        if(self.import_Greece_time_window_is_open==False):  
            self.import_Greece_time_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_import_Greece_time_window = import_Greece_time_ui.Ui_Dialog()
            self.ui_import_Greece_time_window.setupUi(self.import_Greece_time_window)
            self.import_Greece_time_window_is_open = True
            self.import_Greece_time_window_support_code = import_Greece_time_support_ui.Support_Ui_Dialog(self)
            self.import_Greece_time_window.exec()
            
    def open_search_Greece_time_window(self,checked,action):
        if(self.search_Greece_time_window_is_open==False):  
            self.search_Greece_time_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_search_Greece_time_window = search_Greece_time_ui.Ui_Dialog()
            self.ui_search_Greece_time_window.setupUi(self.search_Greece_time_window)
            self.search_Greece_time_window_is_open = True
            self.search_Greece_time_window_support_code = search_Greece_time_support_ui.Support_Ui_Dialog(self,action)
            self.search_Greece_time_window.exec()
            
    def open_export_Greece_time_window(self,Greece_time_number):
        if(self.export_Greece_time_window_is_open==False):  
            self.export_Greece_time_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_export_Greece_time_window = export_Greece_time_ui.Ui_Dialog()
            self.ui_export_Greece_time_window.setupUi(self.export_Greece_time_window)
            self.export_Greece_time_window_is_open = True
            self.export_Greece_time_window_support_code = export_Greece_time_support_ui.Support_Ui_Dialog(self,Greece_time_number)
            self.export_Greece_time_window.exec()
            
    def open_edit_Greece_time_window(self,Greece_time_number):
        if(self.edit_Greece_time_window_is_open==False):    
            self.edit_Greece_time_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_edit_Greece_time_window = edit_Greece_time_ui.Ui_Dialog()
            self.ui_edit_Greece_time_window.setupUi(self.edit_Greece_time_window)
            self.edit_Greece_time_window_is_open = True
            self.edit_Greece_time_window_support_code = edit_Greece_time_support_ui.Support_Ui_Dialog(self,Greece_time_number)
            self.edit_Greece_time_window.exec()
            
    def open_preview_Greece_time_window(self,Greece_time_number):
        if(self.preview_Greece_time_window_is_open==False): 
            self.preview_Greece_time_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_preview_Greece_time_window = preview_Greece_time_ui.Ui_Dialog()
            self.ui_preview_Greece_time_window.setupUi(self.preview_Greece_time_window)
            self.preview_Greece_time_window_is_open = True
            self.preview_Greece_time_window_support_code = preview_Greece_time_support_ui.Support_Ui_Dialog(self,Greece_time_number)
            self.preview_Greece_time_window.exec()
            
    # Δελτίο εκκλησιαστικών ανακοινώσεων #
    def open_import_church_news_window(self,checked):
        if(self.import_church_news_window_is_open==False):  
            self.import_church_news_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_import_church_news_window = import_church_news_ui.Ui_Dialog()
            self.ui_import_church_news_window.setupUi(self.import_church_news_window)
            self.import_church_news_window_is_open = True
            self.import_church_news_window_support_code = import_church_news_support_ui.Support_Ui_Dialog(self)
            self.import_church_news_window.exec()
        
    def open_search_church_news_window(self,checked,action):
        if(self.search_church_news_window_is_open==False):  
            self.search_church_news_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_search_church_news_window = search_church_news_ui.Ui_Dialog()
            self.ui_search_church_news_window.setupUi(self.search_church_news_window)
            self.search_church_news_window_is_open = True
            self.search_church_news_window_support_code = search_church_news_support_ui.Support_Ui_Dialog(self,action)
            self.search_church_news_window.exec()
            
    def open_export_church_news_window(self,church_news_number):
        if(self.export_church_news_window_is_open==False):  
            self.export_church_news_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_export_church_news_window = export_church_news_ui.Ui_Dialog()
            self.ui_export_church_news_window.setupUi(self.export_church_news_window)
            self.export_church_news_window_is_open = True
            self.export_church_news_window_support_code = export_church_news_support_ui.Support_Ui_Dialog(self,church_news_number)
            self.export_church_news_window.exec()
        
    def open_edit_church_news_window(self,church_news_number):
        if(self.edit_church_news_window_is_open==False):    
            self.edit_church_news_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_edit_church_news_window = edit_church_news_ui.Ui_Dialog()
            self.ui_edit_church_news_window.setupUi(self.edit_church_news_window)
            self.edit_church_news_window_is_open = True
            self.edit_church_news_window_support_code = edit_church_news_support_ui.Support_Ui_Dialog(self,church_news_number)
            self.edit_church_news_window.exec()
        
    def open_preview_church_news_window(self,church_news_number):
        if(self.preview_church_news_window_is_open==False): 
            self.preview_church_news_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_preview_church_news_window = preview_church_news_ui.Ui_Dialog()
            self.ui_preview_church_news_window.setupUi(self.preview_church_news_window)
            self.preview_church_news_window_is_open = True
            self.preview_church_news_window_support_code = preview_church_news_support_ui.Support_Ui_Dialog(self,church_news_number)
            self.preview_church_news_window.exec()

    # Δελτίο καιρού #
    def open_import_weather_news_window(self,checked):
        if(self.import_weather_news_window_is_open==False): 
            self.import_weather_news_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_import_weather_news_window = import_weather_news_ui.Ui_Dialog()
            self.ui_import_weather_news_window.setupUi(self.import_weather_news_window)
            self.import_weather_news_window_is_open = True
            self.import_weather_news_window_support_code = import_weather_news_support_ui.Support_Ui_Dialog(self)
            self.import_weather_news_window.exec()
    
    def open_search_weather_news_window(self,checked,action):
        if(self.search_weather_news_window_is_open==False): 
            self.search_weather_news_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_search_weather_news_window = search_weather_news_ui.Ui_Dialog()
            self.ui_search_weather_news_window.setupUi(self.search_weather_news_window)
            self.search_weather_news_window_is_open = True
            self.search_weather_news_window_support_code = search_weather_news_support_ui.Support_Ui_Dialog(self,action)
            self.search_weather_news_window.exec()

    def open_export_weather_news_window(self,weather_news_number):
        if(self.export_weather_news_window_is_open==False): 
            self.export_weather_news_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_export_weather_news_window = export_weather_news_ui.Ui_Dialog()
            self.ui_export_weather_news_window.setupUi(self.export_weather_news_window)
            self.export_weather_news_window_is_open = True
            self.export_weather_news_window_support_code = export_weather_news_support_ui.Support_Ui_Dialog(self,weather_news_number)
            self.export_weather_news_window.exec()
        
    def open_edit_weather_news_window(self,weather_news_number):
        if(self.edit_weather_news_window_is_open==False):   
            self.edit_weather_news_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_edit_weather_news_window = edit_weather_news_ui.Ui_Dialog()
            self.ui_edit_weather_news_window.setupUi(self.edit_weather_news_window)
            self.edit_weather_news_window_is_open = True
            self.edit_weather_news_window_support_code = edit_weather_news_support_ui.Support_Ui_Dialog(self,weather_news_number)
            self.edit_weather_news_window.exec()
        
    def open_preview_weather_news_window(self,weathersss_news_number):
        if(self.preview_weather_news_window_is_open==False):    
            self.preview_weather_news_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_preview_weather_news_window = preview_weather_news_ui.Ui_Dialog()
            self.ui_preview_weather_news_window.setupUi(self.preview_weather_news_window)
            self.preview_weather_news_window_is_open = True
            self.preview_weather_news_window_support_code = preview_weather_news_support_ui.Support_Ui_Dialog(self,weather_news_number)
            self.preview_weather_news_window.exec()

    # Ηχογράφηση #
    def open_start_record_window(self,checked):
        if(self.start_record_window_is_open==False):    
            self.start_record_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_start_record_window = start_record_ui.Ui_Dialog()
            self.ui_start_record_window.setupUi(self.start_record_window)
            self.start_record_window_is_open = True
            self.start_record_window_support_code = start_record_support_ui.Support_Ui_Dialog(self)
            self.start_record_window.exec()

    # Αναφορές #
    def open_scheduled_transmition_report_window(self,checked):
        if(self.scheduled_transmition_report_window_is_open==False):    
            self.scheduled_transmition_report_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_scheduled_transmition_report_window = scheduled_transmition_report_ui.Ui_Dialog()
            self.ui_scheduled_transmition_report_window.setupUi(self.scheduled_transmition_report_window)
            self.scheduled_transmition_report_window_is_open = True
            self.scheduled_transmition_report_window_support_code = scheduled_transmition_report_support_ui.Support_Ui_Dialog(self)
            self.scheduled_transmition_report_window.exec()
            
    def open_week_programm_report_window_window(self,checked):
        if(self.weekly_programm_report_window_is_open==False): 
            self.week_report_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_week_report_window = week_report_ui.Ui_Dialog()
            self.ui_week_report_window.setupUi(self.week_report_window)
            self.weekly_programm_report_window_is_open = True
            self.week_report_window_support_code = week_report_support_ui.Support_Ui_Dialog(self)
            self.week_report_window.exec()
        
    def open_decks_history_report_window(self,checked):
        if(self.player_history_report_window_is_open==False):   
            self.player_history_report_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_player_history_report_window = player_history_report_ui.Ui_Dialog()
            self.ui_player_history_report_window.setupUi(self.player_history_report_window)
            self.player_history_report_window_is_open = True
            self.player_history_report_window_support_code = player_history_report_support_ui.Support_Ui_Dialog(self)
            self.player_history_report_window.exec()

        
    def open_listeners_statistics_window(self,checked):
        if(self.listeners_statistics_report_window_is_open==False): 
            self.listeners_statistics_report_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_listeners_statistics_report_window = listeners_statistics_report_ui.Ui_Dialog()
            self.ui_listeners_statistics_report_window.setupUi(self.listeners_statistics_report_window)
            self.listeners_statistics_report_window_is_open = True
            self.listeners_statistics_report_window_support_code = listeners_statistics_report_support_ui.Support_Ui_Dialog(self)
            self.listeners_statistics_report_window.exec()


    # Διαχείριση συσκευών #
    def open_manage_output_devices_window(self,checked):
        if(self.manage_output_devices_window_is_open==False):   
            self.manage_output_devices_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_manage_output_devices_window = manage_output_devices_ui.Ui_Dialog()
            self.ui_manage_output_devices_window.setupUi(self.manage_output_devices_window)
            self.manage_output_devices_window_is_open = True
            self.manage_output_devices_window_support_code = manage_output_devices_support_ui.Support_Ui_Dialog(self)
            if(self.manage_output_devices_window_is_open==True):
                self.manage_output_devices_window.exec()
            
    def open_manage_output_devices_save_question_window(self):
        pass

    def open_manage_output_unable_to_open_process_window(self,description):
        pass
        
    def open_manage_input_devices_window(self,checked):
        if(self.manage_input_device_window_is_open==False): 
            self.manage_input_device_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_manage_input_device_window = manage_input_device_ui.Ui_Dialog()
            self.ui_manage_input_device_window.setupUi(self.manage_input_device_window)
            self.manage_input_device_window_is_open = True
            self.manage_input_device_window_support_code = manage_input_device_support_ui.Support_Ui_Dialog(self)
            self.manage_input_device_window.exec()

    def open_manage_input_device_save_question_window(self):
        pass

            
    #Διαχείριση διεργασιών #
    def open_manage_tasks_window(self,checked):
        if(self.manage_proccesses_window_is_open==False):   
            self.manage_proccesses_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_manage_proccesses_window = manage_proccesses_ui.Ui_Dialog()
            self.ui_manage_proccesses_window.setupUi(self.manage_proccesses_window)
            self.manage_proccesses_window_is_open = True
            self.manage_proccesses_window_support_code = manage_proccesses_support_ui.Support_Ui_Dialog(self)
            self.manage_proccesses_window.exec()

    
    ### Menu 2 ###

    # Επιλογή θέματος #
    def open_choose_theme_window(self,checked):
        if(self.choose_theme_window_is_open==False):    
            self.choose_theme_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_choose_theme_window = choose_theme_ui.Ui_Dialog()
            self.ui_choose_theme_window.setupUi(self.choose_theme_window)
            self.choose_theme_window_is_open = True
            self.choose_theme_window_support_code = choose_theme_support_ui.Support_Ui_Dialog(self)
            self.choose_theme_window.exec()

    def open_change_theme_save_question_window(self):
        if(self.change_theme_save_question_window_is_open==False):    
            self.change_theme_save_question_window = QtWidgets.QDialog(self.choose_theme_window)
            self.ui_change_theme_save_question_window = change_theme_save_question_ui.Ui_Dialog()
            self.ui_change_theme_save_question_window.setupUi(self.change_theme_save_question_window)
            self.change_theme_save_question_window_is_open = True
            self.change_theme_save_question_window_support_code = change_theme_save_question_support_ui.Support_Ui_Dialog(self)
            self.change_theme_save_question_window.exec()

    # Ορατά πεδία λίστας αναπαραγωγής #
    def open_select_player_list_fields_window(self,checked):
        if(self.visible_player_list_fields_window_is_open==False):  
            self.visible_player_list_fields_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_visible_player_list_fields_window = visible_player_list_fields_ui.Ui_Dialog()
            self.ui_visible_player_list_fields_window.setupUi(self.visible_player_list_fields_window)
            self.visible_player_list_fields_window_is_open = True
            self.visible_player_list_fields_window_support_code = visible_player_list_fields_support_ui.Support_Ui_Dialog(self)
            self.visible_player_list_fields_window.exec()
            
    def open_select_player_list_fields_save_question_window(self):
        pass
 

    # Ορατά πεδία προγράμματος #
    def open_programm_components_window(self,checked):
        if(self.visible_program_components_window_is_open==False): 
            self.visible_programm_components_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_visible_programm_components_window = visible_programm_components_ui.Ui_Dialog()
            self.ui_visible_programm_components_window.setupUi(self.visible_programm_components_window)
            self.visible_program_components_window_is_open = True
            self.visible_programm_components_window_support_code = visible_programm_components_support_ui.Support_Ui_Dialog(self)
            self.visible_programm_components_window.exec()
            
    def open_visible_programm_components_save_question_window(self):
        pass
    
    ### Menu 3 ###

    # Προγραμματισμένες μεταδόσεις #
    def open_new_scheduled_transmition_window(self,checked):
        if(self.create_schedule_transmition_window_is_open==False):    
            self.create_schedule_transmition_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_create_schedule_transmition_window = import_scheduled_transmition_ui.Ui_Dialog()
            self.ui_create_schedule_transmition_window.setupUi(self.create_schedule_transmition_window)
            self.create_schedule_transmition_window_is_open = True
            self.create_schedule_transmition_window_support_code = import_scheduled_transmition_support_ui.Support_Ui_Dialog(self)
            self.create_schedule_transmition_window.exec()
    
    def open_review_transmitions_window(self,checked):
        if(self.explore_scheduled_transmitions_window_is_open==False):   
            self.manage_scheduled_transmitions_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_manage_scheduled_transmitions_window = manage_scheduled_transmitions_ui.Ui_Dialog()
            self.ui_manage_scheduled_transmitions_window.setupUi(self.manage_scheduled_transmitions_window)
            self.explore_scheduled_transmitions_window_is_open = True
            self.manage_scheduled_transmitions_window_support_code = manage_scheduled_transmitions_support_ui.Support_Ui_Dialog(self)
            self.manage_scheduled_transmitions_window.exec()

    # Ραδιοφωνικοί σταθμοί #
    def open_new_radio_connection_window(self,checked):
        if(self.import_radio_station_window_is_open==False):    
            self.import_radio_station_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_import_radio_station_window = import_radio_station_ui.Ui_Dialog()
            self.ui_import_radio_station_window.setupUi(self.import_radio_station_window)
            self.import_radio_station_window_is_open = True
            self.import_radio_station_window_support_code = import_radio_station_support_ui.Support_Ui_Dialog(self)
            self.import_radio_station_window.exec()
            
    def open_modify_radio_connections_window(self,checked):
        if(self.edit_radio_stations_window_is_open==False): 
            self.edit_radio_stations_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_edit_radio_stations_window = edit_radio_stations_ui.Ui_Dialog()
            self.ui_edit_radio_stations_window.setupUi(self.edit_radio_stations_window)
            self.edit_radio_stations_window_is_open = True
            self.edit_radio_stations_window_support_code = edit_radio_stations_support_ui.Support_Ui_Dialog(self)
            self.edit_radio_stations_window.exec()

        
    ### Menu 4 ###

    # Λίγα λόγια για το πρόγραμμα #
    def open_programm_abstract_information_window(self,checked):
        if(self.programm_abstract_information_window_is_open==False):   
            self.programm_abstract_information_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_programm_abstract_information_window = programm_abstract_information_ui.Ui_Dialog()
            self.ui_programm_abstract_information_window.setupUi(self.programm_abstract_information_window)
            self.programm_abstract_information_window_is_open = True
            self.programm_abstract_information_window_support_code = programm_abstract_information_support_ui.Support_Ui_Dialog(self)
            self.programm_abstract_information_window.exec()
            
    # Επικοινωνία #
    def open_contact_window(self,checked):
        if(self.contact_window_is_open==False): 
            self.contact_window = QtWidgets.QDialog(self.MainWindow)
            self.ui_contact_window = contact_ui.Ui_Dialog()
            self.ui_contact_window.setupUi(self.contact_window)
            self.contact_window_is_open = True
            self.contact_window_support_code = contact_support_ui.Support_Ui_Dialog(self)
            self.contact_window.exec()
            
    def closeEvent(self,event):
        event.accept()
        '''
        self.manage_player_list_table_instance.auto_dj = 0
        self.manage_decks_instance.quit_requested = True
        if self.decks_state_saved==False:
            self.manage_decks_instance.save_decks_state()
            self.decks_state_saved = True
        self.manage_decks_instance.deck_1_status_changed("stopped")
        self.manage_decks_instance.deck_2_status_changed("stopped")
        self.manage_decks_instance.music_clip_deck_status_changed("stopped")
        #print(self.manage_decks_instance.saves_in_progress)
        #print(self.manage_player_list_table_instance.saves_in_progress)
        #print(self.manage_microphone_instance.saves_in_progress)
        if self.manage_decks_instance.saves_in_progress<=0 and self.manage_player_list_table_instance.saves_in_progress <= 0 and self.manage_microphone_instance.saves_in_progress<=0:
            
            q_size = self.manage_player_list_table_instance.main_player_list_queue.qsize()
            while(q_size!=0):
                time.sleep(1)
                q_size = self.manage_player_list_table_instance.main_player_list_queue.qsize()
            self.manage_player_list_table_instance.main_player_list_child_process.terminate()
            self.manage_player_list_table_instance.main_player_list_emitter.terminate()
            
            q_size = self.manage_microphone_instance.microphone_queue.qsize()
            while(q_size!=0):
                q_data = self.manage_microphone_instance.microphone_queue.get()
                q_size = self.manage_microphone_instance.microphone_queue.qsize()
            #q_size = self.manage_microphone_instance.microphone_sound_data_queue.qsize()
            #q = Queue.Queue()
            self.manage_microphone_instance.microphone_sound_data_queue = Queue()
            #while(q_size!=0):
            #    q_data = self.manage_microphone_instance.microphone_sound_data_queue.get()
            #    q_size = self.manage_microphone_instance.microphone_sound_data_queue.qsize()
            self.manage_microphone_instance.microphone_child_process.terminate()
            self.manage_microphone_instance.microphone_emitter.terminate()

            q_size = self.manage_decks_instance.manage_deck_1_queue.qsize()
            while(q_size!=0):
                q_data = self.manage_decks_instance.manage_deck_1_queue.get()
                q_size = self.manage_decks_instance.manage_deck_1_queue.qsize()
            self.manage_decks_instance.manage_deck_1_child_process.terminate()
            self.manage_decks_instance.manage_deck_1_emitter.terminate()
            
            q_size = self.manage_decks_instance.manage_deck_2_queue.qsize()
            while(q_size!=0):
                q_data = self.manage_decks_instance.manage_deck_2_queue.get()
                q_size = self.manage_decks_instance.manage_deck_2_queue.qsize()
            self.manage_decks_instance.manage_deck_2_child_process.terminate()
            self.manage_decks_instance.manage_deck_2_emitter.terminate()
            
            q_size = self.manage_decks_instance.manage_music_clip_deck_queue.qsize()
            while(q_size!=0):
                q_data = self.manage_decks_instance.manage_music_clip_deck_queue.get()
                q_size = self.manage_decks_instance.manage_music_clip_deck_queue.qsize()
            self.manage_decks_instance.manage_music_clip_deck_child_process.terminate()
            self.manage_decks_instance.manage_music_clip_deck_emitter.terminate()

            q_size = self.manage_decks_instance.manage_final_sound_queue.qsize()
            while(q_size!=0):
                q_data = self.manage_decks_instance.manage_final_sound_queue.get()
                q_size = self.manage_decks_instance.manage_final_sound_queue.qsize()
            self.manage_decks_instance.manage_final_sound_child_process.terminate()
            self.manage_decks_instance.manage_final_sound_emitter.terminate()
            
            q_size = self.manage_decks_instance.manage_decks_saves_queue.qsize()
            while(q_size!=0):
                q_data = self.manage_decks_instance.manage_decks_saves_queue.get()
                q_size = self.manage_decks_instance.manage_decks_saves_queue.qsize()
            self.manage_decks_instance.manage_decks_saves_child_process.terminate()
            self.manage_decks_instance.manage_decks_saves_emitter.terminate()
            
            q_size = self.manage_decks_instance.system_volume_queue.qsize()
            while(q_size!=0):
                q_data = self.manage_decks_instance.system_volume_queue.get()
                q_size = self.manage_decks_instance.system_volume_queue.qsize()
            self.manage_decks_instance.system_volume_child_process.terminate()
            self.manage_decks_instance.system_volume_emitter.terminate()
            
            q_size = self.manage_decks_instance.internet_connection_queue.qsize()
            while(q_size!=0):
                q_data = self.manage_decks_instance.internet_connection_queue.get()
                q_size = self.manage_decks_instance.internet_connection_queue.qsize()
            self.manage_decks_instance.internet_connection_child_process.terminate()
            self.manage_decks_instance.internet_connection_emitter.terminate()


            self.programm_components_emitter.terminate()
            self.programm_components_child_process.terminate()
            
            counter = 0
            for process in self.manage_processes_instance.processes:
                if "process_number" in process:
                    if process["process_number"]==self.manage_player_list_table_instance.proccess_number or process["process_number"]==self.manage_microphone_instance.proccess_number or process["process_number"]==self.manage_decks_instance.manage_final_sound_process_number or process["process_number"]==self.manage_decks_instance.manage_deck_1_process_number or process["process_number"]==self.manage_decks_instance.manage_deck_2_process_number or process["process_number"]==self.manage_decks_instance.manage_music_clip_deck_process_number or process["process_number"]==self.manage_decks_instance.manage_decks_saves_process_number or process["process_number"]==self.manage_decks_instance.system_volume_process_number or process["process_number"]==self.manage_decks_instance.internet_connection_process_number or process["process_number"]==self.programm_components_proccess_number:
                        self.manage_processes_instance.processes[counter]["pid"] = None
                        self.manage_processes_instance.processes[counter]["start_datetime"] = None
                        self.manage_processes_instance.processes[counter]["status"] = "stopped"
                        self.manage_processes_instance.processes[counter]["cpu"] = 0
                        self.manage_processes_instance.processes[counter]["ram"] = 0
                counter += 1
            
            del self.manage_decks_instance
            del self.manage_microphone_instance
            del self.manage_player_list_table_instance
            
            event.accept()
        else:
            self.manage_player_list_table_instance.quit_requested = True
            self.manage_microphone_instance.quit_requested = True
            event.ignore()
        
        '''
        
        
        
        '''
        self.manage_decks_instance.save_deck_state()
        if self.manage_decks_instance.saves_in_progress==0 and self.manage_player_list_table_instance.saves_in_progress == 0 and self.manage_microphone_instance.saves_in_progress==0:
        
            self.manage_player_list_table_instance.main_player_list_child_process.terminate()
            self.manage_player_list_table_instance.main_player_list_emitter.terminate()
            
            self.manage_microphone_instance.microphone_child_process.terminate()
            self.manage_microphone_instance.microphone_emitter.terminate()
            
            self.manage_decks_instance.manage_deck_1_child_process.terminate()
            self.manage_decks_instance.manage_deck_1_emitter.terminate()
            self.manage_decks_instance.manage_deck_2_child_process.terminate()
            self.manage_decks_instance.manage_deck_2_emitter.terminate()
            self.manage_decks_instance.manage_music_clip_deck_child_process.terminate()
            self.manage_decks_instance.manage_music_clip_deck_emitter.terminate()

            
            self.manage_decks_instance.manage_final_sound_child_process.terminate()
            self.manage_decks_instance.manage_final_sound_emitter.terminate()
            
            counter = 0
            for process in self.manage_processes_instance.processes:
                if "process_number" in process:
                    if process["process_number"]==self.manage_player_list_table_instance.proccess_number or process["process_number"]==self.manage_microphone_instance.proccess_number or process["process_number"]==self.manage_decks_instance.manage_final_sound_process_number or process["process_number"]==self.manage_decks_instance.manage_deck_1_process_number or process["process_number"]==self.manage_decks_instance.manage_deck_2_process_number or process["process_number"]==self.manage_decks_instance.manage_music_clip_deck_process_number:
                        self.manage_processes_instance.processes[counter]["pid"] = None
                        self.manage_processes_instance.processes[counter]["start_datetime"] = None
                        self.manage_processes_instance.processes[counter]["status"] = "stopped"
                        self.manage_processes_instance.processes[counter]["cpu"] = 0
                        self.manage_processes_instance.processes[counter]["ram"] = 0
                counter += 1
                
            
            event.accept()
        else:
            self.manage_player_list_table_instance.quit_requested = True
            self.manage_microphone_instance.quit_requested = True
            event.ignore()
        '''

class Programm_Components_Emitter(QThread):

    programm_components_ready = pyqtSignal(dict)

    def __init__(self, from_process: Pipe):
        super().__init__()
        self.data_from_process = from_process

    def run(self):
        while True:
            data = self.data_from_process.recv()
            if data["type"]=="programm_components_ready":
                self.programm_components_ready.emit(data["settings"])
                
class Programm_Components_Child_Proc(Process):

    def __init__(self, to_emitter, from_mother):
        super().__init__()
        self.daemon = False
        self.to_emitter = to_emitter
        self.data_from_mother = from_mother
        
    def run(self):
        self.programm_components()
        while(True):
            data = self.data_from_mother.get()
            if data["type"] == "programm_components":
                self.programm_components()
                
    def programm_components(self):
        program_component_time_lines = int(database_functions.read_setting("program_component_time_lines")["current_value"])
        program_component_general_deck = int(database_functions.read_setting("program_component_general_deck")["current_value"])
        program_component_deck_1 = int(database_functions.read_setting("program_component_deck_1")["current_value"])
        program_component_deck_2 = int(database_functions.read_setting("program_component_deck_2")["current_value"])
        program_component_music_clip_deck = int(database_functions.read_setting("program_component_music_clip_deck")["current_value"])
        program_component_speackers_deck = int(database_functions.read_setting("program_component_speackers_deck")["current_value"])
        program_component_ip_calls = int(database_functions.read_setting("program_component_ip_calls")["current_value"])
        program_component_player_list = int(database_functions.read_setting("program_component_player_list")["current_value"])
        program_component_web_sites = int(database_functions.read_setting("program_component_web_sites")["current_value"])

        
        settings = {
            "program_component_time_lines":program_component_time_lines,
            "program_component_general_deck":program_component_general_deck,
            "program_component_deck_1":program_component_deck_1,
            "program_component_deck_2":program_component_deck_2,
            "program_component_music_clip_deck":program_component_music_clip_deck,
            "program_component_speackers_deck":program_component_speackers_deck,
            "program_component_ip_calls":program_component_ip_calls,
            "program_component_player_list":program_component_player_list,
            "program_component_web_sites":program_component_web_sites
        }
        
        self.to_emitter.send({"type":"programm_components_ready","settings":settings})

if __name__=="__main__":
    freeze_support()
    programm = Papinhio_player()