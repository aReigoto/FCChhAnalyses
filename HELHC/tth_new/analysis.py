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
    met='met',

    electrons='electrons',
    electronITags='electronITags',
    electronsToMC='electronsToMC',

    muons='muons',
    muonITags='muonITags',
    muonsToMC='muonsToMC',

    # main jets trk02
    trkjets02='trkjets02',
    trkbTags02='trkbTags02',

    trkjetsOneSubJettiness02='trkjetsOneSubJettiness02',
    trkjetsTwoSubJettiness02='trkjetsTwoSubJettiness02',
    trkjetsThreeSubJettiness02='trkjetsThreeSubJettiness02',
    trksubjetsSoftDropTagged02='trksubjetsSoftDropTagged02',
    trksubjetsSoftDrop02='trksubjetsSoftDrop02',
    #
    trksubjetsSoftDropTagged04='trksubjetsSoftDropTagged04',
    trksubjetsSoftDrop04='trksubjetsSoftDrop04',
    trksubjetsSoftDropTagged08='trksubjetsSoftDropTagged08',
    trksubjetsSoftDrop08='trksubjetsSoftDrop08',

    # pf jets pf02 for correction
    pfjets02='pfjets02',
    pfbTags02='pfbTags02',

    pfjetsOneSubJettiness02='pfjetsOneSubJettiness02',
    pfjetsTwoSubJettiness02='pfjetsTwoSubJettiness02',
    pfjetsThreeSubJettiness02='pfjetsThreeSubJettiness02',
    pfsubjetsSoftDropTagged02='pfsubjetsSoftDropTagged02',
    pfsubjetsSoftDrop02='pfsubjetsSoftDrop02',


    # used for b-tagging
    pfjets04='pfjets04',
    pfbTags04='pfbTags04',
    pfjetsFlavor04='pfjetsFlavor04',

    # used for mreco
    pfjets08='pfjets08',
    pfbTags08='pfbTags08',

    trkjets04='trkjets04',
    trkjets08='trkjets08',

    photons='photons',
    pfphotons='pfphotons',

    pfcharged='pfcharged',
    pfneutrals='pfneutrals',



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

    # Raw Variables

    weights='weights',
    gen_particles='gen_particles',
    met='met',
    electrons='electrons',
    electronITags='electronITags',
    electronsToMC='electronsToMC',
    muons='muons',
    muonITags='muonITags',
    muonsToMC='muonsToMC',
    trkjets02='trkjets02',
    trkbTags02='trkbTags02',
    trkjetsOneSubJettiness02='trkjetsOneSubJettiness02',
    trkjetsTwoSubJettiness02='trkjetsTwoSubJettiness02',
    trkjetsThreeSubJettiness02='trkjetsThreeSubJettiness02',
    trksubjetsSoftDropTagged02='trksubjetsSoftDropTagged02',
    trksubjetsSoftDrop02='trksubjetsSoftDrop02',
    trksubjetsSoftDropTagged04='trksubjetsSoftDropTagged04',
    trksubjetsSoftDrop04='trksubjetsSoftDrop04',
    trksubjetsSoftDropTagged08='trksubjetsSoftDropTagged08',
    trksubjetsSoftDrop08='trksubjetsSoftDrop08',
    pfjets02='pfjets02',
    pfbTags02='pfbTags02',
    pfjetsOneSubJettiness02='pfjetsOneSubJettiness02',
    pfjetsTwoSubJettiness02='pfjetsTwoSubJettiness02',
    pfjetsThreeSubJettiness02='pfjetsThreeSubJettiness02',
    pfsubjetsSoftDropTagged02='pfsubjetsSoftDropTagged02',
    pfsubjetsSoftDrop02='pfsubjetsSoftDrop02',
    pfjets04='pfjets04',
    pfbTags04='pfbTags04',
    pfjetsFlavor04='pfjetsFlavor04',
    pfjets08='pfjets08',
    pfbTags08='pfbTags08',
    trkjets04='trkjets04',
    trkjets08='trkjets08',
    photons='photons',
    pfphotons='pfphotons',
    pfcharged='pfcharged',
    pfneutrals='pfneutrals'


)

sequence = cfg.Sequence([
    source,
    # selected_muons,
    # selected_electrons,
    tree
])


# finalization of the configuration object.
config = cfg.Config(components=selectedComponents,
                    sequence=sequence,
                    services=[],
                    events_class=Events)
