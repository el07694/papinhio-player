import os, shutil,sys
sys.path.append("../..")

folders = os.listdir("../../disket-box")


def delete_folder_contents(folder):
	for filename in os.listdir(folder):
		file_path = os.path.join(folder, filename)
		try:
			if os.path.isfile(file_path) or os.path.islink(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)
		except Exception as e:
			print('Failed to delete %s. Reason: %s' % (file_path, e))



def empty_disket_box():
	delete_answer=""
	while(delete_answer!="ΝΑΙ" and delete_answer!="ΟΧΙ"):			
		delete_answer = input("Θα επιχειριθεί διαγραφή όλων των δεδομένων της δισκοθήκης του προγράμματος (εκτός από τα πρότυπα αρχεία της εγκατάστασης).\nΕίστε σίγουροι ότι θέλετε να διαγραφούν; (ΝΑΙ - ΟΧΙ):")		
		if delete_answer=="ΝΑΙ":
			for folder in folders:
				if folder.lower()!="test-contents":
					delete_folder_contents("../../disket-box/"+folder)
		elif delete_answer=="ΟΧΙ":
			print("Η διαδικασία εγκατάστασης της Βάσης δεδομένων ακυρώθηκε από τον χρήστη.")
			sys.exit()
