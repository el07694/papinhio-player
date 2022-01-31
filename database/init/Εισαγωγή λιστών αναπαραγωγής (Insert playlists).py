import os
import shutil
import sqlite3
from sqlite3 import Error
from pydub import AudioSegment
import sys
sys.path.append("..")
import importlib
convert_time_function = importlib.import_module("Αρχεία πηγαίου κώδικα εφαρμογής (Python).Βοηθητικές συναρτήσεις (Ηelpful functions).Μετατροπή από milliseconds σε ανθρώπινη μορφή (Convert time function)")
#del sys.path[-1]

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

	sql = """ INSERT INTO `playlists` (`title`, `relative_type`, `relative_number`, `position`) VALUES ( ?, ?, ?, ?) """
	playlists = []
	
	#1. Απολυτίκια Αγίων
	playlists.append((r'Απολυτίκια Αγίων','sound files','ΑΓΙΑ ΣΚΕΠΗ',1))
	playlists.append((r'Απολυτίκια Αγίων','sound files','ΑΓΙΟΙ ΑΓΓΕΛΟΙ',2))
	playlists.append((r'Απολυτίκια Αγίων','sound files','ΑΓΙΟΙ ΡΑΦΑΗΛ, ΝΙΚΟΛΑΟΣ, ΕΙΡΗΝΗ',3))
	playlists.append((r'Απολυτίκια Αγίων','sound files','ΑΓΙΟΣ ΑΝΔΡΕΑΣ',4))
	playlists.append((r'Απολυτίκια Αγίων','sound files','ΑΓΙΟΣ ΑΝΤΩΝΙΟΣ',5))
	playlists.append((r'Απολυτίκια Αγίων','sound files','ΑΓΙΟΣ ΒΑΣΙΛΕΙΟΣ',6))
	playlists.append((r'Απολυτίκια Αγίων','sound files','ΑΓΙΟΣ ΔΑΥΙΔ ΕΝ ΕΥΒΟΙΑ',7))
	playlists.append((r'Απολυτίκια Αγίων','sound files','ΑΓΙΟΣ ΔΗΜΗΤΡΙΟΣ',8))
	playlists.append((r'Απολυτίκια Αγίων','sound files','ΑΓΙΟΣ ΕΛΕΥΘΕΡΙΟΣ',9))
	playlists.append((r'Απολυτίκια Αγίων','sound files','ΑΓΙΟΣ ΕΦΡΑΙΜ',10))
	playlists.append((r'Απολυτίκια Αγίων','sound files','ΑΓΙΟΣ ΝΕΚΤΑΡΙΟΣ',11))
	playlists.append((r'Απολυτίκια Αγίων','sound files','ΑΓΙΟΣ ΣΠΥΡΙΔΩΝ',12))
	playlists.append((r'Απολυτίκια Αγίων','sound files','ΑΓΙΟΣ ΣΤΕΦΑΝΟΣ',13))
	playlists.append((r'Απολυτίκια Αγίων','sound files','ΑΓΙΟΣ ΧΑΡΑΛΑΜΠΟΣ',14))
	playlists.append((r'Απολυτίκια Αγίων','sound files','ΠΡΟΦΗΤΗΣ ΗΛΙΑΣ',15))
	playlists.append((r'Απολυτίκια Αγίων','sound files','ΤΡΕΙΣ ΙΕΡΑΡΧΕΣ',16))
	playlists.append((r'Απολυτίκια Αγίων','sound files','ΑΓΙΑ ΚΥΡΙΑΚΗ',17))
	playlists.append((r'Απολυτίκια Αγίων','sound files','Απολυτίκιο Αγ. Φανουρίου του Νεοφανούς και Μεγαλομάρτυρος - 27 ΑΥΓΟΥΣΤΟΥ',18))
	
	#2. Αναστάσιμα τροπάρια
	playlists.append((r'Αναστάσιμα τροπάρια','sound files','Αναστάσιμο ήχος α΄ (του λίθου σφραγισθέντος)',1))
	playlists.append((r'Αναστάσιμα τροπάρια','sound files','Αναστάσιμο ήχος β΄ (ότε κατήλθες προς τον θάνατον))',2))
	playlists.append((r'Αναστάσιμα τροπάρια','sound files','Αναστάσιμο ήχος γ΄ (ευφραινέσθω τα ουράνια))',3))
	playlists.append((r'Αναστάσιμα τροπάρια','sound files','Αναστάσιμο ήχος πλ. α΄ (τον συνάναρχον λόγον))',4))
	playlists.append((r'Αναστάσιμα τροπάρια','sound files','Αναστάσιμο ήχος πλ. β΄ (αγγελικαί δυνάμεις))',5))
	playlists.append((r'Αναστάσιμα τροπάρια','sound files','Αναστάσιμο ήχος πλ. δ΄ (εξ΄ ύψους κατήλθες))',6))
	playlists.append((r'Αναστάσιμα τροπάρια','sound files','Αναστάσιμο ήχος δ΄ (το φαιδρόν της αναστάσεως κήρυγμα))',7))
	
	#3. Προσευχές
	playlists.append((r'Προσευχές','sound files','ΑΚΟΛΟΥΘΙΑ ΤΟΥ ΜΙΚΡΟΥ ΠΑΡΑΚΛΗΤΙΚΟΥ ΚΑΝΟΝΟΣ ΕΙΣ ΤΗΝ ΥΠΕΡΑΓΙΑΝ ΘΕΟΤΟΚΟΝ',1))
	playlists.append((r'Προσευχές','sound files','Ο Ακάθιστος Ύμνος (Πέτρος Γαϊτάνος)',2))
	playlists.append((r'Προσευχές','sound files','Πρωινή προσευχή',3))
	playlists.append((r'Προσευχές','sound files','ΚΑΝΩΝ ΠΑΡΑΚΛΗΤΙΚΟΣ ΕΙΣ ΤΟΝ ΑΓΙΟΝ ΙΕΡΟΜΑΡΤΥΡΑ ΓΡΗΓΟΡΙΟΝ Ε΄ ΠΑΤΡΙΑΡΧΗΝ ΚΩΝΣΤΑΝΤΙΝΟΥΠΟΛΕΣ ΤΟΝ ΕΚ ΔΗΜΗΤΣΑΝΗΣ',4))

	#4. Ύμνοι της εκκλησίας μας
	playlists.append((r'Ύμνοι της εκκλησίας μας','sound files','Αγνή Παρθένε Δέσποινα',1))
	playlists.append((r'Ύμνοι της εκκλησίας μας','sound files','Δεύτε ίδωμεν πιστοί',2))
	playlists.append((r'Ύμνοι της εκκλησίας μας','sound files','Εξομολογείσθε - 1',3))
	playlists.append((r'Ύμνοι της εκκλησίας μας','sound files','Εξομολογείσθε - 2 (αγιορείτικο))',4))
	playlists.append((r'Ύμνοι της εκκλησίας μας','sound files','ΘΕΟΦΑΝΕΙΑ',5))
	playlists.append((r'Ύμνοι της εκκλησίας μας','sound files','ΚΟΙΜΗΣΙΣ ΘΕΟΤΟΚΟΥ',6))
	playlists.append((r'Ύμνοι της εκκλησίας μας','sound files','ΜΕΤΑΜΟΡΦΩΣΙΣ',7))
	playlists.append((r'Ύμνοι της εκκλησίας μας','sound files','ΠΕΝΤΗΚΟΣΤΗ',8))
	playlists.append((r'Ύμνοι της εκκλησίας μας','sound files','Την ωραιότητα',9))
	playlists.append((r'Ύμνοι της εκκλησίας μας','sound files','τη Υπερμάχω',10))
	playlists.append((r'Ύμνοι της εκκλησίας μας','sound files','τις Θεός',11))
	playlists.append((r'Ύμνοι της εκκλησίας μας','sound files','Τον Κύριον υμνείτε',12))
	playlists.append((r'Ύμνοι της εκκλησίας μας','sound files','το προσταχθέν',13))
	playlists.append((r'Ύμνοι της εκκλησίας μας','sound files','ΥΠΑΠΑΝΤΗ',14))
	playlists.append((r'Ύμνοι της εκκλησίας μας','sound files','ΥΨΩΣΙΣ ΤΙΜΙΟΥ ΣΤΑΥΡΟΥ',15))

	#5. ΕΠΙΛΟΓΕΣ ΝΕΚ
	playlists.append((r'Επιλογές ΝΕΚ','sound files','ΕΛΑ ΝΑ ΠΑΜΕ Σ΄ΕΝΑ ΜΕΡΟΣ',1))
	playlists.append((r'Επιλογές ΝΕΚ','sound files','ΕΝΑΣ ΑΕΤΟΣ',2))
	playlists.append((r'Επιλογές ΝΕΚ','sound files','ΕΦΤΑ ΒΔΟΜΑΔΕΣ ΕΚΑΝΑ- ΣΥΡΤΟ (ΣΤΑ 3)',3))
	playlists.append((r'Επιλογές ΝΕΚ','sound files','Η ΑΓΑΠΗ ΜΟΥ ΣΤΗΝ ΙΚΑΡΙΑ',4))
	playlists.append((r'Επιλογές ΝΕΚ','sound files','Η ΑΓΑΠΗ ΜΟΥ ΣΤΗΝ ΙΚΑΡΙΑ-ΙΚΑΡΙΩΤΙΚΟΣ (ΓΙΑΝΝΗΣ ΠΑΡΙΟΣ)',5))
	playlists.append((r'Επιλογές ΝΕΚ','sound files','ΘΑΛΑΣΣΑΚΙ ΜΟΥ (ΚΑΛΑΜΑΤΙΑΝΟΣ)',6))
	playlists.append((r'Επιλογές ΝΕΚ','sound files','ΚΑΤΩ ΣΤΟΝ ΚΑΜΠΟ ΤΟΝ ΠΛΑΤΥ- ΚΑΛΑΜΑΤΙΑΝΟ',7))
	playlists.append((r'Επιλογές ΝΕΚ','sound files','ΚΕΙΤΕΤΑΙ ΞΕΝΟΣ ΑΡΡΩΣΤΟΣ - ΖΩΝΑΡΑΔΙΚΟΣ ΒΟΡ. ΘΡΑΚΗΣ',8))
	playlists.append((r'Επιλογές ΝΕΚ','sound files','ΜΑΛΕΒΙΖΙΩΤΙΚΟΣ',9))
	playlists.append((r'Επιλογές ΝΕΚ','sound files','ΜΑΡΙΑ ΠΑΕΙ ΓΙΑ ΠΑΣΧΑΛΙΕΣ (ΚΑΡΩΤΗ ΔΙΔΥΜΟΤΕΙΧΟΥ)',10))
	playlists.append((r'Επιλογές ΝΕΚ','sound files','ΜΕΣ ΤΟΥ ΑΙΓΑΙΟΥ (ΑΙΓΑΙΟΠΕΛΑΓΙΤΙΚΟ)',11))
	playlists.append((r'Επιλογές ΝΕΚ','sound files','ΜΗΛΟ ΜΟΥ ΚΟΚΚΙΝΟ (ΚΑΛΑΜΑΤΙΑΝΟΣ ΜΑΚΕΔΟΝΙΑΣ)',12))
	playlists.append((r'Επιλογές ΝΕΚ','sound files','ΜΩΡΗ ΚΟΝΤΟΥΛΑ ΛΕΜΟΝΙΑ (ΗΠΕΙΡΩΤΙΚΟ)',13))
	playlists.append((r'Επιλογές ΝΕΚ','sound files','ΟΣΟΙ ΞΕΝΟΙ ΚΑΙ ΟΣΟΙ ΔΙΚΟΙ - ΞΕΡΣΥΤΟ ΒΟΡ. ΘΡΑΚΗΣ',14))
	playlists.append((r'Επιλογές ΝΕΚ','sound files','ΠΑΣΧΑΛΙΑΤΙΚΑ ΔΙΣΤΙΧΑ (ΤΡΑΠΕΖΟΥΝΤΑ)',15))
	playlists.append((r'Επιλογές ΝΕΚ','sound files','ΠΑΣΧΑΛΙΑΤΙΚΕΣ ΜΑΝΤΙΝΑΔΕΣ - ΠΕΝΤΟΖΑΛΙ',16))
	playlists.append((r'Επιλογές ΝΕΚ','sound files','ΠΕΡΙΣΤΕΡΙ ΜΟΥ ΧΙΟΝΑΤΟ - ΜΠΑΪΝΤΟΥΣΚΑ ΔΥΤ. ΘΡΑΚΗΣ',17))
	playlists.append((r'Επιλογές ΝΕΚ','sound files','ΠΥΡΡΙΧΙΟΣ ΧΟΡΟΣ (ΠΟΝΤΙΑΚΟ)',18))
	playlists.append((r'Επιλογές ΝΕΚ','sound files','ΣΗΜΕΡΑ ΧΡΙΣΤΟΣ  ΑΝΕΣΤΗ- ΚΑΛΑΜΑΤΙΑΝΟ',19))
	playlists.append((r'Επιλογές ΝΕΚ','sound files','ΤΙΚ- ΠΟΝΤΙΑΚΟ',20))
	playlists.append((r'Επιλογές ΝΕΚ','sound files','ΤΣΑΜΙΚΟ',21))
	playlists.append((r'Επιλογές ΝΕΚ','sound files','ΧΑΣΑΠΩΣΕΡΒΙΚΟ',22))

	#6. Ειρήνη - Δώρο Θεού
	playlists.append((r'Ειρήνη - Δώρο Θεού','sound files','Ειρήνη - Δώρο Θεού - Ομιλία 1',1))
	playlists.append((r'Ειρήνη - Δώρο Θεού','sound files','Ειρήνη - Δώρο Θεού - Ομιλία 2',2))
	
	#7. Σταμάτης Σπανουδάκης - 7 Στιγμές
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΦΘΙΝΟΠΩΡΟ",1))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"Η ΣΤΙΓΜΗ ΠΟΥ ΠΕΡΝΑΕΙ",2))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΠΑΛΙ ΑΠ' ΤΗΝ ΑΡΧΗ",3))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"Ο ΧΟΡΟΣ ΤΟΥ ΓΑΜΟΥ",4))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"Τ' ΑΘΑΝΑΤΟ ΝΕΡΟ",5))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΓΙΑ ΤΗΝ ΝΤΟΡΗ",6))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΒΑΛΣ ΤΗΣ Α΄ ΘΕΣΗΣ",7))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΓΑΛΑΖΙΑ ΩΡΑ",8))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΩΡΕΣ ΑΝΑΤΟΛΗΣ",9))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"Η ΑΓΑΠΗ ΠΟΥ ΔΕΝ ΓΝΩΡΙΣΕΣ",10))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΜΙΚΡΟ ΝΥΧΤΕΡΙΝΟ",11))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"Ο ΧΟΡΟΣ ΤΟΥ ΚΑΠΕΤΑΝΙΟΥ",12))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΞΗΜΕΡΩΜΑ",13))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΘΑΛΑΣΣΑ",14))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΧΡΩΜΑΤΑ ΤΗΣ ΙΡΙΔΟΣ",15))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΠΡΟΜΗΘΕΑΣ",16))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΒΙΟΓΡΑΦΙΑ",17))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΑΓΓΕΛΟΣ",18))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΞΑΦΝΙΚΑ ΕΡΩΤΑΣ",19))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΠΕΤΡΙΝΑ ΧΡΟΝΙΑ",20))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΜΙΑ ΤΟΣΟ ΜΑΚΡΙΝΗ ΑΠΟΥΣΙΑ",21))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΑΠΟΥΣΙΕΣ",22))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"OFFICER'S FACTORY",23))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"I'LL COLORE DELL ODIO",24))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"Η ΦΑΝΕΛΑ ΜΕ ΤΟ 9",25))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΑΝΤΕ ΓΕΙΑ",26))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΖΩΗ",27))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΟΛΑ ΕΙΝΑΙ ΔΡΟΜΟΣ",28))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΝΥΦΕΣ",29))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΔΡΟΜΟΙ ΤΗΣ ΑΝΟΙΞΗΣ",30))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΣΤΙΓΜΗ ΧΑΡΑΣ",31))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΤΗ ΖΩΗ ΜΟΥ ΞΕΤΥΛΙΓΩ",32))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΜΕ ΤΗΝ ΠΝΟΗ ΤΟΥ ΑΝΕΜΟΥ",33))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΚΙΘΑΡΕΣ",34))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΤΑΜΑΛΟ",35))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΞΕΧΑΣΜΕΝΟ ΠΑΙΧΝΙΔΙ",36))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΞΑΦΝΙΚΟΣ ΕΡΩΤΑΣ",37))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΑΛΕ ΙΣΚΑΝΤΑΡ",38))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΣΤΡΑΤΙΩΤΕΣ ΓΥΡΩ ΑΠ' ΤΗ ΦΩΤΙΑ",39))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΚΥΜΑΤΑ",40))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΔΡΟΜΟΙ ΠΟΥ ΔΕΝ ΠΕΡΠΑΤΗΣΕΣ",41))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΖΕΙ ΚΑΙ ΒΑΣΙΛΕΥΕΙ",42))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΣΗΜΕΡΑ",43))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΚΩΝΣΤΑΝΤΙΝΟΣ ΠΑΛΑΙΟΛΟΓΟΣ",44))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΗΦΑΙΣΤΙΩΝ",45))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΑΛΕΞΑΝΔΡΕΙΑ",46))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"Η ΜΟΝΑΞΙΑ ΤΟΥ ΒΑΣΙΛΙΑ",47))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΜΑΥΡΗ ΤΡΙΤΗ",48))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΣΑΪΤΑΝ ΑΣΚΕΡ",49))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΓΙΑ ΤΗ ΣΜΥΡΝΗ",50))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΞΗΜΕΡΩΜΑ ΣΤΑ ΤΕΙΧΗ",51))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΒΡΟΧΕΡΟ ΔΕΙΛΙΝΟ ΣΤΟΝ ΒΟΣΠΟΡΟ",52))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΤΟ ΔΑΚΡΥ ΤΟΥ ΙΩΑΝΝΗ",53))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΒΟΥΚΕΦΑΛΑΣ",54))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΤΑ ΜΑΤΙΑ ΤΗΣ ΔΑΚΡΥΣΑΝ",55))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΠΕΡΙΠΑΤΟΣ ΣΤΟ ΚΑΙ",56))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΜΑΥΡΟΣ ΚΑΒΑΛΑΡΗΣ",57))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΠΡΟΑΓΓΕΛΟΣ",58))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"1999",59))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΜΥΣΤΙΚΟΣ ΔΕΙΠΝΟΣ",60))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"Η ΠΑΡΘΕΝΟΣ ΣΗΜΕΡΟΝ",61))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΕΥΛΟΓΕΙ Η ΨΥΧΗ ΜΟΥ ΤΟΝ ΚΥΡΙΟΝ",62))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΕΠΙΚΛΗΣΗ",63))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΧΙΛΙΑΕΝΝΙΑΚΟΣΙΑΕΝΕΝΗΝΤΑΕΝΝΕΑ",64))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΜΕΤΑΝΟΙΑ",65))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΑΓΓΕΛΟΙ ΜΕΤΑ ΠΟΙΜΕΝΩΝ",66))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΑΠΟΗΧΟΣ",67))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΧΡΙΣΤΟΣ ΓΕΝΝΑΤΑΙ",68))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΧΑΡΑΥΓΗ",69))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΣΑΝ ΟΝΕΙΡΟ",70))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΜΑΡΜΑΡΩΜΕΝΟΣ ΒΑΣΙΛΙΑΣ",71))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΠΟΛΥ ΓΛΥΚΙΑ",72))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΕΙΝΑΙ ΠΟΛΥ ΤΟ ΛΙΓΟ",73))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΚΥΡΙΕ ΤΩΝ ΔΥΝΑΜΕΩΝ",74))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"Σ' ΑΓΑΠΑΩ ΦΩΝΑΖΩ",75))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΠΕΤΡΙΝΑ ΧΡΟΝΙΑ",76))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΕΑΛΩ Η ΠΟΛΗ",77))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΗΘΕΛΑ",78))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΝΑ 'ΜΟΥΝΑ ΛΙΓΟ ΕΚΕΙ",79))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΠΟΙΟΣ ΜΟΥ ΜΙΛΑΕΙ",80))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΖΕΙ ΚΑΙ ΒΑΣΙΛΕΥΕΙ",81))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΘΑ 'ΡΘΕΙΣ ΣΑΝ ΑΣΤΡΑΠΗ",82))
	playlists.append((r'7 Στιγμές (Σταμάτης Σπανουδάκης)','sound files',"ΠΟΥ ΝΑ ΣΕ ΒΡΩ",83))

	#8. Σταμάτης Σπανουδάκης - Χαίρε θάλασσα
	playlists.append((r'Χαίρε θάλασσα (Σταμάτης Σπανουδάκης)','sound files',"Καινούργια σελίδα",1))
	playlists.append((r'Χαίρε θάλασσα (Σταμάτης Σπανουδάκης)','sound files',"Το Adagio Της Θάλασσας",2))
	playlists.append((r'Χαίρε θάλασσα (Σταμάτης Σπανουδάκης)','sound files',"Στου Ονείρου την Άκρη",3))
	playlists.append((r'Χαίρε θάλασσα (Σταμάτης Σπανουδάκης)','sound files',"Το Μεγάλο Ναι",4))
	playlists.append((r'Χαίρε θάλασσα (Σταμάτης Σπανουδάκης)','sound files',"Φως Του Δειλινού",5))
	playlists.append((r'Χαίρε θάλασσα (Σταμάτης Σπανουδάκης)','sound files',"Μικρού Παιδιού Ευχή",6))
	playlists.append((r'Χαίρε θάλασσα (Σταμάτης Σπανουδάκης)','sound files',"Μαρία",7))
	playlists.append((r'Χαίρε θάλασσα (Σταμάτης Σπανουδάκης)','sound files',"Κρυμμένα Σημάδια",8))
	playlists.append((r'Χαίρε θάλασσα (Σταμάτης Σπανουδάκης)','sound files',"Οι Ήρωες Κάνουν Γιορτή",9))
	playlists.append((r'Χαίρε θάλασσα (Σταμάτης Σπανουδάκης)','sound files',"Λόγος Μυστικός",10))
	playlists.append((r'Χαίρε θάλασσα (Σταμάτης Σπανουδάκης)','sound files',"Δέσποινα",11))
	playlists.append((r'Χαίρε θάλασσα (Σταμάτης Σπανουδάκης)','sound files',"Χαίρε Θάλασσα Μου",12))

	sql_2 = """SELECT `number` FROM `sound_files` WHERE `title`=?;"""

	counter = 0
	playlist_items = []
	for playlist_item in playlists:
		playlist_item = list(playlist_item)
		sound_file_title = playlist_item[2]
		cur.execute(sql_2,(sound_file_title,))
		myresult = cur.fetchall()
		for x in myresult:
			playlist_item[2] = x[0]
		conn.commit()
		playlist_item = tuple(playlist_item)
		if counter==17:
			title = r"Απολυτίκια Αγίων 111"
		elif counter==24:
			title = r"Αναστάσιμα τροπάρια 111"
		elif counter==28:
			title = r"Προσευχές 11"
		elif counter==43:
			title = r"Ύμνοι της εκκλησίας μας 11"
		elif counter==65:
			title = r"Επιλογές ΝΕΚ 11"
		elif counter==67:
			title = r"Ειρήνη - Δώρο Θεού 11"
		elif counter==150:
			title = r"7 Στιγμές (Σταμάτης Σπανουδάκης) 11"
		elif counter==162:
			title = r"Χαίρε θάλασσα (Σταμάτης Σπανουδάκης) 11"
		playlist_items.append({
			"relative_type":"sound_files",
			"relative_number":playlist_item[2],
			"position":playlist_item[3],
		})
		if counter == 17 or counter==24 or counter==28 or counter==43 or counter==65 or counter==150 or counter==162:
			sqlite3_functions.import_playlist(title,playlist_items)
			playlist_items = []
		counter += 1
		
main()