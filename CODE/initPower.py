import networkx as nx
import random
import numpy

def main(graph):
	for node in graph.nodes():
		indegree = graph.in_degree(node)
		outdegree = len(set(graph.neighbors(node)))
		graph.node[node]['power'] = float(indegree) / outdegree

	for nd in graph.nodes():
		maxPw = -1
		for ngh in graph.neighbors(nd):
			if(graph.node[ngh]['power'] > maxPw):
				maxPw = graph.node[ngh]['power']
		if(graph.node[nd]['power'] > maxPw):
			maxPw = graph.node[nd]['power']
		graph.node[nd]['power'] = float(graph.node[nd]['power']) / maxPw
	return(graph)