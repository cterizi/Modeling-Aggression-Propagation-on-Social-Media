import multiprocessing
from Voter import *
import random
import time
import csv
import os

def returnOneSelectedAndNondeSelectedNode(selectedList):
	allSelectedNodes = []
	nodesJ = []
	for edge in selectedList:
		allSelectedNodes.append(edge[0])
		nodesJ.append(edge[1])

	selectedNode = allSelectedNodes[0]
	NonSelectedNode = list(set(nodesJ).difference(set(allSelectedNodes)))[0]

	return(selectedNode, NonSelectedNode)


def returnFoldersAndFiles(path):
	listOfFolders = []
	listOfFiles = []
	listOfElements = os.listdir(path)
	for i in listOfElements:
		tmp_path = path + "/" + i
		if(os.path.isdir(tmp_path)):
			listOfFolders.append(i)
		else:
			listOfFiles.append(i)
	return(listOfFolders, listOfFiles)


def voterObject(graph, iteration, network_name, aggressive_bound, aggr_init_type, boundDown, boundUp, selectedEdges, RorS, dBnd_down, dBnd_up, dBnd_step, seedNumber):
	totalProcesses_voter = []
	for percentage in selectedEdges:
		p = multiprocessing.Process(target = parallelVoter, args=(graph, iteration, network_name, aggressive_bound, aggr_init_type, boundDown, boundUp, selectedEdges[percentage], percentage, RorS, dBnd_down, dBnd_up, dBnd_step, seedNumber))
		totalProcesses_voter.append(p)
		p.start()
	for process in totalProcesses_voter:
		process.join()
def parallelVoter(graph, iteration, network_name, aggressive_bound, aggr_init_type, boundDown, boundUp, selectedEdges, percentage, RorS, dBnd_down, dBnd_up, dBnd_step, seedNum):
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
	sortedID = list(R[0].nodes())
	sortedID.sort()

	modelsList = returnFoldersAndFiles("validationResults/")[0]
	for model in modelsList:
		print(model)
		if(not("proposal2" in model)):
			continue
			if(not(os.path.isdir("validationResults/" + model + "/" + str(percentage) + "/"))):
				os.mkdir("validationResults/" + model + "/" + str(percentage) + "/")
			else:
				if(len(returnFoldersAndFiles("validationResults/" + model + "/" + str(percentage) + "/")[1]) > 0):
					for ii in returnFoldersAndFiles("validationResults/" + model + "/" + str(percentage) + "/")[1]:
						os.remove("validationResults/" + model + "/" + str(percentage) + "/" + ii)
		
			if(not(os.path.isdir("validationResults/" + model + "/" + str(percentage) + "/" + seedNum + "/"))):
				os.mkdir("validationResults/" + model + "/" + str(percentage) + "/" + seedNum + "/")
		
			filePath = "validationResults/" + model + "/" + str(percentage) + "/" + seedNum + "/" +  RorS + ".csv"
			if(os.path.isfile(filePath)):
				os.remove(filePath)
		
			writeCSVfile(sortedID, selectedEdges, R[0], filePath, model)
		else:
			if(not(os.path.isdir("validationResults/" + model + "/" + str(percentage) + "/"))):
				os.mkdir("validationResults/" + model + "/" + str(percentage) + "/")
			
			if(not(os.path.isdir("validationResults/" + model + "/" + str(percentage) + "/" + seedNum + "/"))):
				os.mkdir("validationResults/" + model + "/" + str(percentage) + "/" + seedNum + "/")

			if(not(os.path.isdir("validationResults/" + model + "/" + str(percentage) + "/" + seedNum + "/" + str(0.5) + "/"))):
				os.mkdir("validationResults/" + model + "/" + str(percentage) + "/" + seedNum + "/0.5/")
			else:
				print(model+"_0.5")
				filePath = "validationResults/" + model + "/" + str(percentage) + "/" + seedNum + "/0.5/" +  RorS + ".csv"
				writeCSVfile(sortedID, selectedEdges, R[0], filePath, model+"_0.5")

			if(not(os.path.isdir("validationResults/" + model + "/" + str(percentage) + "/" + seedNum + "/" + str(1.0) + "/"))):
				os.mkdir("validationResults/" + model + "/" + str(percentage) + "/" + seedNum + "/1.0/")
			else:
				print(model+"_1.0")
				filePath = "validationResults/" + model + "/" + str(percentage) + "/" + seedNum + "/1.0/" +  RorS + ".csv"
				writeCSVfile(sortedID, selectedEdges, R[0], filePath, model+"_1.0")


	print("----------------------------")
	

def writeCSVfile(ids, edges, data, path, model):
	mapModel = {"degroot_wp": "dg_wp", "proposal4_p":"proposal4_p", "fj_w":"fj_w", "voter":"voter_1", 
			"degroot_w":"dg_w", "degroot_p":"dg_p", "weightedVoter":"voter_w", "fj_wp":"fj_wp",
			 "proposal4_w":"proposal4_w", "proposal3_p":"proposal3_p", "proposal3_w":"proposal3_w",
			 "fj_p":"fj_p", "proposal1_wp":"proposal1_wp", "degroot_1":"dg_1", "proposal1_w":"proposal1_w", 
			"proposal4_wp":"proposal4_wp", "proposal3_wp":"proposal3_wp", "proposal1_p":"proposal1_p",
			"proposal2_w_0.5":"d_0.5_w", "proposal2_w_1.0":"d_1.0_w", "proposal2_p_0.5":"d_0.5_p", "proposal2_p_1.0":"d_1.0_p",
			"proposal2_wp_0.5":"d_0.5_wp", "proposal2_wp_1.0":"d_1.0_wp"}
	dict_ = {}

	for node in ids:
		dict_[node] = {}
		dict_[node]["userId"] = node
		dict_[node]["init"] = data.node[node]["init"]
		dict_[node]["final"] = data.node[node][mapModel[model]]

	
	file_ = open(path, "w")
	with file_:
		fieldNames = ["userId", "init", "final"]
		writer = csv.DictWriter(file_, fieldnames = fieldNames)
		writer.writeheader()
		for n in ids:
			writer.writerow(dict_[n])

		writer = csv.writer(file_)
		writer.writerow([-1, -1, -1])
		for edge in edges:
			writer.writerow([edge[0], edge[1], -1])
	file_.close()
	

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
