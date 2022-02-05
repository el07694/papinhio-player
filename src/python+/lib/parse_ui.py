import os
import sys
import xml.etree.ElementTree as ET
tree = ET.parse('icons.qrc')
root = tree.getroot()

image_filenames = []

for qresource in root.findall('qresource'):
	for file in qresource.findall('file'):
		filename_1 = file.text
		filename_2 = filename_1.replace("-","_")
		image_filenames.append([filename_1,filename_2])

path = os.path.abspath("")

def parse_directory(path):
	for filename in os.listdir(path):
		filepath = os.path.join(path,filename)
		is_directory = os.path.isdir(filepath)
		if is_directory == True:
			parse_directory(filepath)
		else:
			if "parse_ui" not in filepath:
				print("Opening "+filepath)
				with open(filepath, "r") as myfile:
					lines = myfile.readlines()
					counter = 0
					for line in lines:
						lines[counter].replace(":/Εικόνες αναδιόμενων παραθύρων/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Εικόνες αναδιόμενων παραθύρων/",":/rest-windows/assets/images/rest-windows/")
						lines[counter].replace(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/",":/main-window/assets/images/main-window/")
						lines[counter].replace("/Κεντρικό παράθυρο προγράμματος και αρχείο qrc (Main window and qrc)/Εικόνες προγράμματος.qrc","/icons.qrc")
						for image_filename in image_filenames:
							if image_filename[1].split("/")[-1] in line.strip():
								if "_" in image_filename[1].split("/")[-1]:
									lines[counter].replace(image_filename[1].split("/")[-1],image_filename[0].split("/")[-1])
						counter += 1

				with open(filepath, "w") as myfile:
					myfile.writelines(lines)

parse_directory(path)