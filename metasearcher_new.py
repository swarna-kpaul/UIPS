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
					'goalchecker': 'goalchecker(node_label)',
					'constant'+str(add_obj):'constant(node_label,add_obj)'}

time_limit = 10000
node_label = 1
node_list_dict={}
existing_programs = dict()
C = 0.1
call_cnt = 0
					
#corpus_index = ['sensor_number','actuator_number','identity','constant0','constant1','constant2','constant3','gaurd','equal','lambdagraph','recurse']
corpus_index = ['sensor_number','actuator_number','lambdagraph','constant1','recurse','goalchecker','constant2','constant3']
#corpus_index = ['sensor_number','actuator_number','equal','constant1']



	
def modify_probability(child_node_name_link_pair,del_probability,parent_node):
		##### adjust other child node probabilities
	#target_node_name = child_node_probability_dict['node_name']
	divide_factor = len(parent_node.child_node_init_probability) - 1
	for k,v in enumerate(parent_node.child_node_init_probability):
		if v['node_name'] == child_node_name_link_pair[0] and v['link'] == child_node_name_link_pair[1]:
			parent_node.child_node_init_probability[k]['init_probability'] += del_probability
		else:
			parent_node.child_node_init_probability[k]['init_probability'] -= del_probability/divide_factor
		

def check_type_compatibility(source_node,target_node,target_node_link):
	node_output_type = source_node.atype['function']['output'][0]
	node_input_type = target_node.atype['function']['input'][target_node_link]
	if type(target_node).__name__ == 'constant' and (type(source_node).__name__ not in ['sensor','identity']):
		return 1
	elif type(target_node).__name__ == 'goalchecker' and (type(source_node).__name__ not in ['sensor','actuator']):
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
		type_compatible_node_links[i_node][j_node]['init_probability'] = init_probability
	
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


def check_equivalent_program(search_graph,executable_node):
	gen_nodes = [i_nodes for i_nodes_index,i_nodes in enumerate(search_graph.nodes) if  i_nodes.executed == 1 and i_nodes.equivalent_prog == 0]
	#gen_nodes = search_graph.nodes
	for i_node in gen_nodes:
		if i_node.program_expression != None:
			if str(executable_node.program_expression['data']) == str(i_node.program_expression['data']) and str(executable_node.program_expression['world']) == str(i_node.program_expression['world']) and executable_node != i_node:
				executable_node.equivalent_prog =i_node.label
				break

def evaluate_a_graph(search_graph,executable_node,PHASE):
	global node_label
	global time_limit
	global C
	global call_cnt
	executed = 0
	#global all_node_dict
	output = None
	start_node_label = node_label
	#if executable_node.program_probability != None:
	#	if PHASE*executable_node.program_probability/C<1:
	#		return output
	current_program_graph= search_graph.return_subgraph(executable_node)
	new_term_node = current_program_graph.terminalnodes[0]
	probability = executable_node.program_probability
	#print (executable_node,probability)
	time_limit = PHASE*probability/C
	if PHASE*probability/C <1:
		return output
	#goal_checker_node = goalchecker(node_label)
	#current_program_graph.add_node(goal_checker_node,current_program_graph.terminalnodes[0])
	#current_program_graph.terminalnodes.pop(0)
	#print(executable_node)
	#print(probability)
	#print(time_limit)
	try:
		output = current_program_graph.eval_graph()
		reward = output['world'].get_reward()
		output=output['world'].check_goal_state()
		#print('executed')
		executed = 1
		executable_node.program_expression = copy.deepcopy(new_term_node.program_expression)
		check_equivalent_program(search_graph,executable_node)
		executable_node.executed = 1
		executable_node.time_failed = 0
	except world_exception: #### Invalid world action
		#print('world failed')
		reward = 0
		executable_node.world_failed = 1
	except time_exception:
		#print('time failed')
		reward = 0 
		executable_node.time_failed = 1
	except Exception as e:
		#print('semantic failed')
		#print(executable_node)
		#print(e)
		reward = 0
		executable_node.semantic_failed = 1
	finally:
		if call_cnt >100:
			print(executable_node)
		executable_node.reward = reward
		del (current_program_graph.nodes)
		del (current_program_graph.initialnodes)
		del (current_program_graph.terminalnodes)
		del (current_program_graph)
		#del (goal_checker_node)
		#del (output)
		#gc.collect()
		#executable_node
		#if output != None:
		return output
		#else:
		#	return output
		
		
def check_link_group_type_compatibility(source_nodes,target_node_name):
	if target_node_name == 'gaurd':
		if (source_nodes[1].atype['function']['output'] == source_nodes[2].atype['function']['output']) or (source_nodes[1].atype['function']['output'] =='some' or source_nodes[2].atype['function']['output'] =='some') or ('function' in source_nodes[1].atype['function']['output'] and 'function' in source_nodes[2].atype['function']['output']) or ('list' in source_nodes[1].atype['function']['output'] and 'list' in source_nodes[2].atype['function']['output']):
			return 0
		else:
			return 1
	elif target_node_name == 'equal':
		if (source_nodes[0].atype['function']['output'] == source_nodes[1].atype['function']['output']) or (source_nodes[0].atype['function']['output'] =='some' or source_nodes[1].atype['function']['output'] =='some') or ('function' in source_nodes[0].atype['function']['output'] and 'function' in source_nodes[1].atype['function']['output']) or ('list' in source_nodes[0].atype['function']['output'] and 'list' in source_nodes[1].atype['function']['output']):
			return 0
		else:
			return 1
	elif target_node_name == 'recurse':
		if 'iW()' not in (str(source_nodes[1].program_expression['data'])):
			return 1
		else : 
			return 0
	else:
		return 0
		
def check_program_presence(parent_nodes,child_node_name):
	global existing_programs
	# check of the child node already present 
	par_node_label_list = [par_node.label for par_node in parent_nodes]
	prog_name = str(par_node_label_list) + child_node_name
	is_exist_program = existing_programs.get(prog_name,0) ### 0- program not exist , 1 - program exist
	return (is_exist_program,par_node_label_list)
	

def calculate_total_program_probability(merged_factored_program_probability):
	program_probability = 1
	for k,v in merged_factored_program_probability.items():
		program_probability *=v['init_probability']
	return program_probability

def check_program_probability_criteria(parent_nodes,child_node_name):
	global node_label
	program_probability_list = [par_node.factored_program_probability  for par_node in parent_nodes]
	# merge dictionaries
	merged_factored_program_probability  = dict()
	for each_prob_dict in program_probability_list:
		for k, v in each_prob_dict.items():
			merged_factored_program_probability[k] = v
	
	child_probability_list = []
	for k,par_node in enumerate(parent_nodes):
		child_probability_list.append(([ child_probability for child_probability in par_node.child_node_init_probability if child_probability['node_name'] == child_node_name and child_probability['link'] == k][0],par_node.label))
	
	### add child node probabilities in merged probabilities
	for child_probability,par_node_label in child_probability_list:
		merged_factored_program_probability[str(par_node_label)+'-'+str(node_label)] = child_probability
	
	return merged_factored_program_probability


def check_node_compatibitlity(gen,child_node_name,child_node,search_graph):
	# create a tuple of list of nodes parent nodes for child node
	# For each link of child node there should be a list of type compatible parent nodes from graph.nodes
	# For example child node CN has 2 input links of type A and B. The parent node list [n1,n2,n3] is compatible with type A and [n4,n5] is compatible with type B
	# So the output of this function for child node CN will be ([n1,n2,n3],[n4,n5]) 
	par_node_list_tuple = []
	for child_link in range(child_node.no_of_arguments):
		par_node_list = []
		for parent_node in gen:
			type_compatible = check_type_compatibility(parent_node,child_node,child_link) ######## check type compatibility for each link
			if type_compatible == 0:
				par_node_list.append(parent_node)
		par_node_list_tuple.append(par_node_list)
	return tuple(par_node_list_tuple)


def add_multiple_child_node(par_node_list_tuple,child_node,child_node_name,corpus_index,corpus_of_objects,search_graph,type_compatible_node_links,PHASE):
	global node_label
	global existing_programs
	#global already_checked_pairs
	added_node_flag = 0
	########## For no dependency on order of links prune keep only distinct combinations of parent nodes
	if child_node_name in ['equal','add','disjunct','conjunct','multiply']:
		par_node_combi = itertools.combinations_with_replacement(par_node_list_tuple[0],child_node.no_of_arguments)
	else:
		par_node_combi = itertools.product(*par_node_list_tuple,repeat=1)
			
	for parent_nodes in par_node_combi: #iterate all combinations of parent nodes for child node
								
		######## Check for program presence	
		is_exist_program,par_node_label_list = 	check_program_presence(parent_nodes,child_node_name)
		if is_exist_program != 0: ##### Program already exist
			if is_exist_program.executed == 1 or is_exist_program.world_failed == 1 or is_exist_program.semantic_failed == 1 or is_exist_program.equivalent_prog != 0 or is_exist_program.time_failed ==1:
				continue
		########## Check if pair is already checked
		#if [node.label for node in parent_nodes] in already_checked_pairs[PHASE]:
		#	continue
		
		
		if check_link_group_type_compatibility(parent_nodes,child_node_name):
			continue
					
		############## add child node
		if is_exist_program == 0:
			# check of the child node satisfies probability*PHASE>1 criteria
			merged_factored_program_probability  = check_program_probability_criteria(parent_nodes,child_node_name)
			program_probability = calculate_total_program_probability(merged_factored_program_probability)
			if program_probability*PHASE < 1: ####### if probability criteria not satisfied
		#	already_checked_pairs[PHASE].append([node.label for node in parent_nodes])
				continue
			child_node = eval(corpus_of_objects[child_node_name])
			child_node.factored_program_probability  = merged_factored_program_probability 
			child_node.program_probability = program_probability
			search_graph.add_node(child_node,*parent_nodes)
			added_node_flag = 1
			#existing_programs[str(par_node_label_list) + child_node_name] = 1
			existing_programs[str(par_node_label_list) + child_node_name] = child_node
			########## update child init probability of newly added node
			######### execute newly added node 
			output = evaluate_a_graph(search_graph,child_node,PHASE)
			
			############### incremental learning
			update_probability(child_node)
			
			if 	child_node.semantic_failed == 0  and child_node.equivalent_prog == 0:
				if child_node_name in ['identity','head','tail','cons']:
			########### rerun type compatitbilty update
					type_compatible_node_links = create_type_compatibility(type_compatible_node_links,child_node_name,child_node,corpus_of_objects,corpus_index) ## update type compatibility
			
				child_node.child_node_init_probability = copy.deepcopy(type_compatible_node_links[child_node_name])	
		else:
			#print('existin prog')
			#print(is_exist_program)
			is_exist_program.program_probability = calculate_total_program_probability(is_exist_program.factored_program_probability)
			if is_exist_program.program_probability*PHASE < 1: ####### if probability criteria not satisfied
		#	already_checked_pairs[PHASE].append([node.label for node in parent_nodes])
				continue
			output = evaluate_a_graph(search_graph,is_exist_program,PHASE)
			#child_node.child_node_init_probability = type_compatible_node_links[child_node_name][0]['init_probability']
			child_node = is_exist_program
			###### incremental learning
			update_probability(is_exist_program)	
			if output == True:
				print(is_exist_program)
		
		if output == True:
			print('Goal Reached')
			return(child_node,added_node_flag)
			
	return(None,added_node_flag)

	
		
def extend_execute_graph(search_graph,corpus_index,corpus_of_objects,type_compatible_node_links,PHASE):

	#Trying to add all possible corpus new nodes
	global node_label
	added_node_flag = 0
	for child_node_name in corpus_index:
		child_node = eval(corpus_of_objects[child_node_name])
		### Create list of extendable parent nodes
		gen = [extendable_nodes for extendable_nodes_index,extendable_nodes in enumerate(copy.copy(search_graph.nodes)) 
			if  extendable_nodes.executed == 1 and extendable_nodes.semantic_failed == 0 
			and extendable_nodes.world_failed == 0 and extendable_nodes.equivalent_prog == 0
			and extendable_nodes.program_probability*(max([child_probability['init_probability'] for child_probability in extendable_nodes.child_node_init_probability]))*PHASE>1] ## all graph nodes those are executed and not failed and total probability*PHASE >1
		
		## Create type compatible parent node list for each links of child node
		par_node_list_tuple = check_node_compatibitlity(gen,child_node_name,child_node,search_graph)
		########## Add and execute multiple child nodes
		child_node,added_node_flag_temp = add_multiple_child_node(par_node_list_tuple,child_node,child_node_name,corpus_index,corpus_of_objects,search_graph,type_compatible_node_links,PHASE)
		if added_node_flag_temp == 1:
			added_node_flag =1
		if child_node != None:
			return (child_node,added_node_flag)
	gc.collect()
	return(None,added_node_flag)
	
def execute_graph(search_graph,PHASE):
	gen1 = [executable_nodes for executable_nodes in copy.copy(search_graph.nodes) if  executable_nodes.executed == 0 and executable_nodes.time_failed == 1 and executable_nodes.program_probability*PHASE>1]
	executed = 0
	for executable_node in gen1:
		#print(executable_node)
		output=evaluate_a_graph(search_graph,executable_node,PHASE)
		update_probability(executable_node)
		if output == True:
			executed = 1
			print('Goal Reached 2')
			return (executable_node,executed)
		elif output != None:
			executed = 1
	gc.collect()		
	return(None,executed)			

def reset_search_graph(search_graph,init_world):
	for i_nodes in search_graph.nodes:
		i_nodes.executed =0
		i_nodes.world_failed = 0
		i_nodes.time_failed = 0
		i_nodes.world = None
		i_nodes.world_version = None
		i_nodes.reward = 0
	search_graph.nodes[0].links = (init_world,)
	search_graph.nodes[0].executed=1
	
def initialize_search_graph(init_world,corpus_index):
	global graph_label
	global node_label
	global existing_programs
	node_label = 1
	graph_label = 1
	(corpus_of_objects,init_type_compatible_node_links) = initialize_corpus(corpus_index)
	initialinput = eval(corpus_of_objects[corpus_index[0]]) ##### create first sensor node
	#initialinput.links = (init_world,) ##### attach first sensor node with initial world
	initialinput.executed = 1
	initialinput.program_probability =1
	initialinput.factored_program_probability['0-'+str(initialinput.label)] = {'node_name':corpus_index[0],'link':0,'init_probability':1}
	initialinput.child_node_init_probability = copy.deepcopy(init_type_compatible_node_links[corpus_index[0]])
	initialinput.program_expression = {'data':symbols('iW().iS()'),'world':'iW().iS()'}
	search_graph = Graph(graph_label)
	search_graph.add_node(initialinput)
	existing_programs = dict()
	return (search_graph,corpus_of_objects,init_type_compatible_node_links)
		
def metasearcher(search_graph,corpus_index,init_world,corpus_of_objects,init_type_compatible_node_links,PHASE_limit):
	# Initialize corpus
	global graph_label
	global node_label
	#global search_graph
	PHASE = 2
	reset_search_graph(search_graph,init_world)
	#search_graph = extend_graph(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links)
	while PHASE < PHASE_limit:
		# execute time failed nodes from previous phase
		child_node,executed=execute_graph(search_graph,PHASE)
		if executed ==1:
			print('time_executed')
		if child_node != None:
			return (child_node,search_graph)
			
		while True:
			# extend and execute nodes in graph
			child_node,added_node_flag = extend_execute_graph(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,PHASE) 
			if added_node_flag == 0 or child_node != None:
				break
			else : 
				print('executed')
		if child_node != None:
			return (child_node,search_graph)
		print (PHASE)
		PHASE *= 2
	return (None,search_graph)	
import cProfile

(search_graph,corpus_of_objects,init_type_compatible_node_links) = initialize_search_graph(init_world,corpus_index)

#cProfile.run('exec_node,search_graph = metasearcher(search_graph,corpus_index,init_world,corpus_of_objects,init_type_compatible_node_links,150000)')
#exec_node,search_graph = metasearcher(corpus_index,init_world,corpus_of_objects,init_type_compatible_node_links,1200000)