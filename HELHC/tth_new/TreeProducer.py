from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from heppy.analyzers.ntuple import *
from numpy import sign
from ROOT import TFile, TLorentzVector


class SimpleTreeProducer(Analyzer):

    def beginLoop(self, setup):
        super(SimpleTreeProducer, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'simple_tree.root']),
                              'recreate')
        self.tree = Tree(self.cfg_ana.tree_name,
                         self.cfg_ana.tree_title)

        # List of dict
        self.raw_vars_to_save = list()

        self.raw_vars_to_save.append({'container_name': 'electrons',
                                      'save_name': 'electrons_',
                                      'max_number': 6})

        self.raw_vars_to_save.append({'container_name': 'muons',
                                      'save_name': 'muons_',
                                      'max_number': 6})

        self.raw_vars_to_save.append({'container_name': 'pfjets04',
                                      'save_name': 'pfjets04_',
                                      'max_number': 6})

        # self.raw_vars_to_save.append({'container_name': 'pfbTags04',
        #                                 'save_name': 'pfbTags04_',
        #                                 'max_number': 6})

        self.raw_vars_to_save.append({'container_name': 'pfjetsFlavor04',
                                      'save_name': 'pfjetsFlavor04_',
                                      'max_number': 6})

        #self.tree.var('weights', float)
        bookMet(self.tree, 'met')

        for container_i in self.raw_vars_to_save:
            max_number = container_i['max_number']
            save_name = container_i['save_name']
            for index in range(max_number):
                bookParticle(self.tree, '{}{}'.format(save_name, index))

        # e.g:
        # bookParticle(self.tree, 'electron_0')
        # bookParticle(self.tree, 'electron_1')
        # bookParticle(self.tree, 'electron_2')
        # bookParticle(self.tree, 'electron_3')
        # bookParticle(self.tree, 'electron_4')
        # bookParticle(self.tree, 'electron_5')

    def fill_particles_by_index(self, event, max_number=None, container_name=None, save_name=None):
        event_particles = getattr(event, eval('self.cfg_ana.{}'.format(container_name)))
        for index, particle in enumerate(event_particles):
            if index == max_number:
                break
            fillParticle(self.tree, '{}{}'.format(save_name, index), particle)

    def process(self, event):

        #weights = getattr(event, self.cfg_ana.weights)
        #self.tree.fill('weights', weights)

        met = getattr(event, self.cfg_ana.met)
        fillMet(self.tree, 'met', met)

        for container_i in self.raw_vars_to_save:
            max_number = container_i['max_number']
            container_name = container_i['container_name']
            save_name = container_i['save_name']
            self.fill_particles_by_index(event, max_number=max_number, container_name=container_name, save_name=save_name)

        # e.g.
        # electrons = getattr(event, self.cfg_ana.electrons)
        # fillParticle(self.tree, electron_0, electrons[0])
        # ....

        self.tree.tree.Fill()

    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()
