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


# apply jet flavour tagging
from heppy.FCChhAnalyses.analyzers.FlavourTagger import FlavourTagger
pfjets04_pdg = cfg.Analyzer(
    FlavourTagger,
    'pfjets04_pdg',
    input_jets='pfjets04',
    input_genparticles='gen_particles',
    output_jets='pfjets04_pdg',
    dr_match=0.4,
    pdg_tags=[5, 4, 0],
    ptr_min=0.1,
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
    pfjets04_pdg,
    # selected_electrons,
    tree
])


# finalization of the configuration object.
config = cfg.Config(components=selectedComponents,
                    sequence=sequence,
                    services=[],
                    events_class=Events)
