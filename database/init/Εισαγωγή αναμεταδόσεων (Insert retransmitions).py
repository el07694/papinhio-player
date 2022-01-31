#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os
import shutil
import sqlite3
from sqlite3 import Error
from pydub import AudioSegment
import sys
sys.path.append("..")
import importlib
convert_time_function = importlib.import_module("Αρχεία πηγαίου κώδικα εφαρμογής (Python).Βοηθητικές συναρτήσεις (Ηelpful functions).Μετατροπή από milliseconds σε ανθρώπινη μορφή (Convert time function)")
sqlite3_functions = importlib.import_module("Αρχεία πηγαίου κώδικα εφαρμογής (Python).Αρχεία κώδικα python (Python files).Συναρτήσεις sqlite3 (Sqlite3 functions)")

def main():
	
	retransmition_images = []
	retransmition_images.append(r"Πειραϊκή εκκλησία.png")
	retransmition_images.append(r"Συν πάσι τοις Αγίοις.png")
	
	for retransmition_image in retransmition_images:
		shutil.copyfile(os.path.abspath("../Δισκοθήκη (Disket box)/Πρότυπα αρχεία κατά την εγκατάσταση του προγράμματος (Test install contents)/Εικόνες αναμεταδόσεων (Retransmition images)/"+retransmition_image),os.path.abspath("../Δισκοθήκη (Disket box)/Εικόνες αναμεταδόσεων (Retransmitions images)/"+retransmition_image))

	retransmitions = []

	retransmitions.append((r'Πειραϊκή εκκλησία',r'https://www.peradio.com',r'dynamic',r'window.MP3jPLAYERS[0]["list"][0].mp3',r'https://impradio.bytemasters.gr/8002/LIVE',r'Πειραϊκή εκκλησία: Το ραδιόφωνο που μιλάει στην ψυχή μας.',os.path.abspath("../Δισκοθήκη (Disket box)/Εικόνες αναμεταδόσεων (Retransmitions images)/"+retransmition_images[0]),r'Πειραϊκή εκκλησία',10))
	retransmitions.append((r'Ραδιοφωνικός σταθμός: Συν πάσι τοις Αγίοις',r'https://synpasitoisagiois.radio12345.com/',r'dynamic',"document.getElementById('urladdress').innerHTML",r'https://freeuk20.listen2myradio.com/live.mp3?typeportmount=s1_19724_stream_430085248',r'Ραδιοφωνικός σταθμός Συν πάσι τοις Αγίοις',os.path.abspath("../Δισκοθήκη (Disket box)/Εικόνες αναμεταδόσεων (Retransmitions images)/"+retransmition_images[1]),r'Συν πάσι τοις Αγίοις',10))
	
	
	for retransmition in retransmitions:
		retransmition_item = {
			"title":retransmition[0],
			"url":retransmition[1],
			"url_option":retransmition[2],
			"javascript_code":retransmition[3],
			"stream_url":retransmition[4],
			"description":retransmition[5],
			"image_path":retransmition[6],
			"image_title":retransmition[7],
			"rating":retransmition[8],
			"volume":100,
			"normalize":0,
			"pan":0,
			"low_frequency":20,
			"high_frequency":20000
		}
		sqlite3_functions.import_retransmition(retransmition_item)
		
main()