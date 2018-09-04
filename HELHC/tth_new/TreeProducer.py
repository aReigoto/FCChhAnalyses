
from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from ROOT import TFile


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

    def beginLoop(self, setup):
        super(SimpleTreeProducer, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'simple_tree.root']),
                              'recreate')
        # self.tree = Tree(self.cfg_ana.tree_name,
        #                 self.cfg_ana.tree_title)
        self.tree = Tree('events', '')
        # Names of vars must be availebel from
        # from EventStore import EventStore as Events
        # EventStore
        #self.tree = Tree( 'events', '')
        self.tree.var('weight', float)
        # self.tree.var('weights')
        self.tree.var('electrons')

    def process(self, event):
        '''Process the event.

        The input data must contain a variable called "var1",
        which is the case of the L{test tree<heppy.utils.testtree>}.

        The event must contain:
         - var_random, which is the case if the L{RandomAnalyzer<heppy.analyzers.examples.simple.RandomAnalyzer.RandomAnalyzer>}
         has processed the event.

        '''
        #self.tree.fill('weight' , sign(event.weight) )
        self.tree.fill('weight', event.weight)
        self.tree.fill('electrons', event.input.electrons)
        self.tree.tree.Fill()

    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()
