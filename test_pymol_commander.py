#!/usr/bin/env python2

from pymol_commander import PymolCommander
import pymol
from pymol import cmd
from time import sleep
pymol.finish_launching()



commander=PymolCommander()
#default hiding everything
#cmd.do("hide everything")


commander.loadModel("test.pdb","pdb")

stickcolors=["gray","yellow","white","orange","black"]
chaincolors=["green","yellow","white","orange","black"]


commander.read_PDBanalyzer("test.pdb", "test.out",stickcolors,chaincolors)
#commander.showModel("obj0",chaincolors,stickcolors)
#commander.zoom("obj0","chain c")
#sleep(1)
#commander.undoZoom()
#sleep(1)



#commander.zoom("obj0","not pol")
#sleep(1)
#commander.undoZoom()
#sleep(1)


#commander.hideModel("obj0")
#commander.showSticks("obj0","chain c & resi 4","grey")
#commander.zoom("obj0","chain c & resi 4")
#commander.showSticks("obj0","chain d & resi 96+97+98","white")
#commander.showSticks("obj0","chain e & resi 96+50+29+97+98+99","orange")
#commander.hideSticks("obj0","chain a")
#commander.showSpheres("obj0","chain a","grey")
#commander.hideSpheres("obj0","chain a")
#commander.center("chain c")
#commander.showConnection("obj0","F/ILE`861/CA","F/VAL`1080/CA","black")
#commander.hideConnection("obj0","F/ILE`861/CA","F/VAL`1080/CA")
#commander.deleteModel("obj0")



#

