import networkx as nx
import numpy as np
import random

def jaccard_similarity(list1, list2):
	s1 = set(list1)
	s2 = set(list2)
	jaccardSimilarity = float(len(s1.intersection(s2))) / len(s1.union(s2))
	return(jaccardSimilarity) 

def main(graph):
	for edge in graph.edges():
		Ni = graph.neighbors(edge[0])
		Nj = graph.neighbors(edge[1])
		graph[edge[0]][edge[1]]['weight'] = jaccard_similarity(Ni, Nj)
	return(graph)
