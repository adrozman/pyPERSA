# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 18:52:27 2024

@author: admro
"""

import numpy as np

from pyPERSA import process_facet
from pyPERSA import read_taps as tp # functions to read Helios extracts tap files
from pyPERSA import pywopwop as PWW # functions to write data to wopwop input format

###################################
#%% INPUTS - FACET FILE & BIN FILE
##################################        
tapfile = 'tap_48.bin'
facetfile = 'facets_propF/front.facet'
name = 'Front'
helios_grid_to_meter = 0.0254  # multiplier to convert grid to meters for WOPWOP - this is inches to meters

#####################################
#%% Working Code
####################################
xyz, normals, tri_connectivity, quad_connectivity = process_facet(facetfile, conversion = helios_grid_to_meter)

# Settings for readTaps code
tp.stationary = True    	# this tells to save XYZ at first timestep only
tp.setrefs()            	# this requires inputs.py to be in same folder to get reference values
tp.set_and_read(tapfile) 
tp.set_fields(["Density", "XMomentum", "YMomentum", "ZMomentum", "Pressure"])

v = tp.load_fields(itstart=1, ntime=-1) # dictionary with tap data

v['Pressure'] = v['Pressure'] - tp.ref['pinf']  # subtract pinf from taps
v['T'] = v['T'] - v['T'][0]     # set first time value to 0 (optional but convenient for PSU-WOPWOP)
print(f"data is {v['T'][-1]} seconds long.")

# reshape field data v into (nt, 5, nPoints)
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

# this gives overview of geometry/loading inputted, and what will be written.
myWopwopData.print_info(zones_info=True)    

#%% write to output files
myWopwopData.write_geometry_file(f"{name}_Geometry.dat")
myWopwopData.write_loading_file(f"{name}_Loading.dat")
