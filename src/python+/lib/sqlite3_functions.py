import sqlite3
from sqlite3 import Error
import os
import sys

''' 
    Τύποι δεδομένων:
    
    Αρχεία ήχου:                            sound_files
    Ηχητικά clips:                          sound_clips
    Σήματα σταθμού:                         station_logos
    Αναμεταδόσεις:                          retransmitions
    Τηλεφωνικές κλήσεις:                    ip_calls
    Συλλογές Ώρα:                           time_collections - time_items
    Εκκλησιαστικά δελτία ανακοινώσεων:      church_news
    Δελτία καιρού:                          weather_news
    Λίστες αναπαραγωγής:                    playlists - playlists_items
    
'''

### CRUD+ logic (Create - Read - Update - Delete Logic + Extra operations) ###

def create_connection():
    conn = None
    if getattr(sys, 'frozen', False):
        db_file = "database.db"
    else:
        db_file = os.path.abspath("../../database/database.db")
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        
    return conn

### settings ###

def import_setting(setting):
    query = "INSERT INTO `settings` (`keyword`,`current_value`) VALUES(?,?);"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(setting["keyword"]),str(setting["current_value"])))
    conn.commit()
    conn.close()
    setting["number"] = cur.lastrowid
    return setting
   
def read_setting(keyword):
    query = "SELECT * FROM `settings` WHERE `keyword`=? LIMIT 1;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(keyword),))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    if len(rows)>0:
        row = rows[0]
        setting = {"number":row[0],"keyword":row[1],"current_value":row[2]}
    else:
        setting = {}
    return setting

def read_settings():
    query = "SELECT * FROM `settings`;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    settings = []
    for row in rows:
        settings.append({"number":row[0],"keyword":row[1],"current_value":row[2]})
    return settings
    
def search_settings(search_phrase):
    query = "SELECT * FROM `settings` WHERE `keyword` LIKE ? OR `current_value` LIKE ?;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,('%'+str(search_phrase)+'%','%'+str(search_phrase)+'%'))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    settings = []
    for row in rows:
        settings.append({"number":row[0],"keyword":row[1],"current_value":row[2]})
    return settings
    
def update_setting(setting):
    conn = create_connection()
    query = "UPDATE `settings` SET `current_value`=? WHERE `keyword`=?;"
    cur = conn.cursor()
    cur.execute(query,(str(setting["current_value"]),str(setting["keyword"])))
    conn.commit()
    conn.close()
    return setting

def delete_setting(setting):
    conn = create_connection()
    query = "DELETE FROM `settings` WHERE `keyword`=?;"
    cur = conn.cursor()
    cur.execute(query,(str(setting["keyword"]),))
    conn.commit()
    conn.close()
    return 1

### sound_files ###

def import_sound_file(sound_file):
    query = "INSERT INTO `sound_files` (`title`,`artist`,`composer`,`author`,`album`,`year`,`genre`,`image_path`,`image_title`,`description`,`rating`,`volume`,`normalize`,`pan`,`low_frequency`,`high_frequency`,`duration_milliseconds`,`duration_human`,`original_path`,`saved_path`) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(sound_file["title"]),str(sound_file["artist"]),str(sound_file["composer"]),str(sound_file["author"]),str(sound_file["album"]),str(sound_file["year"]),str(sound_file["genre"]),str(sound_file["image_path"]),str(sound_file["image_title"]),str(sound_file["description"]),sound_file["rating"],sound_file["volume"],sound_file["normalize"],sound_file["pan"],sound_file["low_frequency"],sound_file["high_frequency"],sound_file["duration_milliseconds"],str(sound_file["duration_human"]),str(sound_file["original_path"]),str(sound_file["saved_path"])))
    conn.commit()
    conn.close()
    sound_file["number"] = cur.lastrowid
    sound_file["type"] = "sound_files"
    return sound_file
    
def read_sound_file(sound_file_number):
    query = "SELECT * FROM `sound_files` WHERE `number`=? LIMIT 1;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(sound_file_number,))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    row = rows[0]
    sound_file = {"type":"sound_files","number":row[0],"title":row[1],"artist":row[2],"composer":row[3],"author":row[4],"album":row[5],"year":row[6],"genre":row[7],"image_path":row[8],"image_title":row[9],"description":row[10],"rating":row[11],"volume":row[12],"normalize":row[13],"pan":row[14],"low_frequency":row[15],"high_frequency":row[16],"duration_milliseconds":row[17],"duration_human":row[18],"original_path":row[19],"saved_path":row[20]}
    return sound_file

def read_sound_files():
    query = "SELECT * FROM `sound_files`;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    sound_files = []
    for row in rows:
        sound_files.append({"type":"sound_files","number":row[0],"title":row[1],"artist":row[2],"composer":row[3],"author":row[4],"album":row[5],"year":row[6],"genre":row[7],"image_path":row[8],"image_title":row[9],"description":row[10],"rating":row[11],"volume":row[12],"normalize":row[13],"pan":row[14],"low_frequency":row[15],"high_frequency":row[16],"duration_milliseconds":row[17],"duration_human":row[18],"original_path":row[19],"saved_path":row[20]})
    return sound_files

def search_sound_files(search_phrase):
    query = "SELECT * FROM `sound_files` WHERE `title` LIKE ? OR `artist` LIKE ? OR `composer` LIKE ? OR `author` LIKE ? OR `album` LIKE ? OR `year` LIKE ? OR `genre` LIKE ? OR `image_title` LIKE ? OR `description` LIKE ?;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,('%'+str(search_phrase)+'%','%'+str(search_phrase)+'%','%'+str(search_phrase)+'%','%'+str(search_phrase)+'%','%'+str(search_phrase)+'%','%'+str(search_phrase)+'%','%'+str(search_phrase)+'%','%'+str(search_phrase)+'%','%'+str(search_phrase)+'%'))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    sound_files = []
    for row in rows:
        sound_files.append({"type":"sound_files","number":row[0],"title":row[1],"artist":row[2],"composer":row[3],"author":row[4],"album":row[5],"year":row[6],"genre":row[7],"image_path":row[8],"image_title":row[9],"description":row[10],"rating":row[11],"volume":row[12],"normalize":row[13],"pan":row[14],"low_frequency":row[15],"high_frequency":row[16],"duration_milliseconds":row[17],"duration_human":row[18],"original_path":row[19],"saved_path":row[20]})
    return sound_files
    
def update_sound_file(sound_file):
    conn = create_connection()
    query = "UPDATE `sound_files` SET `title`=?,`artist`=?,`composer`=?,`author`=?, `album`=?, `year`=?,`genre`=?,`image_path`=?,`image_title`=?, `description`=?,`rating`=?,`volume`=?,`normalize`=?,`pan`=?,`low_frequency`=?,`high_frequency`=?,`duration_milliseconds`=?,`duration_human`=?,`original_path`=?, `saved_path`=? WHERE `number`=?;"
    cur = conn.cursor()
    cur.execute(query,(str(sound_file["title"]),str(sound_file["artist"]),str(sound_file["composer"]),str(sound_file["author"]),str(sound_file["album"]),str(sound_file["year"]),str(sound_file["genre"]),str(sound_file["image_path"]),str(sound_file["image_title"]),str(sound_file["description"]),sound_file["rating"],sound_file["volume"],sound_file["normalize"],sound_file["pan"],sound_file["low_frequency"],sound_file["high_frequency"],sound_file["duration_milliseconds"],str(sound_file["duration_human"]),str(sound_file["original_path"]),str(sound_file["saved_path"]),sound_file["number"]))
    conn.commit()
    conn.close()
    return sound_file
    
def delete_sound_file(sound_file):
    conn = create_connection()
    query = "DELETE FROM `sound_files` WHERE `number`=? AND `title`=?;"
    cur = conn.cursor()
    cur.execute(query,(sound_file["number"],str(sound_file["title"])))
    conn.commit()
    
    
    conn.close()
    return 1
    
### sound_clips ###

def import_sound_clip(sound_clip):
    query = "INSERT INTO `sound_clips` (`title`,`position`,`description`,`rating`,`volume`,`normalize`,`pan`,`low_frequency`,`high_frequency`,`duration_milliseconds`,`duration_human`,`original_path`,`saved_path`) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?);"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(sound_clip["title"]),sound_clip["position"],str(sound_clip["description"]),sound_clip["rating"],sound_clip["volume"],sound_clip["normalize"],sound_clip["pan"],sound_clip["low_frequency"],sound_clip["high_frequency"],sound_clip["duration_milliseconds"],str(sound_clip["duration_human"]),str(sound_clip["original_path"]),str(sound_clip["saved_path"])))
    conn.commit()
    conn.close()
    sound_clip["number"] = cur.lastrowid
    sound_clip["type"] = "sound_clips"
    return sound_clip
    
def read_sound_clip(sound_clip_number):
    query = "SELECT * FROM `sound_clips` WHERE `number`=? LIMIT 1;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(sound_clip_number,))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    row = rows[0]
    sound_clip = {"type":"sound_clips","number":row[0],"title":row[1],"position":row[2],"description":row[3],"rating":row[4],"volume":row[5],"normalize":row[6],"pan":row[7],"low_frequency":row[8],"high_frequency":row[9],"duration_milliseconds":row[10],"duration_human":row[11],"original_path":row[12],"saved_path":row[13]}
    return sound_clip

def read_sound_clips():
    query = "SELECT * FROM `sound_clips` ORDER BY `position`;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    sound_clips = []
    for row in rows:
        sound_clips.append({"type":"sound_clips","number":row[0],"title":row[1],"position":row[2],"description":row[3],"rating":row[4],"volume":row[5],"normalize":row[6],"pan":row[7],"low_frequency":row[8],"high_frequency":row[9],"duration_milliseconds":row[10],"duration_human":row[11],"original_path":row[12],"saved_path":row[13]})
    return sound_clips

def read_top_sound_clips(total):
    query = "SELECT * FROM `sound_clips` ORDER BY `position` LIMIT ?;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(total,))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    sound_clips = []
    for row in rows:
        sound_clips.append({"type":"sound_clips","number":row[0],"title":row[1],"position":row[2],"description":row[3],"rating":row[4],"volume":row[5],"normalize":row[6],"pan":row[7],"low_frequency":row[8],"high_frequency":row[9],"duration_milliseconds":row[10],"duration_human":row[11],"original_path":row[12],"saved_path":row[13]})
    return sound_clips
    
def search_sound_clips(search_phrase):                                                                        
    query = "SELECT * FROM `sound_clips` WHERE `title` LIKE ? OR `description` LIKE ?;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,('%'+str(search_phrase)+'%','%'+str(search_phrase)+'%'))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    sound_clips = []
    for row in rows:
        sound_clips.append({"type":"sound_clips","number":row[0],"title":row[1],"position":row[2],"description":row[3],"rating":row[4],"volume":row[5],"normalize":row[6],"pan":row[7],"low_frequency":row[8],"high_frequency":row[9],"duration_milliseconds":row[10],"duration_human":row[11],"original_path":row[12],"saved_path":row[13]})
    return sound_clips
    
def update_sound_clip(sound_clip):
    conn = create_connection()
    query = "UPDATE `sound_clips` SET `title`=?,`position`=?,`description`=?,`rating`=?, `volume`=?,`normalize`=?,`pan`=?,`low_frequency`=?,`high_frequency`=?,`duration_milliseconds`=?,`duration_human`=?,`original_path`=?, `saved_path`=? WHERE `number`=?;"
    cur = conn.cursor()
    cur.execute(query,(str(sound_clip["title"]),sound_clip["position"],str(sound_clip["description"]),sound_clip["rating"],sound_clip["volume"],sound_clip["normalize"],sound_clip["pan"],sound_clip["low_frequency"],sound_clip["high_frequency"],sound_clip["duration_milliseconds"],str(sound_clip["duration_human"]),str(sound_clip["original_path"]),str(sound_clip["saved_path"]),sound_clip["number"]))
    conn.commit()
    conn.close()
    return sound_clip

def order_sound_clips(sound_clips):
    sound_clips_len = len(sound_clips)
    conn = create_connection()
    query = "UPDATE `sound clips` SET `position`=? WHERE `number`=?;"
    position = sound_clips_len + 1
    cur = conn.cursor()
    for sound_clip in sound_clips:
        cur.execute(query,(position,sound_clip["number"]))
        conn.commit()
        position += 1
    conn.close()
    for sound_clip in sound_clips:
        update_sound_clip(sound_clip)
    
    return 1
    
def delete_sound_clip(sound_clip):
    conn = create_connection()
    query = "DELETE FROM `sound_clips` WHERE `number`=? AND `title`=?;"
    cur = conn.cursor()
    cur.execute(query,(sound_clip["number"],str(sound_clip["title"])))
    conn.commit()
    
    conn.close()
    return 1
    
### station_logos ###

def import_station_logo(station_logo,is_default=0):
    query = "INSERT INTO `station_logos` (`title`,`description`,`rating`,`volume`,`normalize`,`pan`,`low_frequency`,`high_frequency`,`duration_milliseconds`,`duration_human`,`original_path`,`saved_path`) VALUES(?,?,?,?,?,?,?,?,?,?,?,?);"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(station_logo["title"]),str(station_logo["description"]),station_logo["rating"],station_logo["volume"],station_logo["normalize"],station_logo["pan"],station_logo["low_frequency"],station_logo["high_frequency"],station_logo["duration_milliseconds"],str(station_logo["duration_human"]),str(station_logo["original_path"]),str(station_logo["saved_path"])))
    conn.commit()
    station_logo["number"] = cur.lastrowid
    station_logo["type"] = "station_logos"
    conn.close()
    if is_default==1:
        default_station_logo = read_setting("default_station_logo")
        if default_station_logo != {}:
            update_setting({"number":default_station_logo["number"],"keyword":"default_station_logo","current_value":station_logo["number"]})
        else:
            import_setting({"keyword":"default_station_logo","current_value":station_logo["number"]})    
    return station_logo
    
def read_station_logo(station_logo_number):
    query = "SELECT * FROM `station_logos` WHERE `number`=? LIMIT 1;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(station_logo_number,))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    row = rows[0]
    station_logo = {"type":"station_logos","number":row[0],"title":row[1],"description":row[2],"rating":row[3],"volume":row[4],"normalize":row[5],"pan":row[6],"low_frequency":row[7],"high_frequency":row[8],"duration_milliseconds":row[9],"duration_human":row[10],"original_path":row[11],"saved_path":row[12]}
    return station_logo

def read_station_logos():
    query = "SELECT * FROM `station_logos`;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    station_logos = []
    for row in rows:
        station_logos.append({"type":"station_logos","number":row[0],"title":row[1],"description":row[2],"rating":row[3],"volume":row[4],"normalize":row[5],"pan":row[6],"low_frequency":row[7],"high_frequency":row[8],"duration_milliseconds":row[9],"duration_human":row[10],"original_path":row[11],"saved_path":row[12]})
    return station_logos
    
def read_default_station_logo():
    default_station_logo = read_setting("default_station_logo")
    if default_station_logo == {}:
        return None
    else:
        default_station_logo_number = int(default_station_logo["current_value"])
        query = "SELECT * FROM `station_logos` WHERE `number`=? LIMIT 1;"
        conn = create_connection()
        cur = conn.cursor()
        cur.execute(query,(default_station_logo_number,))
        rows = cur.fetchall()
        conn.commit()
        conn.close()
        row = rows[0]
        station_logo = {"type":"station_logos","number":row[0],"title":row[1],"description":row[2],"rating":row[3],"volume":row[4],"normalize":row[5],"pan":row[6],"low_frequency":row[7],"high_frequency":row[8],"duration_milliseconds":row[9],"duration_human":row[10],"original_path":row[11],"saved_path":row[12]}
        return station_logo

def search_station_logos(search_phrase):
    query = "SELECT * FROM `station_logos` WHERE `title` LIKE ? OR `description` LIKE ? ;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,('%'+str(search_phrase)+'%','%'+str(search_phrase)+'%'))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    station_logos = []
    for row in rows:
        station_logos.append({"type":"station_logos","number":row[0],"title":row[1],"description":row[2],"rating":row[3],"volume":row[4],"normalize":row[5],"pan":row[6],"low_frequency":row[7],"high_frequency":row[8],"duration_milliseconds":row[9],"duration_human":row[10],"original_path":row[11],"saved_path":row[12]})
    return station_logos
 
def update_station_logo(station_logo):
    query = "UPDATE `station_logos` SET `title`=?, `description`=?, `rating`=?, `volume`=?, `normalize`=?, `pan`=?, `low_frequency`=?, `high_frequency`=?, `duration_milliseconds`=?, `duration_human`=?, `original_path`=?, `saved_path`=? WHERE `number`=?;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(station_logo["title"]),str(station_logo["description"]),station_logo["rating"],station_logo["volume"],station_logo["normalize"],station_logo["pan"],station_logo["low_frequency"],station_logo["high_frequency"],station_logo["duration_milliseconds"],str(station_logo["duration_human"]),str(station_logo["original_path"]),str(station_logo["saved_path"]),station_logo["number"]))
    conn.commit()
    conn.close()
    return station_logo
    
def delete_station_logo(station_logo):
    conn = create_connection()
    query = "DELETE FROM `station_logos` WHERE `number`=? AND `title`=?;"
    cur = conn.cursor()
    cur.execute(query,(station_logo["number"],str(station_logo["title"])))
    conn.commit()

    default_station_logo = read_setting("default_station_logo")
    if default_station_logo != {}:
        if int(default_station_logo["number"])==station_logo["number"]:
            delete_setting(default_station_logo)
    
    conn.close()
    return 1

### church_news ###

def import_church_new(church_new):
    query = "INSERT INTO `church_news` (`title`,`date`,`rating`,`volume`,`normalize`,`pan`,`low_frequency`,`high_frequency`,`is_default`,`from`,`duration_milliseconds`,`duration_human`,`original_path`,`saved_path`) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(church_new["title"]),str(church_new["date"]),church_new["rating"],church_new["volume"],church_new["normalize"],church_new["pan"],church_new["low_frequency"],church_new["high_frequency"],church_new["is_default"],str(church_new["from"]),church_new["duration_milliseconds"],str(church_new["duration_human"]),str(church_new["original_path"]),str(church_new["saved_path"])))
    conn.commit()
    conn.close()
    church_new["number"] = cur.lastrowid
    church_new["type"] = "church_news"
    return church_new
    
def read_church_new(church_new_number):
    query = "SELECT * FROM `church_news` WHERE `number`=? LIMIT 1;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(church_new_number,))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    row = rows[0]
    church_new = {"type":"church_news","number":row[0],"title":row[1],"date":row[2],"rating":row[3],"volume":row[4],"normalize":row[5],"pan":row[6],"low_frequency":row[7],"high_frequency":row[8],"is_default":row[9],"from":row[10],"duration_milliseconds":row[11],"duration_human":row[12],"original_path":row[13],"saved_path":row[14]}
    return church_new

def read_church_news():
    query = "SELECT * FROM `church_news`;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    church_news = []
    for row in rows:
        church_news.append({"type":"church_news","number":row[0],"title":row[1],"date":row[2],"rating":row[3],"volume":row[4],"normalize":row[5],"pan":row[6],"low_frequency":row[7],"high_frequency":row[8],"is_default":row[9],"from":row[10],"duration_milliseconds":row[11],"duration_human":row[12],"original_path":row[13],"saved_path":row[14]})
    return church_news
    
def read_default_church_new(church_new_datetime):
    query = "SELECT * FROM `church_news` WHERE `is_default`=1 AND `date`=?;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(church_new_datetime),))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    church_news = []
    for row in rows:
        church_news.append({"type":"church_news","number":row[0],"title":row[1],"date":row[2],"rating":row[3],"volume":row[4],"normalize":row[5],"pan":row[6],"low_frequency":row[7],"high_frequency":row[8],"is_default":row[9],"from":row[10],"duration_milliseconds":row[11],"duration_human":row[12],"original_path":row[13],"saved_path":row[14]})
    return church_news

def search_church_news(search_phrase,church_new_datetime):
    query = "SELECT * FROM `church_news` WHERE `date`=? AND (`title` LIKE ? OR `from` LIKE ? );"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(church_new_datetime),'%'+str(search_phrase)+'%','%'+str(search_phrase)+'%'))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    church_news = []
    for row in rows:
        church_news.append({"type":"church_news","number":row[0],"title":row[1],"date":row[2],"rating":row[3],"volume":row[4],"normalize":row[5],"pan":row[6],"low_frequency":row[7],"high_frequency":row[8],"is_default":row[9],"from":row[10],"duration_milliseconds":row[11],"duration_human":row[12],"original_path":row[13],"saved_path":row[14]})
    return church_news
    
def update_church_new(church_new):
    conn = create_connection()
    query = "UPDATE `church_news` SET `title`=?,`date`=?,`rating`=?,`volume`=?, `normalize`=?,`pan`=?,`low_frequency`=?,`high_frequency`=?,`is_default`=?,`from`=?,`duration_milliseconds`=?,`duration_human`=?, `original_path`=?, `saved_path`=? WHERE `number`=?;"
    cur = conn.cursor()
    cur.execute(query,(str(church_new["title"]),str(church_new["date"]),church_new["rating"],church_new["volume"],church_new["normalize"],church_new["pan"],church_new["low_frequency"],church_new["high_frequency"],church_new["is_default"],str(church_new["from"]),church_new["duration_milliseconds"],str(church_new["duration_human"]),str(church_new["original_path"]),str(church_new["saved_path"]),church_new["number"]))
    conn.commit()
    conn.close()
    return church_new
    
def delete_church_new(church_new):
    conn = create_connection()
    query = "DELETE FROM `church_news` WHERE `number`=?;"
    cur = conn.cursor()
    cur.execute(query,(church_new["number"],))
    conn.commit()

    conn.close()
    return 1
    
### weather_news ###

def import_weather_new(weather_new):
    query = "INSERT INTO `weather_news` (`title`,`date`,`rating`,`volume`,`normalize`,`pan`,`low_frequency`,`high_frequency`,`is_default`,`from`,`duration_milliseconds`,`duration_human`,`original_path`,`saved_path`) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(weather_new["title"]),str(weather_new["date"]),weather_new["rating"],weather_new["volume"],weather_new["normalize"],weather_new["pan"],weather_new["low_frequency"],weather_new["high_frequency"],weather_new["is_default"],str(weather_new["from"]),weather_new["duration_milliseconds"],str(weather_new["duration_human"]),str(weather_new["original_path"]),str(weather_new["saved_path"])))
    conn.commit()
    conn.close()
    weather_new["number"] = cur.lastrowid
    weather_new["type"] = "weather_news"
    return weather_new
    
def read_weather_new(weather_new_number):
    query = "SELECT * FROM `weather_news` WHERE `number`=? LIMIT 1;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(weather_new_number),))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    row = rows[0]
    weather_new = {"type":"weather_news","number":row[0],"title":row[1],"date":row[2],"rating":row[3],"volume":row[4],"normalize":row[5],"pan":row[6],"low_frequency":row[7],"high_frequency":row[8],"is_default":row[9],"from":row[10],"duration_milliseconds":row[11],"duration_human":row[12],"original_path":row[13],"saved_path":row[14]}
    return weather_new

def read_weather_news():
    query = "SELECT * FROM `weather_news`;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    weather_news = []
    for row in rows:
        weather_news.append({"type":"weather_news","number":row[0],"title":row[1],"date":row[2],"rating":row[3],"volume":row[4],"normalize":row[5],"pan":row[6],"low_frequency":row[7],"high_frequency":row[8],"is_default":row[9],"from":row[10],"duration_milliseconds":row[11],"duration_human":row[12],"original_path":row[13],"saved_path":row[14]})
    return weather_news
    
def read_default_weather_new(weather_new_datetime):
    query = "SELECT * FROM `weather_news` WHERE `is_default`=1 AND `date`=?;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(weather_new_datetime),))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    weather_news = []
    for row in rows:
        weather_news.append({"type":"weather_news","number":row[0],"title":row[1],"date":row[2],"rating":row[3],"volume":row[4],"normalize":row[5],"pan":row[6],"low_frequency":row[7],"high_frequency":row[8],"is_default":row[9],"from":row[10],"duration_milliseconds":row[11],"duration_human":row[12],"original_path":row[13],"saved_path":row[14]})
    return weather_news

def search_weather_news(search_phrase,weather_new_datetime):
    query = "SELECT * FROM `weather_news` WHERE `date`=? AND (`title` LIKE ? OR `from` LIKE ?);"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(weather_new_datetime),'%'+str(search_phrase)+'%','%'+str(search_phrase)+'%'))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    weather_news = []
    for row in rows:
        weather_news.append({"type":"weather_news","number":row[0],"title":row[1],"date":row[2],"rating":row[3],"volume":row[4],"normalize":row[5],"pan":row[6],"low_frequency":row[7],"high_frequency":row[8],"is_default":row[9],"from":row[10],"duration_milliseconds":row[11],"duration_human":row[12],"original_path":row[13],"saved_path":row[14]})
    return weather_news
    
def update_weather_new(weather_new):
    conn = create_connection()
    query = "UPDATE `weather_news` SET `title`=?,`date`=?,`rating`=?,`volume`=?, `normalize`=?,`pan`=?,`low_frequency`=?,`high_frequency`=?,`is_default`=?,`from`=?,`duration_milliseconds`=?,`duration_human`=?, `original_path`=?, `saved_path`=? WHERE `number`=?;"
    cur = conn.cursor()
    cur.execute(query,(str(weather_new["title"]),str(weather_new["date"]),weather_new["rating"],weather_new["volume"],weather_new["normalize"],weather_new["pan"],weather_new["low_frequency"],weather_new["high_frequency"],weather_new["is_default"],str(weather_new["from"]),weather_new["duration_milliseconds"],str(weather_new["duration_human"]),str(weather_new["original_path"]),str(weather_new["saved_path"]),weather_new["number"]))
    conn.commit()
    conn.close()
    return weather_new
    
def delete_weather_new(weather_new):
    conn = create_connection()
    query = "DELETE FROM `weather_news` WHERE `number`=?;"
    cur = conn.cursor()
    cur.execute(query,(weather_new["number"],))
    conn.commit()
    
    conn.close()
    return 1
    
### time_collections - time_items ###

def import_time_collection(time_collection,time_items,is_default=0):
    query = "INSERT INTO `time_collections` (`title`,`case`,`append`,`append_relative_type`,`append_relative_number`) VALUES(?,?,?,?,?);"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(time_collection["title"]),time_collection["case"],time_collection["append"],str(time_collection["append_relative_type"]),time_collection["append_relative_number"]))
    conn.commit()
    collection_number = cur.lastrowid
    query = "INSERT INTO `time_items` (`collection_number`,`title`,`when_to_play`,`rating`,`volume`,`normalize`,`pan`,`low_frequency`,`high_frequency`,`duration_milliseconds`,`duration_human`,`original_path`,`saved_path`) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?);"
    counter = 0
    for time_item in time_items:
        cur.execute(query,(collection_number,str(time_item["title"]),str(time_item["when_to_play"]),time_item["rating"],time_item["volume"],time_item["normalize"],time_item["pan"],time_item["low_frequency"],time_item["high_frequency"],time_item["duration_milliseconds"],str(time_item["duration_human"]),str(time_item["original_path"]),str(time_item["saved_path"])))
        conn.commit()        
        time_items[counter]["number"] = cur.lastrowid
        time_items[counter]["type"] = "time_item"
        counter += 1
    time_collection["number"] = collection_number    
    time_collection["type"] = "time_collection"
    append = time_collection["append"]
    append_relative_type = time_collection["append_relative_type"]
    append_relative_number = time_collection["append_relative_number"]
    if int(append)==1:
        if append_relative_type=="sound_files":
            append_item = read_sound_file(append_relative_number)
        elif append_relative_type=="sound_clips":
            append_item = read_sound_clip(append_relative_number)
        elif append_relative_type=="playlists":
            append_item = read_playlist(append_relative_number)
        elif append_relative_type=="retransmitions":
            append_item = read_retransmition(append_relative_number)
        elif append_relative_type=="church_news":
            append_item = read_church_new(append_relative_number)
        elif append_relative_type=="weather_news":
            append_item = read_weather_new(append_relative_number)
        elif append_relative_type=="station_logos":
            append_item = read_station_logo(append_relative_number)
        else:
            append_item = None
    else:
        append_item = None
    time_collection["append_item"] = append_item
    conn.close()
    if is_default==1:
        default_time_collection = read_setting("default_time_collection")
        if default_time_collection != {}:
            update_setting({"number":default_time_collection["number"],"keyword":"default_time_collection","current_value":time_collection["number"]})
        else:
            import_setting({"keyword":"default_time_collection","current_value":time_collection["number"]})        
    return (time_collection,time_items)
    
def read_time_collection(time_collection_number):
    query = "SELECT * FROM `time_collections` WHERE `number`=? LIMIT 1;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(time_collection_number,))
    rows = cur.fetchall()
    conn.commit()
    if len(rows)>0:
        row = rows[0]
        time_collection = {"type":"time_collection","number":row[0],"title":row[1],"case":row[2],"append":row[3],"append_relative_type":row[4],"append_relative_number":row[5]}
        query = "SELECT * FROM `time_items` WHERE `collection_number`=?;"
        cur.execute(query,(str(time_collection_number),))
        rows = cur.fetchall()
        time_items = []
        for row in rows:
            time_items.append({"type":"time_item","number":row[0],"collection_number":row[1],"title":row[2],"when_to_play":row[3],"rating":row[4],"volume":row[5],"normalize":row[6],"pan":row[7],"low_frequency":row[8],"high_frequency":row[9],"duration_milliseconds":row[10],"duration_human":row[11],"original_path":row[12],"saved_path":row[13]})
        conn.commit()
        
        append = time_collection["append"]
        if int(append)==1:
            append_relative_type = time_collection["append_relative_type"]
            append_relative_number = time_collection["append_relative_number"]
            if append_relative_type=="sound_files":
                append_item = read_sound_file(append_relative_number)
            elif append_relative_type=="sound_clips":
                append_item = read_sound_clip(append_relative_number)
            elif append_relative_type=="playlists":
                append_item = read_playlist(append_relative_number)
            elif append_relative_type=="retransmitions":
                append_item = read_retransmition(append_relative_number)
            elif append_relative_type=="church_news":
                append_item = read_church_new(append_relative_number)
            elif append_relative_type=="weather_news":
                append_item = read_weather_new(append_relative_number)
            elif append_relative_type=="station_logos":
                append_item = read_station_logo(append_relative_number)
            else:
                append_item = None
        else:
            append_item = None
        time_collection["append_item"] = append_item    
        conn.close()
        return (time_collection,time_items)
    else:
        return ({},[])

def read_time_collections():
    query = "SELECT * FROM `time_collections`;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.commit()
    time_collections = []
    for row in rows:
        time_collection = {"type":"time_collection","number":row[0],"title":row[1],"case":row[2],"append":row[3],"append_relative_type":row[4],"append_relative_number":row[5]}
        query = "SELECT * FROM `time_items` WHERE `collection_number`=?;"
        cur.execute(query,(str(time_collection["number"]),))
        conn.commit()
        items_rows = cur.fetchall()
        time_items = []
        for item_row in items_rows:
            time_items.append({"type":"time_item","number":item_row[0],"collection_number":item_row[1],"title":item_row[2],"when_to_play":item_row[3],"rating":item_row[4],"volume":item_row[5],"normalize":item_row[6],"pan":item_row[7],"low_frequency":item_row[8],"high_frequency":item_row[9],"duration_milliseconds":item_row[10],"duration_human":item_row[11],"original_path":item_row[12],"saved_path":item_row[13]})
        append = time_collection["append"]
        if int(append)==1:
            append_relative_type = time_collection["append_relative_type"]
            append_relative_number = time_collection["append_relative_number"]
            if append_relative_type=="sound_files":
                append_item = read_sound_file(append_relative_number)
            elif append_relative_type=="sound_clips":
                append_item = read_sound_clip(append_relative_number)
            elif append_relative_type=="playlists":
                append_item = read_playlist(append_relative_number)
            elif append_relative_type=="retransmitions":
                append_item = read_retransmition(append_relative_number)
            elif append_relative_type=="church_news":
                append_item = read_church_new(append_relative_number)
            elif append_relative_type=="weather_news":
                append_item = read_weather_new(append_relative_number)
            elif append_relative_type=="station_logos":
                append_item = read_station_logo(append_relative_number)
            else:
                append_item = None
        else:
            append_item = None
        time_collection["append_item"] = append_item
        time_collections.append([time_collection,time_items])

    conn.close()
    return time_collections
    
def read_default_time_collection():
    default_time_collection = read_setting("default_time_collection")
    if default_time_collection == {}:
        return {}, []
    else:
        default_time_collection_number = default_time_collection["current_value"]    
        return read_time_collection(default_time_collection_number)

def search_time_collections(search_phrase):
    query = "SELECT * FROM `time_collections` WHERE `title` LIKE ?;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(search_phrase),))
    rows = cur.fetchall()
    conn.commit()
    time_collections = []
    for row in rows:
        time_collection = {"type":"time_collection","number":row[0],"title":row[1],"case":row[2],"append":row[3],"append_relative_type":row[4],"append_relative_number":row[5]}
        query = "SELECT * FROM `time_items` WHERE `collection_number`=?;"
        cur.execute(query,(str(time_collection["number"]),))
        conn.commit()
        items_rows = cur.fetchall()
        time_items = []
        for item_row in items_rows:
            time_items.append({"type":"time_item","number":item_row[0],"collection_number":item_row[1],"title":item_row[2],"when_to_play":item_row[3],"rating":item_row[4],"volume":item_row[5],"normalize":item_row[6],"pan":item_row[7],"low_frequency":item_row[8],"high_frequency":item_row[9],"duration_milliseconds":item_row[10],"duration_human":item_row[11],"original_path":item_row[12],"saved_path":item_row[13]})
        append = time_collection["append"]
        if int(append)==1:
            append_relative_type = time_collection["append_relative_type"]
            append_relative_number = time_collection["append_relative_number"]
            if append_relative_type=="sound_files":
                append_item = read_sound_file(append_relative_number)
            elif append_relative_type=="sound_clips":
                append_item = read_sound_clip(append_relative_number)
            elif append_relative_type=="playlists":
                append_item = read_playlist(append_relative_number)
            elif append_relative_type=="retransmitions":
                append_item = read_retransmition(append_relative_number)
            elif append_relative_type=="church_news":
                append_item = read_church_new(append_relative_number)
            elif append_relative_type=="weather_news":
                append_item = read_weather_new(append_relative_number)
            elif append_relative_type=="station_logos":
                append_item = read_station_logo(append_relative_number)
            else:
                append_item = None
        else:
            append_item = None
        time_collection["append_item"] = append_item
        time_collections.append([time_collection,time_items])

    conn.close()
    return time_collections
    
def update_time_collection(time_collection,time_items,is_default=0):
    conn = create_connection()
    query = "UPDATE `time_collections` SET `title`=?, `case`=?, `append`=?, `append_relative_type`=?, `append_relative_number`=? WHERE `number`=?"
    cur = conn.cursor()
    cur.execute(query,(str(time_collection["title"]),time_collection["case"],time_collection["append"],str(time_collection["append_relative_type"]),time_collection["append_relative_number"],time_collection["number"]))
    conn.commit()
    query = "UPDATE `time_items` SET `collection_number`=?, `title`=?, `when_to_play`=?, `rating`=?, `volume`=?, `normalize`=?, `pan`=?, `low_frequency`=?, `high_frequency`=?, `duration_milliseconds`=?, `duration_human`=?,`original_path`=?,`saved_path`=? WHERE `number`=?;"
    for time_item in time_items:
        cur.execute(query,(time_item["collection_number"],str(time_item["title"]),str(time_item["when_to_play"]),time_item["rating"],time_item["volume"],time_item["normalize"],time_item["pan"],time_item["low_frequency"],time_item["high_frequency"],time_item["duration_milliseconds"],str(time_item["duration_human"]),str(time_item["original_path"]),str(time_item["saved_path"]),time_item["number"]))
        conn.commit()
        
    if is_default==1:
        default_time_collection = read_setting("default_time_collection")
        if default_time_collection != {}:
            update_setting({"number":default_time_collection["number"],"keyword":"default_time_collection","current_value":time_collection["number"]})
        else:
            import_setting({"keyword":"default_time_collection","current_value":time_collection["number"]})        
    else:
        default_time_collection = read_setting("default_time_collection")
        if default_time_collection != {}:
            default_time_collection_number = default_time_collection["number"]
            if default_time_collection_number==time_collection["number"]:
                delete_setting(default_time_collection)
    return (time_collection,time_items)
    
def delete_time_collection(time_collection_number):
    conn = create_connection()
    query = "DELETE FROM `time_items` WHERE `collection_number`=?;"
    cur = conn.cursor()
    cur.execute(query,(time_collection_number,))
    conn.commit()
    query = "DELETE FROM `time_collections` WHERE `number`=?;"
    cur = conn.cursor()
    cur.execute(query,(time_collection_number,))
    conn.commit()

    default_time_collection = read_setting("default_time_collection")
    if default_time_collection != {}:
        if default_time_collection["number"]==time_collection_number:
            delete_setting(default_time_collection)
    
    return 1

### retransmitions ###

def import_retransmition(retransmition):
    query = "INSERT INTO `retransmitions` (`title`,`url`,`url_option`,`javascript_code`,`stream_url`,`description`,`image_path`,`image_title`,`rating`,`volume`,`normalize`,`pan`,`low_frequency`,`high_frequency`) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(retransmition["title"]),str(retransmition["url"]),str(retransmition["url_option"]),str(retransmition["javascript_code"]),str(retransmition["stream_url"]),str(retransmition["description"]),str(retransmition["image_path"]),str(retransmition["image_title"]),retransmition["rating"],retransmition["volume"],retransmition["normalize"],retransmition["pan"],retransmition["low_frequency"],retransmition["high_frequency"]))
    conn.commit()
    conn.close()
    retransmition["number"] = cur.lastrowid
    retransmition["type"] = "retransmitions"
    return retransmition
    
def read_retransmition(retransmition_number):
    query = "SELECT * FROM `retransmitions` WHERE `number`=? LIMIT 1;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(retransmition_number),))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    row = rows[0]
    retransmition = {"type":"retransmitions","number":row[0],"title":row[1],"url":row[2],"url_option":row[3],"javascript_code":row[4],"stream_url":row[5],"description":row[6],"image_path":row[7],"image_title":row[8],"rating":row[9],"volume":row[10],"normalize":row[11],"pan":row[12],"low_frequency":row[13],"high_frequency":row[14]}
    return retransmition

def read_retransmitions():
    query = "SELECT * FROM `retransmitions`;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    retransmitions = []
    for row in rows:
        retransmitions.append({"type":"retransmitions","number":row[0],"title":row[1],"url":row[2],"url_option":row[3],"javascript_code":row[4],"stream_url":row[5],"description":row[6],"image_path":row[7],"image_title":row[8],"rating":row[9],"volume":row[10],"normalize":row[11],"pan":row[12],"low_frequency":row[13],"high_frequency":row[14]})
    return retransmitions

def search_retransmitions(search_phrase):
    query = "SELECT * FROM `retransmitions` WHERE `title` LIKE ? OR `url` LIKE ? OR `url_option` LIKE ? OR `javascript_code` LIKE ? OR `stream_url` LIKE ? OR `description` LIKE ? OR `image_title` LIKE ?;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,('%'+str(search_phrase)+'%','%'+str(search_phrase)+'%','%'+str(search_phrase)+'%','%'+str(search_phrase)+'%','%'+str(search_phrase)+'%','%'+str(search_phrase)+'%','%'+str(search_phrase)+'%'))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    retransmitions = []
    for row in rows:
        retransmitions.append({"type":"retransmitions","number":row[0],"title":row[1],"url":row[2],"url_option":row[3],"javascript_code":row[4],"stream_url":row[5],"description":row[6],"image_path":row[7],"image_title":row[8],"rating":row[9],"volume":row[10],"normalize":row[11],"pan":row[12],"low_frequency":row[13],"high_frequency":row[14]})
    return retransmitions
    
def update_retransmition(retransmition):
    query = "UPDATE `retransmitions` SET `title`=?, `url`=?, `url_option`=?, `javascript_code`=?, `stream_url`=?, `description`=?, `image_path`=?, `image_title`=?, `rating`=?, `volume`=?, `normalize`=?, `pan`=?, `low_frequency`=?, `high_frequency`=? WHERE `number`=?;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(retransmition["title"]),str(retransmition["url"]),str(retransmition["url_option"]),str(retransmition["javascript_code"]),str(retransmition["stream_url"]),str(retransmition["description"]),str(retransmition["image_path"]),str(retransmition["image_title"]),retransmition["rating"],retransmition["volume"],retransmition["normalize"],retransmition["pan"],retransmition["low_frequency"],retransmition["high_frequency"],retransmition["number"]))
    conn.commit()
    conn.close()
    return retransmition
    
def delete_retransmition(retransmition):
    conn = create_connection()
    query = "DELETE FROM `retransmitions` WHERE `number`=? AND `title`=?;"
    cur = conn.cursor()
    cur.execute(query,(retransmition["number"],str(retransmition["title"])))
    conn.commit()
    
    conn.close()
    return 1

### ip calls ###

def import_ip_call_item(ip_call_item):
    query = "INSERT INTO `ip_calls` (`title`,`name`,`surname`,`duration_milliseconds`,`duration_human`) VALUES(?,?,?,?,?);"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(ip_call_item["title"]),str(ip_call_item["name"]),str(ip_call_item["surname"]),ip_call_item["duration_milliseconds"],str(ip_call_item["duration_human"])))
    conn.commit()
    conn.close()
    ip_call_item["number"] = cur.lastrowid
    ip_call_item["type"] = "ip_calls"
    return ip_call_item
    
def read_ip_call_item(ip_call_item_number):
    query = "SELECT * FROM `ip_calls` WHERE `number`=? LIMIT 1;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(ip_call_item_number),))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    row = rows[0]
    ip_call_item = {"type":"ip_calls","number":row[0],"title":row[1],"name":row[2],"surname":row[3],"duration_milliseconds":row[4],"duration_human":row[5]}
    return ip_call_item
   
def read_ip_calls_items():
    query = "SELECT * FROM `ip_calls`;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    ip_call_items = []
    for row in rows:
        ip_call_items.append({"type":"ip_calls","number":row[0],"title":row[1],"name":row[2],"surname":row[3],"duration_milliseconds":row[4],"duration_human":row[5]})
    return ip_call_items
    
def search_ip_call_items(search_phrase):
    query = "SELECT * FROM `ip_calls` WHERE `title` LIKE ? OR `name` LIKE ? OR `surname` LIKE ?;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,('%'+str(search_phrase)+'%','%'+str(search_phrase)+'%','%'+str(search_phrase)+'%'))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    ip_call_items = []
    for row in rows:
        ip_call_items.append({"type":"ip_calls","number":row[0],"title":row[1],"name":row[2],"surname":row[3],"duration_milliseconds":row[4],"duration_human":row[5]})
    return ip_call_items
    
def update_ip_call_item(ip_call_item):
    query = "UPDATE `ip_calls` SET `title`=?,`name`=?,`surname`=?,`duration_milliseconds`=?,`duration_human`=? WHERE `number`=?;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(ip_call_item["title"],ip_call_item["name"],ip_call_item["surname"],ip_call_item["duration_milliseconds"],ip_call_item["duration_human"],ip_call_item["number"]))
    conn.commit()
    conn.close()
    return ip_call_item
    
def delete_ip_call_item(ip_call_item):
    query = "DELETE FROM `ip_calls` WHERE `number`=?;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(ip_call_item["number"],))
    conn.commit()
    conn.close()
    return 1

### playlists ###

def import_playlist(title,playlist):
    query = "INSERT INTO `playlists_titles` (`title`) VALUES (?);"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(title),))
    conn.commit()
    playlist_number = cur.lastrowid
    
    query = "INSERT INTO `playlists` (`playlist_number`,`relative_type`,`relative_number`,`position`) VALUES(?,?,?,?);"
    counter = 0
    for playlist_item in playlist:  
        cur.execute(query,(playlist_number,str(playlist_item["relative_type"]),playlist_item["relative_number"],playlist_item["position"]))
        conn.commit()
        playlist[counter]["playlist_number"] = playlist_number
        playlist[counter]["playlist_title"] = title
        playlist[counter]["type"] = "playlists_items"
        playlist[counter]["number"] = cur.lastrowid
        playlist[counter]["item"] = read_item_by_type_and_number(playlist_item["relative_type"],playlist_item["relative_number"])
        counter += 1
    conn.close()
    return playlist
    
def read_playlist(title):
    query = "SELECT `playlists`.`number`,`playlists`.`playlist_number`,`playlists`.`relative_type`,`playlists`.`relative_number`,`playlists`.`position`,`playlists_titles`.`title` FROM `playlists` INNER JOIN `playlists_titles` ON `playlists`.`playlist_number`=`playlists_titles`.`number` WHERE `playlists_titles`.`title`=? ORDER BY `playlists`.`position`;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(title),))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    playlist_items = []
    for row in rows:
        playlist_item = {"type":"playlists_items","number":row[0],"playlist_number":row[1],"relative_type":row[2],"relative_number":row[3],"position":row[4],"playlist_title":row[5]}
        playlist_item["item"] = read_item_by_type_and_number(playlist_item["relative_type"],playlist_item["relative_number"])
        playlist_items.append(playlist_item)

    return playlist_items
    
def read_playlists():
    query = "SELECT `playlists`.`number`,`playlists`.`playlist_number`,`playlists`.`relative_type`,`playlists`.`relative_number`,`playlists`.`position`,`playlists_titles`.`title` FROM `playlists` INNER JOIN `playlists_titles` ON `playlists`.`playlist_number`=`playlists_titles`.`number` ORDER BY `playlists_titles`.`title`,`playlists`.`position`;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    playlists = []
    playlist_items = []
    playlist_title = ""
    if len(rows)>0:
        for row in rows:
            if row[5]!=playlist_title:
                playlist_title = row[5]
                if len(playlist_items)>0:
                    playlists.append(playlist_items)
                    playlist_items = []
            playlist_item = {"type":"playlists_items","number":row[0],"playlist_number":row[1],"relative_type":row[2],"relative_number":row[3],"position":row[4],"playlist_title":row[5]}
            playlist_item["item"] = read_item_by_type_and_number(playlist_item["relative_type"],playlist_item["relative_number"])
            playlist_items.append(playlist_item)
        playlists.append(playlist_items)
    
    return playlists
    
def search_playlists(search_phrase):
    query = "SELECT `playlists`.`number`,`playlists`.`playlist_number`,`playlists`.`relative_type`,`playlists`.`relative_number`,`playlists`.`position`,`playlists_titles`.`title` FROM `playlists` INNER JOIN `playlists_titles` ON `playlists`.`playlist_number`=`playlists_titles`.`number` WHERE `playlists_titles`.`title` LIKE ? ORDER BY `playlists_titles`.`title`,`playlists`.`position`;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(search_phrase),))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    playlists = []
    playlist_items = []
    playlist_title = ""
    if len(rows)>0:
        for row in rows:
            if row[5]!=playlist_title:
                playlist_title = row[5]
                if len(playlist_items)>0:
                    playlists.append(playlist_items)
                    playlist_items = []
            playlist_item = {"type":"playlists_items","number":row[0],"playlist_number":row[1],"relative_type":row[2],"relative_number":row[3],"position":row[4],"playlist_title":row[5]}
            playlist_item["item"] = read_item_by_type_and_number(playlist_item["relative_type"],playlist_item["relative_number"])
            playlist_items.append(playlist_item)
        playlists.append(playlist_items)
    return playlists

def update_playlist(playlist,title):
    playlist_number = int(playlist[0]["playlist_number"])
    query_1 = "UPDATE `playlists_titles` SET `title`=? WHERE `number`=?"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query_1,(str(title),playlist_number))
    conn.commit()
    query_2 = "UPDATE `playlists` SET `relative_type`=?,`relative_number`=?,`position`=? WHERE `number`=?"
    query_3 = "INSERT INTO `playlists` (`playlist_number`,`relative_type`,`relative_number`,`position`) VALUES(?,?,?,?);"
    counter = 0
    for playlist_item in playlist:
        if "number" in playlist_item:
            cur.execute(query_2,(playlist_item["relative_type"],playlist_item["relative_number"],playlist_item["position"],playlist_item["number"]))
            conn.commit()
        else:
            cur.execute(query_3,(playlist_number,str(playlist_item["relative_type"]),playlist_item["relative_number"],playlist_item["position"]))
            conn.commit()
            playlist[counter]["playlist_number"] = playlist_number
            playlist[counter]["playlist_title"] = title
            playlist[counter]["type"] = "playlists_items"
            playlist[counter]["number"] = cur.lastrowid
            playlist[counter]["item"] = read_item_by_type_and_number(playlist_item["relative_type"],playlist_item["relative_number"])
    return playlist
    
def delete_playlist(playlist):
    playlist_number = int(playlist[0]["playlist_number"])
    query = "DELETE FROM `playlists` WHERE `playlist_number`=?"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(playlist_number,))
    conn.commit()
    query = "DELETE FROM `playlists_titles` WHERE `number`=?"
    cur.execute(query,(playlist_number,))
    conn.commit()
    
    return 1

### transmitions - transmitions_items ###

def import_transmition(transmition,transmition_items):
    query = "INSERT INTO `transmitions` (`title`,`live`,`frequency`,`time_settings`,`types`,`active`,`repeat`) VALUES(?,?,?,?,?,?,?);"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(transmition["title"]),str(transmition["live"]),str(transmition["frequency"]),str(transmition["time_settings"]),str(transmition["types"]),transmition["active"],transmition["repeat"]))
    conn.commit()
    transmition["number"] = cur.lastrowid

    query = "INSERT INTO `transmitions_items` (`transmition_number`,`relative_type`,`relative_number`,`relative_time_seconds`,`frequency_type`,`frequency_type_parameters`,`default`) VALUES(?,?,?,?,?,?,?);"        
    counter = 0
    for transmition_item in transmition_items:
        cur.execute(query,(transmition["number"],str(transmition_item["relative_type"]),transmition_item["relative_number"],transmition_item["relative_time_seconds"],str(transmition_item["frequency_type"]),str(transmition_item["frequency_type_parameters"]),transmition_item["default"]))
        conn.commit()
        transmition_items[counter]["number"] = cur.lastrowid
        transmition_items[counter]["transmition_number"] = transmition["number"]
        counter += 1
    conn.close()
    return (transmition,transmition_items)
    
def read_transmition(transmition_number):
    query = "SELECT * FROM `transmitions` WHERE `number`=? LIMIT 1;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(transmition_number,))
    rows = cur.fetchall()
    row = rows[0]
    transmition = {"number":row[0],"title":row[1],"live":row[2],"frequency":row[3],"time_settings":row[4],"types":row[5],"active":row[6]}
    conn.commit()

    query = "SELECT * FROM `transmitions_items` WHERE `transmition_number`=?;"
    cur.execute(query,(transmition_number,))
    rows = cur.fetchall()
    transmition_items = []
    for row in rows:
        transmition_items.append({"number":row[0],"transmition_number":row[1],"relative_type":row[2],"relative_number":row[3],"relative_time_seconds":row[4],"frequency_type":row[5],"frequency_type_parameters":row[6],"default":row[7]})
    conn.commit()

    conn.close()
    return (transmition,transmition_items)
    
def read_transmitions():
    query = "SELECT * FROM `transmitions`;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    rows = cur.fetchall()
    transmitions = []
    counter = 0
    for row in rows:
        transmition = {"number":row[0],"title":row[1],"live":row[2],"frequency":row[3],"time_settings":row[4],"types":row[5],"active":row[6]}
        transmition_number = row[0]
        query = "SELECT * FROM `transmitions_items` WHERE `transmition_number`=?;"
        cur.execute(query,(transmition_number,))
        conn.commit()
        transmition_items_rows = cur.fetchall()
        transmition_items = []
        for transmition_item_row in transmition_items_rows:
            transmition_items.append({"number":transmition_item_row[0],"transmition_number":transmition_item_row[1],"relative_type":transmition_item_row[2],"relative_number":transmition_item_row[3],"relative_time_seconds":transmition_item_row[4],"frequency_type":transmition_item_row[5],"frequency_type_parameters":transmition_item_row[6],"default":transmition_item_row[7]})
        
        transmitions.append([transmition,transmition_items])
    conn.close()
    return transmitions
    
def search_transmitions(search_phrase):
    query = "SELECT * FROM `transmitions` WHERE `title` LIKE ?;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,('%'+str(search_phrase)+'%',))
    conn.commit()
    rows = cur.fetchall()
    transmitions = []
    counter = 0
    for row in rows:
        transmition = {"number":row[0],"title":row[1],"live":row[2],"frequency":row[3],"time_settings":row[4],"types":row[5],"active":row[6]}
        transmition_number = row[0]
        query = "SELECT * FROM `transmitions_items` WHERE `transmition_number`=?;"
        cur.execute(query,(transmition_number,))
        conn.commit()
        transmition_items_rows = cur.fetchall()
        transmition_items = []
        for transmition_item_row in transmition_items_rows:
            transmition_items.append({"number":transmition_item_row[0],"transmition_number":transmition_item_row[1],"relative_type":transmition_item_row[2],"relative_number":transmition_item_row[3],"relative_time_seconds":transmition_item_row[4],"frequency_type":transmition_item_row[5],"frequency_type_parameters":transmition_item_row[6],"default":transmition_item_row[7]})
        
        transmitions.append([transmition,transmition_items])
    conn.close()
    return transmitions
    
def update_transmition(transmition,transmition_items):
    conn = create_connection()
    cur = conn.cursor()
    query_1 = "UPDATE `transmitions` SET `title`=?, `live`=?, `frequency`=?, `time_settings`=?, `types`=?, `active`=? WHERE `number`=?"
    cur.execute(query_1,(str(transmition["title"]),str(transmition["live"]),str(transmition["frequency"]),str(transmition["time_settings"]),str(transmition["types"]),transmition["active"],transmition["number"]))
    conn.commit()
    
    query_2 = "UPDATE `transmitions_items` SET `relative_type`=?,`relative_number`=?,`relative_time_seconds`=?,`frequency_type`=?,`frequency_type_parameters`=?,`default`=? WHERE `number`=?"
    query_3 = "INSERT INTO `transmitions_items` (`transmition_number`,`relative_type`,`relative_number`,`relative_time_seconds`,`frequency_type`,`frequency_type_parameters`,`default`) VALUES(?,?,?,?,?,?,?);"            
    counter = 0
    for transmition_item in transmition_items:
        if "number" in transmition_item:
            cur.execute(query_2,(str(transmition_item["relative_type"]),transmition_item["relative_number"],str(transmition_item["relative_time_seconds"]),str(transmition_item["frequency_type"]),str(transmition_item["frequency_type_parameters"]),transmition_item["default"],transmition_item["number"]))
            conn.commit()
        else:
            cur.execute(query_3,(transmition["number"],str(transmition_item["relative_type"]),transmition_item["relative_number"],transmition_item["relative_time_seconds"],str(transmition_item["frequency_type"]),str(transmition_item["frequency_type_parameters"]),transmition_item["default"]))
            conn.commit()
            transmition_items[counter]["number"] = cur.lastrowid
        counter += 1
    return (transmition,transmition_items)
    
def delete_transmition(transmition):
    conn = create_connection()
    query = "DELETE FROM `transmitions_items` WHERE `transmition_number`=?;"
    cur = conn.cursor()
    cur.execute(query,(transmition["number"],))
    conn.commit()
    query = "DELETE FROM `transmitions` WHERE `number`=?;"
    cur = conn.cursor()
    cur.execute(query,(transmition["number"],))
    conn.commit()
    conn.close()
    return 1
    
### player_list ###

def import_player_list_item(player_list_item):
    conn = create_connection()
    cur = conn.cursor()
    if player_list_item["position"]==1:
        query = "UPDATE `player_list` SET `position` = `position`+1"
        cur.execute(query)
        conn.commit()
        
    query = "INSERT INTO `player_list` (`play`,`relative_type`,`relative_number`,`repeats`,`duration_milliseconds`,`duration_human`,`position`) VALUES(?,?,?,?,?,?,?);"
    
    cur.execute(query,(player_list_item["play"],str(player_list_item["relative_type"]),player_list_item["relative_number"],player_list_item["repeats"],player_list_item["duration_milliseconds"],str(player_list_item["duration_human"]),player_list_item["position"]))
    conn.commit()
    conn.close()
    player_list_item["player_number"] = cur.lastrowid
    player_list_item["type"] = "player_list_item"
    relative_type = player_list_item["relative_type"]
    relative_number = player_list_item["relative_number"]
    if relative_type == "sound_files":
        item_details = read_sound_file(relative_number)
    elif relative_type=="playlists":
        item_details = read_playlist
    elif relative_type=="sound_clips":
        item_details = read_sound_clip(relative_number)
    elif relative_type == "retransmitions":
        item_details = read_retransmition(relative_number)
    elif relative_type == "church_news":
        item_details = read_church_new(relative_number)
    elif relative_type=="weather_news":
        item_details = read_weather_new(relative_number)
    elif relative_type=="station_logos":
        item_details = read_station_logo(relative_number)
    elif relative_type=="time_collections":
        item_details = read_time_collection(relative_number)
    player_list_item["details"] = item_details  

    return player_list_item
    
def read_player_list_item(player_number):
    query = "SELECT * FROM `player_list` WHERE `number`=? LIMIT 1;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(player_number),))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    row = rows[0]
    player_list_item = {"type":"player_list_item","player_number":row[0],"play":row[1],"relative_type":row[2],"relative_number":row[3],"repeats":row[4],"duration_milliseconds":row[5],"duration_human":row[6],"position":row[7]}
    last_play_datetime = find_last_play_datetime(row[2],row[3])
    player_list_item["last_play"] = last_play_datetime
    
    relative_type = row[2]
    relative_number = row[3]
    if relative_type == "sound_files":
        item_details = read_sound_file(relative_number)
    elif relative_type=="playlists":
        item_details = read_playlist
    elif relative_type=="sound_clips":
        item_details = read_sound_clip(relative_number)
    elif relative_type == "retransmitions":
        item_details = read_retransmition(relative_number)
    elif relative_type == "church_news":
        item_details = read_church_new(relative_number)
    elif relative_type=="weather_news":
        item_details = read_weather_new(relative_number)
    elif relative_type=="station_logos":
        item_details = read_station_logo(relative_number)
    elif relative_type=="time_collections":
        item_details = read_time_collection(relative_number)
    player_list_item["details"] = item_details  
    return player_list_item

def find_last_play_datetime(relative_type,relative_number):
    query = "SELECT * FROM `player_history` WHERE `relative_type`=? AND `relative_number`=? ORDER BY `time_started_played` DESC LIMIT 1;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(relative_type),relative_number))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    if len(rows)==0:
        return ""
    else:
        return rows[0][1]

def read_player_list():
    query = "SELECT * FROM `player_list` ORDER BY `position`;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    player_list_items = []
    counter = 0
    for row in rows:
        relative_type = row[2]
        relative_number = row[3]
        if relative_type == "sound_files":
            item_details = read_sound_file(relative_number)
        elif relative_type=="playlists":
            item_details = read_playlist
        elif relative_type=="sound_clips":
            item_details = read_sound_clip(relative_number)
        elif relative_type == "retransmitions":
            item_details = read_retransmition(relative_number)
        elif relative_type == "church_news":
            item_details = read_church_new(relative_number)
        elif relative_type=="weather_news":
            item_details = read_weather_new(relative_number)
        elif relative_type=="station_logos":
            item_details = read_station_logo(relative_number)
        elif relative_type=="time_collections":
            item_details = read_time_collection(relative_number)
        player_list_items.append({"details":item_details,"type":"player_list_item","player_number":row[0],"play":row[1],"relative_type":row[2],"relative_number":row[3],"repeats":row[4],"duration_milliseconds":row[5],"duration_human":row[6],"position":row[7]})
        last_play_datetime = find_last_play_datetime(row[2],row[3])
        player_list_items[counter]["last_play"] = last_play_datetime
        counter += 1
    return player_list_items
        
def update_player_list_item(player_list_item):
    conn = create_connection()
    query = "UPDATE `player_list` SET `play`=?,`relative_type`=?,`relative_number`=?,`repeats`=?, `duration_milliseconds`=?,`duration_human`=?,`position`=? WHERE `number`=?;"
    cur = conn.cursor()
    cur.execute(query,(player_list_item["play"],str(player_list_item["relative_type"]),player_list_item["relative_number"],player_list_item["repeats"],player_list_item["duration_milliseconds"],str(player_list_item["duration_human"]),player_list_item["position"],player_list_item["player_number"]))
    conn.commit()
    relative_type = player_list_item["relative_type"]
    relative_number = player_list_item["relative_number"]
    item = player_list_item["details"]

    conn.close()
    return player_list_item

def player_list_play_all(play):
    conn = create_connection()
    query = "UPDATE `player_list` SET `play`=?;"
    cur = conn.cursor()
    cur.execute(query,(play,))
    conn.commit()
    conn.close()
    return 1
    
def player_list_play_changed(player_number,play):
    conn = create_connection()
    query = "UPDATE `player_list` SET `play`=? WHERE `number`=?;"
    cur = conn.cursor()
    cur.execute(query,(play,player_number))
    conn.commit()
    conn.close()
    return 1
    
def player_list_repeats_changed(player_number,repeats):
    conn = create_connection()
    query = "UPDATE `player_list` SET `repeats`=? WHERE `number`=?;"
    cur = conn.cursor()
    cur.execute(query,(repeats,player_number))
    conn.commit()
    conn.close()
    return read_player_list_item(player_number)
    
def move_player_list_item(start_position,end_position,player_list_item):
    conn = create_connection()
    query = "DELETE FROM `player_list` WHERE `position`=?;"
    cur = conn.cursor()
    cur.execute(query,(start_position,))
    conn.commit()      
    if start_position<end_position:
        query = "UPDATE `player_list` SET `position`=`position`-1 WHERE `position`>? AND `position`<=?;"
        cur = conn.cursor()
        cur.execute(query,(start_position,end_position))
        conn.commit()    
    elif end_position<start_position:
        query = "UPDATE `player_list` SET `position`=`position`+1 WHERE `position`>=? AND `position`< ?;"
        cur = conn.cursor()
        cur.execute(query,(end_position,start_position))
        conn.commit()      
    conn.close()
    player_list_item["position"] = end_position
    import_player_list_item(player_list_item)   
    return 1
    
def delete_player_list_item(player_list_item):
    conn = create_connection()
    position = player_list_item["position"]
    query = "DELETE FROM `player_list` WHERE `number`=?;"
    cur = conn.cursor()
    cur.execute(query,(player_list_item["player_number"],))
    conn.commit()
    
    query = "UPDATE `player_list` SET `position`=`position`-1 WHERE `position`>?"
    cur = conn.cursor()
    cur.execute(query,(position,))
    conn.commit()
    
    conn.close()
    return 1

### player_history ###

def import_player_history(player_history):
    query = "INSERT INTO `player_history` (`time_started_played`,`time_stoped_played`,`relative_type`,`relative_number`,`deck`,`updated`) VALUES(?,?,?,?,?,?);"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(player_history["time_started_played"]),player_history["time_stoped_played"],str(player_history["relative_type"]),player_history["relative_number"],str(player_history["deck"]),player_history["updated"]))
    conn.commit()
    conn.close()
    player_history["number"] = cur.lastrowid
    return player_history
    
def read_player_history(player_history_number):
    query = "SELECT * FROM `player_history` WHERE `number`=? LIMIT 1;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(player_history_number),))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    row = rows[0]
    player_history_item = {"number":row[0],"time_started_played":row[1],"time_stoped_played":row[2],"relative_type":row[3],"relative_number":row[4],"deck":row[5],"updated":row[6]}
    return player_history_item
    
def read_player_histories():
    query = "SELECT * FROM `player_history` ORDER BY datetime(`time_started_played`) ASC;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    player_history_items = []
    for row in rows:
        player_history_items.append({"number":row[0],"time_started_played":row[1],"time_stoped_played":row[2],"relative_type":row[3],"relative_number":row[4],"deck":row[5],"updated":row[6]})
    return player_history_items

def read_last_player_histories():
    conn = create_connection()
    cur = conn.cursor()
    
    query_1 = "SELECT * FROM `player_history` WHERE `deck`='deck_1' AND `time_stoped_played`<>'' ORDER BY datetime(`time_started_played`) DESC LIMIT 2;"
    query_2 = "SELECT * FROM `player_history` WHERE `deck`='deck_2' AND `time_stoped_played`<>'' ORDER BY datetime(`time_started_played`) DESC LIMIT 2;"
    query_3 = "SELECT * FROM `player_history` WHERE `deck`='music_clip_deck' AND `time_stoped_played`<>'' AND `relative_type`<>'time_collections' ORDER BY datetime(`time_started_played`) DESC LIMIT 2;"

    cur.execute(query_1)
    rows = cur.fetchall()
    conn.commit()
    player_history_items = []
    for row in rows:
        player_history_items.append({"number":row[0],"time_started_played":row[1],"time_stoped_played":row[2],"relative_type":row[3],"relative_number":row[4],"deck":row[5],"updated":row[6]})
        
    cur.execute(query_2)
    rows = cur.fetchall()
    conn.commit()
    for row in rows:
        player_history_items.append({"number":row[0],"time_started_played":row[1],"time_stoped_played":row[2],"relative_type":row[3],"relative_number":row[4],"deck":row[5],"updated":row[6]})
        
        
    cur.execute(query_3)
    rows = cur.fetchall()
    conn.commit()
    for row in rows:
        player_history_items.append({"number":row[0],"time_started_played":row[1],"time_stoped_played":row[2],"relative_type":row[3],"relative_number":row[4],"deck":row[5],"updated":row[6]})
        
    counter = 0
    for row in player_history_items:
        item_details = read_item_by_type_and_number(row["relative_type"],row["relative_number"])
        player_history_items[counter]["details"] = item_details
        counter += 1
        
    return player_history_items
    
def search_player_history(start_datetime,end_datetime):
    query = "SELECT * FROM `player_history` WHERE (`time_started_played`>=datetime(?) AND `time_started_played`<=datetime(?) AND `time_stoped_played` IS NULL) OR (`time_started_played`>=datetime(?) AND `time_stoped_played`<=datetime(?)) ORDER BY datetime(`time_started_played`);"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(start_datetime),str(end_datetime),str(start_datetime),str(end_datetime)))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    player_history_items = []
    for row in rows:
        player_history_items.append({"number":row[0],"time_started_played":row[1],"time_stoped_played":row[2],"relative_type":row[3],"relative_number":row[4],"deck":row[5],"updated":row[6]})
    return player_history_items
   
def update_player_history(player_history):
    conn = create_connection()
    query = "UPDATE `player_history` SET `time_started_played`=?,`time_stoped_played`=?,`relative_type`=?,`relative_number`=?,`deck`=?, `updated`=? WHERE `number`=?;"
    cur = conn.cursor()
    cur.execute(query,(str(player_history["time_started_played"]),str(player_history["time_stoped_played"]),str(player_history["relative_type"]),player_history["relative_number"],player_history["deck"],player_history["updated"],player_history["number"]))
    conn.commit()
    conn.close()
    return player_history
    
def delete_player_history(player_history):
    conn = create_connection()
    query = "DELETE FROM `player_history` WHERE `number`=?;"
    cur = conn.cursor()
    cur.execute(query,(player_history["number"],))
    conn.commit()
    conn.close()
    return 1

### radio_connections ###

def import_radio_connection(radio_connection):
    query = "INSERT INTO `radio_connections` (`title`,`address`,`image_path`,`director`,`telephone`,`fax`,`email`,`site`,`description`,`genre`,`web_server_hostname`,`ftp_username`,`ftp_password`,`mysql_hostname`,`mysql_username`,`mysql_password`,`mysql_database`,`metadata`,`radio_page_url`,`radio_type`,`radio_hostname`,`radio_port`,`radio_mount`,`radio_username`,`radio_password`,`bit_rate`,`mp3_stream`,`channels`) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(radio_connection["title"]),str(radio_connection["address"]),str(radio_connection["image_path"]),str(radio_connection["director"]),str(radio_connection["telephone"]),str(radio_connection["fax"]),str(radio_connection["email"]),str(radio_connection["site"]),str(radio_connection["description"]),str(radio_connection["genre"]),str(radio_connection["web_server_hostname"]),str(radio_connection["ftp_username"]),str(radio_connection["ftp_password"]),str(radio_connection["mysql_hostname"]),str(radio_connection["mysql_username"]),str(radio_connection["mysql_password"]),str(radio_connection["mysql_database"]),str(radio_connection["metadata"]),str(radio_connection["radio_page_url"]),str(radio_connection["radio_type"]),str(radio_connection["radio_hostname"]),radio_connection["radio_port"],str(radio_connection["radio_mount"]),str(radio_connection["radio_username"]),str(radio_connection["radio_password"]),radio_connection["bit_rate"],str(radio_connection["mp3_stream"]),radio_connection["channels"]))
    conn.commit()
    conn.close()
    radio_connection["number"] = cur.lastrowid
    return radio_connection

def read_radio_connection(radio_connection_number):
    query = "SELECT * FROM `radio_connections` WHERE `number`=? LIMIT 1;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(radio_connection_number),))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    row = rows[0]
    radio_connection = {"number":row[0],"title":row[1],"address":row[2],"image_path":row[3],"director":row[4],"telephone":row[5],"fax":row[6],"email":row[7],"site":row[8],"description":row[9],"genre":row[10],"web_server_hostname":row[11],"ftp_username":row[12],"ftp_password":row[13],"mysql_hostname":row[14],"mysql_username":row[15],"mysql_password":row[16],"mysql_database":row[17],"metadata":row[18],"radio_page_url":row[19],"radio_type":row[20],"radio_hostname":row[21],"radio_port":row[22],"radio_mount":row[23],"radio_username":row[24],"radio_password":row[25],"bit_rate":row[26],"mp3_stream":row[27],"channels":row[28]}
    return radio_connection
    
def read_radio_connections():
    query = "SELECT * FROM `radio_connections`;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    radio_connections = []
    for row in rows:
        radio_connections.append({"number":row[0],"title":row[1],"address":row[2],"image_path":row[3],"director":row[4],"telephone":row[5],"fax":row[6],"email":row[7],"site":row[8],"description":row[9],"genre":row[10],"web_server_hostname":row[11],"ftp_username":row[12],"ftp_password":row[13],"mysql_hostname":row[14],"mysql_username":row[15],"mysql_password":row[16],"mysql_database":row[17],"metadata":row[18],"radio_page_url":row[19],"radio_type":row[20],"radio_hostname":row[21],"radio_port":row[22],"radio_mount":row[23],"radio_username":row[24],"radio_password":row[25],"bit_rate":row[26],"mp3_stream":row[27],"channels":row[28]})
    return radio_connections
    
def update_radio_connection(radio_connection):
    conn = create_connection()
    query = "UPDATE `radio_connections` SET `title`=?, `address`=?, `image_path`=?, `director`=?, `telephone`=?, `fax`=?, `email`=?,`site`=?, `description`=?, `genre`=?, `web_server_hostname`=?, `ftp_username`=?, `ftp_password`=?, `mysql_hostname`=?,`mysql_username`=?, `mysql_password`=?, `mysql_database`=?, `metadata`=?, `radio_page_url`=?, `radio_type`=?, `radio_hostname`=?,`radio_port`=?, `radio_mount`=?, `radio_username`=?, `radio_password`=?, `bit_rate`=?, `mp3_stream`=?, `channels`=? WHERE `number`=?;"
    cur = conn.cursor()
    cur.execute(query,(str(radio_connection["title"]),str(radio_connection["address"]),str(radio_connection["image_path"]),str(radio_connection["director"]),str(radio_connection["telephone"]),str(radio_connection["fax"]),str(radio_connection["email"]),str(radio_connection["site"]),str(radio_connection["description"]),str(radio_connection["genre"]),str(radio_connection["web_server_hostname"]),str(radio_connection["ftp_username"]),str(radio_connection["ftp_password"]),str(radio_connection["mysql_hostname"]),str(radio_connection["mysql_username"]),str(radio_connection["mysql_password"]),str(radio_connection["mysql_database"]),str(radio_connection["metadata"]),str(radio_connection["radio_page_url"]),str(radio_connection["radio_type"]),str(radio_connection["radio_hostname"]),radio_connection["radio_port"],str(radio_connection["radio_mount"]),str(radio_connection["radio_username"]),str(radio_connection["radio_password"]),radio_connection["bit_rate"],str(radio_connection["mp3_stream"]),radio_connection["channels"],radio_connection["number"]))
    conn.commit()
    conn.close()
    return radio_connection
    
def delete_radio_connection(radio_connection):
    conn = create_connection()
    query = "DELETE FROM `radio_connections` WHERE `number`=? AND `title`=?;"
    cur = conn.cursor()
    cur.execute(query,(radio_connection["number"],str(radio_connection["title"])))
    conn.commit()
    conn.close()
    return 1
    
### listeners_statistics ###

def import_listener_statistic(listeners_statistics):
    query = "INSERT INTO `listeners_statistics` (`connect_datetime`, `disconnect_datetime`, `ip`, `region`, `country`, `coordinates`, `organization`) VALUES(?,?,?,?,?,?,?);"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(listeners_statistics["connect_datetime"]),str(listeners_statistics["disconnect_datetime"]),str(listeners_statistics["ip"]),str(listeners_statistics["region"]),str(listeners_statistics["country"]),str(listeners_statistics["coordinates"]),str(listeners_statistics["organization"])))
    conn.commit()
    conn.close()
    listeners_statistics["number"] = cur.lastrowid
    return listeners_statistics
    
def read_listener_statistic(listeners_statistic_number):
    query = "SELECT * FROM `listeners_statistics` WHERE `number`=? LIMIT 1;"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(str(listeners_statistic_number),))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    row = rows[0]
    listener_statistic_item = {"number":row[0],"connect_datetime":row[1],"disconnect_datetime":row[2],"ip":row[3],"region":row[4],"country":row[5],"coordinates":row[6],"organization":row[7]}
    return listener_statistic_item
    
def read_listener_statistics():
    query = "SELECT * FROM `listeners_statistics` ORDER BY datetime(`connect_datetime`);"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    listener_statistic_items = []
    for row in rows:
        listener_statistic_items.append({"number":row[0],"connect_datetime":row[1],"disconnect_datetime":row[2],"ip":row[3],"region":row[4],"country":row[5],"coordinates":row[6],"organization":row[7]})
    return listener_statistic_items
    
def search_listener_statistics(start_datetime,end_datetime):
    query = "SELECT * FROM `listeners_statistics` WHERE (datetime(`connect_datetime`)>=datetime(?) AND datetime(`disconnect_datetime`)<=datetime(?)) OR (datetime(`connect_datetime`)>=datetime(?) AND datetime(`connect_datetime`)<=datetime(?) AND `disconnect_datetime` IS NULL) ORDER BY datetime(`connect_datetime`);"
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query,(start_datetime,end_datetime,start_datetime,end_datetime))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    listener_statistic_items = []
    for row in rows:
        listener_statistic_items.append({"number":row[0],"connect_datetime":row[1],"disconnect_datetime":row[2],"ip":row[3],"region":row[4],"country":row[5],"coordinates":row[6],"organization":row[7]})
    return listener_statistic_items

def update_listener_statistic(listeners_statistic):
    conn = create_connection()
    query = "UPDATE `listeners_statistics` SET `connect_datetime`=?,`disconnect_datetime`=?,`ip`=?,`region`=?, `country`=?,`coordinates`=?,`organization`=? WHERE `number`=?;"
    cur = conn.cursor()
    cur.execute(query,(str(listeners_statistic["connect_datetime"]),str(listeners_statistic["disconnect_datetime"]),str(listeners_statistic["ip"]),str(listeners_statistic["region"]),str(listeners_statistic["country"]),str(listeners_statistic["coordinates"]),str(listeners_statistic["organization"]),str(listeners_statistic["number"])))
    conn.commit()
    conn.close()
    return listeners_statistic
     
def delete_listener_statistic(listeners_statistic):
    conn = create_connection()
    query = "DELETE FROM `listeners_statistics` WHERE `number`=?;"
    cur = conn.cursor()
    cur.execute(query,(listeners_statistic["number"],))
    conn.commit()
    conn.close()
    return 1

### General functions ###

def import_type_by_type(relative_type,item):
    if relative_type=="sound_files":
        item = import_sound_file(item)
    elif relative_type=="sound_clips":
        item = import_sound_clip(item)
    elif relative_type=="playlists":
        item = import_playlist(item[0],item[1])
    elif relative_type=="retransmitions":
        item = import_retransmition(item)
    elif relative_type=="station_logos":
        item = import_station_logo(item[0],item[1])
    elif relative_type=="church_news":
        item = import_church_new(item)
    elif relative_type=="weather_news":
        item = import_weather_new(item)
    elif relative_type=="time_collections":
        item = import_time_collection(item[0],item[1],item[2])
        
    return items

def read_item_by_type_and_number(relative_type,relative_number):
    if relative_type=="sound_files":
        item = read_sound_file(relative_number)
    elif relative_type=="sound_clips":
        item = read_sound_clip(relative_number)
    elif relative_type=="playlists":
        #relative_number will be the playlist_title
        item = read_playlist(relative_number)
    elif relative_type=="retransmitions":
        item = read_retransmition(relative_number)
    elif relative_type=="station_logos":
        item = read_station_logo(relative_number)
    elif relative_type=="church_news":
        item = read_church_new(relative_number)
    elif relative_type=="weather_news":
        item = read_weather_new(relative_number)
    elif relative_type=="time_collections":
        item = read_time_collection(relative_number)
        
    return item

def read_items_by_type(relative_type):
    if relative_type=="sound_files":
        items = read_sound_files()
    elif relative_type=="sound_clips":
        items = read_sound_clips()
    elif relative_type=="playlists":
        items = read_playlists()
    elif relative_type=="retransmitions":
        items = read_retransmitions()
    elif relative_type=="station_logos":
        items = read_station_logos()
    elif relative_type=="church_news":
        items = read_church_news()
    elif relative_type=="weather_news":
        items = read_weather_news()
    elif relative_type=="time_collections":
        items = read_time_collections()
        
    return items
    
def search_item_by_type_and_number(relative_type,search_phrase,news_datetime=None):

    if relative_type=="sound_files":
        items = search_sound_files(search_phrase)
    elif relative_type=="sound_clips":
        items = search_sound_clips(search_phrase)
    elif relative_type=="playlists":
        items = search_playlists(search_phrase)
    elif relative_type=="retransmitions":
        items = search_retransmitions(search_phrase)
    elif relative_type=="station_logos":
        items = search_station_logos(search_phrase)
    elif relative_type=="church_news":
        items = search_church_news(search_phrase,news_datetime)
    elif relative_type=="weather_news":
        items = search_weather_news(search_phrase,news_datetime)
    elif relative_type=="time_collections":
        items = search_time_collections(search_phrase)
        
    return items
    
def update_type_by_type(relative_type,item):

    if relative_type=="sound_files":
        item = update_sound_file(item)
    elif relative_type=="sound_clips":
        item = update_sound_clip(item)
    elif relative_type=="playlists":
        item = update_playlist(item[0],item[1])
    elif relative_type=="retransmitions":
        item = update_retransmition(item)
    elif relative_type=="station_logos":
        item = update_station_logo(item)
    elif relative_type=="church_news":
        item = update_church_new(item)
    elif relative_type=="weather_news":
        item = update_weather_new(item)
    elif relative_type=="time_collections":
        item = update_time_collection(item[0],item[1],item[2])
        
    return item

def db_item_rating_changed(relative_type,relative_number,rating):
    conn = create_connection()
    query = "UPDATE `"+relative_type+"` SET `rating`=? WHERE `number`=?;"
    cur = conn.cursor()
    cur.execute(query,(rating,relative_number))
    conn.commit()
    conn.close()
    return read_item_by_type_and_number(relative_type,relative_number)

def update_item_volume(relative_type,relative_number,volume):
    conn = create_connection()
    query = "UPDATE `"+relative_type+"` SET `volume`=? WHERE `number`=?;"
    cur = conn.cursor()
    cur.execute(query,(volume,relative_number))
    conn.commit()
    conn.close()
    return read_item_by_type_and_number(relative_type,relative_number)

def update_item_normalize(relative_type,relative_number,normalize):
    conn = create_connection()
    query = "UPDATE `"+relative_type+"` SET `normalize`=? WHERE `number`=?;"
    cur = conn.cursor()
    cur.execute(query,(normalize,relative_number))
    conn.commit()
    conn.close()
    return read_item_by_type_and_number(relative_type,relative_number)

def update_item_pan(relative_type,relative_number,pan):
    conn = create_connection()
    query = "UPDATE `"+relative_type+"` SET `pan`=? WHERE `number`=?;"
    cur = conn.cursor()
    cur.execute(query,(pan,relative_number))
    conn.commit()
    conn.close()
    return read_item_by_type_and_number(relative_type,relative_number)

def update_last_play(relative_type,relative_number,last_play):
    pass
    
def update_item_filter(relative_type,relative_number,low_frequency,high_frequency):
    conn = create_connection()
    query = "UPDATE `"+relative_type+"` SET `low_frequency`=?, `high_frequency`=? WHERE `number`=?;"
    cur = conn.cursor()
    cur.execute(query,(low_frequency,high_frequency,relative_number))
    conn.commit()
    conn.close()
    return read_item_by_type_and_number(relative_type,relative_number)    

def delete_item_by_type_and_number(relative_type,item):
    if relative_type=="sound_files":
        delete_sound_file(item)
    elif relative_type=="sound_clips":
        delete_sound_clip(item)
    elif relative_type=="playlists":
        #relative_number will be the playlist_title
        #playlist = read_item_by_type_and_number("playlists",relative_number)
        delete_playlist(item)
    elif relative_type=="retransmitions":
        delete_retransmition(item)
    elif relative_type=="station_logos":
        delete_station_logo(item)
    elif relative_type=="church_news":
        delete_church_new(item)
    elif relative_type=="weather_news":
        delete_weather_new(item)
    elif relative_type=="time_collections":
        delete_time_collection(item[0]["number"])
        
    return 1