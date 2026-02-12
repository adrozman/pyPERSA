# pyPERSA

Module that converts tap files from CFD to permeable surface input files for PSU-WOPWOP

## 📦 Installation Instructions

Clone the directory then install using `pip` 

```bash
git clone https://github.com/adrozman/pyPERSA.git
cd pyPERSA
pip install .
```

## Complete installation instructions using Python venv
```bash
module load python3
python3 -m venv --system-site-packages ~/persa
source ~/persa/bin/activate
git clone https://github.com/adrozman/pyPERSA.git
cd pyPERSA
pip install .
```

To use on future logins, activate the virtualenv:
```
source ~/persa/bin/activate
```

## Complete installation instructions using Miniforge/Miniconda
```bash
module load miniforge
conda create -n persa numpy python=3.11
conda activate persa
git clone https://github.com/adrozman/pyPERSA.git
cd pyPERSA
pip install .
```

To use on future logins, activate the environment:
```
conda activate persa
```

## Usage Overview
- Create facet files for each part of your permeable surface. Facet files can contain multiple faces if combining their singnal is desired. Faces like endcaps that need to be separated should be written to separate facet files. Make sure the surface normals are correctly oriented outward. I create surfaces using Pointwise.
- Copy and modify ```examples/create_taps.py``` following the instructions in the header. Run ```python create_taps.py``` to create the extract files for the coordinates in the provided facet files.
- Move the generated extracts folder into the Helios run directory and run Helios. The extracts module will save data at the specified tap locations in files named ```tap_00.bin``` ... ```tap_NN.bin``` according to the order in ```tap_extracts.py```.
- Copy and modify ```examples/convert_taps.py``` following the instructions in the header. Run ```python convert_taps.py``` in the main case Helios directory to convert the saved tap files to PSU-WOPWOP input format. This code will create a folder named ```wopwop_input_files``` containing a separate subdirectory for each of the WOPWOP inputs.
- Set up WOPWOP input decks using the generated input files and run WOPWOP to obtain your permeable FW-H solution at desired observer locations. Combine signals from different faces as desired.
