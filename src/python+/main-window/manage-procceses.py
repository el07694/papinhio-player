from PyQt5 import QtCore, QtGui, QtWidgets
import os
import sys

class Manage_Processes:

    def __init__(self,main_self):
        self.main_self = main_self
        
        self.processes = []
        
        # Διεργασίες αρχικού παραθύρου
        
        self.processes.append({
            "process_number":21,
            "name":"Διεργασία ανακτήσης δεδομένων που αφορούν τα ορατά πεδία του προγράμματος",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Ανακτά πληροφορίες που αφορούν τα ορατά πεδία του προγράμματος με σκοπό την εμφάνιση και την απόκρυψη των επιμέρους τμημάτων του κεντρικού παραθύρου.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })

        self.processes.append({
            "process_number":19,
            "name":"Διεργασία για τον έλεγχο της σύνδεσης στο Διαδίκτιο",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Ελέγχει περιοδικά την σύνδεση του υπολογιστή στο διαδίκτυο.",
            "cpu":0,
            "ram":0,
            "type":"primary"
        })
        
        self.processes.append({
            "process_number":18,
            "name":"Διεργασία για την ένταση του ήχου συστήματος (λειτουργικό σύστημα)",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Ελέγχει περιοδικά την ένταση του ήχου συστήματος με σκοπό την απεικόνιση της τιμής στην εφαρμογή.",
            "cpu":0,
            "ram":0,
            "type":"primary"
        })        


        self.processes.append({
            "process_number":17,
            "name":"Διεργασία αποθήκευσης αλλαγών decks",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Αποθηκεύει ποικίλες ρυθμίσεις που αφορούν τα deck 1, deck 2 και music clip deck.",
            "cpu":0,
            "ram":0,
            "type":"primary"
        })        
        
        self.processes.append({
            "process_number":9,
            "name":"Διεργασία διαχείρισης προγραμματισμένων μεταδόσεων",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Ελέγχει περιοδικά της προγραμματισμένες μεταδόσεις και τις εισάγει στην λίστα αναπαραγωγής του main player.",
            "cpu":0,
            "ram":0,
            "type":"primary"
        })
        
        self.processes.append({
            "process_number":7,
            "name":"Διεργασία διαχείρισης speackers deck",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Είναι υπεύθυνη για την λήψη ηχητικού σήματος από το μικρόφωνο εφόσον γίνει ενεργό. Έπειτα αποστέλει τα δεδομένα αυτά στην διεργασία: 'Διεργασία δημιουργίας τελικού ηχητικού σήματος'.",
            "cpu":0,
            "ram":0,
            "type":"primary"
        })
        
        self.processes.append({
            "process_number":8,
            "name":"Διεργασία διαχείρισης ηχητικών κλήσεων",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Αναμένει ηχητικές κλήσεις από τους ακροατές και αποστέλει τα δεδομένα στην διεργάσια: 'Διεργασία δημιουργίας τελικού ηχητικού σήματος'",
            "cpu":0,
            "ram":0,
            "type":"primary"
        })
        
        self.processes.append({
            "process_number":14,
            "name":"Διεργασία προετοιμασίας deck 1",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Διαβάζει το αρχείο ήχου το οποίο έχει φορτωθεί στο deck 1 έτσι ώστε να είναι έτοιμο για την διεργασία δημιουργίας του τελικού ηχητικού σήματος.",
            "cpu":0,
            "ram":0,
            "type":"primary"
        })
        
        self.processes.append({
            "process_number":15,
            "name":"Διεργασία προετοιμασίας deck 2",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Διαβάζει το αρχείο ήχου το οποίο έχει φορτωθεί στο deck 2 έτσι ώστε να είναι έτοιμο για την διεργασία δημιουργίας του τελικού ηχητικού σήματος.",
            "cpu":0,
            "ram":0,
            "type":"primary"
        })        
        
        self.processes.append({
            "process_number":16,
            "name":"Διεργασία προετοιμασίας music clip dec",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Διαβάζει το ηχητικό clip το οποίο έχει φορτωθεί στο music clip deck έτσι ώστε να είναι έτοιμο για την διεργασία δημιουργίας του τελικού ηχητικού σήματος.",
            "cpu":0,
            "ram":0,
            "type":"primary"
        })                
        
        self.processes.append({
            "process_number":6,
            "name":"Διεργασία δημιουργίας τελικού ηχητικού σήματος",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Διαχειρίζετε την δημιουργία του τελικού ηχητικού σήματος από όλα τα decks (deck 1, deck 2, music clip deck, speackers deck, ip call 1, ip call 2, ip call 3).",
            "cpu":0,
            "ram":0,
            "type":"primary"
        })
        
        self.processes.append({
            "process_number":10,
            "name":"Διεργασία αποστολής ηχητικών δεδομένων στους ακροατές",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Λαμβάνει δεδομένα από την διεργασία: 'Διεργασία δημιουργίας τελικού ηχητικού σήματος' και έπειτα αποστέλει τα δεδομένα στους ακροατές.",
            "cpu":0,
            "ram":0,
            "type":"primary"
        })
        
        self.processes.append({
            "name":"Διεργασία κυματομορφών",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Διαχειρίζετε την δημιουργία των δεδομένων από την διεργασία: 'Διεργασία δημιουργίας τελικού ηχητικού σήματος' για την αναπαράσταση των κυματομορφών για κάθε ραδιοφωνική σύνδεση.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία εμφάνισης σελίδων ακρόασης",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Διαχειρίζετε την εμφάνιση των ιστοσελίδων στις οποίες συνδέονται οι ακροατές για ακρόαση.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "process_number":12,
            "name":"Διεργασία αναζήτησης λίστας αναπαραγωγής του main player",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Διαχειρίζετε την αναζήτηση των εγγραφών της λίστας αναπαραγωγής του main player.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        ### Menu 1 ###
        
        # Διεργασία για πολλές χρήσεις #
        self.processes.append({
            "name":"Διεργασία αναζήτησης προγραμματισμένης μετάδοσης",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Αναζητάει προγραμματισμένες μεταδόσεις με στόχο την εισαγωγή  κάποιου είδους μετάδοσης (αρχείου ήχου, λίστας αναπαραγωγής, ηχητικού clip, αναμετάδοσης, σήματος σταθμού, δελτίου εκκλησιαστικών ανακοινώσεων, δελτίο καιρού, ώρα Ελλάδας) σε αυτήν.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        # Διαχείριση ραδιοφωνικών μεταδόσεων #

        self.processes.append({
            "name":"Διεργασία ραδιοφωνικών μεταδόσεων",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Διαχειρίζετε τις ραδιοφωνικές μεταδόσεις (στατιστικών ακροατών, διακοπή σύνδεσης,...).",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        # Αρχεία ήχου #
        self.processes.append({
            "process_number":5,
            "name":"Διεργασία εύρεσης αρχείου ήχου",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Αναζητάει αρχεία ήχου από την βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "process_number":3,
            "name":"Διεργασία εισαγωγής αρχείου ήχου",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εισάγει ένα αρχείο ήχου στην δισκοθήκη και στην βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία εισαγωγής αρχείου ήχου από βίντεο",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Κατεβάζει ένα αρχείο βίντεο από το youtube και το μετατρέπει σε αρχείο ήχου.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία επεξεργασίας αρχείου ήχου",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Επεξεργάζετε ένα αρχείο ήχου στην δισκοθήκη και στην βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία προσθήκης αρχείου ήχου στην λίστα αναπαραγωγής του main player",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Προσθέτει είτε στην αρχή είτε στο τέλος της λίστας αναπαραγωγής του main player ένα αρχείο ήχου.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία εξαγωγής (και προεπισκόπησης) αρχείου ήχου",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εξάγει ένα αρχείο ήχου σε άλλη μορφή (mp3,wav,ogg) και ενδεχομένως εκτελεί το αρχείο ήχου πριν την εξαγωγή εφόσον ζητηθεί.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "process_number":4,
            "name":"Διεργασία προεπισκόπησης αρχείου ήχου",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εκτελεί ένα αρχείο ήχου (προεπισκόπηση).",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία διαγραφής αρχείου ήχου",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Διαγράφει ένα αρχείο ήχου από την βάση δεδομένων και από την δισκοθήκη.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })

        # Λίστες αναπαραγωγής #
        self.processes.append({
            "name":"Διεργασία εύρεσης λίστας αναπαραγωγής",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Αναζητάει λίστες αναπαραγωγής από την βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία προσπέλασης λίστας αναπαραγωγής",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Διαβάζει τα δεδομένα μίας λίστας αναπαραγωγής.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία αποθήκευσης νέας λίστας αναπαραγωγής (από υπάρχον αρχείο playlist)",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Αποθηκεύει μία νέα λίστα αναπαραγωγής (από υπάρχον αρχείο playlist).",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία εύρεσης δεδομένων για λίστα αναπαραγωγής",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Αναζητεί αρχεία ήχου, αναμεταδόσεις και λίστες αναπαραγωγής με σκοπό την δημιουργία ή την επεξεργασία κάποιας λίστας αναπαραγωγής.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })

        self.processes.append({
            "name":"Διεργασία αποθήκευσης νέας λίστας αναπαραγωγής που έχει δημιουργηθεί μέσω αναζήτησης ηχητικών δεδομένων από την δισκοθήκη.",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Αποθηκεύει μία νέα λίστα αναπαραγωγής που έχει δημιουργηθεί μέσω αναζήτησης δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία τροποποίησης λίστας αναπαραγωγής.",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Τροποποιεί μία λίστα αναπαραγωγής.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία προσθήκης λίστας αναπαραγωγής στην λίστα αναπαραγωγής του main player",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Προσθέτει είτε στην αρχή είτε στο τέλος της λίστας αναπαραγωγής του main player μία λίστα αναπαραγωγής.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία εξαγωγής λίστας αναπαραγωγής ως αρχείο λίστας αναπαραγωγής",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εξάγει μία λίστα αναπαραγωγής σε μορφή λίστας αναπαραγωγής.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία εξαγωγής (και προεπισκόπησης) λίστας αναπαραγωγής ως αρχεία ήχου",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εξάγει μία λίστα αναπαραγωγής ως αρχεία ήχου και ενδεχομένως εκτελεί τα αρχεία ήχου πριν την εξαγωγή εφόσον ζητηθεί.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία προεπισκόπησης λίστας αναπαραγωγής",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εκτελεί μία λίστα αναπαραγωγής (προεπισκόπηση).",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία διαγραφής λίστας αναπαραγωγής",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Διαγράφει μία λίστα αναπαραγωγής από την βάση δεδομένων και από την δισκοθήκη.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })

        
        # Ηχητικά clips #
        self.processes.append({
            "name":"Διεργασία εύρεσης ηχητικού clip",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Αναζητάει ηχητικά clips από την βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })

        self.processes.append({
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
            "name":"Διεργασία επεξεργασίας ηχητικού clip",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Επεξεργάζετε ένα ηχητικό clip στην δισκοθήκη και στην βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία προσθήκης ηχητικού clip στην λίστα αναπαραγωγής του main player",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Προσθέτει είτε στην αρχή είτε στο τέλος της λίστας αναπαραγωγής του main player ένα ηχητικό clip.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία εξαγωγής (και προεπισκόπησης) ηχητικού clip",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εξάγει ένα ηχητικό clip σε άλλη μορφή (mp3,wav,ogg) και ενδεχομένως εκτελεί το ηχητικό clip πριν την εξαγωγή εφόσον ζητηθεί.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία προεπισκόπησης ηχητικού clip",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εκτελεί ένα ηχητικό clip (προεπισκόπηση).",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία ταξινόμησης ηχητικών clips",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Αποθηκεύει ταξινομημένα τα ηχητικά clips στην βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία διαγραφής ηχητικού clip",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Διαγράφει ένα ηχητικό clip από την βάση δεδομένων και από την δισκοθήκη.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })       

        # Αναμεταδόσεις #
        
        self.processes.append({
            "name":"Διεργασία εύρεσης αναμεταδόσεων",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Αναζητάει αναμεταδόσεις από την βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })

        self.processes.append({
            "name":"Διεργασία εισαγωγής αναμετάδοσης",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εισάγει μία αναμετάδοση στην δισκοθήκη και στην βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία επεξεργασίας αναμετάδοσης",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Επεξεργάζετε μία αναμετάδοση στην δισκοθήκη και στην βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία προσθήκης αναμετάδοσης στην λίστα αναπαραγωγής του main player",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Προσθέτει είτε στην αρχή είτε στο τέλος της λίστας αναπαραγωγής του main player μία αναμετάδοση.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία εξαγωγής αναμετάδοσης",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εξάγει μία αναμετάδοση σε μορφή λίστας αναπαραγωγής.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία προεπισκόπησης αναμετάδοσης",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εκτελεί μία αναμετάδοση (προεπισκόπηση).",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία διαγραφής αναμετάδοσης",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Διαγράφει μία αναμετάδοση από την βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        # Σήμα σταθμού #

        self.processes.append({
            "name":"Διεργασία εύρεσης σήματος σταθμού",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Αναζητάει σήματα σταθμού από την βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })

        self.processes.append({
            "name":"Διεργασία εισαγωγής σήματος σταθμού",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εισάγει ένα σήμα σταθμού στην δισκοθήκη και στην βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία επεξεργασίας σήματος σταθμού",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Επεξεργάζετε ένα σήμα σταθμού στην δισκοθήκη και στην βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία προσθήκης σήματος σταθμού στην λίστα αναπαραγωγής του main player",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Προσθέτει είτε στην αρχή είτε στο τέλος της λίστας αναπαραγωγής του main player μία αναμετάδοση.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία εξαγωγής (και προεπισκόπησης) σήματος σταθμού",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εξάγει ένα σήμα σταθμού σε άλλη μορφή (mp3,wav,ogg) και ενδεχομένως εκτελεί το σήμα σταθμού πριν την εξαγωγή εφόσον ζητηθεί.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία προεπισκόπησης σήματος σταθμού",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εκτελεί ένα σήμα σταθμού (προεπισκόπηση).",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία επιλογής προεπιλεγμένου σήματος σταθμού",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Αποθηκεύει ως προεπιλεγμένο ένα σήμα σταθμού στην βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία διαγραφής σήματος σταθμού",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Διαγράφει ένα σήμα σταθμού από την βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })

        # Ώρα Ελλάδας #

        self.processes.append({
            "name":"Διεργασία εύρεσης ώρα Ελλάδας",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Αναζητάει συλλογές ώρα Ελλάδας από την βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })

        self.processes.append({
            "name":"Διεργασία εισαγωγής ώρα Ελλάδας",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εισάγει μία συλλογή Ώρα Ελλάδας στην δισκοθήκη και στην βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία επεξεργασίας ώρα Ελλάδας",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Επεξεργάζετε μία συλλογή ώρα Ελλάδας στην δισκοθήκη και στην βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία προσθήκης ώρα Ελλάδας στην λίστα αναπαραγωγής του main player",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Προσθέτει στην λίστα αναπαραγωγής του main player μία συλλογή ώρα Ελλάδας ώστε να γίνει αναπαραγωγή της την κατάλληλη χρονική στιγμή.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία εξαγωγής (και προεπισκόπησης) ώρα Ελλάδας",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εξάγει μία συλλογή ώρα Ελλάδας σε άλλη μορφή (mp3,wav,ogg) και ενδεχομένως εκτελεί τα αρχεία ήχου της συλλογής πριν την εξαγωγή εφόσον ζητηθεί.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία προεπισκόπησης συλλογής ώρα Ελλάδας",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εκτελεί μία συλλογή ώρα Ελλάδας (προεπισκόπηση).",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία επιλογής προεπιλεγμένης συλλογής ώρα Ελλάδας",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Αποθηκεύει ως προεπιλεγμένη μία συλλογή ώρα Ελλάδας στην βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία διαγραφής ώρα Ελλάδας",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Διαγράφει μία συλλογή ώρα Ελλάδας από την βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        # Δελτίο εκκλησιαστικών ανακοινώσεων #
        self.processes.append({
            "name":"Διεργασία εύρεσης δελτίου εκκλησιαστικών ανακοινώσεων",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Αναζητάει δελτία εκκλησιαστικών ανακοινώσεων από την βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })

        self.processes.append({
            "name":"Διεργασία προεπισκόπησης εισαγωγής δελτίου εκκλησιαστικών ανακοινώσεων από αρχείο",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εκτελεί την προεπισκόπηση του δελτίου εκκλησιαστικών ανακοινώσεων το οποίο έχει εισαχθεί ως αρχείο.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία ηχογράφησης δελτίου εκκλησιαστικών ανακοινώσεων",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εκτελεί την ηχογράφηση του δελτίου εκκλησιαστικών ανακοινώσεων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία προεπισκόπησης ηχογραφημένου δελτίου εκκλησιαστικών ανακοινώσεων",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εκτελεί την προεπισκόπηση της ηχογράφησης του δελτίου εκκλησιαστικών ανακοινώσεων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία μετατροπής δελτίου εκκλησιαστικών ανακοινώσεων από κείμενο σε αρχείο ήχου",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Μετατρέπει ένα κείμενο που περιέχει το δελτίο εκκλησιαστικών ανακοινώσεων σε αρχείο ήχου.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία προεπισκόπησης δελτίου εκκλησιαστικών ανακοινώσεων από κείμενο",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εκτελεί την προεπισκόπηση του δελτίου εκκλησιαστικών ανακοινώσεων το οποίο έχει εισαχθεί από κείμενο.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία αυτόματης εύρεσης δελτίου εκκλησιαστικών ανακοινώσεων από την Πειραϊκή εκκλησία",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Κάνει προσπέλαση την ιστοσελίδα peradio.com με σκοπό την εύρεση του δελτίου εκκλησιαστικών ανακοινώσεων. Έπειτα το ευρεθέν κείμενο το μετατρέπει σε αρχείο ήχου και τέλος εκτελεί την προεπισκόπηση του αρχείου ήχου.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία προεπισκόπησης δελτίου εκκλησιαστικών ανακοινώσεων από την ιστοσελίδα peradio.com",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εκτελεί την προεπισκόπηση του αρχείου ήχου το κείμενο του οποίου έχει βρεθεί από την ιστοσελίδα peradio.com.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Εισαγωγή δελτίου εκκλησιαστικών ανακοινώσεων στην βάση δεδομένων",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εισάγει ένα νέο δελτίο εκκλησιαστικών ανακοινώσεων στην βάση δεδομένων και στην δισκοθήκη.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία επεξεργασίας δελτίου εκκλησιαστικών ανακοινώσεων",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Επεξεργάζετε ένα δελτίο εκκλησιαστικών ανακοινώσεων στην δισκοθήκη και στην βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία προσθήκης δελτίου εκκλησιαστικών ανακοινώσεων στην λίστα αναπαραγωγής του main player",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Προσθέτει είτε στην αρχή είτε στο τέλος της λίστας αναπαραγωγής του main player ένα δελτίο εκκλησιαστικών ανακοινώσεων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία εξαγωγής (και προεπισκόπησης) δελτίου εκκλησιαστικών ανακοινώσεων",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εξάγει ένα δελτίο εκκλησιαστικών ανακοινώσεων σε άλλη μορφή (mp3,wav,ogg) και ενδεχομένως εκτελεί το δελτίο πριν την εξαγωγή εφόσον ζητηθεί.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία προεπισκόπησης δελτίου εκκλησιαστικών ανακοινώσεων",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εκτελεί ένα δελτίο εκκλησιαστικών ανακοινώσεων (προεπισκόπηση).",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία επιλογής προεπιλεγμένου δελτίου εκκλησιαστικών ανακοινώσεων",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Αποθηκεύει ως προεπιλεγμένο ένα δελτίο εκκλησιαστικών ανακοινώσεων στην βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία διαγραφής δελτίου εκκλησιαστικών ανακοινώσεων",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Διαγράφει ένα δελτίο εκκλησιαστικών ανακοινώσεων από την βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        # Δελτίο καιρού #

        self.processes.append({
            "name":"Διεργασία εύρεσης δελτίου καιρού",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Αναζητάει δελτία καιρού από την βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })

        self.processes.append({
            "name":"Διεργασία προεπισκόπησης εισαγωγής δελτίου καιρού από αρχείο",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εκτελεί την προεπισκόπηση του δελτίου καιρού το οποίο έχει εισαχθεί ως αρχείο.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία ηχογράφησης δελτίου καιρού",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εκτελεί την ηχογράφηση του δελτίου καιρού.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία προεπισκόπησης ηχογραφημένου δελτίου καιρού",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εκτελεί την προεπισκόπηση της ηχογράφησης του δελτίου καιρού.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία μετατροπής δελτίου καιρού από κείμενο σε αρχείο ήχου",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Μετατρέπει ένα κείμενο που περιέχει το δελτίο καιρού σε αρχείο ήχου.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία προεπισκόπησης δελτίου καιρού από κείμενο",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εκτελεί την προεπισκόπηση του δελτίου καιρού το οποίο έχει εισαχθεί από κείμενο.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία αυτόματης εύρεσης δελτίου καιρού από την ιστοσελίδα k24.gr",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Λαμβάνει από την ιστοσελίδα k24.gr το δελτίο καιρού. Έπειτα εκτελεί την προεπισκόπηση του αρχείου ήχου.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία προεπισκόπησης δελτίου καιρού από την ιστοσελίδα k24.gr",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εκτελεί την προεπισκόπηση του αρχείου ήχου το οποίο έχει ληφθεί από την ιστοσελίδα k24.gr.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Εισαγωγή δελτίου καιρού στην βάση δεδομένων",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εισάγει ένα νέο δελτίο καιρού στην βάση δεδομένων και στην δισκοθήκη.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία επεξεργασίας δελτίου καιρού",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Επεξεργάζετε ένα δελτίο καιρού στην δισκοθήκη και στην βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία προσθήκης δελτίου καιρού στην λίστα αναπαραγωγής του main player",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Προσθέτει είτε στην αρχή είτε στο τέλος της λίστας αναπαραγωγής του main player ένα δελτίο καιρού.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία εξαγωγής (και προεπισκόπησης) δελτίου καιρού",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εξάγει ένα δελτίο καιρού σε άλλη μορφή (mp3,wav,ogg) και ενδεχομένως εκτελεί το δελτίο πριν την εξαγωγή εφόσον ζητηθεί.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία προεπισκόπησης δελτίου καιρού",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εκτελεί ένα δελτίο καιρού (προεπισκόπηση).",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία επιλογής προεπιλεγμένου δελτίου καιρού",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Αποθηκεύει ως προεπιλεγμένο ένα δελτίο καιρού στην βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία διαγραφής δελτίου καιρού",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Διαγράφει ένα δελτίο καιρού από την βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        # Ηχογράφηση #
        
        self.processes.append({
            "name":"Διεργασία διαχείρισης ηχογράφησης",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Διαχειρίζετε την ηχογράφηση του ηχητικού σήματος του general deck.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        # Αναφορές #

        self.processes.append({
            "name":"Διεργασία αναφοράς προγραμματισμένων μεταδόσεων",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Δημιουργεί την αναφορά κάποιας προγραμματισμένης μετάδοσης για το ορισθέν χρονικό διάστημα.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία αναφοράς εβδομαδιαίου προγράμματος",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Δημιουργεί την αναφορά του προγράμματος του σταθμού για το ορισθέν χρονικό διάστημα.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία αναφοράς ιστορικού μεταδόσεων",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Δημιουργεί την αναφορά του ιστορικού μεταδόσεων για το ορισθέν χρονικό διάστημα.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία αναφοράς στατιστικά ακροατών",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Δημιουργεί την αναφορά με τα στατιστικά των ακροατών για το ορισθέν χρονικό διάστημα.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        # Διαχείριση συσκευών #
        
        self.processes.append({
            "process_number":1,
            "name":"Διεργασία προεπισκόπησης test αρχείου κατά την ρύθμιση των ηχείων",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Κάνει προεπισκόπηση ένα δείγμα αρχείου ήχου για την ρύθμιση των ηχείων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "process_number":2,
            "name":"Διεργασία λήψης αναπαραγωγής σήματος μικροφώνου κατά την ρύθμιση του μικροφώνου",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Λαμβάνει σήμα από το μικρόφωνο και το αναπαράγει στα ηχεία. Επίσης δημιουργεί τα απαραίτητα δεδομένα για την οπτικοποίηση του σήματος μικροφώνου.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        '''
        self.processes.append({
            "name":"Διεργασία προβολής κυματομορφής σήματος μικροφώνου κατά την ρύθμιση του μικροφώνου",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Οπτικοποιεί το σήμα από το μικρόφωνο κατά την ρύθμισή του.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        '''

        #Διαχείριση διεργασιών #
        
        self.processes.append({
            "process_number":11,
            "name":"Διεργασία διαχείρισης διεργασιών",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Σταματάει ή διακόπτει κάποια δευτερεύουσα διεργασία. Επίσης ανανεώνει τις ενδείξεις των διεργασιών (CPU, RAM, κ.α.)",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        ### Menu 2 ###

        # Επιλογή θέματος #
        
        self.processes.append({
            "process_number":13,
            "name":"Διεργασία αποθήκευσης θέματος",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Αποθηκεύει τις ρυθμίσεις θέματος στην βάση δεδομένων",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })

        # Ορατά πεδία λίστας αναπαραγωγής #

        self.processes.append({
            "process_number":20,
            "name":"Διεργασία αποθήκευσης ορατών πεδίων λίστας αναπαραγωγής",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Αποθηκεύει ποια θα είναι τα ορατά πεδία της λίστας αναπαραγωγής του main player και ποιά όχι.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })

        # Ορατά πεδία προγράμματος #

        self.processes.append({
            "process_number":22,
            "name":"Διεργασία αποθήκευσης ορατών πεδίων προγράμματος",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Αποθηκεύει στην βάση δεδομένων ποιά θα είναι τα ορατά πεδία του προγράμματος Papinhio player και ποιά όχι.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        ### Menu 3 ###

        # Προγραμματισμένες μεταδόσεις #

        self.processes.append({
            "name":"Διεργασία εισαγωγής προγραμματισμένης μετάδοσης",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εισάγει μία νέα προγραμματισμένη μετάδοση στην βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία επεξεργασίας προγραμματισμένης μετάδοσης",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Τροποποιεί μία προγραμματισμένη μετάδοση στην βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία προεπισκόπησης προγραμματισμένης μετάδοσης",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εκτελεί την προεπισκόπηση μίας προγραμματισμένης μετάδοσης.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία διαγραφής προγραμματισμένης μετάδοσης",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εκτελεί την διαγραφή μίας προγραμματισμένης μετάδοσης.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία ενεργοποίησης προγραμματισμένης μετάδοσης",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Εκτελεί την ενεργοποίηση/απενεργοποίηση μίας προγραμματισμένης μετάδοσης ή όλων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })

        # Ραδιοφωνικοί σταθμοί #
        
        self.processes.append({
            "process_number":24,
            "name":"Διεργασία εισαγωγής ραδιοφωνικού σταθμού",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Αποθηκεύει τις ρυθμίσεις μίας νέας ραδιοφωνικής σύνδεσης στην βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία επεξεργασίας ραδιοφωνικού σταθμού",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Τροποποιεί τις ρυθμίσεις μίας ραδιοφωνικής σύνδεσης στην βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        self.processes.append({
            "name":"Διεργασία διαγραφής ραδιοφωνικού σταθμού",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Διαγράφει μία ραδιοφωνική σύνδεση από την βάση δεδομένων.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })
        
        ### Menu 4 ###

        # Επικοινωνία #
        
        self.processes.append({
            "process_number":23,
            "name":"Διεργασία επικοινωνίας",
            "pid":None,
            "status":"stopped",
            "start_datetime":None,
            "description":"Αποστολή ηλεκτρονικού μηνύματος ταχυδρομείου (e-mail) στον συντάκτη του προγράμματος.",
            "cpu":0,
            "ram":0,
            "type":"secondary"
        })

        # Λίγα λόγια για το πρόγραμμα # (δεν χρειάζετε διεργασία)