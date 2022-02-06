import os
import sys

root_folder = "../../src/"
hidden_imports = []

def parse_path(path):
    path_contents = os.listdir(path)
    for path_content in path_contents:
        if "__pycache__" not in path_content:
            if os.path.isdir(path+"/"+path_content):
                h_import = path+"/"+path_content
                h_import = h_import.replace(root_folder,"").replace("/",".")
                
                hidden_imports.append(h_import[1:])
                parse_path(path+"/"+path_content)
            else:
                extension = path_content.split(".")[-1].lower()
                if extension == "py":
                    h_import = path+"/"+path_content
                    h_import = h_import.replace(root_folder,"").replace(".py","").replace("/",".")
                
                    hidden_imports.append(h_import[1:])

parse_path(root_folder)


hidden_imports.append("main-window")
hidden_imports.append("compiled-ui")
hidden_imports.append("compiled-ui.main-window")
hidden_imports.append("compiled-ui.main-window.papinhio-player")
hidden_imports.append("main-window.icons")




hidden_imports = str(hidden_imports)

fin = open("Papinhio player.spec", "rt")
lines = fin.readlines()
fin.close()

output_file = ""
for line in lines:
    if "hiddenimports" in line:
        split_line = line.split("hiddenimports")
        output_file += str(split_line[0])+"hiddenimports="+hidden_imports+",\n"
    else:
        output_file += line

fin = open("Papinhio player.spec", "wt")
fin.write(output_file)
fin.close()