BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "settings" (
    "number"    INTEGER NOT NULL UNIQUE,
    "keyword"   TEXT NOT NULL UNIQUE,
    "current_value" TEXT NOT NULL,
    PRIMARY KEY("number" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "sound_files" (
    "number"    INTEGER NOT NULL UNIQUE,
    "title" text NOT NULL UNIQUE,
    "artist"    text NOT NULL,
    "composer"  text NOT NULL,
    "author"    text NOT NULL,
    "album" text NOT NULL,
    "year"  TEXT NOT NULL,
    "genre" TEXT NOT NULL DEFAULT 'Other',
    "image_path"    text NOT NULL,
    "image_title"   text NOT NULL,
    "description"   text NOT NULL,
    "rating"    INTEGER NOT NULL DEFAULT 10,
    "volume"    INTEGER NOT NULL DEFAULT 100,
    "normalize" INTEGER NOT NULL DEFAULT 0,
    "pan"   INTEGER NOT NULL DEFAULT 0,
    "low_frequency" INTEGER NOT NULL DEFAULT 20,
    "high_frequency"    INTEGER NOT NULL DEFAULT 20000,
    "duration_milliseconds" INTEGER NOT NULL DEFAULT 0,
    "duration_human"    text NOT NULL DEFAULT '00:00:00',
    "original_path" text NOT NULL,
    "saved_path"    text NOT NULL UNIQUE,
    PRIMARY KEY("number" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "sound_clips" (
    "number"    INTEGER NOT NULL UNIQUE,
    "title" text NOT NULL UNIQUE,
    "position"  INTEGER NOT NULL UNIQUE,
    "description"   text NOT NULL,
    "rating"    INTEGER NOT NULL DEFAULT 10,
    "volume"    INTEGER NOT NULL DEFAULT 100,
    "normalize" INTEGER NOT NULL DEFAULT 0,
    "pan"   float NOT NULL DEFAULT 0,
    "low_frequency" float NOT NULL DEFAULT 20,
    "high_frequency"    float NOT NULL DEFAULT 20000,
    "duration_milliseconds" INTEGER NOT NULL DEFAULT 0,
    "duration_human"    text NOT NULL DEFAULT '00:00:00',
    "original_path" text NOT NULL,
    "saved_path"    text NOT NULL UNIQUE,
    PRIMARY KEY("number" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "station_logos" (
    "number"    INTEGER NOT NULL UNIQUE,
    "title" text NOT NULL UNIQUE,
    "description"   text NOT NULL,
    "rating"    INTEGER NOT NULL DEFAULT 10,
    "volume"    INTEGER NOT NULL DEFAULT 100,
    "normalize" INTEGER NOT NULL DEFAULT 0,
    "pan"   float NOT NULL DEFAULT 0,
    "low_frequency" float NOT NULL DEFAULT 20,
    "high_frequency"    float NOT NULL DEFAULT 20000,
    "duration_milliseconds" INTEGER NOT NULL DEFAULT 0,
    "duration_human"    text NOT NULL DEFAULT '00:00:00',
    "original_path" text NOT NULL,
    "saved_path"    text NOT NULL UNIQUE,
    PRIMARY KEY("number" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "church_news" (
    "number"    INTEGER NOT NULL UNIQUE,
    "title" text NOT NULL,
    "date"  datetime NOT NULL,
    "rating"    INTEGER NOT NULL DEFAULT 10,
    "volume"    INTEGER NOT NULL DEFAULT 100,
    "normalize" INTEGER NOT NULL DEFAULT 0,
    "pan"   INTEGER NOT NULL DEFAULT 0,
    "low_frequency" INTEGER NOT NULL DEFAULT 20,
    "high_frequency"    INTEGER NOT NULL DEFAULT 20000,
    "is_default" INTEGER NOT NULL DEFAULT 0,
    "from"  TEXT NOT NULL DEFAULT '',
    "duration_milliseconds" INTEGER NOT NULL DEFAULT 0,
    "duration_human"    text NOT NULL DEFAULT '00:00:00',
    "original_path" text NOT NULL,
    "saved_path"    text NOT NULL UNIQUE,
    PRIMARY KEY("number" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "weather_news" (
    "number"    INTEGER NOT NULL UNIQUE,
    "title" text NOT NULL,
    "date"  datetime NOT NULL,
    "rating"    INTEGER NOT NULL DEFAULT 10,
    "volume"    INTEGER NOT NULL DEFAULT 100,
    "normalize" INTEGER NOT NULL DEFAULT 0,
    "pan"   INTEGER NOT NULL DEFAULT 0,
    "low_frequency" INTEGER NOT NULL DEFAULT 20,
    "high_frequency"    INTEGER NOT NULL DEFAULT 20000,
    "is_default" INTEGER NOT NULL DEFAULT 0,
    "from"  TEXT NOT NULL DEFAULT '',
    "duration_milliseconds" INTEGER NOT NULL DEFAULT 0,
    "duration_human"    text NOT NULL DEFAULT '00:00:00',
    "original_path" text NOT NULL,
    "saved_path"    text NOT NULL UNIQUE,
    PRIMARY KEY("number" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "time_collections" (
    "number"    INTEGER NOT NULL UNIQUE,
    "title" text NOT NULL UNIQUE,
    "case"  INTEGER NOT NULL,
    "append" INTEGER NOT NULL DEFAULT 0,
    "append_relative_type"  TEXT NOT NULL,
    "append_relative_number"    INTEGER,
    PRIMARY KEY("number" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "time_items" (
    "number"    INTEGER NOT NULL UNIQUE,
    "collection_number" INTEGER NOT NULL,
    "title" text NOT NULL,
    "when_to_play"  time NOT NULL,
    "rating"    INTEGER NOT NULL DEFAULT 10,
    "volume"    INTEGER NOT NULL DEFAULT 100,
    "normalize" INTEGER NOT NULL DEFAULT 0,
    "pan"   INTEGER NOT NULL DEFAULT 0,
    "low_frequency" INTEGER NOT NULL DEFAULT 20,
    "high_frequency"    INTEGER NOT NULL DEFAULT 20000,
    "duration_milliseconds" INTEGER NOT NULL DEFAULT 0,
    "duration_human"    text NOT NULL DEFAULT '00:00:00',
    "original_path" text NOT NULL,
    "saved_path"    text NOT NULL UNIQUE,
    FOREIGN KEY("collection_number") REFERENCES "time_collections"("number"),
    PRIMARY KEY("number" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "retransmitions" (
    "number"    INTEGER NOT NULL UNIQUE,
    "title" text NOT NULL UNIQUE,
    "url"   TEXT NOT NULL,
    "url_option"    TEXT NOT NULL DEFAULT 'const',
    "javascript_code"   TEXT NOT NULL,
    "stream_url"    TEXT NOT NULL,
    "description"   text NOT NULL,
    "image_path"    text NOT NULL,
    "image_title"   text NOT NULL,
    "rating"    INTEGER NOT NULL DEFAULT 10,
    "volume"    INTEGER NOT NULL DEFAULT 100,
    "normalize" INTEGER NOT NULL DEFAULT 0,
    "pan"   INTEGER NOT NULL DEFAULT 0,
    "low_frequency" INTEGER NOT NULL DEFAULT 20,
    "high_frequency"    INTEGER NOT NULL DEFAULT 20000,
    PRIMARY KEY("number" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ip_calls" (
    "number"    INTEGER NOT NULL UNIQUE,
    "title" INTEGER NOT NULL,
    "name"  TEXT NOT NULL,
    "surname"   INTEGER NOT NULL,
    "duration_milliseconds" INTEGER NOT NULL DEFAULT 0,
    "duration_human"    INTEGER NOT NULL DEFAULT '00:00:00',
    PRIMARY KEY("number" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "playlists_titles" (
    "number"    INTEGER NOT NULL UNIQUE,
    "title" text NOT NULL UNIQUE,
    PRIMARY KEY("number" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "playlists" (
    "number"    INTEGER NOT NULL UNIQUE,
    "playlist_number"   INTEGER,
    "relative_type" INTEGER NOT NULL,
    "relative_number"   INTEGER NOT NULL,
    "position"  INTEGER NOT NULL,
    PRIMARY KEY("number" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "transmitions" (
    "number"    INTEGER NOT NULL UNIQUE,
    "title" text NOT NULL UNIQUE,
    "live"  text NOT NULL DEFAULT '{}',
    "frequency" TEXT NOT NULL,
    "time_settings" TEXT NOT NULL,
    "types" TEXT NOT NULL DEFAULT 0,
    "active"    INTEGER NOT NULL DEFAULT 1,
    "repeat"    INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY("number" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "transmitions_items" (
    "number"    INTEGER NOT NULL UNIQUE,
    "transmition_number"    INTEGER NOT NULL,
    "relative_type" TEXT NOT NULL,
    "relative_number"   INTEGER NOT NULL,
    "relative_time_seconds" INTEGER,
    "frequency_type"    TEXT NOT NULL,
    "frequency_type_parameters" TEXT NOT NULL,
    "default"   INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY("number" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "player_list" (
    "number"    INTEGER NOT NULL UNIQUE,
    "play"  INTEGER NOT NULL DEFAULT 1,
    "relative_type" TEXT NOT NULL,
    "relative_number"   INTEGER NOT NULL,
    "repeats"   INTEGER NOT NULL DEFAULT 0,
    "duration_milliseconds" INTEGER NOT NULL DEFAULT 0,
    "duration_human"    text NOT NULL DEFAULT '00:00:00',
    "position"  INTEGER NOT NULL,
    PRIMARY KEY("number" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "player_history" (
    "number"    INTEGER NOT NULL UNIQUE,
    "time_started_played"   datetime NOT NULL,
    "time_stoped_played"    datetime,
    "relative_type" TEXT NOT NULL,
    "relative_number"   INTEGER NOT NULL,
    "deck"   TEXT NOT NULL,
    "updated"   INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY("number" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "radio_connections" (
    "number"    INTEGER NOT NULL UNIQUE,
    "title" TEXT NOT NULL UNIQUE,
    "address"   TEXT NOT NULL,
    "image_path"    TEXT NOT NULL,
    "director"  TEXT NOT NULL,
    "telephone" TEXT NOT NULL,
    "fax"   TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "site"  TEXT NOT NULL,
    "description"   TEXT NOT NULL,
    "genre" TEXT NOT NULL,
    "web_server_hostname"   TEXT NOT NULL,
    "ftp_username"  TEXT NOT NULL,
    "ftp_password"  TEXT NOT NULL,
    "mysql_hostname"    TEXT NOT NULL,
    "mysql_username"    TEXT NOT NULL,
    "mysql_password"    TEXT NOT NULL,
    "mysql_database"    TEXT NOT NULL,
    "metadata"  TEXT NOT NULL,
    "radio_page_url"    TEXT NOT NULL DEFAULT '',
    "radio_type"    TEXT NOT NULL,
    "radio_hostname"    TEXT NOT NULL,
    "radio_port"    INTEGER NOT NULL DEFAULT 8000,
    "radio_mount"   TEXT NOT NULL,
    "radio_username"    TEXT NOT NULL,
    "radio_password"    TEXT NOT NULL,
    "bit_rate"  INTEGER NOT NULL DEFAULT 128,
    "mp3_stream"    tinyint(4) NOT NULL DEFAULT 1,
    "channels"  INTEGER NOT NULL DEFAULT 2,
    PRIMARY KEY("number" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "listeners_statistics" (
    "number"    INTEGER NOT NULL UNIQUE,
    "connect_datetime"  datetime NOT NULL,
    "disconnect_datetime"   datetime NOT NULL,
    "ip"    TEXT NOT NULL,
    "region"    TEXT NOT NULL,
    "country"   TEXT NOT NULL,
    "coordinates"   TEXT NOT NULL,
    "organization"  TEXT NOT NULL,
    PRIMARY KEY("number" AUTOINCREMENT)
);
COMMIT;