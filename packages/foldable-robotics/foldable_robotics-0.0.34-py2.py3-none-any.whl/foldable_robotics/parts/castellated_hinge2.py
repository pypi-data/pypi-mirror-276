# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes and CONTRIBUTORS
Email: danaukes<at>asu.edu.
Please see LICENSE for full license.
"""

#import modules from shapely and matplotlib
import shapely.geometry as sg
import matplotlib.pyplot as plt

#import classes from my local modules
from foldable_robotics.laminate import Laminate
from foldable_robotics.layer import Layer

import foldable_robotics.manufacturing

def generate(g=1,w=None):

    #create a layer named box
    layer12 = Layer(sg.box(0,0,1,1)) | Layer(sg.box(1,1,2,2)) | Layer(sg.box(3,1,4,2)) | Layer(sg.box(4,0,5,1))
    layer12 = layer12.translate(0,-1)
    layer34 = layer12.scale(1,-1)
    hinge = Laminate(layer12,layer12,Layer(),layer34,layer34)

    hinge_hole = Layer(sg.box(2,-1,3,1))
    hinge_hole =  Laminate(hinge_hole,hinge_hole,hinge_hole,hinge_hole,hinge_hole)

    hinge |= hinge_hole

    

    hinge = hinge.scale(1,g/2)

    if (w is not None or w<=0):
        gap_layer = Layer(sg.box(0,-w/2,5,w/2))
    else:
        gap_layer = Layer()

    gap = Laminate(gap_layer,gap_layer,Layer(),gap_layer,gap_layer)
    hinge |= gap

    hinge = hinge.scale(1/5,1)

    return hinge

if __name__=='__main__':
    hinge = generate()
#    hinge = hinge.scale(1,.1)
    hinge.plot()
    
    from foldable_robotics.dynamics_info import MaterialProperty
    import idealab_tools.plot_tris as pt
    
    m = MaterialProperty.make_n_blank(5,thickness = .1)
    
    mesh_items = hinge.mesh_items(m)
    pt.plot_mi(mesh_items)
