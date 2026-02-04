"""
These functions are taken from Dylan Jude's readTaps code distributed with Helios.
Reads tap files of field variables and converts to useful values.
See example file for usage
"""

import numpy as np
import sys
import pickle

taps_file  = None
ref        = None
fields     = ["Density", "XMomentum"]
stationary = False

allfields = {}
allfields["Density"]           = lambda q: q[:,:,0]
allfields["XMomentum"]         = lambda q: q[:,:,1]
allfields["YMomentum"]         = lambda q: q[:,:,2]
allfields["ZMomentum"]         = lambda q: q[:,:,3]
allfields["Pressure"]          = lambda q: (ref['gamma']-1)*(q[:,:,4]-0.5*(q[:,:,1]**2 + q[:,:,2]**2 + q[:,:,3]**2)/q[:,:,0])


def tapinfo(taps_file):
    fsize,dsize,isize,csize=4,8,4,1 # float size
    with open(taps_file, mode='rb') as f: 
        bindata  = f.read(2*isize)
        nq, npts = np.ndarray((2), dtype=np.intc, buffer=bindata, offset=0)
        f.seek(0)
        nt=0
        entrysize = 2*isize + dsize + 3*npts*dsize + nq*npts*dsize
        end = f.seek(0,2) # end of file
        nt = int(end/entrysize)
    return nt,npts,nq

def readtaps(taps_file,itstart=0,ntime=-1):
    
    print("--------------------------------------------------")
    print("readTaps_perm.py initiated ... reading .bin file")
    print("-------------------------------------------------")
    
    global stationary
    nt,npts,nq = tapinfo(taps_file)
    # print(nt,npts,nq)
    if(ntime==-1):
        ntime = nt
    fsize,dsize,isize,csize=4,8,4,1 # float size
    entrysize = 2*isize + dsize + 3*npts*dsize + nq*npts*dsize
    with open(taps_file, mode='rb') as f: 
        f.seek(itstart*entrysize)
        readsize = np.int64(ntime)*np.int64(entrysize)
        print("  readsize is " + str(readsize) + " bytes")
        bindata = f.read(readsize)
    print("  bindata read successful.")
    size = np.ndarray((-1), dtype=np.byte, buffer=bindata, offset=0).size # size of whole dataset
    loc,q,x,t = np.int64(0),[],[],[]
    
    print(f"  readTaps found {npts} points.")
    print(f"  readTaps found {nt} timesteps.")
    
    while(loc < size):
        nq, npts = np.ndarray((2),       dtype=np.intc,   buffer=bindata, offset=loc)
        loc     += 2*isize
        time     = np.ndarray((1),        dtype=np.double, buffer=bindata, offset=loc)
        loc     += dsize
        xx       = np.ndarray((npts,3), dtype=np.double, buffer=bindata, offset=loc)
        loc     += 3*npts*dsize
        qq       = np.ndarray((npts,nq), dtype=np.double, buffer=bindata, offset=loc)
        loc     += nq*npts*dsize
        t.append(time[0])
        q.append(qq)
        
        if stationary:
            if len(x) == 0:
                x = np.squeeze(xx)
        else:
            x.append(xx)
    
    if not stationary:
        x = np.array(x)
    
    q = np.array(q)
    t = np.array(t)
    return t,x,q

def set_and_read(tapfile):
    global taps_file
    try:
        nt,npts,nq = tapinfo(tapfile)
        taps_file  = tapfile
        return ""
    except:
        return "could not read: "+str(tapfile) 

def setrefs():
    global ref
    ref = {}
    try:
        from inputs import referenceValues
        rv = referenceValues()
        for k in ['gamma','rgas','rinf','pinf','tinf','ainf','refMach']:
            ref[k] = getattr(rv,k)
    except:
        ref = None
        quit("Could not find or read inputs.py file")
              
def convert_to_pickle(outfile):
    t,x,q = readtaps(taps_file)
    v = {"XYZ":x,"T":t}
    for field in fields:
        v[field] = allfields[field](q)
    with open(outfile, 'wb') as f:
        pickle.dump(v, f);
    return ""

def load_fields(itstart = 0, ntime=-1):
    t,x,q = readtaps(taps_file, itstart=itstart, ntime=ntime)
    v = {"XYZ":x,"T":t}
    for field in fields:
        v[field] = allfields[field](q)
    return v

def set_fields(newfields):
    global fields
    # newfields = newfields.split(',')
    # newfields = [f.strip() for f in newfields]
    fields = []
    for field in newfields:
        if not field in allfields.keys():
            return "Did not recognize: "+str(field)
        else:
            fields.append(field)
    return ""
