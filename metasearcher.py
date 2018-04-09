##### initialize all function objects
import itertools
from collections import defaultdict
import gc
add_obj = add(node_label)
corpus_of_all_objects = {'sensor_number':'sensor(node_label,\'number\')',
					'actuator_number':'actuator(node_label,\'number\')',
					'identity':'identity(node_label)',
					'constant0':'constant(node_label,0)',
					'constant1':'constant(node_label,1)',
					'constant2':'constant(node_label,2)',
					'constant3':'constant(node_label,3)',
					'gaurd':'gaurd(node_label)',
					'equal':'equal(node_label)',
					'lambdagraph':'lambdagraph(node_label)',
					'recurse':'recurse(node_label)',
					'apply':'apply(node_label)',
					'add':'add(node_label)',
					'subtract':'subtract(node_label)',
					'multiply':'multiply(node_label)',
					'greater':'greater(node_label)',
					'conjunct':'conjunct(node_label)',
					'disjunct':'disjunct(node_label)',
					'negate':'negate(node_label)',
					'constant'+str(add_obj):'constant(node_label,add_obj)'}

time_limit = 10000
node_label = 1
node_list_dict={}
C = 0.1
					
#corpus_index = ['sensor_number','actuator_number','identity','constant0','constant1','constant2','constant3','gaurd','equal','lambdagraph','recurse']
corpus_index = ['sensor_number','actuator_number','equal','gaurd','lambdagraph','recurse','constant1']
#corpus_index = ['sensor_number','actuator_number','equal','constant1']


def check_type_compatibility(source_node,target_node,target_node_link):
	node_output_type = source_node.atype['function']['output'][0]
	node_input_type = target_node.atype['function']['input'][target_node_link]
	if type(target_node).__name__ == 'constant' and (type(source_node).__name__ not in ['sensor','identity']):
		return 1
	elif (node_output_type == 'some' or node_output_type == 'any' or node_input_type == 'some' or node_input_type == 'any' ) and node_output_type != 'world' and node_input_type != 'world': ### all inputs are accepted
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
		target_node = eval(corpus_of_objects[j_node])
		for k_in_links in range(target_node.no_of_arguments):
				#node_input_type = corpus_of_objects[j_node].atype['function']['input'][k_in_links]
				####### match input - output type
				
			if check_type_compatibility(output_node,target_node,k_in_links) == 0:
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
		#print(i_node)
		type_compatible_node_links[i_node] = []
		type_compatible_node_links = create_type_compatibility(type_compatible_node_links,i_node,eval(corpus_of_objects[i_node]),corpus_of_objects,corpus_index)
		
	return 	(corpus_of_objects,type_compatible_node_links)
					
	
#(corpus_of_objects,init_type_compatible_node_links) = initialize_corpus(corpus_index)





def extend_a_terminalnode(search_graph,extendable_nodes_index,type_compatible_node_links,gen,corpus_of_objects):
	global node_label
	extendable_node = search_graph.terminalnodes[extendable_nodes_index]
	def get_node_name(extendable_node):
		if type(extendable_node).__name__ == 'sensor':
			extendable_node_name = type(extendable_node).__name__ +'_'+ extendable_node.atype['function']['output'][0]
		elif type(extendable_node).__name__ == 'actuator':
			extendable_node_name = type(extendable_node).__name__ +'_'+ extendable_node.atype['function']['input'][0]
		elif type(extendable_node).__name__ == 'constant':
			extendable_node_name = type(extendable_node).__name__ + str(extendable_node.K)
		else:
			extendable_node_name = type(extendable_node).__name__
		return (extendable_node_name)
		
	extendable_node_name = get_node_name(extendable_node)
	if extendable_node_name in ['identity','head','tail','cons']:
		type_compatible_node_links = create_type_compatibility(type_compatible_node_links,extendable_node_name,extendable_node,corpus_of_objects,corpus_index)
		##### for each child nodes in type compatible list
		
	#to_cleaned_up_terminalnode_index =[]
	def extend_node(type_compatible_node_links,extendable_node_name,extendable_node,search_graph,gen):
		for child_node_link_index,child_node_links in enumerate(copy.copy(type_compatible_node_links[extendable_node_name])):
			child_node_name = child_node_links['node_name']
			child_node_binding_link = child_node_links['link']
			child_node = eval(corpus_of_objects[child_node_name])
			no_of_arguments_of_child_node = child_node.no_of_arguments
			child_node_other_link_list = list(range(no_of_arguments_of_child_node))
			child_node_other_link_list.remove(child_node_binding_link)
			
			if no_of_arguments_of_child_node == 1:
				def extend_single_child(child_node,search_graph,extendable_nodes_index):
					global node_label
					########## create the child node 
					#print(child_node_name)
					#child_node = copy.deepcopy(corpus_of_objects[child_node_name])
					child_node.probability.append(extendable_node.child_node_init_probability)             #child_node_links['init_probability']
					child_node.label = node_label
					node_label += 1
					########## add child node in graph
					#print(child_node)
					#print(type(child_node))
					#print(isinstance(child_node,node))
					search_graph.add_node(child_node,extendable_nodes_index)
					#to_cleaned_up_terminalnode_index.append(extendable_nodes_index)
					#print(child_node)
				extend_single_child(child_node,search_graph,extendable_nodes_index)
				########### update type child node init probability of child node 
				if child_node_name in ['identity','head','tail','cons']:
					########### rerun type compatitbilty update
					type_compatible_node_links = create_type_compatibility(type_compatible_node_links,child_node_name,child_node,corpus_of_objects,corpus_index)
				
				child_node.child_node_init_probability = type_compatible_node_links[child_node_name][0]['init_probability']
				
			else:
			######## Generate all possible permutations of parent nodes
				
				def check_node_compatibitlity(gen,child_node_other_link_list,search_graph):
				######### Enumerate all child node link types
					par_node_idx_list_tuple = []
					for child_link_index in range(no_of_arguments_of_child_node-1):
						par_node_idx_list = []
						for parent_node_index in gen:
							type_compatible = check_type_compatibility(search_graph.terminalnodes[parent_node_index],child_node,child_node_other_link_list[child_link_index])
								#child_node_probability.append(search_graph.terminalnodes[parent_node_index].child_node_init_probability)
							if type_compatible == 0:
								par_node_idx_list.append(parent_node_index)
						par_node_idx_list_tuple.append(par_node_idx_list)
					par_node_idx_list_tuple = tuple(par_node_idx_list_tuple)
					return(par_node_idx_list_tuple)
				
				par_node_idx_list_tuple = check_node_compatibitlity(gen,child_node_other_link_list,search_graph)
				
				def extend_multiple_child(par_node_idx_list_tuple,no_of_arguments_of_child_node,child_node,child_node_other_link_list,search_graph,child_node_binding_link,extendable_nodes_index):
					global node_label
					#gen_parent_nodes = gen
					#gen_parent_nodes.remove(extendable_node)
					for parent_nodes_indices in itertools.product(*par_node_idx_list_tuple,repeat=1):	
						##### check type compatibility
						child_node_probability = []
						# def check_node_compatibitlity(child_node_other_link_list,parent_nodes_indices,search_graph):
							# for child_link_index,parent_node_index in enumerate(parent_nodes_indices):
								# type_compatible = check_type_compatibility(search_graph.terminalnodes[parent_node_index],child_node,child_node_other_link_list[child_link_index])
								# child_node_probability.append(search_graph.terminalnodes[parent_node_index].child_node_init_probability)
								# if type_compatible == 1:
									# break
							# return(type_compatible)
						# type_compatible = check_node_compatibitlity(child_node_other_link_list,parent_nodes_indices,search_graph)
						for parent_node_index in parent_nodes_indices:
							child_node_probability.append(search_graph.terminalnodes[parent_node_index].child_node_init_probability)
				########## add node in graph
						#if type_compatible == 0:
						child_node_probability.insert(child_node_binding_link,extendable_node.child_node_init_probability)
							#child_node = copy.deepcopy(corpus_of_objects[child_node_name])
						child_node.probability = child_node_probability
						child_node.label = node_label
						node_label += 1
						parent_nodes_tuple = list(parent_nodes_indices)
						parent_nodes_tuple.insert(child_node_binding_link,extendable_nodes_index)
							#to_cleaned_up_terminalnode_index += parent_nodes_tuple
						parent_nodes_tuple = tuple(parent_nodes_tuple)
						search_graph.add_node(child_node,*parent_nodes_tuple)
				
				extend_multiple_child(par_node_idx_list_tuple,no_of_arguments_of_child_node,child_node,child_node_other_link_list,search_graph,child_node_binding_link,extendable_nodes_index)
						########### update type child node init probability of child node 
				if child_node_name in ['identity','head','tail','cons']:
				########### rerun type compatitbilty update
					type_compatible_node_links = create_type_compatibility(type_compatible_node_links,child_node_name,child_node,corpus_of_objects,corpus_index)
				
				child_node.child_node_init_probability = type_compatible_node_links[child_node_name][0]['init_probability']
				#################################################################################################
		#to_cleaned_up_terminalnode_index = list(set(to_cleaned_up_terminalnode_index))
		#search_graph.cleanup_terminalnodes(to_cleaned_up_terminalnode_index)
	extend_node(type_compatible_node_links,extendable_node_name,extendable_node,search_graph,gen)
	return search_graph
	
import gc	
	
def evaluate_a_graph(search_graph,executable_node,PHASE):
	global node_label
	global time_limit
	global C
	executed = 0
	#global all_node_dict
	output = None
	start_node_label = node_label
	if executable_node.program_probability != None:
		if PHASE*executable_node.program_probability/C<1:
			return(search_graph,output)
	(current_program_graph,probability) = search_graph.return_subgraph(executable_node,PHASE)
	executable_node.program_probability = probability
	time_limit = PHASE*probability/C
	if PHASE*probability/C <1:
		return(search_graph,output)
	goal_checker_node = goalchecker(node_label)
	current_program_graph.add_node(goal_checker_node,current_program_graph.terminalnodes[0])
	current_program_graph.terminalnodes.pop(0)
	#print(executable_node)
	#print(probability)
	#print(time_limit)
	try:
		output = current_program_graph.eval_graph()
		#print('executed')
		executed = 1
		executable_node.executed = 1
	except world_exception: #### Invalid world action
		#print('world failed')
		executable_node.world_failed = 1
	except time_exception:
		#print('time failed')
		pass
	except:
		#print('semantic failed')
		executable_node.semantic_failed = 1
	finally:
		del (current_program_graph.nodes)
		del (current_program_graph.initialnodes)
		del (current_program_graph.terminalnodes)
		del (current_program_graph)
		del (goal_checker_node)
		#del (output)
		#gc.collect()
		return (search_graph,output)
	

def check_link_group_type_compatibility(target_node,source_nodes,target_node_name):
	if target_node_name == 'gaurd':
		if source_nodes[1].atype['function']['output'] == source_nodes[2].atype['function']['output']:
			return 0
		else:
			return 1
	else:
		return 0




	
	
def extend_graph(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,PHASE):
	global node_label
	gen = [extendable_nodes for extendable_nodes_index,extendable_nodes in enumerate(copy.copy(search_graph.terminalnodes)) 
			if  extendable_nodes.executed == 1 and extendable_nodes.semantic_failed == 0 
			and extendable_nodes.world_failed == 0 
			]
	genidx = [extendable_nodes_index for extendable_nodes_index,extendable_nodes in enumerate(copy.copy(search_graph.terminalnodes)) 
			if  extendable_nodes.executed == 1 and extendable_nodes.semantic_failed == 0 
			and extendable_nodes.world_failed == 0 ]
			#and extendable_nodes.program_probability*extendable_nodes.child_node_init_probability*PHASE > 1]			#extendable_nodes.executed == 1 and
	gennodes = [extendable_nodes for extendable_nodes_index,extendable_nodes in enumerate(copy.copy(search_graph.nodes)) 
				if  extendable_nodes.executed == 1 and extendable_nodes.semantic_failed == 0 
				and extendable_nodes.world_failed == 0 ]
				#and extendable_nodes not in gen] #extendable_nodes.executed == 1 and
	type_compatible_node_links = init_type_compatible_node_links
	for child_node_name in corpus_index:
		child_node = eval(corpus_of_objects[child_node_name])
		
		def check_node_compatibitlity(gen,child_node_name,child_node,search_graph):
			######### Enumerate all child node link types
			par_termnode_list_tuple = []
			for child_link in range(child_node.no_of_arguments):
				par_termnode_list = []
				for parent_node in gen:
					type_compatible = check_type_compatibility(parent_node,child_node,child_link)
						#child_node_probability.append(search_graph.terminalnodes[parent_node_index].child_node_init_probability)
					if type_compatible == 0:
						par_termnode_list.append(parent_node)
				par_termnode_list_tuple.append(par_termnode_list)
			par_termnode_list_tuple = tuple(par_termnode_list_tuple)  ########### all terminalnodes
			
			
			par_node_list_tuple =[]
			for child_link in range(child_node.no_of_arguments):
				par_node_list = []
				for parent_node in gennodes:
					type_compatible = check_type_compatibility(parent_node,child_node,child_link)
						#child_node_probability.append(search_graph.terminalnodes[parent_node_index].child_node_init_probability)
					if type_compatible == 0:
						par_node_list.append(parent_node)
					#else:
						
				par_node_list_tuple.append(par_node_list)  ########## all nodes
			
			final_par_node_list=[]
			if child_node.no_of_arguments == 1 or (len(par_node_list_tuple) ==1 and len(par_node_list_tuple[0])==0):
				final_par_node_list.append(par_termnode_list_tuple)
			else:
				
				########## For no dependency on order of links
				if child_node_name in ['equal','add','disjunct','conjunct','multiply']:
					no_of_iterations=1
				else:
					no_of_iterations = child_node.no_of_arguments
				
				for child_link_termnodes in range(no_of_iterations):
					final_par_node_list_tuple = []
					
					if child_link_termnodes>0:
						remove_idx = child_link_termnodes -1
						par_node_list_tuple[remove_idx] = [x for x in par_node_list_tuple[remove_idx] if x not in par_termnode_list_tuple[remove_idx]]
					
					
					for child_link_nodes in range(child_node.no_of_arguments):
						if child_link_nodes == child_link_termnodes:
							final_par_node_list_tuple.append(par_termnode_list_tuple[child_link_termnodes])
						else:
							#f len(par_node_list_tuple[child_link_nodes]) ==0:
							#	final_par_node_list_tuple =[]
							#	break
							#else:
							final_par_node_list_tuple.append(par_node_list_tuple[child_link_nodes])
					if tuple(final_par_node_list_tuple) not in final_par_node_list:
						final_par_node_list.append(tuple(final_par_node_list_tuple))
				
				#final_par_node_list.append(par_termnode_list_tuple)
				
			return(final_par_node_list)
				
		final_par_node_list = check_node_compatibitlity(gen,child_node_name,child_node,search_graph)
		
		def add_multiple_child(final_par_node_list,child_node,child_node_name,corpus_index,search_graph,type_compatible_node_links):
			global node_label
			for par_node_list_tuple in final_par_node_list:
				########## For no dependency on order of links
				if child_node_name in ['equal','add','disjunct','conjunct','multiply']:
					par_node_combi =defaultdict(list)
					for x in itertools.product(*par_node_list_tuple,repeat=1):
						par_node_combi[tuple(sorted(str(x)))].append(x)
					par_node_combi = [x[0] for x in par_node_combi.values()]
				else:
					par_node_combi = itertools.product(*par_node_list_tuple,repeat=1)
					
				for parent_nodes in par_node_combi:	
					type_compatible = check_link_group_type_compatibility(child_node,parent_nodes,child_node_name)
					if type_compatible == 0:
						child_node_probability = []
						for parent_node in parent_nodes:
							child_node_probability.append(parent_node.child_node_init_probability)
					########## add node in graph
						child_node = eval(corpus_of_objects[child_node_name])
						child_node.probability = child_node_probability

						search_graph.add_node(child_node,*parent_nodes)
						########### update type child node init probability of child node 
						if child_node_name in ['identity','head','tail','cons']:
					########### rerun type compatitbilty update
							type_compatible_node_links = create_type_compatibility(type_compatible_node_links,child_node_name,child_node,corpus_of_objects,corpus_index)
						child_node.child_node_init_probability = type_compatible_node_links[child_node_name][0]['init_probability']
				
		add_multiple_child(final_par_node_list,child_node,child_node_name,corpus_index,search_graph,type_compatible_node_links)
	
				#################################################################################################
	#extend_node(type_compatible_node_links,extendable_node_name,extendable_node,search_graph,gen)
	
	#for extendable_nodes_index in gen: ### for all executed terminal nodes
	#	search_graph = extend_a_terminalnode(search_graph,extendable_nodes_index,type_compatible_node_links,gen,corpus_of_objects)
	search_graph.cleanup_terminalnodes(genidx)
	return search_graph

							

def execute_graph(search_graph,PHASE):
	gen1 = [executable_nodes for executable_nodes in copy.copy(search_graph.terminalnodes) if  executable_nodes.executed == 0 and executable_nodes.semantic_failed == 0 and executable_nodes.world_failed == 0]
	executed = 0
	for executable_node in gen1:
		#print(executable_node)
		(search_graph,output)=evaluate_a_graph(search_graph,executable_node,PHASE)
		if output == 'goal reached':
			return(search_graph,executable_node,executed)
		elif output != None:
			executed = 1
	gc.collect()		
	return(search_graph,None,executed)
							
(corpus_of_objects,init_type_compatible_node_links) = initialize_corpus(corpus_index)


def metasearcher(corpus_index,init_world,corpus_of_objects,init_type_compatible_node_links):
	# Initialize corpus
	global graph_label
	global node_label
	PHASE = 2
	#corpus_of_objects = init_corpus[0]
	#init_type_compatible_node_links = init_corpus[1]
	search_graph = Graph(graph_label)
	initialinput = eval(corpus_of_objects[corpus_index[0]]) ##### create first sensor node
	initialinput.links = (init_world,) ##### attach first sensor node with initial world
	initialinput.executed = 1
	initialinput.probability = [1]
	#initialinput.program_probability =1
	initialinput.child_node_init_probability = init_type_compatible_node_links[corpus_index[0]][0]['init_probability']
	search_graph.add_node(initialinput)
	print(search_graph)
	#search_graph = extend_graph(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links)
	while PHASE < 10000:
		while True:
			search_graph = extend_graph(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,PHASE)
			(search_graph,executable_node,executed)=execute_graph(search_graph,PHASE)
			if executed == 0 or executable_node != None:
				break
			else : 
				print('executed')
		if executable_node != None:
			return (search_graph,executable_node)
		print (PHASE)
		PHASE *= 2
	return (search_graph,None)	
				

#search_graph,exec_node = metasearcher(corpus_index,init_world,corpus_of_objects,init_type_compatible_node_links)	

#cProfile.run('search_graph,exec_node = metasearcher(corpus_index,init_world,corpus_of_objects,init_type_compatible_node_links)')

#cProfile.run('search_graph = extend_graph(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links)')

#cProfile.run('(search_graph,executable_node,executed)=execute_graph(search_graph,PHASE)')		
#print (len(search_graph.nodes))		
#print (len(search_graph.terminalnodes))	
#print(search_graph.terminalnodes)