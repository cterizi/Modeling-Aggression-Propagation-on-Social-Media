# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import initOpinion
import readGraph
import random
import time
import sys
import os


''' Global Variables'''
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
		return(G)

	def initOpinion(self, myGraph, agrressType, bndDown, bndUp,aggressive_bnd, dBnds_down, dBnds_up, dBnds_step):
		G = initOpinion.main(myGraph, agrressType, bndDown, bndUp, aggressive_bnd, dBnds_down, dBnds_up, dBnds_step)
		return(G)

object_= init()
G = object_.loadNetwork(network_name)
G1 = object_.initOpinion(G, aggressiveness_initialization_type, boundDown, boundUp, aggressive_bound, dBounds_down, dBounds_up, dBounds_step)

def statisticsForRandomSelectedEdges(edgesLst):
	global aggressive_bound

	howManyEdgesHaveIAggrUser = 0
	howManyEdgesHaveINormUser = 0

	howManyEdgesHaveJAggrUser = 0
	howManyEdgesHaveJNormUser = 0
	
	ijAggressiveUsers = 0

	totalEd = 0
	totalUsers = []

	aggrUsersI = []
	aggrUsersJ = []

	normUsersI = []
	normUsersJ = []

	for e in edgesLst:
		totalEd = totalEd + 1
		totalUsers.append(e[0])

		if(G1.node[e[0]]["init"] >= aggressive_bound):
			howManyEdgesHaveIAggrUser = howManyEdgesHaveIAggrUser + 1
			aggrUsersI.append(e[0])
		if(G1.node[e[1]]["init"] >= aggressive_bound):
			howManyEdgesHaveJAggrUser = howManyEdgesHaveJAggrUser + 1
			aggrUsersJ.append(e[1])
		if(G1.node[e[0]]["init"] < aggressive_bound):
			howManyEdgesHaveINormUser = howManyEdgesHaveINormUser + 1
			normUsersI.append(e[0])
		if(G1.node[e[1]]["init"] < aggressive_bound):
                        howManyEdgesHaveJNormUser = howManyEdgesHaveJNormUser + 1
                        normUsersJ.append(e[1])
		if(G1.node[e[0]]["init"] >= aggressive_bound and G1.node[e[1]]["init"] >= aggressive_bound):
			ijAggressiveUsers = ijAggressiveUsers + 1

	#reciprocal edges
	'''	
	final = len(edgesLst)
	step = 1000
	tmp_final = 0
	list_ = []
	while(tmp_final < final):
	    list_.append(tmp_final)
	    tmp_final = tmp_final + step
	    
	tmp_edge_list = []
	for i in edgesLst:
		tmp_edge_list.append(i)
	reciprocalCount = 0
	tmptmp = 0
	for j in edgesLst:
		tmptmp = tmptmp + 1
		if(tmptmp in list_):
			print(tmptmp)
		if(j in tmp_edge_list):
			tmp_edge_list.remove(j)
			if((j[1], j[0]) in tmp_edge_list):
				reciprocalCount = reciprocalCount + 1
				tmp_edge_list.remove((j[1], j[0]))

	print("reciprocalCount: " + str(reciprocalCount))
	'''
	print("Total edges: " + str(totalEd))
	print("Total users: " + str(len(list(set(totalUsers)))))
	print("#(i, j) ∈ E, i ∈ SA: " + str(howManyEdgesHaveIAggrUser))
	x = float(howManyEdgesHaveIAggrUser*100) / totalEd
	print(x)
	
	print("#(i, j) ∈ E, j ∈ SA: " + str(howManyEdgesHaveJAggrUser))
        x = float(howManyEdgesHaveJAggrUser*100) / totalEd
        print(x)

	print("#(i, j) ∈ E, i ∈ SN: " + str(howManyEdgesHaveINormUser))
        x = float(howManyEdgesHaveINormUser*100) / totalEd
        print(x)

	print("#(i, j) ∈ E, j ∈ SN: " + str(howManyEdgesHaveJNormUser))
        x = float(howManyEdgesHaveJNormUser*100) / totalEd
        print(x)

	print("#(i, j) ∈ E, i and j ∈ SA: " + str(ijAggressiveUsers))
	x = float(ijAggressiveUsers*100) / totalEd
        print(x)
	
	print("#n, n ∈  V, (i, j) ∈ E, i ∈  VA: " + str(len(list(set(aggrUsersI)))))
	x = float(len(list(set(aggrUsersI)))*100) / len(list(set(totalUsers)))
	print(x)

	print("#n, n ∈  V, (i, j) ∈ E, j ∈  VA: " + str(len(list(set(aggrUsersJ)))))
	x = float(len(list(set(aggrUsersJ)))*100) / len(list(set(totalUsers)))
        print(x)

	print("#n, n ∈  V, (i, j) ∈ E, i ∈  VN: " + str(len(list(set(normUsersI)))))
        x = float(len(list(set(normUsersI)))*100) / len(list(set(totalUsers)))
        print(x)

        print("#n, n ∈  V, (i, j) ∈ E, j ∈  VN: " + str(len(list(set(normUsersJ)))))
        x = float(len(list(set(normUsersJ)))*100) / len(list(set(totalUsers)))
        print(x)


SEED = [1]
selectedEdges = {}
for iter__ in range(0, total_iterations):
	selectedEdges[iter__] = {}
	for selectedPercentage in range(10, 11):
		#selectedPercentage = 0.001
		numberOfEdges = int((float(selectedPercentage)/100) * G1.number_of_edges())
		random.seed(SEED[iter__])
		randomSample = random.sample(G1.edges(), numberOfEdges)
		selectedEdges[iter__][selectedPercentage] = np.asarray(randomSample)
		statisticsForRandomSelectedEdges(randomSample)
		#print(selectedEdges[iter__][selectedPercentage])
