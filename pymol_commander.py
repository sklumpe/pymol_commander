#!/usr/bin/env python2

from interface import PymolCommander as Base
from pymol import stored
from pymol import cmd

class PymolCommander(Base):

    def __init__(self):
        self.count=0
        self.connection_count=0
        self.zoom_history=[]
        self.connection_dictionary={}

    def showModel(self, model, chainColors, stickColors):
        cmd.do("hide")
        cmd.do("bg_color white")
        cmd.do("show cartoon, "+ str(model))
        chains=[]
        for ch in cmd.get_chains(model):
            chains.append(ch)
        for i in range(0,len(chains)):
            try:
                cmd.do("color "+chainColors[i]+", chain "+chains[i])
            except IndexError:
                cmd.do("color " + chainColors[-1] + ", chain " + chains[i])
                print("Error: Detected more chains than colors. Last color in color list will be used.")

        cmd.do("show spheres, all and not bound_to all")
        cmd.do("util.cnc('all and not bound_to all')")
        cmd.do("show sticks, not pol")
        cmd.do("color "+stickColors[0]+", not pol")
        cmd.do("util.cnc('not pol')")

    
    def hideModel(self, model):
        cmd.do("hide everything, "+str(model))


    def showSticks(self, model, sel, color):
        cmd.do("show sticks, "+str(model)+" & " + str(sel))
        cmd.do("color "+str(color)+", "+str(model)+" & " + str(sel))
        cmd.do("util.cnc('"+str(model)+" & " + str(sel)+"')")


    def hideSticks(self, model, sel):
        cmd.do("hide sticks, "+str(model)+" & " + str(sel))


    def showSpheres(self, model, sel, color):
        cmd.do("show spheres, "+str(model)+" & " + str(sel))
        cmd.do("color "+str(color)+", "+str(model)+" & " + str(sel))
        cmd.do("util.cnc('"+str(model)+" & " + str(sel)+"')")

    
    def hideSpheres(self, model,sel):
        cmd.do("hide spheres, "+str(model)+" and " + str(sel))


    def showConnection(self, model, atom1, atom2, color):
        name="connection"+str(self.connection_count)

        self.connection_dictionary.update({(str(model)+str(atom1)+str(atom2)):(self.connection_count)})
        self.connection_count += 1
        cmd.do("distance "+str(name)+", /"+ str(model)+"//"+str(atom1)+", /"+ str(model)+"//"+str(atom2))
        cmd.do("color "+str(color)+", "+str(name))


    def hideConnection(self, model, atom1, atom2):
        id=self.connection_dictionary[str(model)+str(atom1)+str(atom2)]
        cmd.do('hide everything, connection'+str(id))


    def loadModel(self,path,form):
        if form=="pdb" or form=="prmtop":
            try:
                cmd.load(path, "obj"+str(self.count),0,form )
                self.count+=1
            except:
                print("Something went wrong when loading the PDB file")
        else:
            print("Unsupported File Format.")

    
    def loadTraj(self, model,path,form):
        #dont
        pass

    def deleteModel(self, model):
        cmd.do("delete " + str(model))

    def center(self, model):
        cmd.do("center " + str(model))

    def zoom(self, model, sel):
        cmd.do("zoom " + str(model) + " and " + str(sel))
        self.zoom_history.append(cmd.get_view())
        if len(self.zoom_history) > 10:
            del self.zoom_history[0]

    
    def undoZoom(self):
        try:
            cmd.do("set_view "+str(self.zoom_history[-1]))
            del self.zoom_history[-1]
        except:
            print("Number of undoZooms has been exhausted.")


    def setFrame(self, model, n):
        #dont
        pass

