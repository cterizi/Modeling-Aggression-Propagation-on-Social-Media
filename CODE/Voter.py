import networkx as nx
import multiprocessing
import numpy as np
import random
import time
import os

path_rdm = "results/twitter/random/"
path_srt = "results/twitter/sorted/"
path_plrCr = "results/twitter/popularity_increase/"
path_plrDsc = "results/twitter/popularity_descending/"
path_neig = "results/twitter/neighborhood/"

paths = {"twitter": {
					"random":
					{"voter_1": path_rdm + "voter/iter_", "voter_w": path_rdm + "weightedVoter/iter_",
					"proposal1_w": path_rdm + "proposal1_w/iter_", "proposal1_p": path_rdm + "proposal1_p/iter_", "proposal1_wp": path_rdm + "proposal1_wp/iter_",
					"proposal2_w": path_rdm + "proposal2_w/iter_", "proposal2_p": path_rdm + "proposal2_p/iter_", "proposal2_wp": path_rdm + "proposal2_wp/iter_",
					"degroot_1": path_rdm + "degroot_1/iter_", "degroot_w": path_rdm + "degroot_w/iter_", "degroot_p": path_rdm + "degroot_p/iter_", "degroot_wp": path_rdm + "degroot_wp/iter_",
					"fj_w": path_rdm + "fj_w/iter_", "fj_p": path_rdm + "fj_p/iter_", "fj_wp": path_rdm + "fj_wp/iter_",
					"proposal3_w": path_rdm + "proposal3_w/iter_", "proposal3_p": path_rdm + "proposal3_p/iter_", "proposal3_wp": path_rdm + "proposal3_wp/iter_",
					"proposal4_w": path_rdm + "proposal4_w/iter_", "proposal4_p": path_rdm + "proposal4_p/iter_", "proposal4_wp": path_rdm + "proposal4_wp/iter_"
					}, 
					"sorted": 
					{"voter_1": path_srt + "voter/iter_", "voter_w": path_srt + "weightedVoter/iter_",
					"proposal1_w": path_srt + "proposal1_w/iter_", "proposal1_p": path_srt + "proposal1_p/iter_", "proposal1_wp": path_srt + "proposal1_wp/iter_",
					"proposal2_w": path_srt + "proposal2_w/iter_", "proposal2_p": path_srt + "proposal2_p/iter_", "proposal2_wp": path_srt + "proposal2_wp/iter_",
					"degroot_1": path_srt + "degroot_1/iter_", "degroot_w": path_srt + "degroot_w/iter_", "degroot_p": path_srt + "degroot_p/iter_", "degroot_wp": path_srt + "degroot_wp/iter_",
					"fj_w": path_srt + "fj_w/iter_", "fj_p": path_srt + "fj_p/iter_", "fj_wp": path_srt + "fj_wp/iter_",
					"proposal3_w": path_srt + "proposal3_w/iter_", "proposal3_p": path_srt + "proposal3_p/iter_", "proposal3_wp": path_srt + "proposal3_wp/iter_",
					"proposal4_w": path_srt + "proposal4_w/iter_", "proposal4_p": path_srt + "proposal4_p/iter_", "proposal4_wp": path_srt + "proposal4_wp/iter_"
					},
					"popularity_increase":
					{"voter_1": path_plrCr + "voter/iter_", "voter_w": path_plrCr + "weightedVoter/iter_",
					"proposal1_w": path_plrCr + "proposal1_w/iter_", "proposal1_p": path_plrCr + "proposal1_p/iter_", "proposal1_wp": path_plrCr + "proposal1_wp/iter_",
					"proposal2_w": path_plrCr + "proposal2_w/iter_", "proposal2_p": path_plrCr + "proposal2_p/iter_", "proposal2_wp": path_plrCr + "proposal2_wp/iter_",
					"degroot_1": path_plrCr + "degroot_1/iter_", "degroot_w": path_plrCr + "degroot_w/iter_", "degroot_p": path_plrCr + "degroot_p/iter_", "degroot_wp": path_plrCr + "degroot_wp/iter_",
					"fj_w": path_plrCr + "fj_w/iter_", "fj_p": path_plrCr + "fj_p/iter_", "fj_wp": path_plrCr + "fj_wp/iter_",
					"proposal3_w": path_plrCr + "proposal3_w/iter_", "proposal3_p": path_plrCr + "proposal3_p/iter_", "proposal3_wp": path_plrCr + "proposal3_wp/iter_",
					"proposal4_w": path_plrCr + "proposal4_w/iter_", "proposal4_p": path_plrCr + "proposal4_p/iter_", "proposal4_wp": path_plrCr + "proposal4_wp/iter_"
					},
					"popularity_descending":
					{"voter_1": path_plrDsc + "voter/iter_", "voter_w": path_plrDsc + "weightedVoter/iter_",
					"proposal1_w": path_plrDsc + "proposal1_w/iter_", "proposal1_p": path_plrDsc + "proposal1_p/iter_", "proposal1_wp": path_plrDsc + "proposal1_wp/iter_",
					"proposal2_w": path_plrDsc + "proposal2_w/iter_", "proposal2_p": path_plrDsc + "proposal2_p/iter_", "proposal2_wp": path_plrDsc + "proposal2_wp/iter_",
					"degroot_1": path_plrDsc + "degroot_1/iter_", "degroot_w": path_plrDsc + "degroot_w/iter_", "degroot_p": path_plrDsc + "degroot_p/iter_", "degroot_wp": path_plrDsc + "degroot_wp/iter_",
					"fj_w": path_plrDsc + "fj_w/iter_", "fj_p": path_plrDsc + "fj_p/iter_", "fj_wp": path_plrDsc + "fj_wp/iter_",
					"proposal3_w": path_plrDsc + "proposal3_w/iter_", "proposal3_p": path_plrDsc + "proposal3_p/iter_", "proposal3_wp": path_plrDsc + "proposal3_wp/iter_",
					"proposal4_w": path_plrDsc + "proposal4_w/iter_", "proposal4_p": path_plrDsc + "proposal4_p/iter_", "proposal4_wp": path_plrDsc + "proposal4_wp/iter_"
					},
					"neighborhood":
					{"voter_1": path_neig + "voter/iter_", "voter_w": path_neig + "weightedVoter/iter_",
					"proposal1_w": path_neig + "proposal1_w/iter_", "proposal1_p": path_neig + "proposal1_p/iter_", "proposal1_wp": path_neig + "proposal1_wp/iter_",
					"proposal2_w": path_neig + "proposal2_w/iter_", "proposal2_p": path_neig + "proposal2_p/iter_", "proposal2_wp": path_neig + "proposal2_wp/iter_",
					"degroot_1": path_neig + "degroot_1/iter_", "degroot_w": path_neig + "degroot_w/iter_", "degroot_p": path_neig + "degroot_p/iter_", "degroot_wp": path_neig + "degroot_wp/iter_",
					"fj_w": path_neig + "fj_w/iter_", "fj_p": path_neig + "fj_p/iter_", "fj_wp": path_neig + "fj_wp/iter_",
					"proposal3_w": path_neig + "proposal3_w/iter_", "proposal3_p": path_neig + "proposal3_p/iter_", "proposal3_wp": path_neig + "proposal3_wp/iter_",
					"proposal4_w": path_neig + "proposal4_w/iter_", "proposal4_p": path_neig + "proposal4_p/iter_", "proposal4_wp": path_neig + "proposal4_wp/iter_"
					}
					}
		}

class Voter:

	def __init__(self, graph):
		self.graph = graph
		self.processData = {}
		for eachNode in self.graph.nodes():
			self.processData[eachNode] = np.asarray([self.graph.node[eachNode]["init"]])

	def voter_model(self, selectedEdges, dBnds_down, dBnds_up, dBnds_step, bndUp):
		start_time = time.time()
		
		iterCheck = [5000, 10000, 20000, 50000, 80000, 100000, 120000, 140000, 160000]

		listPairsNodeScoreInit = {}
		for n in self.graph.nodes():
			listPairsNodeScoreInit[n] = self.graph.node[n]['init']

		listWithChanges_voter_1 = []
		listWithChanges_voter_w = []
		listWithChanges_proposal1_w = []
		listWithChanges_proposal1_p = []
		listWithChanges_proposal1_wp = []
		listWithChanges_d = {"w":{}, "p":{}, "wp":{}}
		listWithChanges_degroot = {"1": [], "w":[], "p":[], "wp":[]}
		listWithChanges_fj = {"w":[], "p":[], "wp":[]}
		listWithChanges_proposal3 = {"w":[], "p":[], "wp":[]}
		listWithChanges_proposal4 = {"w":[], "p":[], "wp":[]}
		tmp_v = dBnds_down
		while(True):
			for i in listWithChanges_d:
				listWithChanges_d[i][tmp_v] = []
			tmp_v = tmp_v + dBnds_step
			if(tmp_v > dBnds_up):
				break
		
		tm_x = 0
		for e in selectedEdges:
			tm_x = tm_x + 1
			if(tm_x in iterCheck):
				print(str(multiprocessing.current_process()) + str(tm_x))

			#voter_1
			self.graph.node[e[0]]['voter_1'] = self.graph.node[e[1]]['voter_1']
			listWithChanges_voter_1.append((e[0], self.graph.node[e[0]]['voter_1']))

			#voter_w
			self.graph.node[e[0]]['voter_w'] = self.graph.get_edge_data(e[0], e[1])["weight"] * self.graph.node[e[1]]['voter_w']
			listWithChanges_voter_w.append((e[0], self.graph.node[e[0]]['voter_w']))

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
			listWithChanges_proposal1_w.append((e[0], self.graph.node[e[0]]['proposal1_w']))

			#proposal1_p
			self.graph.node[e[0]]['proposal1_p'] =  self.graph.node[e[0]]['proposal1_p'] * self.graph.node[e[0]]['power'] + self.graph.node[e[1]]['proposal1_p'] * self.graph.node[e[1]]['power']
			if(not(maxValue_proposal1_p == 0)):
				self.graph.node[e[0]]['proposal1_p'] = float(self.graph.node[e[0]]['proposal1_p']) / maxValue_proposal1_p
			else:
				self.graph.node[e[0]]['proposal1_p'] = 0
			listWithChanges_proposal1_p.append((e[0], self.graph.node[e[0]]['proposal1_p']))

			#proposal1_wp
			self.graph.node[e[0]]['proposal1_wp'] =  self.graph.node[e[0]]['proposal1_wp'] * self.graph.node[e[0]]['power'] * self.graph.get_edge_data(e[0], e[1])["weight"] + self.graph.node[e[1]]['proposal1_wp'] * self.graph.node[e[1]]['power'] * self.graph.get_edge_data(e[0], e[1])["weight"]
			if(not(maxValue_proposal1_wp == 0)):
				self.graph.node[e[0]]['proposal1_wp'] = float(self.graph.node[e[0]]['proposal1_wp']) / maxValue_proposal1_wp
			else:
				self.graph.node[e[0]]['proposal1_wp'] = 0
			listWithChanges_proposal1_wp.append((e[0], self.graph.node[e[0]]['proposal1_wp']))

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
				listWithChanges_d["w"][tmp_v].append((e[0], self.graph.node[e[0]][tmp_attr_name + "w"]))

				#p
				if(abs(self.graph.node[e[0]][tmp_attr_name + "p"] * self.graph.node[e[0]]['power'] - self.graph.node[e[1]][tmp_attr_name + "p"] * self.graph.node[e[1]]['power']) < tmp_v):
					self.graph.node[e[0]][tmp_attr_name + "p"] = self.graph.node[e[0]][tmp_attr_name + "p"] * self.graph.node[e[0]]['power'] + self.graph.node[e[1]][tmp_attr_name + "p"] * self.graph.node[e[1]]['power']
					if(not(maxValue_proposal2["p"][tmp_v] == 0)):
						self.graph.node[e[0]][tmp_attr_name + "p"] = float(self.graph.node[e[0]][tmp_attr_name + "p"]) / maxValue_proposal2["p"][tmp_v]
					else:
						self.graph.node[e[0]][tmp_attr_name + "p"] = 0
				listWithChanges_d["p"][tmp_v].append((e[0], self.graph.node[e[0]][tmp_attr_name + "p"]))

				#wp
				if(abs(self.graph.node[e[0]][tmp_attr_name + "wp"] * self.graph.node[e[0]]['power'] * self.graph.get_edge_data(e[0], e[1])["weight"] - self.graph.node[e[1]][tmp_attr_name + "wp"] * self.graph.node[e[1]]['power'] * self.graph.get_edge_data(e[0], e[1])["weight"]) < tmp_v):
					self.graph.node[e[0]][tmp_attr_name + "wp"] = self.graph.node[e[0]][tmp_attr_name + "wp"] * self.graph.node[e[0]]['power'] * self.graph.get_edge_data(e[0], e[1])["weight"] + self.graph.node[e[1]][tmp_attr_name + "wp"] * self.graph.node[e[1]]['power'] * self.graph.get_edge_data(e[0], e[1])["weight"]
					if(not(maxValue_proposal2["wp"][tmp_v] == 0)):
						self.graph.node[e[0]][tmp_attr_name + "wp"] = float(self.graph.node[e[0]][tmp_attr_name + "wp"]) / maxValue_proposal2["wp"][tmp_v]
					else:
						self.graph.node[e[0]][tmp_attr_name + "wp"] = 0
				listWithChanges_d["wp"][tmp_v].append((e[0], self.graph.node[e[0]][tmp_attr_name + "wp"]))

				tmp_v = tmp_v + dBnds_step
				if(tmp_v > dBnds_up):
					break

			#degroot adjusments
			denominator = countOfNeighbors + 1

			#1
			numerator = sumDegroot["1"] + self.graph.node[e[0]]['dg_1']
			self.graph.node[e[0]]['dg_1'] = float(numerator) / denominator
			listWithChanges_degroot["1"].append((e[0], self.graph.node[e[0]]['dg_1']))

			#w
			numerator = sumDegroot["w"] + self.graph.node[e[0]]['dg_w']
			self.graph.node[e[0]]['dg_w'] = float(numerator) / denominator
			listWithChanges_degroot["w"].append((e[0], self.graph.node[e[0]]['dg_w']))

			#p
			numerator = sumDegroot["p"] + self.graph.node[e[0]]['power'] * self.graph.node[e[0]]['dg_p']
			self.graph.node[e[0]]['dg_p'] = float(numerator) / denominator
			listWithChanges_degroot["p"].append((e[0], self.graph.node[e[0]]['dg_p']))

			#wp
			numerator = sumDegroot["wp"] + self.graph.node[e[0]]['power'] * self.graph.node[e[0]]['dg_wp']
			self.graph.node[e[0]]['dg_wp'] = float(numerator) / denominator
			listWithChanges_degroot["wp"].append((e[0], self.graph.node[e[0]]['dg_wp']))


			#fj adjusments
			denominator = countOfNeighbors + 2

			#w
			numerator = sumFj["w"] + self.graph.node[e[0]]['fj_w'] + self.graph.node[e[0]]['init']
			self.graph.node[e[0]]['fj_w'] = float(numerator) / denominator
			listWithChanges_fj["w"].append((e[0], self.graph.node[e[0]]['fj_w']))

			#p
			numerator = sumFj["p"] + self.graph.node[e[0]]['power'] * (self.graph.node[e[0]]['fj_p'] + self.graph.node[e[0]]['init'])
			self.graph.node[e[0]]['fj_p'] = float(numerator) / denominator
			listWithChanges_fj["p"].append((e[0], self.graph.node[e[0]]['fj_p']))

			#wp
			numerator = sumFj["wp"] + self.graph.node[e[0]]['power'] * (self.graph.node[e[0]]['fj_wp'] + self.graph.node[e[0]]['init'])
			self.graph.node[e[0]]['fj_wp'] = float(numerator) / denominator
			listWithChanges_fj["wp"].append((e[0], self.graph.node[e[0]]['fj_wp']))


			#proposal3
			denominator = (countOfNeighbors + 1) * (countOfNeighbors + 1)

			#w
			numerator = sumProposal3["A"]["w"] * sumProposal3["score"]["w"]
			self.graph.node[e[0]]['proposal3_w'] = float(numerator) / denominator
			listWithChanges_proposal3["w"].append((e[0], self.graph.node[e[0]]['proposal3_w']))

			#p
			numerator = sumProposal3["A"]["p"] * sumProposal3["score"]["p"]
			self.graph.node[e[0]]['proposal3_p'] = float(numerator) / denominator
			listWithChanges_proposal3["p"].append((e[0], self.graph.node[e[0]]['proposal3_p']))

			#wp
			numerator = sumProposal3["A"]["wp"] * sumProposal3["score"]["wp"]
			self.graph.node[e[0]]['proposal3_wp'] = float(numerator) / denominator
			listWithChanges_proposal3["wp"].append((e[0], self.graph.node[e[0]]['proposal3_wp']))


			#proposal4
			denominator = (countOfNeighbors + 2) * (countOfNeighbors + 2)

			#w
			numerator = sumProposal4["A"]["w"] * sumProposal4["score"]["w"]
			self.graph.node[e[0]]['proposal4_w'] = float(numerator) / denominator
			listWithChanges_proposal4["w"].append((e[0], self.graph.node[e[0]]['proposal4_w']))

			#p
			numerator = sumProposal4["A"]["p"] * sumProposal4["score"]["p"]
			self.graph.node[e[0]]['proposal4_p'] = float(numerator) / denominator
			listWithChanges_proposal4["p"].append((e[0], self.graph.node[e[0]]['proposal4_p']))

			#wp
			numerator = sumProposal4["A"]["wp"] * sumProposal4["score"]["wp"]
			self.graph.node[e[0]]['proposal4_wp'] = float(numerator) / denominator
			listWithChanges_proposal4["wp"].append((e[0], self.graph.node[e[0]]['proposal4_wp']))

		total_time = float(time.time() - start_time)/60 #minutes
		return(self.graph, listPairsNodeScoreInit, listWithChanges_voter_1, listWithChanges_voter_w, listWithChanges_proposal1_w, listWithChanges_proposal1_p, listWithChanges_proposal1_wp, listWithChanges_d, listWithChanges_degroot, listWithChanges_fj, listWithChanges_proposal3, listWithChanges_proposal4, total_time)

	def returnAverages(self, init_copy, changed, aggressive_bound):
		totalAverage = np.asarray([])
		normalAverage = np.asarray([])
		aggressiveAverage = np.asarray([])

		sumTotal = 0
		amountTotal = 0
		sumNormal = 0
		amountNormal = 0
		sumAggressive = 0
		amountAggressive = 0

		for cc in init_copy:
		 	sumTotal = sumTotal + init_copy[cc]
		 	amountTotal = amountTotal + 1

		 	if(init_copy[cc] >= aggressive_bound):
		 		sumAggressive = sumAggressive + init_copy[cc]
		 		amountAggressive = amountAggressive + 1
		 	else:
		 		sumNormal = sumNormal + init_copy[cc]
		 		amountNormal = amountNormal + 1

		totalAverage = np.append(totalAverage, [float(sumTotal) / amountTotal])
		normalAverage = np.append(normalAverage, [float(sumNormal) / amountNormal])
		aggressiveAverage = np.append(aggressiveAverage, [float(sumAggressive) / amountAggressive])

		init = {}
		for i in init_copy:
			init[i] = init_copy[i]

		tm = 0
		iterCheck = [5000, 10000, 20000, 50000, 80000, 100000, 120000, 140000, 160000, 200000, 400000, 600000, 800000]
		for c in changed:
			tm = tm + 1
			if(tm in iterCheck):
				print("Average: " + str(multiprocessing.current_process()) + str(tm))
			sumTotal = 0
			amountTotal = 0
			sumNormal = 0
			amountNormal = 0
			sumAggressive = 0
			amountAggressive = 0

			sumTotal = sumTotal + c[1]
			amountTotal = amountTotal + 1

			if(init_copy[c[0]] >= aggressive_bound):
				sumAggressive = sumAggressive + c[1]
				amountAggressive = amountAggressive + 1
			else:
				sumNormal = sumNormal + c[1]
				amountNormal = amountNormal + 1

			for i in init:
				if(not(i == c[0])):
					sumTotal = sumTotal + init[i]
					amountTotal = amountTotal + 1

					if(init_copy[i] >= aggressive_bound):
						sumAggressive = sumAggressive + init[i]
						amountAggressive = amountAggressive + 1
					else:
						sumNormal = sumNormal + init[i]
						amountNormal = amountNormal + 1

			init[c[0]] = c[1]

			totalAverage = np.append(totalAverage, [float(sumTotal) / amountTotal])
			normalAverage = np.append(normalAverage, [float(sumNormal) / amountNormal])
			aggressiveAverage = np.append(aggressiveAverage, [float(sumAggressive) / amountAggressive])

		return(totalAverage, normalAverage, aggressiveAverage)


	def writeAveragesToFile(self, R, iteration, percentage, network_name, aggressive_bound, aggr_init_type, bndDown, bndUp, modelType, RorS, d, finalGraph):
		averageScoreTotalNetwork_ = R[0]
		averageScoreNormal_ = R[1]
		averageScoreAggressive_ = R[2]
		
		if(not(os.path.isdir(paths[network_name][RorS][modelType] + str(iteration)))):
			os.mkdir(paths[network_name][RorS][modelType] + str(iteration))

		if(not(d == -1)):
			if(not(os.path.isdir(paths[network_name][RorS][modelType] + str(iteration) + "/d:" + str(d)))):
				os.mkdir(paths[network_name][RorS][modelType] + str(iteration) + "/d:" + str(d))

		if(d == -1):
			path = paths[network_name][RorS][modelType] + str(iteration) + "/" + aggr_init_type + "_down_" + str(float(bndDown)) + "_up_" + str(float(bndUp)) + "_aggrBnd_" + str(float(aggressive_bound)) + "_perc_" + str(percentage) + ".txt"
		else:
			path = paths[network_name][RorS][modelType] + str(iteration) + "/" + "d:" + str(d) + "/" + aggr_init_type + "_down_" + str(float(bndDown)) + "_up_" + str(float(bndUp)) + "_aggrBnd_" + str(float(aggressive_bound)) + "_perc_" + str(percentage) + "_d_" + str(d) + ".txt"

		''' Check if exists the specific file. If YES => delete it! '''
		if(os.path.isfile(path)):
			os.remove(path)

		self.writeToFile(path, averageScoreTotalNetwork_, "totalNetwork: ")
		self.writeToFile(path, averageScoreNormal_, "normalNetwork: ")
		self.writeToFile(path, averageScoreAggressive_, "aggressiveNetwork: ")
		#self.writeToFile(path, self.returnInitFinalScoreForEachNode(finalGraph, modelType), "initFinalScore: ")

	def writeToFile(self, path, array, label):
		file = open(path, "a")
		
		file.write(label)
		for i in array:
			file.write(str(i) + " ")

		file.write("\n")
		file.close()

	def returnInitFinalScoreForEachNode(self, g, mdlTp):
		tmp_list = []
		for n in g.nodes():
			tmp_list.append((n, g.node[n]["init"], g.node[n][mdlTp]))
		return(tmp_list)
