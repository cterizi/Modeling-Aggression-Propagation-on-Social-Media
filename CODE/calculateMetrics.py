# -*- coding: utf-8 -*-

import numpy as np
import networkx as nx
import initWeight
import readGraph
import random
import time
import math
import sys
import csv
import os


''' Global Variables'''
network_name = sys.argv[1]

class init:	
	def loadNetwork(self, network_name):
		''' Load the network'''
		G = readGraph.returnGraph(network_name)
		return(G)

	def initWeight(self, myGraph):
		G = initWeight.main(myGraph)
		return(G)

object_= init()
G = object_.loadNetwork(network_name)
G1 = object_.initWeight(G)

start = time.time()
metrics = {}
for node in G1.nodes():
	metrics[node] = {}
	metrics[node]["userid"] = node
	metrics[node]["cntFriends"] = G1.out_degree(node)
	metrics[node]["cntFollowers"] = G1.in_degree(node)
	metrics[node]["followers2friends"] = float(G1.in_degree(node))/G1.out_degree(node)
	metrics[node]["clusteringCoefficient"] = nx.clustering(G1, node)

hubs, authority = nx.hits(G1)
centrality = nx.eigenvector_centrality(G1, weight='weight')

for n in G1.nodes():
	metrics[n]["hubscore"] = hubs[n]
	metrics[n]["authorityscore"] = authority[n]
	metrics[n]["eigenvector"] = centrality[n]


finish = time.time()
print("Time: " + str(float(finish - start)/60) + " minutes")

metricsFile = open("metrics.csv", "w")
with metricsFile:
	fieldNames = ["userid", "cntFriends", "cntFollowers", "followers2friends", "clusteringCoefficient", "hubscore", "authorityscore", "eigenvector"]
	writer = csv.DictWriter(metricsFile, fieldnames = fieldNames)
	writer.writeheader()
	for n in G.nodes():
		writer.writerow(metrics[n])
metricsFile.close()
