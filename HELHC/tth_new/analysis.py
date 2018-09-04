import os
import sys
import copy
import math
import heppy.framework.config as cfg
import logging
import imp
# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

sample = imp.load_source('heppylist', '/afs/cern.ch/work/h/helsens/public/FCCDicts/HELHC_heppySampleList_helhc_v01.py')

comp = cfg.Component(
    'example',
    files=["/eos/experiment/fcc/helhc/generation/DelphesEvents/helhc_v01/mgp8_pp_tth0123j_5f_hbb/events_000838653.root"]
)
