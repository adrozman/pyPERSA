"""
Utility for PSU-WOPWOP Case Setup

Create a PSU-WOPWOP namelist input file in the 'wopwop_input_files' directory
created by 'convert_taps.py'. This folder should contain the subfolders with
geometry and loading files for each permeable surface generated. Change the
'namelist_file' variable below to the name of your namelist file e.g. 
"wopwop.nam".

Run this code in the 'wopwop_input_files' directory to copy the namelist file
into each folder and create a 'cases.nam' pointing WOPWOP to the permeable 
surface folders. After running this code, the directories should be set up to
run WOPWOP to obtain the far-field noise for each surface.
"""
import os

###########################
# INPUT
###########################
namelist_file="wopwop.nam"

# get a list of all the folders in this directory, considering each one to 
# contain permeable surface inputs
case_folders = [ f.path for f in os.scandir(".") if f.is_dir() ]

print("cases: ", case_folders)


# copy wopwop.nam to all folders
for case_folder in case_folders:
    os.system(f"cp {namelist_file} " + case_folder)

# write "cases.nam" file pointing WOPWOP to all of the case folders
with open("cases.nam", "w") as f:
    for case_folder in case_folders:
        f.write("&caseName\n")
        f.write("globalFolderName='"+case_folder+"/'\n")
        f.write(f"caseNameFile='{namelist_file}'\n")
        f.write("/\n")
