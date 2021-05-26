import createGroups
import createOurGraph
import readGraph
from Voter import Voter
from DegrootFormula import DegrootFormula
from FriedkinJohnsen import FriedkinJohnsen
from BEBA import BEBA

import networkx as nx	
import numpy as np
import operator
import decimal
import random
import time


'''
	################################
	################################
		WEIGHT INITIALIZATION
	################################
	################################
'''

def initWeight_noGr(graph, type):
	tmp_graph = nx.Graph()
	tmp_graph.add_edges_from(graph.edges())
	if(type == "one"):
		for edge in tmp_graph.edges():
			tmp_graph[edge[0]][edge[1]]['weight'] = 1
			tmp_graph.node[edge[0]]['weight'] = 1
			tmp_graph.node[edge[1]]['weight'] = 1
	elif(type == "decimal_positive"):
		for edge in tmp_graph.edges():
			tmp_graph[edge[0]][edge[1]]['weight'] = random.randint(1, 100)/100
			tmp_graph.node[edge[0]]['weight'] = 1
			tmp_graph.node[edge[1]]['weight'] = 1

	return(tmp_graph)

'''
	################################
	################################
				VOTER
	################################
	################################
'''

def voter_cases_yesGr(graph, current_iter, tmp_path, topNodes, grp1, grp2, opinion_discrete, opinion_decimal_negative, tp):
	tmp_path = tmp_path + "voter/"
	
	if(tp == "dis"):
		current_path = tmp_path + "discrete_" + str(current_iter) + ".txt"
		obj = Voter(graph, opinion_discrete, current_path, grp1, grp2)
	else:
		current_path = tmp_path + "decimalPosNeg_" + str(current_iter) + ".txt"
		obj = Voter(graph, opinion_decimal_negative, current_path, grp1, grp2)

'''
	################################
	################################
				DE-GROOT
	################################
	################################
'''

def degroot_cases_yesGr(graph_1, graph_decimal_positive, current_iter, tmp_path, topNodes, grp1, grp2, opinion_discrete, opinion_decimal_negative, tp):
	tmp_path = tmp_path + "degroot/"
	
	if(tp == "dis"):
		current_path = tmp_path + "discrete_" + str(current_iter) + ".txt"
		obj = DegrootFormula(graph_1, opinion_discrete, current_path, grp1, grp2)
	else:
		current_path = tmp_path + "decimalPosNeg_" + str(current_iter) + ".txt"
		obj = DegrootFormula(graph_1, opinion_decimal_negative, current_path, grp1, grp2)

'''
	################################
	################################
			Friedkin Johnsen
	################################
	################################
'''

def fj_cases_yesGr(graph_1, graph_decimal_positive, current_iter, tmp_path, topNodes, grp1, grp2, opinion_discrete, opinion_decimal_negative, tp):
	tmp_path = tmp_path + "fj/"
	
	if(tp == "dis"):
		current_path = tmp_path + "discrete_weight_1_" + str(current_iter) + ".txt"
		obj = FriedkinJohnsen(graph_1, opinion_discrete, current_path, grp1, grp2)
	else:
		current_path = tmp_path + "decimalPosNeg_weight_1_" + str(current_iter) + ".txt"
		obj = FriedkinJohnsen(graph_1, opinion_decimal_negative, current_path, grp1, grp2)

'''
	################################
	################################
			BEBA
	################################
	################################
'''
b_value = {1: "beba/b = 1/", 1.5:"beba/b = 1.5/", 2:"beba/b = 2/", 2.5:"beba/b = 2.5/", 5:"beba/b = 5/", 10:"beba/b = 10/", 20:"beba/b = 20/", 0:"beba/b = 0/", 0.20:"beba/b = 0.20/", 0.50:"beba/b = 0.50/", 5:"beba/b = 5/"}

def beba_cases_yesGr(graph_1, graph_decimal_positive, current_iter, tmp_path, topNodes, grp1, grp2, opinion_discrete, opinion_decimal_negative, b, tp):
	tmp_path = tmp_path + b_value[b]
	
	if(tp == "dis"):
		current_path = tmp_path + "discrete_" + str(current_iter) + ".txt"
		obj = BEBA(graph_1, opinion_discrete, current_path, grp1, grp2, b)
	else:
		current_path = tmp_path + "decimalPosNeg_" + str(current_iter) + ".txt"
		obj = BEBA(graph_1, opinion_decimal_negative, current_path, grp1, grp2, b)


'''
	################################
	################################
		PATHS & LOAD GRAPH
	################################
	################################
'''

pathYesGroupsDis = {"karate": "Results/withGroup/karate/discrete/",
				"dolphins": "Results/withGroup/dolphins/discrete/",
				"books": "Results/withGroup/books/discrete/",
				"blogs": "Results/withGroup/blogs/discrete/",
				"ourGraph": "Results/withGroup/ourGraph/discrete/"
				}

pathYesGroupsDec = {"karate": "Results/withGroup/karate/decimal/",
				"dolphins": "Results/withGroup/dolphins/decimal/",
				"books": "Results/withGroup/books/decimal/",
				"blogs": "Results/withGroup/blogs/decimal/",
				"ourGraph": "Results/withGroup/ourGraph/decimal/"
				}

'''
	################################
	################################
		CASES NO - YES GROUPS
	################################
	################################
'''

def main_with_groups(name, current_iter, graph, tmp_path, topNodes, grp1, grp2, tp):
	tmp_path_ = tmp_path + f_values[f]
	opinion_discrete = initOpinion_discrete_(graph, grp1, grp2, f)
	opinion_decimal_negative = initOpinion_decimal_(graph, grp1, grp2, f)
	#weight initialization
	graph_1 = initWeight_noGr(graph, "one")
	graph_decimal_positive = initWeight_noGr(graph, "decimal_positive")
	#voter_cases_yesGr(graph, current_iter, tmp_path, topNodes, grp1, grp2, opinion_discrete, opinion_decimal_negative)
	#degroot_cases_yesGr(graph_1, graph_decimal_positive, current_iter, tmp_path_, topNodes, grp1, grp2, opinion_discrete, opinion_decimal_negative, tp)
	#print("degroot")
	#fj_cases_yesGrvi(graph_1, graph_decimal_positive, current_iter, tmp_path_, topNodes, grp1, grp2, opinion_discrete, opinion_decimal_negative, tp)
	#print("fj")
	#beba_cases_yesGr(graph_1, graph_decimal_positive, current_iter, tmp_path_, topNodes, grp1, grp2, opinion_discrete, opinion_decimal_negative, 2, tp)
	# b = [0, 0.20, 0.50, 1, 1.5, 2, 2.5, 5, 10, 20]
	# for b_value in b:
	# 	print("beba, b: " + str(b_value))
	# 	beba_cases_yesGr(graph_1, graph_decimal_positive, current_iter, tmp_path_, topNodes, grp1, grp2, opinion_discrete, opinion_decimal_negative, b_value, tp)


def main(network_name, total_iterations):
	[group1, group2] = createGroups.main_(name)
	main_with_groups(name, iter_, graph_X, pathYesGroupsDec[name], topNodes, group1, group2, "dec")