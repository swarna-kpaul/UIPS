##### initialize all function objects
import itertools
corpus_of_all_objects = {'sensor_number':sensor(node_label,'number'),
					'actuator_number':actuator(node_label,'number'),
					'identity':identity(node_label),
					'constant0':constant(node_label,0),
					'constant1':constant(node_label,1),
					'constant2':constant(node_label,2),
					'constant3':constant(node_label,3),
					'gaurd':gaurd(node_label),
					'equal':equal(node_label),
					'lambdagraph':lambdagraph(node_label),
					'recurse':recurse(node_label),
					'apply':apply(node_label),
					'add':add(node_label),
					'subtract':subtract(node_label),
					'multiply':multiply(node_label),
					'greater':greater(node_label),
					'conjunct':conjunct(node_label),
					'disjunct':disjunct(node_label),
					'negate':negate(node_label)}

time_limit = 10000
node_label = 1
node_list_dict={}
					
corpus_index = ['sensor_number','actuator_number','identity','constant0','constant1','constant2','constant3','gaurd','equal','lambdagraph','recurse']

def check_type_compatibility(source_node,target_node,target_node_link):
	node_output_type = source_node.atype['function']['output'][0]
	node_input_type = target_node.atype['function']['input'][target_node_link]
	if (node_output_type == 'some' or node_output_type == 'any' or node_input_type == 'some' or node_input_type == 'any' ) and node_output_type != 'world' and node_input_type != 'world': ### all inputs are accepted
					return 0
				elif 'function' in node_input_type and 'function' in node_output_type: ## both are function types
					return 0
				elif 'list' in node_input_type and 'list' in node_output_type: #both are list type
					node_output_type_list_of = node_output_type['list']
					node_input_type_list_of = node_input_type['list']
					if node_output_type_list_of == 'some' or node_output_type_list_of == 'any' or node_input_type_list_of == 'some' or node_input_type_list_of == 'any': ## type compatible list
						return 0
					elif node_output_type_list_of == node_output_type_list_of : ## type compatible list
						return 0
				elif node_output_type == node_input_type:
					return 0
	return 1
					
	
def create_type_compatibility(type_compatible_node_links,i_node,output_node,corpus_of_objects,corpus_index):
	for j_node in corpus_index:
			for k_in_links in range(corpus_of_objects[j_node].no_of_arguments):
				#node_input_type = corpus_of_objects[j_node].atype['function']['input'][k_in_links]
				####### match input - output type
				
				if check_type_compatibility(output_node,corpus_of_objects[j_node],k_in_links) == 0:
					type_compatible_node_links[i_node].append({'node_name':j_node,'link':k_in_links})
			
	########## calculating initial probability
	init_probability = 1/len(type_compatible_node_links[i_node])
	for j_node in range(len(type_compatible_node_links[i_node])):
		type_compatible_node_links[i_node][j_node]['init_probability'] =init_probability
	
	return type_compatible_node_links
				
def initialize_corpus(corpus_index):
	corpus_of_objects = { i: corpus_of_all_objects[i] for i in corpus_index}
	##### creating initial type graph
	type_compatible_node_links ={}
	for i_node in corpus_index:
		#node_output_type=corpus_of_objects[i_node].atype['function']['output'][0]
		type_compatible_node_links[i_node] = []
		type_compatible_node_links = create_type_compatibility(type_compatible_node_links,i_node,corpus_of_objects[i_node],corpus_of_objects,corpus_index)
		
	return 	(corpus_of_objects,type_compatible_node_links)
					
	
(corpus_of_objects,init_type_compatible_node_links) = initialize_corpus(corpus_index)


def extend_a_terminalnode(search_graph,extendable_node,type_compatible_node_links,gen):
	if type(extendable_node).__name__ == 'sensor':
		extendable_node_name = type(extendable_node).__name__ +'_'+ extendable_node.atype['function']['output'][0]
	elif type(extendable_node).__name__ == 'actuator':
		extendable_node_name = type(extendable_node).__name__ +'_'+ extendable_node.atype['function']['input'][0]
	else:
		extendable_node_name = type(extendable_node).__name__
	if extendable_node_name in ['identity','head','tail','cons']:
		type_compatible_node_links = create_type_compatibility(type_compatible_node_links,extendable_node_name,extendable_node,corpus_of_objects,corpus_index)
		##### for each child nodes in type compatible list
	for child_node_link_index,child_node_links in enumerate(type_compatible_node_links[extendable_node_name]):
		child_node_name = child_node_links['node_name']
		child_node_binding_link = child_node_links['link']
		no_of_arguments_of_child_node = corpus_of_objects[child_node_name].no_of_arguments
		child_node_other_link_list = list(range(no_of_arguments_of_child_node))
		child_node_other_link_list.remove(child_node_binding_link)
			
		if no_of_arguments_of_child_node == 1:
			########## create the child node 
			child_node = copy.deepcopy(corpus_of_objects[child_node_name])
			child_node.probability[0] = extendable_node.child_node_init_probability             #child_node_links['init_probability']
			########## add child node in graph
			search_graph.add_node(child_node,extendable_node)
			########### update type child node init probability of child node 
			if child_node_name in ['identity','head','tail','cons']:
				########### rerun type compatitbilty update
				type_compatible_node_links = create_type_compatibility(type_compatible_node_links,child_node_name,child_node,corpus_of_objects,corpus_index)
				
			child_node.child_node_init_probability = type_compatible_node_links[child_node_name][0]['init_probability']
				
		else:
		######## Generate all possible permutations of parent nodes
			gen_parent_nodes = gen
			#gen_parent_nodes.remove(extendable_node)
			for parent_nodes in itertools.product(gen_parent_nodes,repeat=no_of_arguments_of_child_node-1):	
				##### check type compatibility
				child_node_probability = []
				for child_link_index,parent_node in enumerate(parent_nodes):
					type_compatible = check_type_compatibility(parent_node,corpus_of_objects[child_node_name],child_node_other_link_list[child_link_index])
					child_node_probability.append(parent_node.child_node_init_probability)
					if type_compatible == 1:
						break
						
			########## add node in graph
				if type_compatible == 0:
					child_node_probability.insert(child_node_binding_link,extendable_node.child_node_init_probability)
					child_node = copy.deepcopy(corpus_of_objects[child_node_name])
					child_node.probability = child_node_probability
					parent_nodes_tuple = list(parent_nodes)
					parent_nodes_tuple.insert(child_node_binding_link,extendable_node)
					parent_nodes_tuple = tuple(parent_nodes_tuple)
					search_graph.add_node(child_node,*parent_nodes_tuple)
					########### update type child node init probability of child node 
					if child_node_name in ['identity','head','tail','cons']:
					########### rerun type compatitbilty update
						type_compatible_node_links = create_type_compatibility(type_compatible_node_links,child_node_name,child_node,corpus_of_objects,corpus_index)
				
					child_node.child_node_init_probability = type_compatible_node_links[child_node_name][0]['init_probability']
				#################################################################################################
	return search_graph
	

def eval_graph(search_graph,terminalnode,PHASE):
	global node_label
	global time_limit
	current_program_graph = search_graph.return_subgraph(terminalnode)
	goal_checker_node = goalchecker(node_label)
	current_program_graph.add_node(goal_checker_node,current_program_graph.terminalnodes[0])
	try:
		output = current_program_graph.eval_graph()
	except:
	
	
	
def extend_graph(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links):
	gen = [extendable_nodes for extendable_nodes in search_graph.terminalnodes if extendable_nodes.executed == 1 and extendable_nodes.semantic_failed == 0 and extendable_nodes.world_failed == 0]
	type_compatible_node_links = init_type_compatible_node_links
	for extendable_node in gen: ### for all executed terminal nodes
		search_graph = extend_a_terminalnode(search_graph,extendable_node,type_compatible_node_links,gen)
	
	return search_graph
				################ add child node with multiple links from current parent 
			# if child_node_link_index+1 < len(type_compatible_node_links[extendable_node_name]):				
				# if extendable_node_name in ['identity','head','tail','cons']:
					# type_compatible_node_links = create_type_compatibility(type_compatible_node_links,extendable_node_name,extendable_node,corpus_of_objects,corpus_index)		
					# for next_same_child_nodes in type_compatible_node_links[extendable_node_name][child_node_link_index+1:len(type_compatible_node_links[extendable_node_name])]
						# if next_same_child_nodes['node_name'] == child_node_name:
							
							
						
def metasearcher(corpus_index,init_world):
	# Initialize corpus
	global graph_label
	global node_label
	(corpus_of_objects,init_type_compatible_node_links) = initialize_corpus(corpus_index)
	search_graph = Graph(graph_label)
	initialinput = copy.deepcopy(corpus_of_objects[corpus_index[0]]) ##### create first sensor node
	initialinput.links = (init_world,) ##### attach first sensor node with initial world
	search_graph.add_node(initialinput)
	search_graph = extend_graph(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links)			
				
				
			
			
