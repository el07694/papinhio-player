import sys
import os

def delete_database_file():
	if os.path.exists("../database.db"):
		delete_answer=""
		while(delete_answer!="ΝΑΙ" and delete_answer!="ΟΧΙ"):			
			delete_answer = input("Θα επιχειριθεί διαγραφή της Βάσης δεδομένων.\nΕίστε σίγουροι ότι θέλετε να διαγραφούν; (ΝΑΙ - ΟΧΙ):")		
			if delete_answer=="ΝΑΙ":
				os.remove("../database.db")
			elif delete_answer=="ΟΧΙ":
				print("Η διαδικασία εγκατάστασης της Βάσης δεδομένων ακυρώθηκε από τον χρήστη.")
				sys.exit()
