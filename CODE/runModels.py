import multiprocessing
from Voter import *
import random
import time


def voterObject(graph, iteration, network_name, aggressive_bound, aggr_init_type, boundDown, boundUp, selectedEdges, RorS, dBnd_down, dBnd_up, dBnd_step):
	totalProcesses_voter = []
	for percentage in selectedEdges:
		p = multiprocessing.Process(target = parallelVoter, args=(graph, iteration, network_name, aggressive_bound, aggr_init_type, boundDown, boundUp, selectedEdges[percentage], percentage, RorS, dBnd_down, dBnd_up, dBnd_step))
		totalProcesses_voter.append(p)
		p.start()
	for process in totalProcesses_voter:
		process.join()
def parallelVoter(graph, iteration, network_name, aggressive_bound, aggr_init_type, boundDown, boundUp, selectedEdges, percentage, RorS, dBnd_down, dBnd_up, dBnd_step):
	voter_object = Voter(graph)

	if(RorS == "sorted"):
		selectedEdges = sorted(selectedEdges, key=lambda a_entry: a_entry[0])
	elif(RorS == "neighborhood"):
		selectedEdges = returnEdgesNeighboor(graph, selectedEdges)
	elif(RorS == "popularity_increase"):
		selectedEdges = returnEdgesPopularity(graph, selectedEdges, "increase")
	elif(RorS == "popularity_descending"):
		selectedEdges = returnEdgesPopularity(graph, selectedEdges, "descending")

	
	R = voter_object.voter_model(selectedEdges, dBnd_down, dBnd_up, dBnd_step, boundUp)

	tmp_lR = []
	tmp_nR = []
	tmp_d = []
	for tp in R[7]:
		for d in R[7][tp]:
			tmp_lR.append(R[7][tp][d])
			tmp_nR.append("proposal2_" + tp)
			tmp_d.append(d)
	tmp_R = [R[2], R[3], R[4], R[5], R[6], R[8]["1"], R[8]["w"], R[8]["p"], R[8]["wp"], R[9]["w"], R[9]["p"], R[9]["wp"], R[10]["w"], R[10]["p"], R[10]["wp"], R[11]["w"], R[11]["p"], R[11]["wp"]]
	tmp_R = tmp_R + tmp_lR
	tmp_name = ["voter_1", "voter_w", "proposal1_w", "proposal1_p", "proposal1_wp", "degroot_1", "degroot_w", "degroot_p", "degroot_wp", "fj_w", "fj_p", "fj_wp", "proposal3_w", "proposal3_p", "proposal3_wp", "proposal4_w", "proposal4_p", "proposal4_wp"]
	tmp_name = tmp_name + tmp_nR
	tmp_numb = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
	tmp_numb = tmp_numb + tmp_d
	
	
	totalProcesses_write = []
	for i in range(0, len(tmp_R)):
		pp = multiprocessing.Process(target = parallelWrite, args=(voter_object, tmp_R[i], R[1], aggressive_bound, iteration, percentage, network_name, aggr_init_type, boundDown, boundUp, tmp_name[i], RorS, tmp_numb[i], R[0]))
		totalProcesses_write.append(pp)
		pp.start()
	for process in totalProcesses_write:
		process.join()
	

def parallelWrite(ob, r, R1, aggr_bnd, itn, per, name, aggr_type, bndDown, bndUp, x, RS, n, finalGraph):
	averages = ob.returnAverages(R1, r, aggr_bnd)
	ob.writeAveragesToFile(averages, itn, per, name, aggr_bnd, aggr_type, bndDown, bndUp, x, RS, n, finalGraph)


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
