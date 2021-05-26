import matplotlib.pyplot as plt
import networkx as nx
import operator
import inspect
import random
import sys
import os

graphPath = {"twitter":"networks/twitter/", "karate":"networks/karate/"}
 
def calculateStatistics(myGraph, name):
	
	tmp_path = graphPath[name] + "statistics.txt"
	infoFile = open(tmp_path, 'w')

	total_number_of_nodes = myGraph.number_of_nodes()
	infoFile.write("Nodes " + str(total_number_of_nodes) + "\n")

	total_number_of_edges = myGraph.number_of_edges()
	infoFile.write("Edges: " + str(total_number_of_edges) + "\n")

	#pr_directed = nx.pagerank(myGraph, alpha = 0.9)
	#pr_directed_sorted = sorted(pr_directed.items(), key = operator.itemgetter(1))[::-1]

	infoFile.close()

def displayGraph(myGraph, path):
	#display a subgraph
	nodes = myGraph.nodes()
	tmp_nodes = random.sample(nodes, 10)
	H = myGraph.subgraph(tmp_nodes)
	nx.draw(H, pos=nx.spring_layout(H), node_size=2)

	# tmp_title = path.replace("/", "").upper()
	plt.show()


def returnTheFolder(path):
	if("txt" in path):
		tmp_path = path.replace("dataset.txt", "")
	elif("gml" in path):
		tmp_path = path.replace("dataset.gml", "")
	elif("mtx" in path):
		tmp_path = path.replace("dataset.mtx", "")
	elif("csv" in path):
		tmp_path = path.replace("dataset.csv", "")
	return(tmp_path)

def readEdgelistFile(path):
	graph_X = nx.read_edgelist(path, nodetype = int, create_using = nx.DiGraph())
	
	return(graph_X)

def createEdgelistFile(path):
	graph_X = nx.DiGraph()
	myFile = open(path)
	for line in myFile:
		try:
			tmp_line = line.replace("\n", "").split(" ")
			source = int(tmp_line[0])
			target = int(tmp_line[1])
			graph_X.add_edge(source, target)
		except:
			print("error")

	myFile.close()

	'''Write edgelist file'''
	nx.write_edgelist(graph_X, returnTheFolder(path) + "edgelist")

	return(graph_X)

def returnTheLargestCC(graph):
	largest_cc = max(nx.strongly_connected_component_subgraphs(graph), key=len)
	return(largest_cc)

def returnGraph(name):
	tmp_network_name = graphPath[name] + "edgelist"
	if(os.path.isfile(tmp_network_name)):
		''' Read the edgelist file'''
		graph_X = readEdgelistFile(graphPath[name] + "edgelist")
	else:
		''' Create the edgelist file'''
		createEdgelistFile(graphPath[name] + "dataset.txt")
		graph_X = readEdgelistFile(graphPath[name] + "edgelist")
	
	''' Return the largest strongly connected component network'''
	if(not(name == "karate")):
		graph_X = returnTheLargestCC(graph_X)
	return(graph_X)
