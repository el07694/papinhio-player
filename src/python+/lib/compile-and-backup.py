from datetime import datetime
from shutil import copyfile
import shutil
import subprocess
import os
import sys

import os
from distutils.dir_util import copy_tree
from datetime import datetime

import xml.etree.ElementTree as ET


# Getting the current date and time
dt = datetime.now()

# getting the timestamp
ts = datetime.timestamp(dt)

folders = os.listdir("../../..")

os.mkdir("../../../back-up/"+str(ts))


for folder in folders:
    if folder.lower() != "back-up":
        if os.path.isdir("../../../"+folder)==True:
            if "disket-box" not in folder:
                copy_tree("../../../"+folder, "../../../back-up/"+str(ts)+"/"+folder)
        else:
            shutil.copyfile("../../../"+folder, "../../../back-up/"+str(ts)+"/"+folder)

#shutil.make_archive("../../back-up/"+str(ts), 'zip', "../../back-up/"+str(ts))
#os.remove("../../back-up/"+str(ts))

ui_main_dir = os.path.abspath("../../../ui")
py_from_ui_dir = os.path.abspath("../../compiled-ui")

#2. Compile all ui files and qrc file with pyuic5 command.
def parse_directory_2(path):
    path_contents = os.listdir(path)
    if os.path.exists(path.replace(ui_main_dir,py_from_ui_dir))==False:
        os.mkdir(path.replace(ui_main_dir,py_from_ui_dir))
    for path_content in path_contents:
        if os.path.isdir(path+"/"+path_content):
            parse_directory_2(path+"/"+path_content)
        else:
            original_path = path+"/"+path_content
            extension = original_path.split(".")[-1].lower()
            if extension == "ui":
                #ui_file = open(original_path,"r+",encoding="utf-8")
                print("Edditing:"+str(original_path))

                '''
                #read input file
                fin = open(original_path, "rt")
                #read file contents to string
                data = fin.read()
                #replace all occurrences of the required string

                data = data.replace("Εικόνες προγράμματος.qrc","icons.qrc")
                data = data.replace(":/Εικόνες κεντρικού παραθύρου/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Εικόνες κεντρικού παραθύρου/",":/Εικόνες κεντρικού παραθύρου/assets/images/main-window/")
                data = data.replace(":/Εικόνες αναδιόμενων παραθύρων/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Εικόνες αναδιόμενων παραθύρων/",":/Εικόνες αναδιόμενων παραθύρων/assets/images/rest-windows/")
                data = data.replace(":/Ώρα/Εικόνες και ήχοι προγράμματος (media)/Εικόνες (images)/Ώρα/",":/Ώρα/assets/images/time/")

                for image_filename in image_filenames:
                    underscore_filename = image_filename.replace("-","_")
                    dash_filename = image_filename
                    data = data.replace(underscore_filename,dash_filename)
                
                #close the input file
                fin.close()
                #open the input file in write mode
                fin = open(original_path, "wt")
                #overrite the input file with the resulting data
                fin.write(data)
                #close the file
                fin.close()
                '''
                saved_path = original_path.replace(".ui",".py").replace(ui_main_dir,py_from_ui_dir)
                process = subprocess.Popen(["python3.9","-m","PyQt5.uic.pyuic","-x",original_path,"-o",saved_path], shell=False)   
                process.wait()

                
                #read output file
                fin = open(saved_path, "rt")
                #read file contents to string
                data = fin.read()
                #replace all occurrences of the required string

                folders = saved_path.split("/")
                folders_back = 0
                start_count = False
                for folder in folders:
                    if "compiled-ui" in folder:
                        start_count = True
                    else:
                        if start_count == True:
                            folders_back += 1

                folders_back_str = ""
                for k in range(1,folders_back):
                    folders_back_str += "../"

                replace_str = "import sys\nsys.path.append('"+folders_back_str+"')\n\nimport importlib\nicons = importlib.import_module('compiled-ui.icons')"

                data = data.replace("import icons_rc",replace_str)
                
                #close the output file
                fin.close()

                #open the output file in write mode
                fin = open(saved_path, "wt")
                #overrite the input file with the resulting data
                fin.write(data)
                #close the file
                fin.close()
                
            elif extension=="qrc":
                saved_path = original_path.replace(".qrc",".py").replace(ui_main_dir,py_from_ui_dir)
                process = subprocess.Popen(["python3.9","-m","PyQt5.pyrcc_main",original_path,"-o",saved_path],shell=False)
                process.wait()

parse_directory_2(ui_main_dir)