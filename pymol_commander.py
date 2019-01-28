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
        #name="connection"+str(self.connection_count)
        name=str(atom1.split("/")[1]) + "_" +str(atom1.split("/")[-1]) + "--" + str(atom2.split("/")[1])+"_"+str(atom2.split("/")[-1])
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

    def read_PDBanalyzer(self,filename,outname,stickColors,chainColors):
        import re
        contacts=[]
#        stickcolors = ["gray", "yellow", "red", "white", "orange"]
#        chaincolors = ["green", "yellow", "red", "white", "orange"]
        with open(outname,"r") as contact_file:
            contacts_lines=contact_file.readlines()
            for line in contacts_lines:
                contacts.append(line.split())
        #print contacts
        self.loadModel(filename,"pdb")
        model="obj"+str(self.count-1)
        self.showModel(model,chainColors,stickColors)
        for i in contacts:
            id1=re.findall(r'\d+', i[0])
            id2=re.findall(r'\d+', i[2])
            atom1=str(i[1])+"/"+i[0][0:3]+"`"+i[0][3:]+"/"+i[4]
            atom2=str(i[3])+"/"+i[2][0:3]+"`"+i[2][3:]+"/"+i[5]
            selection="chain "+str(i[1])+" & resi "+str(id1[0])+" + chain "+str(i[3])+" & resi "+str(id2[0])
            cmd.set("label_position", "(1,1,1)")
            try:
                color=chainColors[contacts.index(i)]
            except IndexError:
                color = chainColors[-1]
            self.showSticks(model,selection,"none")
            if ("O" in i[4]) or ("N" in i[4]) or ("S" in i[4]):
                if ("O" in i[5]) or ("N" in i[5]) or ("S" in i[5]):
                    self.showConnection(model, atom1, atom2, "yellow")
            else:
                self.showConnection(model,atom1,atom2,"black")






