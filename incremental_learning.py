from functools import reduce

def modify_probability(child_node_name_link_pair,del_probability,parent_node):
		##### adjust other child node probabilities
	#target_node_name = child_node_probability_dict['node_name']
	divide_factor = len(parent_node.child_node_init_probability) - 1
	total_residue_prob = 0
	for k,v in enumerate(parent_node.child_node_init_probability):
		if v['node_name'] == child_node_name_link_pair[0] and v['link'] == child_node_name_link_pair[1]:
			parent_node.child_node_init_probability[k]['init_probability'] += del_probability
		else:
			if del_probability < 0:
				total_residue_prob += (1-parent_node.child_node_init_probability[k]['init_probability'])
			else:
				total_residue_prob += parent_node.child_node_init_probability[k]['init_probability']
	
	for k,v in enumerate(parent_node.child_node_init_probability):
		if v['node_name'] != child_node_name_link_pair[0] or v['link'] != child_node_name_link_pair[1]:
			if del_probability < 0:
				parent_node.child_node_init_probability[k]['init_probability'] -= del_probability*(1-parent_node.child_node_init_probability[k]['init_probability'])/total_residue_prob
			else:
				parent_node.child_node_init_probability[k]['init_probability'] -= del_probability*parent_node.child_node_init_probability[k]['init_probability']/total_residue_prob
		
			#del_probability/divide_factor


def calculate_trailing_probability(factored_program_probability,current_edge_node_labels):
	next_edge = [(k,v) for k,v in factored_program_probability.items() if  k.split('-')[0] == current_edge_node_labels[1]]
	if next_edge: #### next_edge is not empty
		next_edge = next_edge[0]
		curr_edge_probability =next_edge[1]['init_probability']
		current_edge_node_labels = next_edge[0].split('-')
		return calculate_trailing_probability(factored_program_probability,current_edge_node_labels) *curr_edge_probability 
	else:
		return 1
		

def calculate_delta_probability(factored_program_probability,sourcenode,terminalnode,reward,link_no):
	delta_probability = 1
	alpha = 0.5
	current_edge = [(k,v) for k,v in factored_program_probability.items() if  k == str(sourcenode.label)+'-'+str(terminalnode.label)+'-'+str(link_no)][0]
	current_edge_node_labels = current_edge[0].split('-')
	current_probability_mass = current_edge[1]['init_probability']
	
	total_program_probability = reduce((lambda x, y: x * y), [v['init_probability'] for k,v in factored_program_probability.items()])
	program_probability_sourcenode = reduce((lambda x, y: x * y), [v['init_probability'] for k,v in sourcenode.factored_program_probability.items()])
		
	#delta_probability = calculate_trailing_probability(factored_program_probability,current_edge_node_labels)	
	delta_probability = total_program_probability/(program_probability_sourcenode*current_probability_mass)
	#delta_probability = total_program_probability/(current_probability_mass)
	
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
		print (terminalnode)
		print (terminalnode.label)
		temp_g_nodes = []
		def graph_return_nodes_for_update_probability(temp_g_nodes,terminalnode,factored_program_probability,reward):
		# Recursively fetch all parent nodes
			for i,sourcenode in enumerate(terminalnode.links):
				#print (sourcenode)
				if type(sourcenode).__name__=='initWorld': ### terminalnode initialnode
					None
				elif len(sourcenode.links) == 0 and sourcenode.no_of_arguments >0: ######### sourcenode initialnode
					###### calculate delta probability
					delta_probability = calculate_delta_probability(factored_program_probability,sourcenode,terminalnode,reward,i)
					######### make pair of (child node name,link),deltaprobability and parentnode	
					child_node_name = get_node_name(terminalnode)
					
					temp_g_nodes.append(((child_node_name,i), delta_probability, sourcenode))
				else:
					graph_return_nodes_for_update_probability(temp_g_nodes,sourcenode,factored_program_probability,reward)
					###### calculate delta probability
					delta_probability = calculate_delta_probability(factored_program_probability,sourcenode,terminalnode,reward,i)
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
			
			
def get_program_tree_stack(terminalnode):
	#print(terminalnode)
	node_stack = []
	all_nodes= [terminalnode]
	while all_nodes:
		for i,sourcenode in enumerate(all_nodes[0].links):
			if str(sourcenode.program_expression['data']) =='iW().iS()':
				None
			else:
				node_stack.append(get_node_name(sourcenode))
				all_nodes.append(sourcenode)
		all_nodes.pop(0)
	return(node_stack)
	
def get_total_child_probability(childnode):
	child_node_name = get_node_name(childnode)
	tot_probability = 1
	probability_list = []
	for i,v in enumerate(childnode.links):
		i_probability = [i_prob['init_probability'] for i_prob in v.child_node_init_probability if i_prob['link']==i and i_prob['node_name']==child_node_name][0]
		probability_list.append(i_probability)
		tot_probability *= i_probability
	return (probability_list,tot_probability)
	
def match_subprograms(search_graph,terminalnode,match_depth):
	program_node_stack = get_program_tree_stack(terminalnode)
	same_nodes = [i for i in search_graph.nodes if get_node_name(terminalnode) == get_node_name(i) and i.executed == 1 and i.equivalent_prog == 0 and i != terminalnode and i != search_graph.nodes[0] ]
	prev_same_node_stack_len = 0
	same_node = None
	match_len = 0
	init_probability_list,child_probablity = get_total_child_probability(terminalnode)
	probability_list = init_probability_list
	for i_nodes in same_nodes:
		maybe_same_program_node_stack = get_program_tree_stack(i_nodes)
		iter_len = min(len(maybe_same_program_node_stack),len(program_node_stack),match_depth)
		
		for j in range(0,iter_len):
			if (j == iter_len or program_node_stack[j] !=  maybe_same_program_node_stack[j]):
				if j==match_len and j>0:
					same_child_probability_list,same_child_node_probability = get_total_child_probability(i_nodes)
					if same_child_node_probability > child_probablity:
						match_len = j
						same_node = i_nodes
						child_probablity = same_child_node_probability
						probability_list = same_child_probability_list
				elif j>match_len:
					match_len = j
					same_node = i_nodes
					probability_list,child_probablity = get_total_child_probability(i_nodes)
				break
			
	return same_node,[j-i for i,j in zip(init_probability_list,probability_list)]
				
				