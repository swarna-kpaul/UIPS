##### initialize all function objects

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

def check_type_compatibility(type_compatible_node_links,i_node,node_output_type,corpus_of_objects,corpus_index):
	for j_node in corpus_index:
			for k_in_links in range(corpus_of_objects[j_node].no_of_arguments):
				node_input_type = corpus_of_objects[j_node].atype['function']['input'][k_in_links]
				####### match input - output type
				if (node_output_type == 'some' or node_output_type == 'any' or node_input_type == 'some' or node_input_type == 'any' ) and node_output_type != 'world' and node_input_type != 'world': ### all inputs are accepted
					type_compatible_node_links[i_node].append({'node_name':j_node,'link':k_in_links})
				elif 'function' in node_input_type and 'function' in node_output_type: ## both are function types
					type_compatible_node_links[i_node].append({'node_name':j_node,'link':k_in_links})
				elif 'list' in node_input_type and 'list' in node_output_type: #both are list type
					node_output_type_list_of = node_output_type['list']
					node_input_type_list_of = node_input_type['list']
					if node_output_type_list_of == 'some' or node_output_type_list_of == 'any' or node_input_type_list_of == 'some' or node_input_type_list_of == 'any': ## type compatible list
						type_compatible_node_links[i_node].append({'node_name':j_node,'link':k_in_links})
					elif node_output_type_list_of == node_output_type_list_of : ## type compatible list
						type_compatible_node_links[i_node].append({'node_name':j_node,'link':k_in_links})
				elif node_output_type == node_input_type:
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
		node_output_type=corpus_of_objects[i_node].atype['function']['output'][0]
		type_compatible_node_links[i_node] = []
		type_compatible_node_links = check_type_compatibility(type_compatible_node_links,i_node,node_output_type,corpus_of_objects,corpus_index)
		
	return 	(corpus_of_objects,type_compatible_node_links)
					
	
(corpus_of_objects,type_compatible_node_links) = initialize_corpus(corpus_index)


def extend_graph(search_graph,corpus_index,corpus_of_objects,type_compatible_node_links):
	for extendable_nodes in search_graph.terminalnodes


def metasearcher(corpus_index,init_world):
	# Initialize corpus
	global graph_label
	global node_label
	(corpus_of_objects,type_compatible_node_links) = initialize_corpus(corpus_index)
	search_graph = Graph(graph_label)
	initialinput = copy.deepcopy(corpus_of_objects[corpus_index[0]]) ##### create first sensor node
	initialinput.links = (init_world,) ##### attach first sensor node with initial world
	search_graph.add_node(initialinput)
				
				
				
			
			
