from __future__ import print_function
import unittest
from rdkit.Chem import AllChem
from descriptastorus import make_store, DescriptaStore
from descriptastorus.descriptors.rdDescriptors import RDKit2D

import contextlib, tempfile, os, shutil, sys
import datahook

one_smiles = "c1ccccc1 0"
many_smiles = "\n".join( [ "C"*i + "c1ccccc1 " + str(i) for i in range(10) ] )

from rdkit.Chem import Descriptors

class RDKit2DSubset(RDKit2D):
    NAME="RDKit2DSubset"
    def __init__(self):
        RDKit2D.__init__(self, properties=[
            'ExactMolWt',
            'NumAliphaticRings', 'NumAromaticCarbocycles',
            'NumAromaticHeterocycles', 'NumAromaticRings'])
RDKit2DSubset()

class TestCase(unittest.TestCase):
    def testOffByOne(self):
        try:
            fname = tempfile.mktemp()+".smi"
            storefname = tempfile.mktemp()+".store"
            print("\n\nfilename:", fname, file=sys.stderr)
            print("storefilename:", storefname, file=sys.stderr)
            with open(fname, 'w') as f:
                f.write(one_smiles)
                
            opts = make_store.MakeStorageOptions( storage=storefname, smilesfile=fname,
                                                  hasHeader=False,
                                                  batchsize=1,
                                                  smilesColumn=0, nameColumn=1,
                                                  seperator=" ", descriptors="RDKit2DSubset",
                                                  index_inchikey=True )
            make_store.make_store(opts)

            with contextlib.closing(DescriptaStore(storefname)) as store:
                self.assertEqual( store.lookupName("0"), 0)

                self.assertEqual( store.lookupInchiKey("UHOVQNZJYSORNB-UHFFFAOYSA-N"), [0])
                self.assertEqual(store.descriptors().get(0), (78.046950192, 0.0, 1.0, 0.0, 1.0))

        finally:
            if os.path.exists(fname):
                os.unlink(fname)
            if os.path.exists(storefname):
                shutil.rmtree(storefname)
                
    def testMany(self):
        try:
            fname = tempfile.mktemp()+".smi"
            storefname = tempfile.mktemp()+".store"
            with open(fname, 'w') as f:
                f.write(many_smiles)
                
            opts = make_store.MakeStorageOptions( storage=storefname, smilesfile=fname,
                                                  hasHeader=False,
                                                  smilesColumn=0, nameColumn=1,
                                                  seperator=" ", descriptors="RDKit2DSubset",
                                                  index_inchikey=True )
            make_store.make_store(opts)

            with contextlib.closing(DescriptaStore(storefname)) as store:

                for i in range(10):
                    self.assertEqual( store.lookupName(str(i)), i)

                self.assertEqual(store.descriptors().get(0), (78.046950192, 0.0, 1.0, 0.0, 1.0))
                self.assertEqual(store.descriptors().get(1), (92.062600256, 0.0, 1.0, 0.0, 1.0))
                self.assertEqual(store.descriptors().get(2), (106.07825032, 0.0, 1.0, 0.0, 1.0))
                self.assertEqual(store.descriptors().get(3), (120.093900384, 0.0, 1.0, 0.0, 1.0))
                self.assertEqual(store.descriptors().get(4), (134.109550448, 0.0, 1.0, 0.0, 1.0))
                self.assertEqual(store.descriptors().get(5), (148.125200512, 0.0, 1.0, 0.0, 1.0))
                self.assertEqual(store.descriptors().get(6), (162.140850576, 0.0, 1.0, 0.0, 1.0))
                self.assertEqual(store.descriptors().get(7), (176.15650064, 0.0, 1.0, 0.0, 1.0))
                self.assertEqual(store.descriptors().get(8), (190.172150704, 0.0, 1.0, 0.0, 1.0))
                self.assertEqual(store.descriptors().get(9), (204.187800768, 0.0, 1.0, 0.0, 1.0))                    

                for i in range(10):
                    m = store.molIndex().getRDMol(i)
                    inchi = AllChem.InchiToInchiKey(AllChem.MolToInchi(m))
                    self.assertEqual( store.lookupInchiKey(inchi), [i])


        finally:
            if os.path.exists(fname):
                os.unlink(fname)
            if os.path.exists(storefname):
                shutil.rmtree(storefname)

    def testManyNoInchi(self):
        try:
            fname = tempfile.mktemp()+".smi"
            storefname = tempfile.mktemp()+".store"
            with open(fname, 'w') as f:
                f.write(many_smiles)
                
            opts = make_store.MakeStorageOptions( storage=storefname, smilesfile=fname,
                                                  hasHeader=False,
                                                  batchsize=1,
                                                  smilesColumn=0, nameColumn=1,
                                                  seperator=" ", descriptors="RDKit2DSubset",
                                                  index_inchikey=False )
            make_store.make_store(opts)

            with contextlib.closing(DescriptaStore(storefname)) as store:
                for i in range(10):
                    self.assertEqual( store.lookupName(str(i)), i)

                self.assertEqual(store.descriptors().get(0), (78.046950192, 0.0, 1.0, 0.0, 1.0))
                self.assertEqual(store.descriptors().get(1), (92.062600256, 0.0, 1.0, 0.0, 1.0))
                self.assertEqual(store.descriptors().get(2), (106.07825032, 0.0, 1.0, 0.0, 1.0))
                self.assertEqual(store.descriptors().get(3), (120.093900384, 0.0, 1.0, 0.0, 1.0))
                self.assertEqual(store.descriptors().get(4), (134.109550448, 0.0, 1.0, 0.0, 1.0))
                self.assertEqual(store.descriptors().get(5), (148.125200512, 0.0, 1.0, 0.0, 1.0))
                self.assertEqual(store.descriptors().get(6), (162.140850576, 0.0, 1.0, 0.0, 1.0))
                self.assertEqual(store.descriptors().get(7), (176.15650064, 0.0, 1.0, 0.0, 1.0))
                self.assertEqual(store.descriptors().get(8), (190.172150704, 0.0, 1.0, 0.0, 1.0))
                self.assertEqual(store.descriptors().get(9), (204.187800768, 0.0, 1.0, 0.0, 1.0))       
                for i in range(10):
                    m = store.molIndex().getRDMol(i)


        finally:
            if os.path.exists(fname):
                os.unlink(fname)
            if os.path.exists(storefname):
                shutil.rmtree(storefname)
                

    def testContainer(self):
        try:
            fname = tempfile.mktemp()+".smi"
            storefname = tempfile.mktemp()+".store"
            with open(fname, 'w') as f:
                f.write(many_smiles)
                
            opts = make_store.MakeStorageOptions( storage=storefname, smilesfile=fname,
                                                  hasHeader=False,
                                                  smilesColumn=0, nameColumn=1,
                                                  seperator=" ", descriptors="RDKit2DSubset,RDKit2DSubset",
                                                  index_inchikey=True )
            make_store.make_store(opts)

            with contextlib.closing(DescriptaStore(storefname)) as store:

                for i in range(10):
                    self.assertEqual( store.lookupName(str(i)), i)

                for i in range(10):
                    m = store.molIndex().getRDMol(i)
                    inchi = AllChem.InchiToInchiKey(AllChem.MolToInchi(m))
                    self.assertEqual( store.lookupInchiKey(inchi), [i])
                self.assertEqual(store.descriptors().get(0), (78.046950192, 0.0, 1.0, 0.0, 1.0)*2)
                self.assertEqual(store.descriptors().get(1), (92.062600256, 0.0, 1.0, 0.0, 1.0)*2)
                self.assertEqual(store.descriptors().get(2), (106.07825032, 0.0, 1.0, 0.0, 1.0)*2)
                self.assertEqual(store.descriptors().get(3), (120.093900384, 0.0, 1.0, 0.0, 1.0)*2)
                self.assertEqual(store.descriptors().get(4), (134.109550448, 0.0, 1.0, 0.0, 1.0)*2)
                self.assertEqual(store.descriptors().get(5), (148.125200512, 0.0, 1.0, 0.0, 1.0)*2)
                self.assertEqual(store.descriptors().get(6), (162.140850576, 0.0, 1.0, 0.0, 1.0)*2)
                self.assertEqual(store.descriptors().get(7), (176.15650064, 0.0, 1.0, 0.0, 1.0)*2)
                self.assertEqual(store.descriptors().get(8), (190.172150704, 0.0, 1.0, 0.0, 1.0)*2)
                self.assertEqual(store.descriptors().get(9), (204.187800768, 0.0, 1.0, 0.0, 1.0)*2)       

        finally:
            if os.path.exists(fname):
                os.unlink(fname)
            if os.path.exists(storefname):
                shutil.rmtree(storefname)
                
