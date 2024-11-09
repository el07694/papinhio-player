class Manage_Processes:

	def __init__(self,main_self):
		self.main_self = main_self
		
		self.processes = []
		
		### menu 1 ###
		self.processes.append({
			"process_number":1,
			"name":"Διεργασία εξαγωγής ηχητικής κλήσης",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Μετατρέπει μία ηχογραφημένη ηχητική κλήση σε άλλη ηχητική μορφή.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":2,
			"name":"Διεργασία προεπισκόπισης ηχητικής κλήσης",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Διαχειρίζετε την προεπισκόπιση μίας ηχογραφημένης ηχητικής κλήσης.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		}) 

		self.processes.append({
			"process_number":3,
			"name":"Διεργασία αναζήτησης ηχητικής κλήσης",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Διαχειρίζετε την αναζήτηση ηχογραφημένων ηχητικών κλήσεων.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})  

		self.processes.append({
			"process_number":4,
			"name":"Διεργασία χρονικής αποκοπής ηχητικής κλήσης",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Διαχειρίζετε την χρονική αποκοπή ηχογραφημένων ηχητικών κλήσεων.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})				

		self.processes.append({
			"process_number":5,
			"name":"Διεργασία διαχείρισης συσκευών μικροφώνου",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Διαχειρίζετε τις ρυθμίσεις των συσκευών εισόδου (μικρόφωνο).",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})						

		self.processes.append({
			"process_number":6,
			"name":"Διεργασία διαχείρισης ηχείων",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Διαχειρίζετε τις ρυθμίσεις των συσκευών εξόδου (ηχεία).",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		}) 

		self.processes.append({
			"process_number":7,
			"name":"Διεργασία διεργασιών",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Διαχειρίζετε τις διεργασίες (προβολή στατιστικών, τερματισμός και άλλα).",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})			 

		self.processes.append({
			"process_number":8,
			"name":"Διεργασία δημιουργίας λίστας αναπαραγωγής",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εκτελεί τις απαραίτητες ενέργειες για την δημιουργία μίας λίστας αναπαραγωγής.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":9,
			"name":"Διεργασία επεξεργασίας λίστας αναπαραγωγής",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εκτελεί τις απαραίτητες ενέργειες για την επεξεργασία μίας λίστας αναπαραγωγής.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":10,
			"name":"Διεργασία εξαγωγής λίστας αναπαραγωγής ως λίστα αναπαραγωγής",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εξάγει μία λίστα αναπαραγωγής σε αρχείο λίστας αναπαραγωγής.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":11,
			"name":"Διεργασία εξαγωγής λίστας αναπαραγωγής ως αρχεία ήχου",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εξάγει μία λίστα αναπαραγωγής σε μορφή αρχείων ήχου.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":12,
			"name":"Διεργασία εισαγωγής λίστας αναπαραγωγής από αρχείο λίστας αναπαραγωγής",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εισάγει μία λίστα αναπαραγωγής στην δισκοθήκη από αρχείο λίστας αναπαραγωγής.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})		

		self.processes.append({
			"process_number":13,
			"name":"Διεργασία προεπισκόπισης λίστας αναπαραγωγής",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εκτελεί τις απαραίτητες ενέργειες για την προεπισκόπιση μίας λίστας αναπαραγωγής.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})				

		self.processes.append({
			"process_number":14,
			"name":"Διεργασία αναζήτησης λίστας αναπαραγωγής",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Αναζητάει λίστες αναπαραγωγής με σκοπό διάφορες ενέργειες.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})				

		self.processes.append({
			"process_number":15,
			"name":"Διεργασία επεξεργασίας αναμετάδοσης",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Επεξεργάζετε μία ήδη αποθηκευμένη αναμετάδοση.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})				

		self.processes.append({
			"process_number":16,
			"name":"Διεργασία εξαγωγής αναμετάδοσης",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Μετατρέπει και εξάγει μία αναμετάδοση ως αρχείο λίστας αναπαραγωγής.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})				

		self.processes.append({
			"process_number":17,
			"name":"Διεργασία εισαγωγής αναμετάδοσης",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Αποθηκεύει και εκτελεί τους απαραίτητους ελέγχους για την εισαγωγή μίας νέας αναμετάδοσης.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})				

		self.processes.append({
			"process_number":18,
			"name":"Διεργασία προεπισκόπισης αναμετάδοσης",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εκτελεί τις απαραίτητες ενέργειες για την προεπισκόπιση μιάς αναμετάδοσης.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})				

		self.processes.append({
			"process_number":19,
			"name":"Διεργασία αναζήτησης αναμεταδόσεων",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Αναζητάει αναμεταδόσεις για διάφορες ενέργειες.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":20,
			"name":"Διεργασία ταξινόμισης ηχητικών clips",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Ταξινομεί τα ηχητικά clips για την επιθυμητή απεικόνισή τους στο deck 3 (music clip deck).",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":21,
			"name":"Διεργασία επεξεργασίας ηχητικού clip",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Επεξεργάζετε ήδη αποθηκευμένο ηχητικό clip.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":22,
			"name":"Διεργασία εξαγωγής ηχητικού clip",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Μετατρέπει και εξάγει ήδη αποθηκευμένο ηχητικό clip.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":23,
			"name":"Διεργασία εισαγωγής ηχητικού clip",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εισάγει ένα ηχητικό clip στην δισκοθήκη και στην βάση δεδομένων.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":24,
			"name":"Διεργασία προεπισκόπισης ηχητικού clip",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εκτελεί τις απαραίτητες ενέργειες για την προεπισκόπιση ενός ηχητικού clip.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":25,
			"name":"Διεργασία αναζήτησης ηχητικών clips",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Αναζητάει ηχητικά clips με σκοπό διάφορες ενέργειες.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		'''
		self.processes.append({
			"process_number":26,
			"name":"Διεργασία χρονικής αποκοπής ηχητικού clip",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εκτελεί την χρονική αποκοπή ενός ηχητικού clip.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})
		'''
	
		self.processes.append({
			"process_number":27,
			"name":"Διεργασία επεξεργασίας αρχείου ήχου",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Επεξεργάζετε ήδη αποθηκευμένο αρχείο ήχου.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":28,
			"name":"Διεργασία εξαγωγής αρχείου ήχου",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Μετατρέπει και εξάγει ήδη αποθηκευμένο αρχείο ήχου.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":29,
			"name":"Διεργασία εισαγωγής αρχείου ήχου από αρχείο ήχου",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εισάγει ένα αρχείο ήχου στην δισκοθήκη και στην βάση δεδομένων.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":30,
			"name":"Διεργασία εισαγωγής αρχείου ήχου από αρχείο video",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εισάγει ένα αρχείο ήχου. Πήγη: τοπικό αρχείο video ή ο ιστότοπος youtube.com",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})		

		self.processes.append({
			"process_number":31,
			"name":"Διεργασία προεπισκόπισης αρχείου ήχου",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εκτελεί τις απαραίτητες ενέργειες για την προεπισκόπιση ενός αρχείου ήχου.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":32,
			"name":"Διεργασία αναζήτησης αρχείου ήχου",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Αναζητάει αρχεία ήχου με σκοπό διάφορες ενέργειες.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})


		self.processes.append({
			"process_number":33,
			"name":"Διεργασία χρονικής αποκοπής αρχείου ήχου",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εκτελεί την χρονική αποκοπή ενός αρχείου ήχου.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":34,
			"name":"Διεργασία επεξεργασίας δελτίου εκκλησιαστικών ανακοινώσεων",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Επεξεργάζετε ήδη αποθηκευμένα δελτία εκκλησιαστικών ανακοινώσεων.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":35,
			"name":"Διεργασία εξαγωγής δελτίου εκκλησιαστικών ανακοινώσεων",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Μετατρέπει και εξάγει σε άλλη μορφή ήχου ήδη αποθηκευμένα δελτία εκκλησιαστικών ανακοινώσεων.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":36,
			"name":"Διεργασία εισαγωγής δελτίου εκκλησιαστικών ανακοινώσεων",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εισάγει δελτίο εκκλησιαστικών ανακοινώσεων είτε από αρχείο ήχου, είτε από ηχογράφηση, είτε από κείμενο είτε απεθεύας από την ιστοσελίδα peradio.com.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":37,
			"name":"Διεργασία προεπισκόπισης δελτίου εκκλησιαστικών ανακοινώσεων",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εκτελεί τις απαραίτητες ενέργειες ώστε να γίνει εφικτή η προεπισκόπιση δελτίου εκκλησιαστικών ανακοινώσεων.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":38,
			"name":"Διεργασία αναζήτησης δελτίου εκκλησιαστικών ανακοινώσεων",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Αναζητάει δελτία εκκλησιαστικών ανακοινώσεων με σκοπό διάφορες ενέργειες.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})


		self.processes.append({
			"process_number":39,
			"name":"Διεργασία χρονικής αποκοπής δελτίου εκκλησιαστικών ανακοινώσεων",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εκτελεί την χρονική αποκοπή διαστήματος ήδη αποθηκευμένου δελτίου εκκλησιαστικών ανακοινώσεων.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":40,
			"name":"Διεργασία επεξεργασίας συλλογής Ώρας Ελλάδας",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Επεξεργάζετε ήδη αποθηκευμένες συλλογές Ώρας Ελλάδας.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":41,
			"name":"Διεργασία εξαγωγής συλλογής Ώρας Ελλάδας",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Μετατρέπει και εξάγει σε άλλη μορφή ήχου ήδη αποθηκευμένες συλλογές Ώρας Ελλάδας.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":42,
			"name":"Διεργασία εισαγωγής συλλογής Ώρας Ελλάδας",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εισάγει συλλογές Ώρας Ελλάδας από προτεινόμενη πρότυπη μορφή.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":43,
			"name":"Διεργασία προεπισκόπισης συλλογής Ώρας Ελλάδας",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εκτελεί τις απαραίτητες ενέργειες ώστε να γίνει εφικτή η προεπισκόπιση συλλογών Ώρας Ελλάδας.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":44,
			"name":"Διεργασία αναζήτησης συλλογής Ώρας Ελλάδας",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Αναζητάει συλλογές Ώρας Ελλάδας με σκοπό διάφορες ενέργειες.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":45,
			"name":"Διεργασία επεξεργασίας δελτίου ειδήσεων",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Επεξεργάζετε ήδη αποθηκευμένα δελτία ειδήσεων.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":46,
			"name":"Διεργασία εξαγωγής δελτίου ειδήσεων",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Μετατρέπει και εξάγει σε άλλη μορφή ήχου ήδη αποθηκευμένα δελτία ειδήσεων.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":47,
			"name":"Διεργασία εισαγωγής δελτίου ειδήσεων",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εισάγει δελτίο ειδήσεων είτε από αρχείο ήχου, είτε από ηχογράφηση, είτε από κείμενο.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":48,
			"name":"Διεργασία προεπισκόπισης δελτίου ειδήσεων",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εκτελεί τις απαραίτητες ενέργειες ώστε να γίνει εφικτή η προεπισκόπιση δελτίου ειδήσεων.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":49,
			"name":"Διεργασία αναζήτησης δελτίου ειδήσεων",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Αναζητάει δελτία ειδήσεων με σκοπό διάφορες ενέργειες.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})


		self.processes.append({
			"process_number":50,
			"name":"Διεργασία χρονικής αποκοπής δελτίου ειδήσεων",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εκτελεί την χρονική αποκοπή διαστήματος ήδη αποθηκευμένου δελτίου ειδήσεων.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":51,
			"name":"Διεργασία επεξεργασίας σήματος σταθμού",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Επεξεργάζετε ήδη αποθηκευμένα σήματα σταθμού.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":52,
			"name":"Διεργασία εξαγωγής σήματος σταθμού",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Μετατρέπει και εξάγει σε άλλη μορφή ήχου ήδη αποθηκευμένα σήματα σταθμού.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":53,
			"name":"Διεργασία εισαγωγής σήματος σταθμού",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εισάγει σήματα σταθμού είτε από αρχείο ήχου, είτε από ηχογράφηση, είτε από κείμενο.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":54,
			"name":"Διεργασία προεπισκόπισης σήματος σταθμού",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εκτελεί τις απαραίτητες ενέργειες ώστε να γίνει εφικτή η προεπισκόπιση σήματος σταθμού.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":55,
			"name":"Διεργασία αναζήτησης σήματος σταθμού",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Αναζητάει σήματα σταθμού με σκοπό διάφορες ενέργειες.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})


		self.processes.append({
			"process_number":56,
			"name":"Διεργασία χρονικής αποκοπής σήματος σταθμού",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εκτελεί την χρονική αποκοπή διαστήματος ήδη αποθηκευμένου σήματα σταθμού.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":57,
			"name":"Διεργασία επεξεργασίας δελτίου καιρού",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Επεξεργάζετε ήδη αποθηκευμένα δελτία καιρού.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":58,
			"name":"Διεργασία εξαγωγής δελτίου καιρού",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Μετατρέπει και εξάγει σε άλλη μορφή ήχου ήδη αποθηκευμένα δελτία καιρού.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":59,
			"name":"Διεργασία εισαγωγής δελτίου καιρού",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εισάγει δελτίο καιρού είτε από αρχείο ήχου, είτε από ηχογράφηση, είτε από κείμενο, είτε από την ιστοσελίδα k24.gr.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":60,
			"name":"Διεργασία προεπισκόπισης δελτίου καιρού",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εκτελεί τις απαραίτητες ενέργειες ώστε να γίνει εφικτή η προεπισκόπιση δελτίου καιρού.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":61,
			"name":"Διεργασία αναζήτησης δελτίου καιρού",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Αναζητάει δελτία καιρού με σκοπό διάφορες ενέργειες.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})


		self.processes.append({
			"process_number":62,
			"name":"Διεργασία χρονικής αποκοπής δελτίου καιρού",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εκτελεί την χρονική αποκοπή διαστήματος ήδη αποθηκευμένου δελτίου καιρού.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		### menu 2 ###

		self.processes.append({
			"process_number":63,
			"name":"Διεργασία επεξεργασίας ραδιοφωνικών συνδέσεων",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Επεξεργάζετε ήδη αποθηκευμένες ραδιοφωνικές συνδέσεις.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":64,
			"name":"Διεργασία εισαγωγής ραδιοφωνικών συνδέσεων",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εισάγει μία νέα ραδιοφωνική σύνδεση στην δισκοθήκη.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":65,
			"name":"Διεργασία διαχείρισης ραδιοφωνικών συνδέσεων",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Διαχειρίζετε τις ραδιοφωνικές συνδέσεις (σύνδεση και αποσύνδεση).",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})				

		self.processes.append({
			"process_number":66,
			"name":"Διεργασία αναζήτηση ραδιοφωνικών συνδέσεων",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Αναζητάει ραδιοφωνικές συνδέσεις με σκοπό είτε την επεξεργασία είτε την διαγραφή κάποιας συγκεκριμένης ραδιοφωνικής σύνδεσης.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})				
		
		### menu 3 ###
		self.processes.append({
			"process_number":67,
			"name":"Διεργασία επεξεργασίας ηχογραφημένων αρχείων",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Επεξεργάζετε ήδη αποθηκευμένα ηχογραφημένα αρχεία.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})				

		self.processes.append({
			"process_number":68,
			"name":"Διεργασία εξαγωγής ηχογραφημένων αρχείων",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Μετατρέπει και εξάγει σε άλλη μορφή ήχου ήδη αποθηκευμένα ηχογραφημένα αρχεία.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})						

		self.processes.append({
			"process_number":69,
			"name":"Διεργασία εισαγωγής ηχογραφημένων αρχείων",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εισάγει ένα νέο ηχογραφημένο αρχείο είτε στην δισκοθήκη είτε στην βάση δεδομένων.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})						

		self.processes.append({
			"process_number":70,
			"name":"Διεργασία προεπισκόπισης ηχογραφημένων αρχείων",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εκτελεί τις απαραίτητες ενέργειες ώστε να γίνει προεπισκόπιση ενός ήδη αποθηκευμένου ηχογραφημένου αρχείου.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})						

		self.processes.append({
			"process_number":71,
			"name":"Διεργασία αναζήτησης ηχογραφημένων αρχείων",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Αναζητάει ηχογραφημένα αρχεία με σκοπό διάφορες ενέργειες.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})						

		self.processes.append({
			"process_number":72,
			"name":"Διεργασία χρονικής αποκοπής ηχογραφημένων αρχείων",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εκτελεί την χρονική αποκοπή διαστήματος ηχογραφημένου αρχείου ήχου.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})						

		self.processes.append({
			"process_number":73,
			"name":"Διεργασία διαχείρισης ηχογράφησης",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Είναι υπεύθυνη για την ηχογράφηση (έναρξη - παύση - τερματισμός).",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})						

		### menu 4 ###
		self.processes.append({
			"process_number":74,
			"name":"Διεργασία δημιουργίας προγραμματισμένης μετάδοσης",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Δημιουργεί μία νέα προγραμματισμένη μετάδοση.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})						

		self.processes.append({
			"process_number":75,
			"name":"Διεργασία επεξεργασίας προγραμματισμένης μετάδοσης",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Επεξεργάζετε μία ήδη αποθηκευμένη προγραμματισμένη μετάδοση.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})						

		self.processes.append({
			"process_number":76,
			"name":"Διεργασία πλογήσης προγραμματισμένων μετάδοσεων",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Προβάλει αποθηκευμένες προγραμματισμένες μεταδόσεις και εκτελεί διάφορες ενέργειες.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})						

		self.processes.append({
			"process_number":77,
			"name":"Διεργασία προεπισκόπισης προγραμματισμένων μετάδοσεων",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εκτελεί τις απαραίτητες ενέργειες για την προεπισκόπιση προγραμματισμένης μετάδοσης.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})						

		self.processes.append({
			"process_number":78,
			"name":"Διεργασία αναζήτησης προγραμματισμένων μετάδοσεων",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Αναζητάει προγραμματισμένες μετάδοσες με σκοπό διάφορες ενέργειες.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		### menu 5 ###
		self.processes.append({
			"process_number":79,
			"name":"Διεργασία δημιουργίας αναφοράς 'Στατιστικά ακροατών'",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Δημιουργεί την αναφορά με τα στατιστικά των ακροατών για το καθορισμένο χρονικό διάστημα.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})						

		self.processes.append({
			"process_number":80,
			"name":"Διεργασία δημιουργίας αναφοράς 'Ιστορικό μεταδόσεων'",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Δημιουργεί την αναφορά με το ιστορικό των decks για το καθορισμένο χρονικό διάστημα.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})						

		self.processes.append({
			"process_number":81,
			"name":"Διεργασία δημιουργίας αναφοράς 'Προγραμματισμένης μετάδοσης'",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Δημιουργεί την αναφορά με την προβλεπόμενη εκτέλεση μίας προγραμματισμένης μετάδοσης για το καθορισμένο χρονικό διάστημα.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		self.processes.append({
			"process_number":82,
			"name":"Διεργασία δημιουργίας αναφοράς 'Εβδομαδιαίου προγράμματος'",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Δημιουργεί την αναφορά με το Εβδομαδιαίου πρόγραμμα του σταθμού.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})

		### menu 6 ###
		self.processes.append({
			"process_number":83,
			"name":"Διεργασία επιλογής θέματος",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Αλλάζει τις ρυθμίσεις επιλογής θέματος.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})  

		self.processes.append({
			"process_number":84,
			"name":"Διεργασία ορατών πεδίων λίστας αναπαραγωγής των decks",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Αποθηκεύει τις επιλογές που αφορούν τα ορατά πεδία της λίστας αναπαραγωγής των decks.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})										

		self.processes.append({
			"process_number":85,
			"name":"Διεργασία ορατών πεδίων προγράμματος",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Αποθηκεύει τις επιλογές που αφορούν τα ορατά πεδία προγράμματος (Widgets).",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})			
									
		### menu 7 ###
		self.processes.append({
			"process_number":86,
			"name":"Διεργασία επικοινωνίας",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Αποστέλει ηλεκτρονικό μήνυμα ταχυδρομείου στον δημιουργό του προγράμματος.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})										

		### extra ###
		self.processes.append({
			"process_number":87,
			"name":"Διεργασία προβολής προγραμματισμένων μετάδοσεων",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Είναι υπεύθυνη για την προβολή των ημερίσιων προγραμματισμένων μεταδόσεων.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})	

		self.processes.append({
			"process_number":88,
			"name":"Διεργασία δοκιμής ραδιοφωνικών συνδέσεων κατά την εισαγωγή μιάς ραδιοφωνικής σύνδεσης",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Δοκιμαστικός έλεγχος http, mysql ftp, icecast/aiortc συνδέσεων.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})	

		self.processes.append({
			"process_number":89,
			"name":"Διεργασία δοκιμής ραδιοφωνικών συνδέσεων κατά την επεξεργασία μιάς ραδιοφωνικής σύνδεσης",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Δοκιμαστικός έλεγχος http, mysql ftp, icecast/aiortc συνδέσεων.",
			"cpu":0,
			"ram":0,
			"type":"secondary"
		})														

		self.processes.append({
			"process_number":90,
			"name":"Διεργασία εμφάνισης και απόκρυψης QWidgets του main window",
			"pid":None,
			"status":"stopped",
			"start_datetime":None,
			"description":"Εμφανίζει ή αποκρύπτει τα επιμέρους μέρης της κύριας σελίδας του προγράμματος.",
			"cpu":0,
			"ram":0,
			"type":"primary"
		})														

		self.processes.append({
			"process_number": 91,
			"name": "Διεργασία player list των decks",
			"pid": None,
			"status": "stopped",
			"start_datetime": None,
			"description": "Διαχειρίζετε το player list table καθώς και το player list list.",
			"cpu": 0,
			"ram": 0,
			"type": "primary"
		})

		self.processes.append({
			"process_number": 92,
			"name": "Διεργασία διαχείρισης speackers deck",
			"pid": None,
			"status": "stopped",
			"start_datetime": None,
			"description": "Διαχειρίζετε το speackers deck (κουμπιά και ήχος από το μικρόφωνο).",
			"cpu": 0,
			"ram": 0,
			"type": "primary"
		})

		self.processes.append({
			"process_number": 93,
			"name": "Διεργασία άθροισης επιμέρους σημάτων",
			"pid": None,
			"status": "stopped",
			"start_datetime": None,
			"description": "Αθροίζει τα επιμέρους σήματα από τα διάφορα decks και εκτελεί την τελική επεξεργασία του σήματος",
			"cpu": 0,
			"ram": 0,
			"type": "primary"
		})

		self.processes.append({
			"process_number": 94,
			"name": "Διεργασία διαμόρφωσης κεντρικού σήματος απεικόνισης",
			"pid": None,
			"status": "stopped",
			"start_datetime": None,
			"description": "Διαμορφώνει το τελικό σήμα έτσι ώστε να είναι κατάλληλο προς απεικόνιση στο κεντρικό γράφημα.",
			"cpu": 0,
			"ram": 0,
			"type": "primary"
		})

		self.processes.append({
			"process_number": 95,
			"name": "Διεργασία αναπαραγωγής τελικού σήματος εξόδου",
			"pid": None,
			"status": "stopped",
			"start_datetime": None,
			"description": "Κάνει αναπαραγωγή του τελικού σήματος εξόδου στην πρωτεύουσα επιλογή (ηχείο), έτσι ώστε να είναι δυνατή η ακρόαση του ηχητικού σήματος από τον ραδιοφωνικό παραγωγό.",
			"cpu": 0,
			"ram": 0,
			"type": "primary"
		})

		self.processes.append({
			"process_number": 96,
			"name": "Διεργασία διαχείρισης music clip deck",
			"pid": None,
			"status": "stopped",
			"start_datetime": None,
			"description": "Διαχειρίζετε το music clip deck",
			"cpu": 0,
			"ram": 0,
			"type": "primary"
		})

		self.processes.append({
			"process_number": 97,
			"name": "Διεργασία απεικόνισης πληροφοριών σε πλαίσιο",
			"pid": None,
			"status": "stopped",
			"start_datetime": None,
			"description": "Απεικονίζει πληροφορίες σε πλαίσιο όπως η τρέχων ημερομηνία, το ποσοστό χρήσης της κεντρικής μονάδας επεξεργασίας κ.α.",
			"cpu": 0,
			"ram": 0,
			"type": "primary"
		})

		self.processes.append({
			"process_number": 98,
			"name": "Διεργασία διαχείρισης deck 1",
			"pid": None,
			"status": "stopped",
			"start_datetime": None,
			"description": "Διαχειρίζετε το deck 1",
			"cpu": 0,
			"ram": 0,
			"type": "primary"
		})

		self.processes.append({
			"process_number": 99,
			"name": "Διεργασία διαχείρισης deck 2",
			"pid": None,
			"status": "stopped",
			"start_datetime": None,
			"description": "Διαχειρίζετε το deck 2",
			"cpu": 0,
			"ram": 0,
			"type": "primary"
		})

		self.processes.append({
			"process_number": 100,
			"name": "Διεργασία ηχογράφησης",
			"pid": None,
			"status": "stopped",
			"start_datetime": None,
			"description": "Εκτελεί την αποθήκευση του τελικού σήματος εξόδου σε αρχείο",
			"cpu": 0,
			"ram": 0,
			"type": "primary"
		})

		self.processes.append({
			"process_number": 101,
			"name": "Διεργασία διαδικτυακών κλήσεων video",
			"pid": None,
			"status": "stopped",
			"start_datetime": None,
			"description": "Εκτελεί τον server ο οποίος διαχειρίζετε τις διαδικτυακές κλήσεις video",
			"cpu": 0,
			"ram": 0,
			"type": "primary"
		})

		self.processes.append({
			"process_number": 102,
			"name": "Διεργασία σύνθεσης σήματος ηχητικών κλήσεων και μικροφώνου (τοπικά)",
			"pid": None,
			"status": "stopped",
			"start_datetime": None,
			"description": "Δημιουργεί το σήμα από τις ηχητικές κλήσεις όση ώρα αυτές απαντούνται τοπικά",
			"cpu": 0,
			"ram": 0,
			"type": "primary"
		})

		self.processes.append({
			"process_number": 103,
			"name": "Διεργασία μικροφώνου σε περίπτωση ηχητικών κλήσεων",
			"pid": None,
			"status": "stopped",
			"start_datetime": None,
			"description": "Δέχεται και αποστέλει σήμα από το μικρόφωνο σε περίπτωση ηχητικών κλήσεων όση ώρα αυτές απαντούνται τοπικά.",
			"cpu": 0,
			"ram": 0,
			"type": "primary"
		})

		self.processes.append({
			"process_number": 104,
			"name": "Διεργασία αναπαραγωγής τοπικών ηχητικών κλήσεων",
			"pid": None,
			"status": "stopped",
			"start_datetime": None,
			"description": "Κάνει αναπαραγωγή τις ηχητικές κλήσεις και το σήμα από το μικρόφωνο εφόσον οι κλήσεις έχουν απαντηθεί τοπικά.",
			"cpu": 0,
			"ram": 0,
			"type": "primary"
		})

		self.processes.append({
			"process_number": 105,
			"name": "Διεργασία απάντησης ή απόρριψης ηχητικών κλήσεων",
			"pid": None,
			"status": "stopped",
			"start_datetime": None,
			"description": "Κάνει αναπαραγωγή (ντριν - ντριν) μέχρι η ηχητική κλήση να απαντηθεί ή να απορριφθεί η να περάσει το χρονικό διάστημα απάντησης της κλήσης",
			"cpu": 0,
			"ram": 0,
			"type": "primary"
		})

		self.processes.append({
			"process_number": 106,
			"name": "Διεργασία διαχείριση ηχητικής κλήσης 1",
			"pid": None,
			"status": "stopped",
			"start_datetime": None,
			"description": "Διαχειρίζετε το σήμα από την ηχητική κλήση 1 (ενίσχυση, στερεοφωνική ισοστάθμιση, κ.α.)",
			"cpu": 0,
			"ram": 0,
			"type": "primary"
		})

		self.processes.append({
			"process_number": 107,
			"name": "Διεργασία διαχείριση ηχητικής κλήσης 2",
			"pid": None,
			"status": "stopped",
			"start_datetime": None,
			"description": "Διαχειρίζετε το σήμα από την ηχητική κλήση 1 (ενίσχυση, στερεοφωνική ισοστάθμιση, κ.α.)",
			"cpu": 0,
			"ram": 0,
			"type": "primary"
		})

		self.processes.append({
			"process_number": 108,
			"name": "Διεργασία διαχείριση ηχητικής κλήσης 3",
			"pid": None,
			"status": "stopped",
			"start_datetime": None,
			"description": "Διαχειρίζετε το σήμα από την ηχητική κλήση 1 (ενίσχυση, στερεοφωνική ισοστάθμιση, κ.α.)",
			"cpu": 0,
			"ram": 0,
			"type": "primary"
		})

		self.processes.append({
			"process_number": 109,
			"name": "Διεργασία διαχείριση κεντρικής λίστας αναπαραγωγής",
			"pid": None,
			"status": "stopped",
			"start_datetime": None,
			"description": "Διαχειρίζετε την κεντρική λίστα αναπαραγωγής",
			"cpu": 0,
			"ram": 0,
			"type": "primary"
		})

		self.processes.append({
			"process_number": 110,
			"name": "Διεργασία ηχογράφησης ηχητικών κλήσεων",
			"pid": None,
			"status": "stopped",
			"start_datetime": None,
			"description": "Ηχογραφεί τις ηχητικές κλήσεις αυτόματα όση ώρα διαρκούν",
			"cpu": 0,
			"ram": 0,
			"type": "primary"
		})

		self.processes.append({
			"process_number": 111,
			"name": "Διεργασία διαχείρισης συσκευών κάμερας",
			"pid": None,
			"status": "stopped",
			"start_datetime": None,
			"description": "Διαχειρίζετε τις ρυθμίσεις των οπτικών συσκευών εισόδου (κάμερα).",
			"cpu": 0,
			"ram": 0,
			"type": "secondary"
		})