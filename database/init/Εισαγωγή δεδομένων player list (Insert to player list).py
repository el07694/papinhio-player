import os
import sqlite3
from sqlite3 import Error
import sys

sys.path.append("..")
import importlib
sqlite3_functions = importlib.import_module("Αρχεία πηγαίου κώδικα εφαρμογής (Python).Αρχεία κώδικα python (Python files).Συναρτήσεις sqlite3 (Sqlite3 functions)")


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

def main():
    conn = create_connection("Βάση δεδομένων (Database).db")
    cur = conn.cursor()

    sql = """ DELETE FROM `player_list`;"""
    cur.execute(sql)
    conn.commit()

    sql = """ INSERT INTO `player_list` (`play`, `relative_type`, `relative_number`, `repeats`, `duration_milliseconds`, `duration_human`, `position`) VALUES ( ?, ?, ?, ?, ?, ?, ?) """

    sql_2 = """SELECT * FROM `sound_files`;"""
    
    cur.execute(sql_2)
    all_songs = cur.fetchall()
    conn.commit()
    position = 0
    for song in all_songs:
        position += 1
        player_list_entry = (1,"sound files",song[0],0,song[17],song[18],position)
        playlist_list_item = {
            "play":1,
            "relative_type":"sound_files",
            "relative_number":player_list_entry[2],
            "repeats":0,
            "duration_milliseconds":player_list_entry[4],
            "duration_human":player_list_entry[5],
            "position":player_list_entry[6]
        }
        sqlite3_functions.import_player_list_item(playlist_list_item)
        

    sql_2 = """SELECT * FROM `sound_clips`;"""
    
    cur.execute(sql_2)
    all_songs = cur.fetchall()
    conn.commit()
    for song in all_songs:
        position += 1
        player_list_entry = (1,"sound clips",song[0],0,song[10],song[11],position)
        playlist_list_item = {
            "play":1,
            "relative_type":"sound_clips",
            "relative_number":player_list_entry[2],
            "repeats":0,
            "duration_milliseconds":player_list_entry[4],
            "duration_human":player_list_entry[5],
            "position":player_list_entry[6]
        }
        sqlite3_functions.import_player_list_item(playlist_list_item)
    
    sql_2 = """SELECT * FROM `retransmitions`;"""
    
    cur.execute(sql_2)
    all_songs = cur.fetchall()
    conn.commit()
    for song in all_songs:
        position += 1
        player_list_entry = (1,"retransmitions",song[0],0,3600000,"01:00:00",position)
        playlist_list_item = {
            "play":1,
            "relative_type":"retransmitions",
            "relative_number":player_list_entry[2],
            "repeats":0,
            "duration_milliseconds":player_list_entry[4],
            "duration_human":player_list_entry[5],
            "position":player_list_entry[6]
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
        
main()