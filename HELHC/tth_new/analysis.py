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

selectedComponents = [comp]

# FCChhAnalyses specific
from heppy.FCChhAnalyses.analyzers.Reader import Reader
source = cfg.Analyzer(
    Reader,

    weights='mcEventWeights',

    gen_particles='skimmedGenParticles',

    electrons='electrons',
    electronITags='electronITags',
    electronsToMC='electronsToMC',

    muons='muons',
    muonITags='muonITags',
    muonsToMC='muonsToMC',

    jets='pfjets04',
    bTags='pfbTags04',

    photons='photons',

    pfphotons='pfphotons',
    pfcharged='pfcharged',
    pfneutrals='pfneutrals',

    met='met',

)

from ROOT import gSystem
gSystem.Load("libdatamodelDict")
from EventStore import EventStore as Events
# FCChhAnalyses specific

# select isolated muons with pT > 50 GeV and relIso < 0.4
from heppy.analyzers.Selector import Selector
selected_muons = cfg.Analyzer(
    Selector,
    'selected_muons',
    output='selected_muons',
    input_objects='muons',
    filter_func=lambda ptc: ptc.pt() > 50 and ptc.iso.sumpt / ptc.pt() < 0.4
    #filter_func = lambda ptc: ptc.pt()>5

)

# select electrons with pT > 50 GeV and relIso < 0.4
selected_electrons = cfg.Analyzer(
    Selector,
    'selected_electrons',
    output='selected_electrons',
    input_objects='electrons',
    filter_func=lambda ptc: ptc.pt() > 50 and ptc.iso.sumpt / ptc.pt() < 0.4
    #filter_func = lambda ptc: ptc.pt()>5

)


from heppy.FCChhAnalyses.HELHC.tth_new.TreeProducer import SimpleTreeProducer
tree = cfg.Analyzer(
    SimpleTreeProducer,
    tree_name='events',
    tree_title='A simple test tree',
    electrons='selected_electrons',
    muons='selected_muons'
    # weights='mcEventWeights',
    # gen_particles='skimmedGenParticles',
    # electronITags='electronITags',
    # electronsToMC='electronsToMC',
    # muonITags='muonITags',
    # muonsToMC='muonsToMC',
    # jets='pfjets04',
    # bTags='pfbTags04',
    # photons='photons',
    # pfphotons='pfphotons',
    # pfcharged='pfcharged',
    # pfneutrals='pfneutrals',
    # met='met'
)

sequence = cfg.Sequence([
    source,
    selected_muons,
    selected_electrons,
    tree
])


# finalization of the configuration object.
config = cfg.Config(components=selectedComponents,
                    sequence=sequence,
                    services=[],
                    events_class=Events)


"""

from heppy.framework.services.tfile import TFileService
output_rootfile = cfg.Service(
    TFileService,
    'myhists',
    fname='histograms.root',
    option='recreate'
)

services = [output_rootfile]

# finalization of the configuration object.
config = cfg.Config( components = selectedComponents,
                     sequence = sequence,
                     services = services,
                     events_class = Events )

"""
