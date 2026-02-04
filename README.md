# pyPERSA

Module that converts tap files from CFD to permeable surface inputs for PSU-WOPWOP

## 📦 Installation Instructions

Clone the directory then install using `pip` 

```bash
git clone https://github.com/adrozman/pyPERSA.git
cd pyPERSA
pip install .
```

## Complete installation instructions for NAS computer
```bash
module load python3/3.11.5
virtualenv --system-site-packages ~/persa
source ~/persa/bin/activate
git clone https://github.com/adrozman/pyPERSA.git
cd pyPERSA
pip install .
```

To use on future logins, activate the virtualenv:
```
source ~/persa/bin/activate
