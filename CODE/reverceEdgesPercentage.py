# -*- coding: utf-8 -*-

import numpy as np
import readGraph
import random
import time
import math
import sys
import os


''' Global Variables'''
network_name = sys.argv[1]

class init:	

	def loadNetwork(self, network_name):
		''' Load the network'''
		G = readGraph.returnGraph(network_name)
		return(G)

object_= init()
G = object_.loadNetwork(network_name)
tmp_edges = []
cntRevEd = 0
for edge in G.edges():
	if(G.has_edge(edge[1], edge[0])):
		cntRevEd = cntRevEd + 1
		tmp_edges.append(str(edge))
		#print(edge)
		print(cntRevEd)
