# import functions to read facets, write them in format for Helios extracts module
from pyPERSA import read_facet, write_extract_points, write_extracts_py

patch_folder = '.'
tap_write_dir= 'taps'

patches = [f for f in os.listdir(patch_folder) if f.endswith('.facet')]
tapnames = []

for patch in patches:
    xyz = read_facet(os.path.join(patch_folder, patch))

    # transform XYZ from CFD frame to wing frame.
#    xyz = rotate(xyz, 'z', angle=-90)
#    xyz = rotate(xyz, 'y', angle=-90)
#    xyz[:,0] += 29.25
#    xyz[:,1] += -13.506

    write_extract_points(xyz, tap_write_dir=tap_write_dir, tapname=patch.split('.')[0])

    tapnames.append(patch.replace('.facet','.txt'))

# write tap_extracts.py file for all tap files just written.
#%%
write_extracts_py(tapnames, frequency=6)
