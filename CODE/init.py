# -*- coding: utf-8 -*-

import multiprocessing
import numpy as np
import initOpinion
import initWeight
import runModels
import readGraph
import initPower
import random
import signal
import time
import math
import sys
import os


''' Global Variables'''
#python3 init.py small discrete-0-1-1 aggr-0-1-0.50 iter-1
network_name = sys.argv[1]
aggressiveness_initialization_tp = sys.argv[2].split("-")
aggressiveness_initialization_type = aggressiveness_initialization_tp[0]
if(aggressiveness_initialization_type == "discrete"):
	boundDown = int(aggressiveness_initialization_tp[1])
	boundUp = int(aggressiveness_initialization_tp[2])
else:
	boundDown = float(aggressiveness_initialization_tp[1])
	boundUp = float(aggressiveness_initialization_tp[2])
aggressive_bound = float(aggressiveness_initialization_tp[3])
dBounds_down = int(sys.argv[3].split("-")[1])
dBounds_up = int(sys.argv[3].split("-")[2])
dBounds_step = float(sys.argv[3].split("-")[3])
total_iterations = int(sys.argv[4].split("-")[1])

class init:	

	def loadNetwork(self, network_name):
		''' Load the network'''
		G = readGraph.returnGraph(network_name)
		''' Calculate statistics for the network'''
		#readGraph.calculateStatistics(G, network_name)
		''' Display the network'''
		#readGraph.displayGraph(G, network_name)
		return(G)

	def initOpinion(self, myGraph, agrressType, bndDown, bndUp,aggressive_bnd, dBnds_down, dBnds_up, dBnds_step):
		G = initOpinion.main(myGraph, agrressType, bndDown, bndUp, aggressive_bnd, dBnds_down, dBnds_up, dBnds_step)
		return(G)

	def initWeight(self, myGraph):
		G = initWeight.main(myGraph)
		return(G)

	def initPower(self, myGraph):
		G = initPower.main(myGraph)
		return(G)

''' 
############################################
############################################
	Parallel code
############################################
############################################
'''

G_list = []
for iter_ in range(0, total_iterations):
	object_= init()
	G = object_.loadNetwork(network_name)
	G1 = object_.initOpinion(G, aggressiveness_initialization_type, boundDown, boundUp, aggressive_bound, dBounds_down, dBounds_up, dBounds_step)
	G2 = object_.initWeight(G1)
	G3 = object_.initPower(G2)
	G_list.append(G3)

''' 
############################################
############################################
	Pairwise models - A pair
############################################
############################################
'''
def returnRandomSample(g):
	global aggressive_bound

	agNd = []
	for n in g.nodes():
		if(g.node[n]["init"] >= aggressive_bound):
			agNd.append(n)

	ed = g.edges(agNd)
	print("number of edges: " + str(len(list(ed))))

	return(list(ed))


def returnHowManyAggUsersMoreThanOne(edgesList, graph__):
	global aggressive_bound

	howManyAggUsers = []
	moreThanOne = {}
	for e in edgesList:
		if(graph__.node[e[0]]["init"] >= aggressive_bound):
			howManyAggUsers.append(e[0])
			if(e[0] in list(moreThanOne.keys())):
				moreThanOne[e[0]] = moreThanOne[e[0]] + 1
			else:
				moreThanOne[e[0]] = 1
	
	moreThatOne_variable = 0
	for j in list(moreThanOne.values()):
		if(j > 1):
			moreThatOne_variable = moreThatOne_variable + 1
	return(len(set(howManyAggUsers)), moreThatOne_variable)


#SEED = [x for x in range(0, total_iterations)]
#SEED = [1]
selectedEdges = {}
for iter__ in range(0, total_iterations):
	selectedEdges[iter__] = {}
	for selectedPercentage in range(20, 21):
		#selectedPercentage = 0.001
		numberOfEdges = int((float(selectedPercentage)/100) * G_list[iter__].number_of_edges())
		#random.seed(SEED[iter__])
		#randomSample = random.sample(G_list[iter__].edges(), numberOfEdges)
		randomSample = returnRandomSample(G_list[iter__])
		selectedEdges[iter__][selectedPercentage] = np.asarray(randomSample)

allTimesPairwise = {}



''' 
############################################
############################################
	Pairwise models - random pairs
############################################
############################################
'''

s = time.time()
iter_processes_voter = []
for iter_ in range(0, total_iterations):
	p = multiprocessing.Process(target = runModels.voterObject, args=(G_list[iter_], iter_, network_name, aggressive_bound, aggressiveness_initialization_type, boundDown, boundUp, selectedEdges[iter_], "random", dBounds_down, dBounds_up, dBounds_step))
	iter_processes_voter.append(p)
	p.start()

for process in iter_processes_voter:
	process.join()
allTimesPairwise["edges-random"] = (time.time() - s)/60


''' 
############################################
############################################
	Pairwise models - sorted pairs
############################################
############################################
'''

s = time.time()
iter_processes_voter_sorted = []
for iter_ in range(0, total_iterations):
	p = multiprocessing.Process(target = runModels.voterObject, args=(G_list[iter_], iter_, network_name, aggressive_bound, aggressiveness_initialization_type, boundDown, boundUp, selectedEdges[iter_], "sorted", dBounds_down, dBounds_up, dBounds_step))
	iter_processes_voter_sorted.append(p)
	p.start()

for process in iter_processes_voter_sorted:
	process.join()
allTimesPairwise["edges-sorted"] = (time.time() - s)/60


''' 
############################################
############################################
		Neighborhood by neighborhood
############################################
############################################
'''

s = time.time()
iter_processes_neighborhood = []
for iter_ in range(0, total_iterations):
	p = multiprocessing.Process(target = runModels.voterObject, args=(G_list[iter_], iter_, network_name, aggressive_bound, aggressiveness_initialization_type, boundDown, boundUp, selectedEdges[iter_], "neighborhood", dBounds_down, dBounds_up, dBounds_step))
	iter_processes_neighborhood.append(p)
	p.start()

for process in iter_processes_neighborhood:
	process.join()
allTimesPairwise["neighborhood"] = (time.time() - s)/60

''' 
############################################
############################################
		Popularity increase
############################################
############################################
'''

s = time.time()
iter_processes_neighborhood = []
for iter_ in range(0, total_iterations):
	p = multiprocessing.Process(target = runModels.voterObject, args=(G_list[iter_], iter_, network_name, aggressive_bound, aggressiveness_initialization_type, boundDown, boundUp, selectedEdges[iter_], "popularity_increase", dBounds_down, dBounds_up, dBounds_step))
	iter_processes_neighborhood.append(p)
	p.start()

for process in iter_processes_neighborhood:
	process.join()
allTimesPairwise["popularity_increase"] = (time.time() - s)/60


''' 
############################################
############################################
		Popularity descending
############################################
############################################
'''

s = time.time()
iter_processes_neighborhood = []
for iter_ in range(0, total_iterations):
	p = multiprocessing.Process(target = runModels.voterObject, args=(G_list[iter_], iter_, network_name, aggressive_bound, aggressiveness_initialization_type, boundDown, boundUp, selectedEdges[iter_], "popularity_descending", dBounds_down, dBounds_up, dBounds_step))
	iter_processes_neighborhood.append(p)
	p.start()

for process in iter_processes_neighborhood:
	process.join()
allTimesPairwise["popularity_descending"] = (time.time() - s)/60


print(allTimesPairwise)
