def calculate_trailing_probability(factored_program_probability,current_edge_node_labels):
	next_edge = [(k,v) for k,v in factored_program_probability.items() if  k.split('-')[0] == current_edge_node_labels[1]]
	if next_edge: #### next_edge is not empty
		next_edge = next_edge[0]
		curr_edge_probability =next_edge[1]['init_probability']
		current_edge_node_labels = next_edge[0].split('-')
		return calculate_trailing_probability(factored_program_probability,current_edge_node_labels) *curr_edge_probability 
	else:
		return 1


def calculate_delta_probability(factored_program_probability,sourcenode,terminalnode,reward):
	delta_probability = 1
	alpha = 0.8
	current_edge = [(k,v) for k,v in factored_program_probability.items() if  k == str(sourcenode.label)+'-'+str(terminalnode.label)][0]
	current_edge_node_labels = current_edge[0].split('-')
	current_probability_mass = current_edge[1]['init_probability']
	delta_probability = calculate_trailing_probability(factored_program_probability,current_edge_node_labels)	
	
	if reward > 0:
		delta_probability *= alpha*reward*(1-current_probability_mass)
	else:
		delta_probability *= alpha*reward*current_probability_mass
	return delta_probability
	
def get_node_name(terminalnode):
	child_node_name = type(terminalnode).__name__
	if child_node_name == 'sensor':
		child_node_name +='_'+terminalnode.atype['function']['output'][0]
	elif child_node_name == 'actuator':
		child_node_name +='_'+terminalnode.atype['function']['input'][0]
	elif child_node_name == 'constant':
		child_node_name += str(terminalnode.K)
	return child_node_name

def update_probability(terminalnode):
	if terminalnode.reward == 0: ###### no reward 
		None
	else:                        ###### update probabilities recursively
		temp_g_nodes = []
		def graph_return_nodes_for_update_probability(temp_g_nodes,terminalnode,factored_program_probability,reward):
		# Recursively fetch all parent nodes
			for i,sourcenode in enumerate(terminalnode.links):
				#print (sourcenode)
				if type(sourcenode).__name__=='world': ### terminalnode initialnode
					None
				elif len(sourcenode.links) == 0 and sourcenode.no_of_arguments >0: ######### sourcenode initialnode
					###### calculate delta probability
					delta_probability = calculate_delta_probability(factored_program_probability,sourcenode,terminalnode,reward)
					######### make pair of (child node name,link),deltaprobability and parentnode	
					child_node_name = get_node_name(terminalnode)
					
					temp_g_nodes.append(((child_node_name,i), delta_probability, sourcenode))
				else:
					graph_return_nodes_for_update_probability(temp_g_nodes,sourcenode,factored_program_probability,reward)
					###### calculate delta probability
					delta_probability = calculate_delta_probability(factored_program_probability,sourcenode,terminalnode,reward)
					######### make pair of (child node name,link),deltaprobability and parentnode
					child_node_name = get_node_name(terminalnode)
					temp_g_nodes.append(((child_node_name,i), delta_probability, sourcenode))
			#temp_g_nodes.append(terminalnode)
			return temp_g_nodes
		reward = terminalnode.reward
		factored_program_probability = terminalnode.factored_program_probability
		temp_g_nodes = graph_return_nodes_for_update_probability(temp_g_nodes,terminalnode,factored_program_probability,reward)
		temp_g_nodes = list(set(temp_g_nodes))
	
		####### Update probabilities of all program nodes
		for i_nodes in temp_g_nodes:
			modify_probability(i_nodes[0],i_nodes[1],i_nodes[2])
			