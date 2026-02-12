"""
Helios Extracts to PSU-WOPWOP Converter

Modify helios_grid_to_meter corresponding to your .facet file units. Modify facet_folder
to point to a folder containing the .facet files that the extracts tap files  were
created from. Run this code inside the main helios directory. It will create a directory 
"wopwop_input_files" with subdirectories for each extract name, where the geometry and 
loading wopwop input files will be written.

This code uses the pyPERSA module to read facet and tap files, and pywopwop to write in 
PSU-WOPWOP input format. High-level processes are exposed and can be modified for your 
application.

Calling the module functions, python buffers the output by default. To monitor the print
outputs of the code more closely, run with the unbuffered flag as "python -u convert_taps.py"
or set the environment variable PYTHONUNBUFFERED=1
"""

import numpy as np
import re
from pyPERSA import process_facet
from pyPERSA import read_taps as tp # functions to read Helios extracts tap files
import pywopwop as PWW # functions to write data to wopwop input format
import os

###############################################
#%% Inputs
###############################################

# multiplier to convert facet grid to meters for WOPWOP - this is inches to meters
helios_grid_to_meter = 0.0254

# path to the .facet files that the tap files were created from. We need to 
# read them again to calculate the output surface connectivity
facet_folder = "../perm/perm_surface/facetfiles/"

# read tap_extracts to determine with tap corresponds to which surface name
with open("extracts/tap_extracts.py") as f:
    # Extracts content of all open('extracts/*.txt')
    tapnames = re.findall(r"open\('(extracts/.*?\.txt)'\)", f.read())

# remove extracts folder prefix and file extension, get to list of [extractname0.txt...extractnameN.txt]
tapnames = [tapname.split("/")[-1].split(".")[0] for tapname in tapnames] 

#####################################
#%% Working Code
####################################

# write the input files to their own directories which we can run wopwop from
os.makedirs("wopwop_input_files",exist_ok=True)

for i, name in enumerate(tapnames):

    # define paths
    facetfile = facet_folder + name + ".facet"
    tapfile = "extracts/tap_" + f"{i:02}.bin"
    geometry_output_file="wopwop_input_files/" +name+ f"/{name}_Geometry.dat"
    loading_output_file="wopwop_input_files/" +name+ f"/{name}_Leometry.dat"
    
    os.makedirs("wopwop_input_files/"+name,exist_ok=True)

    # get surface connectivity from facet file
    xyz, normals, tri_connectivity, quad_connectivity = process_facet(facetfile, conversion = helios_grid_to_meter)

    # Settings for read_taps submodule
    tp.stationary = True    	# this tells to save XYZ at first timestep only
    tp.setrefs()            	# this requires inputs.py to be in same folder to get reference values
    print("reading tap file " + tapfile)
    tp.set_and_read(tapfile) 
    tp.set_fields(["Density", "XMomentum", "YMomentum", "ZMomentum", "Pressure"])
   
    # Load tap data
    v = tp.load_fields(itstart=1, ntime=-1)

    v['Pressure'] = v['Pressure'] - tp.ref['pinf']  # subtract pinf from taps
    v['T'] = v['T'] - v['T'][0]     # set first time value to 0 (optional but convenient for PSU-WOPWOP)
    print(f"data is {v['T'][-1]} seconds long.")

    # reshape field data v into (nt, 5, nPoints) array
    loading_data = np.stack((v['Density'],v['XMomentum'],v['YMomentum'],\
                              v['ZMomentum'],v['Pressure']), axis=1)

    #################################
    #%% initialize PWWPatch instance
    #################################
    myWopwopData = PWW.PWWPatch()

    # add general header info
    myWopwopData.is_structured = False
    myWopwopData.centered_type = 'node'
    myWopwopData.float_type = 'single'
    myWopwopData.has_iblank = False
    myWopwopData.set_units_string('Pa')

    # add geometry info
    myWopwopData.geometry_type = 'geometry'
    myWopwopData.geometry_time_type = 'constant'
    myWopwopData.set_geometry_comment('Unstructured file - patch')

    # add loading info
    myWopwopData.loading_time_type = 'aperiodic'
    myWopwopData.loading_data_type = 'flow_params'	# flow_params is permeable
    myWopwopData.loading_ref_frame = 'ground_fixed'
    myWopwopData.set_loading_comment('Unstructured file - loading')

    myWopwopData.add_UnstructuredZone(name, xyz, normals, \
                quad_connectivity=quad_connectivity, \
                loading_data=loading_data, time_steps=v['T'])

    # this prints an overview of geometry/loading inputted, and what will be written.
    myWopwopData.print_info(zones_info=True)    

    # write to wopwop input format in the created tap name subdirectories
    myWopwopData.write_geometry_file(geometry_output_file)
    myWopwopData.write_loading_file(loading_output_file)
