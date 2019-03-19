################################################# Experiment 1
from metasearcher_agent import *
from graph_draw import *


def run_experiment1():
######### before ruuning this function comment line#41 and 42 and uncomment line#43 and 44 in metasearcher_agent
######### to inactivate equivalent program pruning comment line#148 in metasearcher_agent   
	sp=list()
	rt=list()
	globalvars.C=0.01
	(search_graph,corpus_of_objects,init_type_compatible_node_links) = initialize_search_graph(corpus_index)
	exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,10)
	sp.append(len(search_graph.nodes))
	rt.append(globalvars.totalruntime)
	globalvars.totalruntime=0

	exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,20)
	sp.append(len(search_graph.nodes))
	rt.append(globalvars.totalruntime)
	globalvars.totalruntime=0

	exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,40)
	sp.append(len(search_graph.nodes))
	rt.append(globalvars.totalruntime)
	globalvars.totalruntime=0

	exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,80)
	sp.append(len(search_graph.nodes))
	rt.append(globalvars.totalruntime)
	globalvars.totalruntime=0

	exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,160)
	sp.append(len(search_graph.nodes))
	rt.append(globalvars.totalruntime)
	globalvars.totalruntime=0

	exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,320)
	sp.append(len(search_graph.nodes))
	rt.append(globalvars.totalruntime)
	globalvars.totalruntime=0

	exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,640)
	sp.append(len(search_graph.nodes))
	rt.append(globalvars.totalruntime)
	globalvars.totalruntime=0

	exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,1280)
	sp.append(len(search_graph.nodes))
	rt.append(globalvars.totalruntime)
	globalvars.totalruntime=0

	exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,2560)
	sp.append(len(search_graph.nodes))
	rt.append(globalvars.totalruntime)
	globalvars.totalruntime=0

	exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,4120)
	sp.append(len(search_graph.nodes))
	rt.append(globalvars.totalruntime)
	globalvars.totalruntime=0

	exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,8240)
	sp.append(len(search_graph.nodes))
	rt.append(globalvars.totalruntime)
	globalvars.totalruntime=0
	(search_graph,corpus_of_objects,init_type_compatible_node_links) = initialize_search_graph(corpus_index)
	exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,16480)
	sp.append(len(search_graph.nodes))
	rt.append(globalvars.totalruntime)
	globalvars.totalruntime=0
	
	print(sp)
	print(rt)
	
	
########################################## Experiment 2

def run_experiment2():
######## before running this function uncomment line#41 and 42 and comment line#43 and 44 in metasearcher_agent
######## to inactivate incremental learning comment line#350, 373 and 413
	globalvars.C=0.01
	(search_graph,corpus_of_objects,init_type_compatible_node_links) = initialize_search_graph(corpus_index)
	environment.goal_state = [2,1,[1,0]]
	environment.init_world = environment.world('number',environment.maze,environment.init_state,environment.goal_state)
	exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,500000)
	init_prob1=exec_node.program_probability
	#print("prog prob")
	fin_prob1=calculate_total_program_probability(exec_node.factored_program_probability)

	environment.goal_state = [2,1,[0,1]]
	environment.init_world = environment.world('number',environment.maze,environment.init_state,environment.goal_state)
	exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,500000)
	init_prob2=exec_node.program_probability
	#node1= exec_node

	fin_prob2=calculate_total_program_probability(exec_node.factored_program_probability)
	node2= exec_node

	environment.goal_state = [2,2,[0,1]]
	environment.init_world = environment.world('number',environment.maze,environment.init_state,environment.goal_state)
	exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,5000000)
	init_prob3=exec_node.program_probability
	fin_prob3=calculate_total_program_probability(exec_node.factored_program_probability)

	node3=exec_node

	environment.goal_state = [2,2,[1,0]]
	environment.init_world = environment.world('number',environment.maze,environment.init_state,environment.goal_state)
	exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,5000000)
	init_prob4=exec_node.program_probability
	fin_prob4=calculate_total_program_probability(exec_node.factored_program_probability)
	#environment.goal_state = [3,2,[1,0]]
	#environment.init_world = environment.world('number',environment.maze,environment.init_state,environment.goal_state)
	#exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,5000000)
	#init_prob5=exec_node.program_probability

	print(init_prob1,init_prob2,init_prob3,init_prob4)
	print(fin_prob1,fin_prob2,fin_prob3,fin_prob4)

######################### Experiment 3 ###########################################

def run_experiment3():
######## before running this function uncomment line#41 and 42 and comment line#43 and 44 in metasearcher_agent
######### modify C =0.05 in globalvars
	globalvars.C=0.05
	(search_graph,corpus_of_objects,init_type_compatible_node_links) = initialize_search_graph(corpus_index)
	environment.goal_state = [2,1,[1,0]]
	environment.init_world = environment.world('number',environment.maze,environment.init_state,environment.goal_state)
	exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,500000)
	init_prob1=exec_node.program_probability
	fin_prob1=calculate_total_program_probability(exec_node.factored_program_probability)

	environment.goal_state = [10,1,[1,0]]
	environment.init_world = environment.world('number',environment.maze,environment.init_state,environment.goal_state)
	exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,500000)
	init_prob2=exec_node.program_probability
	for i in range(8):
		exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,500000)
	fin_prob2=calculate_total_program_probability(exec_node.factored_program_probability)

	environment.goal_state = [2,2,[0,1]]
	environment.init_world = environment.world('number',environment.maze,environment.init_state,environment.goal_state)
	exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,500000)
	init_prob3=exec_node.program_probability
	fin_prob3=calculate_total_program_probability(exec_node.factored_program_probability)

	environment.goal_state = [2,2,[1,0]]
	environment.init_world = environment.world('number',environment.maze,environment.init_state,environment.goal_state)
	exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,500000)
	init_prob4=exec_node.program_probability
	for i in range(6):
		exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,500000)
	fin_prob4=calculate_total_program_probability(exec_node.factored_program_probability)


	environment.goal_state = [10,10,[1,0]]
	environment.init_world = environment.world('number',environment.maze,environment.init_state,environment.goal_state)	
	exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,5000000)
	init_prob5=exec_node.program_probability
	fin_prob5=calculate_total_program_probability(exec_node.factored_program_probability)

	temp=exec_node

	environment.goal_state = [20,20,[1,0]]
	environment.init_world = environment.world('number',environment.maze,environment.init_state,environment.goal_state)
	exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,5000000)
	init_prob6=exec_node.program_probability
	fin_prob6=calculate_total_program_probability(exec_node.factored_program_probability)

	print("initial_prob")
	print(init_prob1,init_prob2,init_prob3,init_prob4,init_prob5,init_prob6)
	print("final prob")
	print(fin_prob1,fin_prob2,fin_prob3,fin_prob4,fin_prob5,fin_prob6)

	#k=search_graph.return_subgraph(exec_node)
	#draw_graph(k)