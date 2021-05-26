import matplotlib.pyplot as plt
from matplotlib.pyplot import *
import pandas as pd
import sys
import os

''' Global Variables'''
#paths = {"twitter":"results/twitter/"}
paths = {"twitter": "results_copy/v4-twitter-10/"}

network_name = sys.argv[1]

def returnFoldersAndFiles(path):
	listOfFolders = []
	listOfFiles = []
	listOfElements = os.listdir(paths[network_name])
	for i in listOfElements:
		tmp_path = path + i 
		if(os.path.isdir(tmp_path)):
			listOfFolders.append(i)
		else:
			listOfFiles.append(i)
	return(listOfFolders, listOfFiles)

tmp_path = paths[network_name]
while(True):
	[folders,files] = returnFoldersAndFiles(paths[network_name])
	if(len(folders) == 0):
		break
	else:
		for f in folders:
			tmp_path = tmp_path

# listFolders = os.listdir(paths[network_name])
# if(len(listFolders) > 0):
# 	for folder_models in listFolders:
# 		tmp_path = paths[network_name] + folder_models
# 		if(os.path.isdir(tmp_path)):
# 			tmp_path = tmp_path + "/"
# 			listOfIters = os.listdir(tmp_path)
# 			if(len(listOfIters) > 0):
# 				for folder_iter in listOfIters:
# 					tmp_path = paths[network_name] + folder_iter
# 					if(os.path.isdir(tmp_path)):
# 						tmp_path = tmp_path + "/"
# 						listOfElements = 

		
		#print(os.listdir(tmp_path))
		#os.path.isfile(path)
# else:
# 	print("Folder ' " + paths[network_name] + " ' is empty.")



# Import Data