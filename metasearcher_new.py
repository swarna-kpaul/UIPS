import itertools
from collections import defaultdict
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
existing_programs = dict()
C = 0.02
					
#corpus_index = ['sensor_number','actuator_number','identity','constant0','constant1','constant2','constant3','gaurd','equal','lambdagraph','recurse']
#corpus_index = ['sensor_number','actuator_number','equal','gaurd','lambdagraph','recurse','constant1']
corpus_index = ['sensor_number','actuator_number','equal','constant1']


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
	

def evaluate_a_graph(search_graph,executable_node,PHASE):
	global node_label
	global time_limit
	global C
	executed = 0
	#global all_node_dict
	output = None
	start_node_label = node_label
	#if executable_node.program_probability != None:
	#	if PHASE*executable_node.program_probability/C<1:
	#		return output
	current_program_graph= search_graph.return_subgraph(executable_node)
	probability = executable_node.program_probability
	time_limit = PHASE*probability/C
	if PHASE*probability/C <1:
		return output
	goal_checker_node = goalchecker(node_label)
	current_program_graph.add_node(goal_checker_node,current_program_graph.terminalnodes[0])
	#current_program_graph.terminalnodes.pop(0)
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
		executable_node.time_failed = 1
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
		return output
		
		
def check_link_group_type_compatibility(target_node,source_nodes,target_node_name):
	if target_node_name == 'gaurd':
		if source_nodes[1].atype['function']['output'] == source_nodes[2].atype['function']['output']:
			return 0
		else:
			return 1
	else:
		return 0
		
def check_program_presence(parent_nodes,child_node_name):
	global existing_programs
	# check of the child node already present 
	par_node_label_list = [par_node.label for par_node in parent_nodes]
	prog_name = str(par_node_label_list) + child_node_name
	is_exist_program = existing_programs.get(prog_name,0) ### 0- program not exist , 1 - program exist
	return (is_exist_program,par_node_label_list)
	
	
def check_program_probability_criteria(parent_nodes):
	global node_label
	program_probability_list = [par_node.factored_program_probability  for par_node in parent_nodes]
	# merge dictionaries
	merged_factored_program_probability  = dict()
	for each_prob_dict in program_probability_list:
		for k, v in each_prob_dict.items():
			merged_factored_program_probability[k] = v
				
	child_probability_list = [(par_node.child_node_init_probability,par_node.label) for par_node in parent_nodes]
	
	### add child node probabilities in merged probabilities
	for child_probability,par_node_label in child_probability_list:
		merged_factored_program_probability[str(par_node_label)+'-'+str(node_label)] = child_probability
	
	### Calculate total program_probability
	program_probability = 1
	for k,v in merged_factored_program_probability.items():
		program_probability *=v
		
	return (program_probability,merged_factored_program_probability)


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
	global already_checked_pairs
	if PHASE not in already_checked_pairs:
		already_checked_pairs = dict()
		already_checked_pairs[PHASE] = []
	added_node_flag = 0
	########## For no dependency on order of links prune keep only distinct combinations of parent nodes
	if child_node_name in ['equal','add','disjunct','conjunct','multiply']:
		par_node_combi_temp =defaultdict(list)
		#print(par_node_list_tuple)
		for x in itertools.product(*par_node_list_tuple,repeat=1):
			xlabel = [node.label for node in x]
			par_node_combi_temp[tuple(str(sorted(xlabel)))].append(x)
		par_node_combi = [x[0] for x in par_node_combi_temp.values()]
	else:
		par_node_combi = itertools.product(*par_node_list_tuple,repeat=1)
			
	for parent_nodes in par_node_combi: #iterate all combinations of parent nodes for child node
								
		######## Check for program presence	
		is_exist_program,par_node_label_list = 	check_program_presence(parent_nodes,child_node_name)
		if is_exist_program == 1: ##### Program already exist
			continue
		########## Check if pair is already checked
		if [node.label for node in parent_nodes] in already_checked_pairs[PHASE]:
			continue
		
		# check of the child node satisfies probability*PHASE>1 criteria
		program_probability,merged_factored_program_probability  = check_program_probability_criteria(parent_nodes)
		if program_probability*PHASE < 1: ####### if probability criteria not satisfied
			already_checked_pairs[PHASE].append([node.label for node in parent_nodes])
			continue
					
		############## add child node
		child_node = eval(corpus_of_objects[child_node_name])
		child_node.factored_program_probability  = merged_factored_program_probability 
		child_node.program_probability = program_probability
		search_graph.add_node(child_node,*parent_nodes)
		added_node_flag = 1
		existing_programs[str(par_node_label_list) + child_node_name] = 1
		########## update child init probability of newly added node
		if child_node_name in ['identity','head','tail','cons']:
			########### rerun type compatitbilty update
			type_compatible_node_links = create_type_compatibility(type_compatible_node_links,child_node_name,child_node,corpus_of_objects,corpus_index)
		child_node.child_node_init_probability = type_compatible_node_links[child_node_name][0]['init_probability']
				
		######### execute newly added node 
		output = evaluate_a_graph(search_graph,child_node,PHASE)
		if output == 'goal reached':
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
			and extendable_nodes.world_failed == 0 
			and extendable_nodes.program_probability*extendable_nodes.child_node_init_probability*PHASE>1] ## all graph nodes those are executed and not failed and total probability*PHASE >1
		
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
	gen1 = [executable_nodes for executable_nodes in copy.copy(search_graph.nodes) if  executable_nodes.executed == 0 and executable_nodes.time_failed == 1]
	executed = 0
	for executable_node in gen1:
		#print(executable_node)
		output=evaluate_a_graph(search_graph,executable_node,PHASE)
		if output == 'goal reached':
			executed = 1
			return (executable_node,executed)
		elif output != None:
			executed = 1
	gc.collect()		
	return(None,executed)			

		
def metasearcher(search_graph,corpus_index,init_world,corpus_of_objects,init_type_compatible_node_links,PHASE_limit):
	# Initialize corpus
	global graph_label
	global node_label
	PHASE = 2
	#corpus_of_objects = init_corpus[0]
	#init_type_compatible_node_links = init_corpus[1]
	
	print(search_graph)
	#search_graph = extend_graph(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links)
	while PHASE < PHASE_limit:
		# execute time failed nodes from previous phase
		child_node,executed=execute_graph(search_graph,PHASE)
		if child_node != None:
			return child_node
		while True:
			# extend and execute nodes in graph
			child_node,added_node_flag = extend_execute_graph(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,PHASE) 
			if added_node_flag == 0 or child_node != None:
				break
			else : 
				print('executed')
		if child_node != None:
			return child_node
		print (PHASE)
		PHASE *= 2
	return None	
import cProfile
(corpus_of_objects,init_type_compatible_node_links) = initialize_corpus(corpus_index)
already_checked_pairs = dict()
initialinput = eval(corpus_of_objects[corpus_index[0]]) ##### create first sensor node
initialinput.links = (init_world,) ##### attach first sensor node with initial world
initialinput.executed = 1
#initialinput.probability = [1]
initialinput.program_probability =1
initialinput.factored_program_probability['0-'+str(initialinput.label)] = 1
initialinput.child_node_init_probability = init_type_compatible_node_links[corpus_index[0]][0]['init_probability']
search_graph = Graph(graph_label)
search_graph.add_node(initialinput)
existing_programs = dict()
#cProfile.run('exec_node = metasearcher(search_graph,corpus_index,init_world,corpus_of_objects,init_type_compatible_node_links,20000)')
