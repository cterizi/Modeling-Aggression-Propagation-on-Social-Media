import networkx as nx
import random
import numpy
import csv

def main(graph, agrressType, boundDown, boundUp, aggressive_bound, dBnds_down, dBnds_up, dBnds_step):
	''' Choose 7.9% aggressive nodes '''
	rate_10 = int(0.079*graph.number_of_nodes())
	selected_aggressive_nodes = returnPredictedAggressiveUsers()
	#selected_aggressive_nodes = random.sample(list(graph.nodes()), rate_10)
	nodes = list(set(list(graph.nodes())).difference(set(selected_aggressive_nodes)))
				
	if(agrressType == "discrete"):
		discrete_list = []
		for number in range(boundDown, boundUp + 1):
			discrete_list.append(number)
		
		normalList = []
		aggressiveList = []
		for i in discrete_list:
			if(i < aggressive_bound):
				normalList.append(i)
			elif(i >= aggressive_bound):
				aggressiveList.append(i)

		''' Fill in = 0 the non-aggressive nodes'''
		for eachNode in nodes:
			graph.node[eachNode]['init'] = random.choice(normalList)
			graph.node[eachNode]['voter_1'] = graph.node[eachNode]['init']
			graph.node[eachNode]['voter_w'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal1_w'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal1_p'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal1_wp'] = graph.node[eachNode]['init']
			tmp_v = dBnds_down
			while(True):
				tmp_attr_name = "d_" + str(tmp_v) + "_"
				graph.node[eachNode][tmp_attr_name + "w"] = graph.node[eachNode]['init']
				graph.node[eachNode][tmp_attr_name + "p"] = graph.node[eachNode]['init']
				graph.node[eachNode][tmp_attr_name + "wp"] = graph.node[eachNode]['init']
				tmp_v = tmp_v + dBnds_step
				if(tmp_v > dBnds_up):
					break
			graph.node[eachNode]['dg_1'] = graph.node[eachNode]['init']
			graph.node[eachNode]['dg_w'] = graph.node[eachNode]['init']
			graph.node[eachNode]['dg_p'] = graph.node[eachNode]['init']
			graph.node[eachNode]['dg_wp'] = graph.node[eachNode]['init']
			graph.node[eachNode]['fj_w'] = graph.node[eachNode]['init']
			graph.node[eachNode]['fj_p'] = graph.node[eachNode]['init']
			graph.node[eachNode]['fj_wp'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal3_w'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal3_p'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal3_wp'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal4_w'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal4_p'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal4_wp'] = graph.node[eachNode]['init']


		''' Fill in = 1 the aggressive nodes'''
		for eachNode in selected_aggressive_nodes:
			graph.node[eachNode]['init'] = random.choice(aggressiveList)
			graph.node[eachNode]['voter_1'] = graph.node[eachNode]['init']
			graph.node[eachNode]['voter_w'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal1_w'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal1_p'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal1_wp'] = graph.node[eachNode]['init']
			tmp_v = dBnds_down
			while(True):
				tmp_attr_name = "d_" + str(tmp_v) + "_"
				graph.node[eachNode][tmp_attr_name + "w"] = graph.node[eachNode]['init']
				graph.node[eachNode][tmp_attr_name + "p"] = graph.node[eachNode]['init']
				graph.node[eachNode][tmp_attr_name + "wp"] = graph.node[eachNode]['init']
				tmp_v = tmp_v + dBnds_step
				if(tmp_v > dBnds_up):
					break
			graph.node[eachNode]['dg_1'] = graph.node[eachNode]['init']
			graph.node[eachNode]['dg_w'] = graph.node[eachNode]['init']
			graph.node[eachNode]['dg_p'] = graph.node[eachNode]['init']
			graph.node[eachNode]['dg_wp'] = graph.node[eachNode]['init']
			graph.node[eachNode]['fj_w'] = graph.node[eachNode]['init']
			graph.node[eachNode]['fj_p'] = graph.node[eachNode]['init']
			graph.node[eachNode]['fj_wp'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal3_w'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal3_p'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal3_wp'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal4_w'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal4_p'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal4_wp'] = graph.node[eachNode]['init']

	elif(agrressType == "decimal"):
		for eachNode in nodes:
			graph.node[eachNode]['init'] = random.uniform(boundDown, aggressive_bound - 0.01)
			graph.node[eachNode]['voter_1'] = graph.node[eachNode]['init']
			graph.node[eachNode]['voter_w'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal1_w'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal1_p'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal1_wp'] = graph.node[eachNode]['init']
			tmp_v = dBnds_down
			while(True):
				tmp_attr_name = "d_" + str(tmp_v) + "_"
				graph.node[eachNode][tmp_attr_name + "w"] = graph.node[eachNode]['init']
				graph.node[eachNode][tmp_attr_name + "p"] = graph.node[eachNode]['init']
				graph.node[eachNode][tmp_attr_name + "wp"] = graph.node[eachNode]['init']
				tmp_v = tmp_v + dBnds_step
				if(tmp_v > dBnds_up):
					break
			graph.node[eachNode]['dg_1'] = graph.node[eachNode]['init']
			graph.node[eachNode]['dg_w'] = graph.node[eachNode]['init']
			graph.node[eachNode]['dg_p'] = graph.node[eachNode]['init']
			graph.node[eachNode]['dg_wp'] = graph.node[eachNode]['init']
			graph.node[eachNode]['fj_w'] = graph.node[eachNode]['init']
			graph.node[eachNode]['fj_p'] = graph.node[eachNode]['init']
			graph.node[eachNode]['fj_wp'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal3_w'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal3_p'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal3_wp'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal4_w'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal4_p'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal4_wp'] = graph.node[eachNode]['init']

		for eachNode in selected_aggressive_nodes:
			graph.node[eachNode]['init'] = random.uniform(aggressive_bound, boundUp)
			graph.node[eachNode]['voter_1'] = graph.node[eachNode]['init']
			graph.node[eachNode]['voter_w'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal1_w'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal1_p'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal1_wp'] = graph.node[eachNode]['init']
			tmp_v = dBnds_down
			while(True):
				tmp_attr_name = "d_" + str(tmp_v) + "_"
				graph.node[eachNode][tmp_attr_name + "w"] = graph.node[eachNode]['init']
				graph.node[eachNode][tmp_attr_name + "p"] = graph.node[eachNode]['init']
				graph.node[eachNode][tmp_attr_name + "wp"] = graph.node[eachNode]['init']
				tmp_v = tmp_v + dBnds_step
				if(tmp_v > dBnds_up):
					break
			graph.node[eachNode]['dg_1'] = graph.node[eachNode]['init']
			graph.node[eachNode]['dg_w'] = graph.node[eachNode]['init']
			graph.node[eachNode]['dg_p'] = graph.node[eachNode]['init']
			graph.node[eachNode]['dg_wp'] = graph.node[eachNode]['init']
			graph.node[eachNode]['fj_w'] = graph.node[eachNode]['init']
			graph.node[eachNode]['fj_p'] = graph.node[eachNode]['init']
			graph.node[eachNode]['fj_wp'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal3_w'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal3_p'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal3_wp'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal4_w'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal4_p'] = graph.node[eachNode]['init']
			graph.node[eachNode]['proposal4_wp'] = graph.node[eachNode]['init']

	return(graph)

def returnPredictedAggressiveUsers():
	with open("metrics.predictions.csv", 'r') as f:
		reader = csv.reader(f)
		your_list = list(reader)
		f.close()
	your_list = your_list[1:]

	aggressiveUsers = []
	normalScore = 0
	for element in your_list:
		if(not(element[2] == "normal")):
			aggressiveUsers.append(int(element[1]))
		if(element[2] == "normal" and float(element[3]) < 0.70):
			aggressiveUsers.append(int(element[1]))
	return(aggressiveUsers)
