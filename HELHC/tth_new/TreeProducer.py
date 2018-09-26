from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from heppy.analyzers.ntuple import *
from numpy import sign
from ROOT import TFile, TLorentzVector


class SimpleTreeProducer(Analyzer):
    '''Test analyzer creating a simple root tree.

    Example::

        tree = cfg.Analyzer(
          SimpleTreeProducer,
          tree_name = 'events',
          tree_title = 'A simple test tree'
        )

    The TTree is written to the file C{simple_tree.root} in the analyzer directory.

    @param tree_name: Name of the tree (Key in the output root file).
    @param tree_title: Title of the tree.




    from heppy.test.simple_example_cfg import *

    from ROOT import TFile

    files=["/eos/experiment/fcc/helhc/generation/DelphesEvents/helhc_v01/mgp8_pp_tth0123j_5f_hbb/events_000838653.root"]

    f = TFile.Open(files[0], "read")

    t = f.Get("events")

    for i in t.GetListOfLeaves():
        print i.GetName()


    '''

    def __init__(self):
        super(SimpleTreeProducer, self).__init__()
        self.raw_vars_to_save = list()
        self.raw_vars_to_save.append({'particles_name': 'pfjets04', 'save_name': 'pfjets04_', 'max_number': 6})

    def beginLoop(self, setup):
        super(SimpleTreeProducer, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'simple_tree.root']),
                              'recreate')
        self.tree = Tree(self.cfg_ana.tree_name,
                         self.cfg_ana.tree_title)
        #self.tree = Tree('events', '')
        # Names of vars must be availebel from
        # from EventStore import EventStore as Events
        # EventStore
        self.tree.var('weights', float)

        bookMet(self.tree, 'met')

        for i in range(6):
            bookParticle(self.tree, 'electron_{}'.format(i))
        #bookParticle(self.tree, 'electron_0')
        #bookParticle(self.tree, 'electron_1')
        #bookParticle(self.tree, 'electron_2')
        #bookParticle(self.tree, 'electron_3')
        #bookParticle(self.tree, 'electron_4')
        #bookParticle(self.tree, 'electron_5')

        for i in range(6):
            bookParticle(self.tree, 'muon_{}'.format(i))
        #bookParticle(self.tree, 'muon_0')
        #bookParticle(self.tree, 'muon_1')
        #bookParticle(self.tree, 'muon_2')
        #bookParticle(self.tree, 'muon_3')
        #bookParticle(self.tree, 'muon_4')
        #bookParticle(self.tree, 'muon_5')

        for i in range(6):
            bookParticle(self.tree, 'pfjets04_{}'.format(i))
        #bookParticle(self.tree, 'pfjets04_0')
        #bookParticle(self.tree, 'pfjets04_1')
        #bookParticle(self.tree, 'pfjets04_2')
        #bookParticle(self.tree, 'pfjets04_3')
        #bookParticle(self.tree, 'pfjets04_4')
        #bookParticle(self.tree, 'pfjets04_5')

    def fill_particles_by_index(self, max_number=None, particles=None, particle_name=None):
        for index, particle in enumerate(particles):
            if index == max_number:
                break
            fillParticle(self.tree, '{}{}'.format(particle_name, index), particle)

    def fill_particles_by_index2(self, event, max_number=None, particles_name=None, save_name=None):
        event_particles = getattr(event, eval('self.cfg_ana.{}'.format(particles_name)))
        for index, particle in enumerate(event_particles):
            if index == max_number:
                break
            fillParticle(self.tree, '{}{}'.format(save_name, index), particle)

    def process(self, event):
        '''Process the event.

        The input data must contain a variable called "var1",
        which is the case of the L{test tree<heppy.utils.testtree>}.

        The event must contain:
         - var_random, which is the case if the L{RandomAnalyzer<heppy.analyzers.examples.simple.RandomAnalyzer.RandomAnalyzer>}
         has processed the event.

        '''

        # weights = getattr(event, self.cfg_ana.weights)

        met = getattr(event, self.cfg_ana.met)
        fillMet(self.tree, 'met', met)

        electrons = getattr(event, self.cfg_ana.electrons)
        self.fill_particles_by_index(max_number=6, particles=electrons, particle_name='electron_')

        muons = getattr(event, self.cfg_ana.muons)
        self.fill_particles_by_index(max_number=6, particles=muons, particle_name='muon_')

        max_number = self.raw_vars_to_save[0]['max_number']
        particles_name = self.raw_vars_to_save[0]['particles_name']
        save_name = self.raw_vars_to_save[0]['save_name']
        self.fill_particles_by_index2(event, max_number=max_number, particles_name=particles_name, save_name=save_name)

        # pfjets04 = getattr(event, self.cfg_ana.pfjets04)
        # self.fill_particles_by_index(max_number=6, particles=pfjets04, particle_name='pfjets04_')

        self.tree.tree.Fill()

    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()


"""
tree_name
tree_title
weights
gen_particles
electrons
electronITags
electronsToMC
muons
muonITags
muonsToMC
jets
bTags
photons
pfphotons
pfcharged
pfneutrals
met
"""
