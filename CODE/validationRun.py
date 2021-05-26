from ValidationVoter import *
import multiprocessing
import numpy as np


def voterObject(graph, iteration, network_name, aggressive_bound, aggr_init_type, boundDown, boundUp, selectedEdges, RorS, dBnd_down, dBnd_up, dBnd_step, seedNumber):
	totalProcesses_voter = []
	for percentage in selectedEdges:
		p = multiprocessing.Process(target = parallelVoter, args=(graph, iteration, network_name, aggressive_bound, aggr_init_type, boundDown, boundUp, selectedEdges[percentage], percentage, RorS, dBnd_down, dBnd_up, dBnd_step, seedNumber))
		totalProcesses_voter.append(p)
		p.start()
	for process in totalProcesses_voter:
		process.join()
def parallelVoter(graph, iteration, network_name, aggressive_bound, aggr_init_type, boundDown, boundUp, selectedEdges, percentage, RorS, dBnd_down, dBnd_up, dBnd_step, seedNumber):
	voter_object = ValidationVoter(graph)

	if(RorS == "sorted"):
		selectedEdges = sorted(selectedEdges, key=lambda a_entry: a_entry[0])
	elif(RorS == "neighborhood"):
		selectedEdges = returnEdgesNeighboor(graph, selectedEdges)
	elif(RorS == "popularity_increase"):
		selectedEdges = returnEdgesPopularity(graph, selectedEdges, "increase")
	elif(RorS == "popularity_descending"):
		selectedEdges = returnEdgesPopularity(graph, selectedEdges, "descending")

	print(RorS)
	R = voter_object.voter_model(selectedEdges, dBnd_down, dBnd_up, dBnd_step, boundUp)
	writeValidationPercentage(R, "validResults/" + RorS + "_" + str(percentage) + "_seed_" + str(seedNumber) +".txt")



def writeValidationPercentage(r, fileName):
	allModels = ['voter_1', 'voter_w', 'proposal1_w', 'proposal1_p', 
					'proposal1_wp', 'dg_1', 'dg_w', 'dg_p', 'dg_wp',
					'fj_w', 'fj_p', 'fj_wp', 'proposal3_w', 'proposal3_p',
					'proposal3_wp', 'proposal4_w', 'proposal4_p', 'proposal4_wp',
					"d_1.0_w", "d_0.5_w", "d_1.0_p", "d_0.5_p", "d_1.0_wp", "d_0.5_wp"]

	f = open(fileName, 'w')
	for m in allModels:
		f.write(m + "\n")
		for t in r:
			f.write(t + ":" + str(r[t][m]) + "\n")

	f.close()


def returnEdgesPopularity(gph, edgesList, tp):
	tmpEdges = []
	inDegreeDict = {}
	sourceNodes = []
	for edge in edgesList:
		sourceNodes.append(edge[0])
	sourceNodes = set(sourceNodes)
	for n in sourceNodes:
		inDegreeDict[n] = gph.in_degree(n)
	if(tp == "increase"):
		sortedIndegreeDict = sorted(inDegreeDict.items(), key=lambda kv: kv[1])
	elif(tp == "descending"):
		sortedIndegreeDict = sorted(inDegreeDict.items(), key=lambda kv: kv[1], reverse=True)
	for pair in sortedIndegreeDict:
		source = pair[0]
		for ed in edgesList:
			if(ed[0] == source):
				tmpEdges.append(ed)
	return(np.asarray(tmpEdges))

def returnEdgesNeighboor(gph, slcEdg):
	allUsersI = []
	for edge in slcEdg:
		allUsersI.append(edge[0])
	allUsersI = set(allUsersI)
	
	betterFormatForEdged = {}
	for i in slcEdg:
		if(i[0] in list(betterFormatForEdged.keys())):
			betterFormatForEdged[i[0]].append(i[1])
		else:
			betterFormatForEdged[i[0]] = [i[1]]
	tmp_Edges = []
	while(True):
		if(len(allUsersI) == 0):
			break
		choiceRandomI = random.choice(list(allUsersI))
		for n in  betterFormatForEdged[choiceRandomI]:
			tmp_Edges.append((choiceRandomI, n))
		allUsersI.remove(choiceRandomI)

		for nei in betterFormatForEdged[choiceRandomI]:
			if(nei in allUsersI):
				for n in betterFormatForEdged[nei]:
					tmp_Edges.append((nei, n))
				allUsersI.remove(nei)
	return(tmp_Edges)
