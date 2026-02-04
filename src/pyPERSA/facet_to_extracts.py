"""
@author: admro
"""

import numpy as np
import os

def write_extract_points(Coordinates, tap_write_dir = 'Taps', tapname="Tap"):        
    """
    Writes an array of coordinates to a text file formatted for Helios extracts module

    Parameters
    ----------
    Coordinates : array_like
        An array of shape (N, 3) containing X, Y, Z coordinates.
    tap_write_dir : str, optional
        The directory path where the file will be saved. Defaults to 'Taps'.
    tapname : str, optional
        The base name of the file (without extension). Defaults to "Tap".
    """
    os.makedirs(tap_write_dir, exist_ok=True)
    tapfilestring = f"{tap_write_dir}/{tapname}.txt"

    print(Coordinates.shape)
    
    np.savetxt(tapfilestring, Coordinates, fmt='%.7f', delimiter=' ')

    print("-----------------------------------------------------")
    print(f"wrote {tapname} to {tap_write_dir}")
            
def write_extracts_py(tapnames, frequency=1):
    """
    Generates the Python script 'tap_extracts.py' necessary for Helios extracts module 
    using the list of tap names and extract frequency.

    Parameters
    ----------
    tapnames : list of str
        A list of filenames corresponding to the tap files stored in the 'extracts/' directory.
    frequency : int, optional
        The sampling frequency for the extraction. Defaults to 1.
    """
    ntapfiles = len(tapnames)
    with open('tap_extracts.py', 'w') as f:

        f.write('class tap_extracts:\n')
        f.write('    nslices=0\n')
        f.write(f'    ntaps={ntapfiles}\n')

        for i in range(ntapfiles):
            f.write(f'    class tap{i}:\n')
            f.write(f'        frequency={frequency}\n')
            
            f.write(f"        x = [[float(a) for a in b.split()] for b in open('extracts/{tapnames[i]}').readlines()]\n")
            f.write('        bodyID = 2\n')
        
        print("-----------------------------------------------------")
        print(f"wrote tap_extracts.py file for {ntapfiles} tap files")
        
def rotate(Coordinates, axis, angle=-90):
    """
    Rotates a set of 3D coordinates around a primary axis (x, y, or z). This may be useful
    if taps are defined in a different coordinate frame than desired out of Helios.

    Parameters
    ----------
    Coordinates : numpy.ndarray
        An (N, 3) array of 3D coordinates to be rotated.
    axis : {'x', 'y', 'z'}
        The axis about which to rotate the coordinates.
    angle : float
        The angle of rotation in degrees. Defaults to -90.

    Returns
    -------
    numpy.ndarray or None
        An (N, 3) array of rotated coordinates.
    """
    radians = np.deg2rad(angle)
    
    if axis == 'x':
        R_x = np.array([[1, 0, 0],
                    [0, np.cos(radians), -np.sin(radians)],
                    [0, np.sin(radians), np.cos(radians)]])
    elif axis == 'y':
        R_x = np.array([[np.cos(radians), 0, np.sin(radians)],
                    [0, 1, 0],
                    [-np.sin(radians), 0, np.cos(radians)]])
                        
    elif axis == 'z':
        R_x = np.array([[np.cos(radians), -np.sin(radians), 0],
                    [np.sin(radians), np.cos(radians), 0],
                    [0, 0, 1]])
        
    else:
        print('not valid axis')
        return
    
    print(f"rotated {angle} degrees about {axis}")
    return np.dot(xyz, R_x.T)
