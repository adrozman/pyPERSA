import numpy as np
#############################
#%% facet functions
############################
def read_facet(facetfile):
    """
    Reads a .facet grid file and extracts grid coordinates and connectivity.
    Supports facet files containing triangles or quadrilaterals.

    Parameters
    ----------
    facetfile : str
        Path to the facet file to be read.

    Returns
    -------
    coordinates : numpy.ndarray
        A (npoints, 3) array of vertex coordinates (X, Y, Z).
    tri_connectivity : numpy.ndarray or None
        A (n_triangles, 3) integer array defining triangular connectivity, or None
        if no triangles are found. Indices correspond to columns in `coordinates`.
    quad_connectivity : numpy.ndarray or None
        A (n_quads, 4) integer array defining quadrilateral connectivity, or None
        if no quadrilaterals are found. Indices correspond to columns in `coordinates`.
    """
    print("--------------------------------------------------")
    print("facetReader initiated ... reading facet file")
    print("-------------------------------------------------")

    with open(facetfile, 'r') as f:
        # First line is a facet header
        f.readline()  # Skip the first line
        f.readline()  # '1'
        f.readline()  # 'Grid'
        f.readline()  # '0, 0.00 0.00 0.00 0.00'

        npoints = int(f.readline().strip())
        print(f" Found {npoints} points")

        # Allocate for coordinates
        coordinates = np.zeros((npoints, 3))

        # Read coordinates
        for i in range(npoints):
            coordinates[i] = list(map(float, f.readline().split()))

        ncelltypes = int(f.readline().strip())

        # connectivity = []
        # # Reading cell types
        # for i in range(ncelltypes):
        #     f.readline()  # 'Quadrilaterals' or 'Triangles'
        #     ncells, nedgescell = map(int, f.readline().split())
        #     print(f" Found {ncells} {nedgescell}-sided cells")
        #     for j in range(ncells):
        #         corners = list(map(int, f.readline().split()))[:nedgescell]
        #         connectivity.append(corners)

        tri_connectivity  = None
        quad_connectivity = None
        for i in range(ncelltypes):
            f.readline()  # 'Quadrilaterals' or 'Triangles'
            ncells, nedgescell = map(int, f.readline().split())
            # print(f" Found {ncells} {nedgescell}-sided cells")

            if nedgescell == 3:
                print(f" Found {ncells} triangles")

                tri_connectivity = np.zeros((ncells,nedgescell), dtype=int)
                for j in range(ncells):
                    tri_connectivity[j] = list(map(int, f.readline().split()))[:nedgescell]


            elif nedgescell == 4:
                print(f" Found {ncells} quadrilaterals")

                quad_connectivity = np.zeros((ncells,nedgescell), dtype=int)
                for j in range(ncells):
                    quad_connectivity[j] = list(map(int, f.readline().split()))[:nedgescell]

            else:
                print(" Sorry, only Quads or Tris are currently supported by facetReader.py")
                print(" Stopping...")
                return

    print("Successfully Read User Facet File")
    print("--------------------------------------------------------")

    return coordinates, tri_connectivity, quad_connectivity

# read points from facet file & calculate normals
def process_facet(filename, conversion = 1):
    """
    Reads a facet file, optionally scales, and computes vertex normal vectors.

    Parameters
    ----------
    filename : str
        Path to the facet file to be processed.
    conversion : float, optional
        Scaling factor multiplied to all coordinates (e.g., 0.0254 for in to m).
        PSU-WOPWOP requires inputs in meters.

    Returns
    -------
    coordinates : numpy.ndarray
        A (npoints, 3) array of scaled vertex coordinates (X,Y,Z).
    normals : numpy.ndarray
        A (npoints, 3) array of computed unit normal vectors at each vertex.
    tri_connectivity : numpy.ndarray or None
        A (n_triangles, 3) integer array defining triangular connectivity, or None
        if no triangles are found. Indices correspond to columns in `coordinates`.
    quad_connectivity : numpy.ndarray or None
        A (n_quads, 4) integer array defining quadrilateral connectivity, or None
        if no quadrilaterals are found. Indices correspond to columns in `coordinates`.

    Raises
    ------
    Exception
        If a face has a zero-magnitude normal (i.e., degenerate geometry).
    """
    xyz, tri_connectivity, quad_connectivity = read_facet(filename)

    xyz *= conversion

    normals = np.zeros((xyz.shape[1], 3))

    if tri_connectivity is not None:
        nnode_face = 3
        for i in range(tri_connectivity.shape[1]):
            r1 = xyz[tri_connectivity[0,i]-1] # subtract 1 because connectivity
            r2 = xyz[tri_connectivity[1,i]-1] # indices start at 1 and python
            r3 = xyz[tri_connectivity[2,i]-1] # indices start at 0

            v1 = r2 - r1
            v2 = r3 - r1

            vcross = np.cross(v1, v2)

            if np.linalg.norm(vcross) == 0:
                raise Exception("Face {i} has a zero-magnitude normal!")

            for j in range(nnode_face):
                normals[tri_connectivity[i,j]-1] = normals[tri_connectivity[i,j]-1] + \
                    0.5*vcross/nnode_face

    elif quad_connectivity is not None:
        nnode_face = 4
        for i in range(quad_connectivity.shape[1]):
            r1 = xyz[quad_connectivity[0,i]-1]
            r2 = xyz[quad_connectivity[1,i]-1]
            r3 = xyz[quad_connectivity[2,i]-1]
            r4 = xyz[quad_connectivity[3,i]-1]

            v1 = r3 - r1
            v2 = r4 - r2

            vcross = np.cross(v1, v2)

            if np.linalg.norm(vcross) == 0:
                raise Exception("Face {i} has a zero-magnitude normal!")

            for j in range(nnode_face):
                normals[quad_connectivity[i,j]-1] = normals[quad_connectivity[i,j]-1] + \
                    0.5*vcross/nnode_face

    return coordinates, normals, tri_connectivity, quad_connectivity
