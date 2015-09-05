#!/usr/bin/env python

import os
import sys

import ase.io
from ase.calculators.gaussian import Gaussian

from ipi.interfaces.sockets import ClientASE


# get command-line arguments
try:
    nthreads = int(sys.argv[1])
    dir_calc = sys.argv[2]
except IndexError:
    print 'command line arguments: <number of Gaussian threads> <calculator directory name>'
    sys.exit(1)


# print some info
print 'Gaussian ASE i-PI socket runner'
print '-------------------------------'
print
print '   number of threads: {:d}'.format(nthreads)
print 'calculator directory: {:s}'.format(dir_calc)
print

# fast scratch directory for Gaussian
os.environ['GAUSS_SCRDIR'] = '/dev/shm'

# create ASE atoms and calculator
atoms = ase.io.read('W2-MP2-6311ppGss.xyz')
atoms.set_calculator(
    Gaussian(
        xc = 'MP2',
        # Note that 6-31G is for faster testing only, not a good basis set
        # for gas-phase W2. Use the bigger one instead.
        basis = '6-31G',
        #basis = '6-311++G**',
        nproc = nthreads,
        label = dir_calc + '/calculator'
    )
)

# create the socket client and run it
client = ClientASE(atoms, verbose=True, address='ase')
#client = ClientASE(atoms, verbose=True, mode='inet', address='localhost', port=12345)
client.run()
