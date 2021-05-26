import networkx as nx
import multiprocessing
import numpy as np
import random
import time
import os


class ValidationVoter:

	def __init__(self, graph):
		self.graph = graph
		self.processData = {}
		for eachNode in self.graph.nodes():
			self.processData[eachNode] = np.asarray([self.graph.node[eachNode]["init"]])

	def voter_model(self, selectedEdges, dBnds_down, dBnds_up, dBnds_step, bndUp):
		start_time = time.time()

		'''
		Code for the validation
		'''
		vector = {}
		snapshoot = 0
		vector["time_" + str(snapshoot)] = self.returnEdgesUsersVector()

		tmp_ed = 0
		variableSnapshoots = 10
		tmpStep = int(len(selectedEdges) / variableSnapshoots)
		tmpStep_ = int(len(selectedEdges) / variableSnapshoots)


		for e in selectedEdges:
			#voter_1
			self.graph.node[e[0]]['voter_1'] = self.graph.node[e[1]]['voter_1']

			#voter_w
			self.graph.node[e[0]]['voter_w'] = self.graph.get_edge_data(e[0], e[1])["weight"] * self.graph.node[e[1]]['voter_w']

			maxValue_proposal1_w = -1
			maxValue_proposal1_p = -1
			maxValue_proposal1_wp = -1
			maxValue_proposal2 = {"w":{}, "p":{}, "wp":{}}
			tmp_v = dBnds_down
			while(True):
				for i in maxValue_proposal2:
					maxValue_proposal2[i][tmp_v] = -1
				tmp_v = tmp_v + dBnds_step
				if(tmp_v > dBnds_up):
					break

			sumDegroot = {"1": 0, "w": 0, "p": 0, "wp": 0}
			sumFj = {"w": 0, "p": 0, "wp": 0}
			sumProposal3 = {"A": {"w": 1, "p": self.graph.node[e[0]]['power'], "wp": self.graph.node[e[0]]['power']}, "score": {"w": self.graph.node[e[0]]["proposal3_w"], "p": self.graph.node[e[0]]["proposal3_p"], "wp": self.graph.node[e[0]]["proposal3_wp"]}}
			sumProposal4 = {"A": {"w": 2, "p": 2*self.graph.node[e[0]]['power'], "wp": 2*self.graph.node[e[0]]['power']}, "score": {"w": self.graph.node[e[0]]["proposal4_w"] + self.graph.node[e[0]]["init"], "p": self.graph.node[e[0]]["proposal4_p"] + self.graph.node[e[0]]["init"], "wp": self.graph.node[e[0]]["proposal4_wp"] + self.graph.node[e[0]]["init"]}}
			countOfNeighbors = 0
			for nei in self.graph.neighbors(e[0]):
				countOfNeighbors = countOfNeighbors + 1
				sumDegroot["1"] = sumDegroot["1"] + self.graph.node[nei]['dg_1']
				sumDegroot["w"] = sumDegroot["w"] + self.graph.get_edge_data(e[0], nei)["weight"] * self.graph.node[nei]['dg_w']
				sumDegroot["p"] = sumDegroot["p"] + self.graph.node[nei]['power'] * self.graph.node[nei]['dg_p']
				sumDegroot["wp"] = sumDegroot["wp"] + self.graph.get_edge_data(e[0], nei)["weight"] * self.graph.node[nei]['power'] * self.graph.node[nei]['dg_wp']

				sumFj["w"] = sumFj["w"] + self.graph.get_edge_data(e[0], nei)["weight"] * self.graph.node[nei]['fj_w']
				sumFj["p"] = sumFj["p"] + self.graph.node[nei]['power'] * self.graph.node[nei]['fj_p']
				sumFj["wp"] = sumFj["wp"] + self.graph.get_edge_data(e[0], nei)["weight"] * self.graph.node[nei]['power'] * self.graph.node[nei]['fj_wp']

				sumProposal3["A"]["w"] = sumProposal3["A"]["w"] + self.graph.get_edge_data(e[0], nei)["weight"]
				sumProposal3["A"]["p"] = sumProposal3["A"]["p"] + self.graph.node[nei]['power']
				sumProposal3["A"]["wp"] = sumProposal3["A"]["wp"] + self.graph.get_edge_data(e[0], nei)["weight"] * self.graph.node[nei]['power']
				sumProposal3["score"]["w"] = sumProposal3["score"]["w"] + self.graph.node[nei]["proposal3_w"]
				sumProposal3["score"]["p"] = sumProposal3["score"]["p"] + self.graph.node[nei]["proposal3_p"]
				sumProposal3["score"]["wp"] = sumProposal3["score"]["wp"] + self.graph.node[nei]["proposal3_wp"]

				sumProposal4["A"]["w"] = sumProposal4["A"]["w"] + self.graph.get_edge_data(e[0], nei)["weight"]
				sumProposal4["A"]["p"] = sumProposal4["A"]["p"] + self.graph.node[nei]['power']
				sumProposal4["A"]["wp"] = sumProposal4["A"]["wp"] + self.graph.get_edge_data(e[0], nei)["weight"] * self.graph.node[nei]['power']
				sumProposal4["score"]["w"] = sumProposal4["score"]["w"] + self.graph.node[nei]["proposal4_w"]
				sumProposal4["score"]["p"] = sumProposal4["score"]["p"] + self.graph.node[nei]["proposal4_p"]
				sumProposal4["score"]["wp"] = sumProposal4["score"]["wp"] + self.graph.node[nei]["proposal4_wp"]


				tmp_score = self.graph.node[e[0]]['proposal1_w'] * self.graph.get_edge_data(e[0], nei)["weight"] + self.graph.node[nei]['proposal1_w'] * self.graph.get_edge_data(e[0], nei)["weight"]
				if(abs(tmp_score) > maxValue_proposal1_w):
					maxValue_proposal1_w = abs(tmp_score)

				tmp_score = self.graph.node[e[0]]['proposal1_p'] * self.graph.node[e[0]]['power'] + self.graph.node[nei]['proposal1_p'] * self.graph.node[nei]['power']
				if(abs(tmp_score) > maxValue_proposal1_p):
					maxValue_proposal1_p = abs(tmp_score)

				tmp_score = self.graph.node[e[0]]['proposal1_wp'] * self.graph.node[e[0]]['power'] * self.graph.get_edge_data(e[0], nei)["weight"] + self.graph.node[nei]['proposal1_wp'] * self.graph.node[nei]['power'] * self.graph.get_edge_data(e[0], nei)["weight"]
				if(abs(tmp_score) > maxValue_proposal1_wp):
					maxValue_proposal1_wp = abs(tmp_score)

				for d in maxValue_proposal2["w"]:
					tmp_attr_name = "d_" + str(d) + "_w"
					tmp_score = self.graph.node[e[0]][tmp_attr_name] * self.graph.get_edge_data(e[0], nei)["weight"] + self.graph.node[nei][tmp_attr_name] * self.graph.get_edge_data(e[0], nei)["weight"]
					if(abs(tmp_score) > maxValue_proposal2["w"][d]):
						maxValue_proposal2["w"][d] = abs(tmp_score)

					tmp_attr_name = "d_" + str(d) + "_p"
					tmp_score = self.graph.node[e[0]][tmp_attr_name] * self.graph.node[e[0]]['power'] + self.graph.node[nei][tmp_attr_name] * self.graph.node[nei]['power']
					if(abs(tmp_score) > maxValue_proposal2["p"][d]):
						maxValue_proposal2["p"][d] = abs(tmp_score)

					tmp_attr_name = "d_" + str(d) + "_wp"
					tmp_score = self.graph.node[e[0]][tmp_attr_name] * self.graph.node[e[0]]['power'] * self.graph.get_edge_data(e[0], nei)["weight"] + self.graph.node[nei][tmp_attr_name] * self.graph.node[nei]['power'] * self.graph.get_edge_data(e[0], nei)["weight"]
					if(abs(tmp_score) > maxValue_proposal2["wp"][d]):
						maxValue_proposal2["wp"][d] = abs(tmp_score)


			#proposal1_w
			self.graph.node[e[0]]['proposal1_w'] =  self.graph.node[e[0]]['proposal1_w'] * self.graph.get_edge_data(e[0], e[1])["weight"] + self.graph.node[e[1]]['proposal1_w'] * self.graph.get_edge_data(e[0], e[1])["weight"]
			if(not(maxValue_proposal1_w == 0)):
				self.graph.node[e[0]]['proposal1_w'] = float(self.graph.node[e[0]]['proposal1_w']) / maxValue_proposal1_w
			else:
				self.graph.node[e[0]]['proposal1_w'] = 0

			#proposal1_p
			self.graph.node[e[0]]['proposal1_p'] =  self.graph.node[e[0]]['proposal1_p'] * self.graph.node[e[0]]['power'] + self.graph.node[e[1]]['proposal1_p'] * self.graph.node[e[1]]['power']
			if(not(maxValue_proposal1_p == 0)):
				self.graph.node[e[0]]['proposal1_p'] = float(self.graph.node[e[0]]['proposal1_p']) / maxValue_proposal1_p
			else:
				self.graph.node[e[0]]['proposal1_p'] = 0

			#proposal1_wp
			self.graph.node[e[0]]['proposal1_wp'] =  self.graph.node[e[0]]['proposal1_wp'] * self.graph.node[e[0]]['power'] * self.graph.get_edge_data(e[0], e[1])["weight"] + self.graph.node[e[1]]['proposal1_wp'] * self.graph.node[e[1]]['power'] * self.graph.get_edge_data(e[0], e[1])["weight"]
			if(not(maxValue_proposal1_wp == 0)):
				self.graph.node[e[0]]['proposal1_wp'] = float(self.graph.node[e[0]]['proposal1_wp']) / maxValue_proposal1_wp
			else:
				self.graph.node[e[0]]['proposal1_wp'] = 0

			#proposal2_d
			tmp_v = dBnds_down
			while(True):
				tmp_attr_name = "d_" + str(tmp_v) + "_"
				#w
				if(abs(self.graph.node[e[0]][tmp_attr_name + "w"] * self.graph.get_edge_data(e[0], e[1])["weight"] - self.graph.node[e[1]][tmp_attr_name + "w"] * self.graph.get_edge_data(e[0], e[1])["weight"]) < tmp_v):
					self.graph.node[e[0]][tmp_attr_name + "w"] = self.graph.node[e[0]][tmp_attr_name + "w"] * self.graph.get_edge_data(e[0], e[1])["weight"] + self.graph.node[e[1]][tmp_attr_name + "w"] * self.graph.get_edge_data(e[0], e[1])["weight"]
					if(not(maxValue_proposal2["w"][tmp_v] == 0)):
						self.graph.node[e[0]][tmp_attr_name + "w"] = float(self.graph.node[e[0]][tmp_attr_name + "w"]) / maxValue_proposal2["w"][tmp_v]
					else:
						self.graph.node[e[0]][tmp_attr_name + "w"] = 0

				#p
				if(abs(self.graph.node[e[0]][tmp_attr_name + "p"] * self.graph.node[e[0]]['power'] - self.graph.node[e[1]][tmp_attr_name + "p"] * self.graph.node[e[1]]['power']) < tmp_v):
					self.graph.node[e[0]][tmp_attr_name + "p"] = self.graph.node[e[0]][tmp_attr_name + "p"] * self.graph.node[e[0]]['power'] + self.graph.node[e[1]][tmp_attr_name + "p"] * self.graph.node[e[1]]['power']
					if(not(maxValue_proposal2["p"][tmp_v] == 0)):
						self.graph.node[e[0]][tmp_attr_name + "p"] = float(self.graph.node[e[0]][tmp_attr_name + "p"]) / maxValue_proposal2["p"][tmp_v]
					else:
						self.graph.node[e[0]][tmp_attr_name + "p"] = 0

				#wp
				if(abs(self.graph.node[e[0]][tmp_attr_name + "wp"] * self.graph.node[e[0]]['power'] * self.graph.get_edge_data(e[0], e[1])["weight"] - self.graph.node[e[1]][tmp_attr_name + "wp"] * self.graph.node[e[1]]['power'] * self.graph.get_edge_data(e[0], e[1])["weight"]) < tmp_v):
					self.graph.node[e[0]][tmp_attr_name + "wp"] = self.graph.node[e[0]][tmp_attr_name + "wp"] * self.graph.node[e[0]]['power'] * self.graph.get_edge_data(e[0], e[1])["weight"] + self.graph.node[e[1]][tmp_attr_name + "wp"] * self.graph.node[e[1]]['power'] * self.graph.get_edge_data(e[0], e[1])["weight"]
					if(not(maxValue_proposal2["wp"][tmp_v] == 0)):
						self.graph.node[e[0]][tmp_attr_name + "wp"] = float(self.graph.node[e[0]][tmp_attr_name + "wp"]) / maxValue_proposal2["wp"][tmp_v]
					else:
						self.graph.node[e[0]][tmp_attr_name + "wp"] = 0

				tmp_v = tmp_v + dBnds_step
				if(tmp_v > dBnds_up):
					break

			#degroot adjusments
			denominator = countOfNeighbors + 1

			#1
			numerator = sumDegroot["1"] + self.graph.node[e[0]]['dg_1']
			self.graph.node[e[0]]['dg_1'] = float(numerator) / denominator

			#w
			numerator = sumDegroot["w"] + self.graph.node[e[0]]['dg_w']
			self.graph.node[e[0]]['dg_w'] = float(numerator) / denominator

			#p
			numerator = sumDegroot["p"] + self.graph.node[e[0]]['power'] * self.graph.node[e[0]]['dg_p']
			self.graph.node[e[0]]['dg_p'] = float(numerator) / denominator

			#wp
			numerator = sumDegroot["wp"] + self.graph.node[e[0]]['power'] * self.graph.node[e[0]]['dg_wp']
			self.graph.node[e[0]]['dg_wp'] = float(numerator) / denominator


			#fj adjusments
			denominator = countOfNeighbors + 2

			#w
			numerator = sumFj["w"] + self.graph.node[e[0]]['fj_w'] + self.graph.node[e[0]]['init']
			self.graph.node[e[0]]['fj_w'] = float(numerator) / denominator

			#p
			numerator = sumFj["p"] + self.graph.node[e[0]]['power'] * (self.graph.node[e[0]]['fj_p'] + self.graph.node[e[0]]['init'])
			self.graph.node[e[0]]['fj_p'] = float(numerator) / denominator

			#wp
			numerator = sumFj["wp"] + self.graph.node[e[0]]['power'] * (self.graph.node[e[0]]['fj_wp'] + self.graph.node[e[0]]['init'])
			self.graph.node[e[0]]['fj_wp'] = float(numerator) / denominator


			#proposal3
			denominator = (countOfNeighbors + 1) * (countOfNeighbors + 1)

			#w
			numerator = sumProposal3["A"]["w"] * sumProposal3["score"]["w"]
			self.graph.node[e[0]]['proposal3_w'] = float(numerator) / denominator

			#p
			numerator = sumProposal3["A"]["p"] * sumProposal3["score"]["p"]
			self.graph.node[e[0]]['proposal3_p'] = float(numerator) / denominator

			#wp
			numerator = sumProposal3["A"]["wp"] * sumProposal3["score"]["wp"]
			self.graph.node[e[0]]['proposal3_wp'] = float(numerator) / denominator


			#proposal4
			denominator = (countOfNeighbors + 2) * (countOfNeighbors + 2)

			#w
			numerator = sumProposal4["A"]["w"] * sumProposal4["score"]["w"]
			self.graph.node[e[0]]['proposal4_w'] = float(numerator) / denominator

			#p
			numerator = sumProposal4["A"]["p"] * sumProposal4["score"]["p"]
			self.graph.node[e[0]]['proposal4_p'] = float(numerator) / denominator

			#wp
			numerator = sumProposal4["A"]["wp"] * sumProposal4["score"]["wp"]
			self.graph.node[e[0]]['proposal4_wp'] = float(numerator) / denominator

			tmp_ed = tmp_ed + 1
			tmpStep_ = tmpStep_ - 1
			equal = "false"
			if(tmpStep_ == 0):
				print("tmp_ed: " + str(tmp_ed))
				tmpStep_ = tmpStep
				snapshoot = snapshoot + 1
				vector["time_" + str(snapshoot)] = self.returnEdgesUsersVector()
				if(tmp_ed == len(selectedEdges)):
					equal = "true"
				else:
					equal = "false"
			
			if(tmp_ed == len(selectedEdges) and tmpStep_ > 0 and equal == "false"):
				print("FINAL SNAPSHOOT")
				snapshoot = snapshoot + 1
				vector["time_" + str(snapshoot)] = self.returnEdgesUsersVector()
		return(vector)

	def returnEdgesUsersVector(self):
		returnVariable = {}
		allModels = ['voter_1', 'voter_w', 'proposal1_w', 'proposal1_p', 
					'proposal1_wp', 'dg_1', 'dg_w', 'dg_p', 'dg_wp',
					'fj_w', 'fj_p', 'fj_wp', 'proposal3_w', 'proposal3_p',
					'proposal3_wp', 'proposal4_w', 'proposal4_p', 'proposal4_wp',
					"d_1.0_w", "d_0.5_w", "d_1.0_p", "d_0.5_p", "d_1.0_wp", "d_0.5_wp"]
		
		#Threshold -> will change after the upcoming meeting
		aggressionScoreThreshold = 0.50
		for eachModel in allModels:
			edgesResults = []
			allEdges = self.graph.edges()
			normal_normal = 0
			normal_aggressive = 0
			aggressive_normal = 0
			aggressive_aggressive = 0
			for edge in allEdges:
				node_i = edge[0]
				node_j = edge[1]
				if(float(self.graph.node[node_i][eachModel]) < aggressionScoreThreshold and float(self.graph.node[node_j][eachModel]) < aggressionScoreThreshold):
					normal_normal = normal_normal + 1
				if(float(self.graph.node[node_i][eachModel]) < aggressionScoreThreshold and float(self.graph.node[node_j][eachModel]) > aggressionScoreThreshold):
					normal_aggressive = normal_aggressive + 1
				if(float(self.graph.node[node_i][eachModel]) > aggressionScoreThreshold and float(self.graph.node[node_j][eachModel]) < aggressionScoreThreshold):
					aggressive_normal = aggressive_normal + 1
				if(float(self.graph.node[node_i][eachModel]) > aggressionScoreThreshold and float(self.graph.node[node_j][eachModel]) > aggressionScoreThreshold):
					aggressive_aggressive = aggressive_aggressive + 1
			normal_normal = float(normal_normal)*100 / self.graph.number_of_edges()
			normal_aggressive = float(normal_aggressive)*100 / self.graph.number_of_edges()
			aggressive_normal = float(aggressive_normal)*100 / self.graph.number_of_edges()
			aggressive_aggressive = float(aggressive_aggressive)*100 / self.graph.number_of_edges()
			edgesResults.append(normal_normal)
			edgesResults.append(normal_aggressive)
			edgesResults.append(aggressive_normal)
			edgesResults.append(aggressive_aggressive)

			usersResults = []
			allNodes = self.graph.nodes()
			normal_normal = 0
			normal_aggressive = 0
			aggressive_normal = 0
			aggressive_aggressive = 0
			for nd in allNodes:
				if(float(self.graph.node[nd]['init']) < aggressionScoreThreshold and float(self.graph.node[nd][eachModel]) < aggressionScoreThreshold):
					normal_normal = normal_normal + 1
				if(float(self.graph.node[nd]['init']) < aggressionScoreThreshold and float(self.graph.node[nd][eachModel]) > aggressionScoreThreshold):
					normal_aggressive = normal_aggressive + 1
				if(float(self.graph.node[nd]['init']) > aggressionScoreThreshold and float(self.graph.node[nd][eachModel]) < aggressionScoreThreshold):
					aggressive_normal = aggressive_normal + 1
				if(float(self.graph.node[nd]['init']) > aggressionScoreThreshold and float(self.graph.node[nd][eachModel]) > aggressionScoreThreshold):
					aggressive_aggressive = aggressive_aggressive + 1
			normal_normal = float(normal_normal)*100 / self.graph.number_of_nodes()
			normal_aggressive = float(normal_aggressive)*100 / self.graph.number_of_nodes()
			aggressive_normal = float(aggressive_normal)*100 / self.graph.number_of_nodes()
			aggressive_aggressive = float(aggressive_aggressive)*100 / self.graph.number_of_nodes()
			usersResults.append(normal_normal)
			usersResults.append(normal_aggressive)
			usersResults.append(aggressive_normal)
			usersResults.append(aggressive_aggressive)

			returnVariable[eachModel] = edgesResults + usersResults

		print("------------------")
		return(returnVariable)
