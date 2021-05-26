from scipy import spatial
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial import distance
import scipy
import pandas as pd
import numpy as np
import json
import sys
import csv
import os


networkName = sys.argv[1]
percentage = int(sys.argv[3])
threshold = float(sys.argv[2])


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


def fillOutData(file):
	global data

	allModels = ['voter_1', 'voter_w', 'proposal1_w', 'proposal1_p', 
					'proposal1_wp', 'dg_1', 'dg_w', 'dg_p', 'dg_wp',
					'fj_w', 'fj_p', 'fj_wp', 'proposal3_w', 'proposal3_p',
					'proposal3_wp', 'proposal4_w', 'proposal4_p', 'proposal4_wp',
					"d_1.0_w", "d_0.5_w", "d_1.0_p", "d_0.5_p", "d_1.0_wp", "d_0.5_wp"]

	for line in file:
		if(line.replace("\n", "") in allModels):
			model = line.replace("\n", "")
			if(not(line.replace("\n", "") in data)):
				data[line.replace("\n", "")] = {}
		if("time_" in line):
			tmpLine = line.replace("\n", "").split(":")
			#index 0 = time_snapshot
			tmpLineTime = int(tmpLine[0].split("_")[1])

			#index 1 = percentages
			tmpLinePercentage = json.loads(tmpLine[1])

			if(not(tmpLineTime in data[model])):
				data[model][tmpLineTime] = tmpLinePercentage
			else:
				for i in range(0, len(tmpLinePercentage)):
					data[model][tmpLineTime][i] = data[model][tmpLineTime][i] + tmpLinePercentage[i]

readFiles = returnFoldersAndFiles("validResults/threshold_" + str(threshold) + "/" + str(percentage) + "/")[1]
data = {}
totalLenFiles = len(readFiles)
for f in readFiles:
	fl = open("validResults/threshold_" + str(threshold) + "/" + str(percentage) + "/" + f,  'r')
	fillOutData(fl)
	fl.close()


def writeCSFile(dt, path):
	global maxTime

	_file = open(path, "w")
	with _file:
		fieldNames = ["cosine_26", "jaccard_26", "pearsonr_26", "spearman_26", "cosine_22", "jaccard_22", "pearsonr_22", "spearman_22"]
		writer = csv.DictWriter(_file, fieldnames = fieldNames)
		writer.writeheader()

		for tm in range(0, maxTime + 1):
			writer.writerow(dt[tm])
	_file.close()


def removeSpikes(vctr):
	#remove index: 0, 2, 6, 10
	newVector_1 = vctr[1:2]
	newVector_2 = vctr[3:6]
	newVector_3 = vctr[7:10]
	newVector_4 = vctr[11:]
	newVector = newVector_1 + newVector_2 + newVector_3 + newVector_4
	return(newVector)


#calculate the average
maxTime = 0
for m in data:
	for t in data[m]:
		for i in range(0, len(data[m][t])):
			data[m][t][i] = float(data[m][t][i]) / totalLenFiles
		if(t > maxTime):
			maxTime = t


standardVector_tmp = [0.7443693693693694,0.25563063063063063,0.6970720720720721,0.1891891891891892,0.06644144144144144,0.0472972972972973,0.9091093917499097,0.04079549364338705,0.04592514238756146,0.0041699722191417795,0.8728563296535575,0.03934650628445388,0.04160504015769757,0.0027086663236296957,0.03162196000056344,0.0014376066293966111,0.009520104535131045,9.037864155702327E-4,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
standardVector = []
for i in standardVector_tmp:
	standardVector.append(100*i)

tittleMap = {'voter_1': "Voter", 'voter_w':"weightedVoter", 'proposal1_w':"proposal1_w", 'proposal1_p':"proposal1_p", 
					'proposal1_wp':"proposal1_wp", 'dg_1':"degroot_1", 'dg_w':"degroot_w", 'dg_p':"degroot_p", 'dg_wp':"degroot_wp",
					'fj_w':"fj_w", 'fj_p':"fj_p", 'fj_wp':"fj_wp", 'proposal3_w':"proposal3_w", 'proposal3_p':"proposal3_p",
					'proposal3_wp':"proposal3_wp", 'proposal4_w':"proposal4_w", 'proposal4_p':"proposal4_p", 'proposal4_wp':"proposal4_wp",
					"d_1.0_w":"proposal2_w_1.0", "d_0.5_w":"proposal2_w_0.5", "d_1.0_p":"proposal2_p_1.0", "d_0.5_p":"proposal2_p_0.5", "d_1.0_wp":"proposal2_wp_1.0", "d_0.5_wp":"proposal2_wp_0.5"}

for md in data:
	writeDict = {}
	for tm in range(0, maxTime + 1):
		cosineSimilarity = 1 - spatial.distance.cosine(standardVector, data[md][tm])
		jaccardSimilarity = distance.jaccard(standardVector, data[md][tm])
		pearsonrCorrelation = scipy.stats.pearsonr(standardVector, data[md][tm])
		spearmanCorrelation = scipy.stats.spearmanr(standardVector, data[md][tm])
		
		
		cosineSimilarity_removeSpikes = 1 - spatial.distance.cosine(removeSpikes(standardVector), removeSpikes(data[md][tm]))
		jaccardSimilarity_removeSpikes = distance.jaccard(removeSpikes(standardVector), removeSpikes(data[md][tm]))
		pearsonrCorrelation_removeSpikes = scipy.stats.pearsonr(removeSpikes(standardVector), removeSpikes(data[md][tm]))
		spearmanCorrelation_removeSpikes = scipy.stats.spearmanr(removeSpikes(standardVector), removeSpikes(data[md][tm]))

		writeDict[tm] = {"cosine_26": cosineSimilarity, "jaccard_26": jaccardSimilarity, "pearsonr_26": {"correlation":pearsonrCorrelation[0], "pvalue":pearsonrCorrelation[1]}, "spearman_26": {"correlation":spearmanCorrelation[0], "pvalue":spearmanCorrelation[1]},
						"cosine_22":cosineSimilarity_removeSpikes, "jaccard_22": jaccardSimilarity_removeSpikes, "pearsonr_22":{"correlation":pearsonrCorrelation_removeSpikes[0], "pvalue":pearsonrCorrelation_removeSpikes[1]}, "spearman_22": {"correlation":spearmanCorrelation_removeSpikes[0], "pvalue":spearmanCorrelation_removeSpikes[1]}}
	writeCSFile(writeDict, "similarityFiles/threshold_" + str(threshold) + "/" + str(percentage) + "/" + tittleMap[md] + ".csv")
	