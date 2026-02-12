"""
Facet Files to Helios Extracts Converter

Modify facet_folder to the folder containing the .facet files for your permeable
surfaces. Order does not matter; each surface is treated completely separately.
Modify reference to the helios coordinate frame to attach the taps. If unsure,
set up the sensors in higen to the desired coordinate frame or body, write the input 
files, and see the bodyID or frameID generated.

This code will generate an extracts folder, a tap file for each .facet file in 
the target directory, and a tap_extracts.py setting up the extracts interface 
for Helios. Move this "extracts" folder to the main the Helios run directory and
it will automatically save data at these taps when run.

This code uses the pyPERSA module to read facets and write them in format for the 
Helios extracts module
"""

from pyPERSA import read_facet, write_extract_points, write_extracts_py
import os

facet_folder = 'facetfiles'
reference="frameID=-2"
frequency=6
tap_write_dir= 'extracts'

facet_files = [f for f in os.listdir(facet_folder) if f.endswith('.facet')]
print("converting facet files: ", facet_files)

os.makedirs(tap_write_dir, exist_ok=True)

# read each file, write xyz coordinates as 3 column list, add its name to tapnames list
tapnames = []
for facet_file in facet_files:
    xyz, _, _ = read_facet(os.path.join(facet_folder, facet_file))

    # write the tap file
    write_extract_points(xyz, tap_write_dir=tap_write_dir, tapname=facet_file.split('.')[0])

    # add name to list for tap_extracts.py
    tapnames.append(facet_file.replace('.facet','.txt'))

# write tap_extracts.py file to point to the tap files just written.
write_extracts_py(tapnames, reference=reference, frequency=frequency)
# move the generated file into the folder with the taps
os.system("mv tap_extracts.py " + tap_write_dir)
