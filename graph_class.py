import copy
from operator import itemgetter
graph_label = 1
from functools import reduce
class Graph:
	def __init__(self,label,*options):
		global graph_label
		self.label = label
		self.nodes = []
		self.terminalnodes = []
		self.initialnodes = []
		self.atype = {'function':{'input':['none'],'output':['none']}}
		self.glinks = ()
		if len(options)>0:
			self.delterminalnodes = options[0]
		else:
			self.delterminalnodes = 1
		graph_label += 1
			
	def add_node(self, innode,*links):
		#self.atype['function']['output'] += innode.atype['function']['output']
		if len(links) == 0 and innode.no_of_arguments > 0:
			self.initialnodes.append(innode)
			self.atype['function']['input'] += innode.atype['function']['input']
		else:
			# check innode type
			#if not isinstance(innode,node):
			#	raise Exception('invalid input node type')
			# check no. of links
			#if len(links) != innode.no_of_arguments:
			#	raise Exception('invalid number of input links for input node')
			# check link node in graph
			# for item in links:
				# #print(item)
				# if not item in self.nodes:
					# raise Exception ('links not in graph')
			innode.links = links
			# Remove non terminal nodes
			if self.delterminalnodes == 1:
				for item in links:
					try:
						self.terminalnodes.remove(item)
					except:
						valid = 'ok'
				#self.atype['function']['output'].remove(innode.atype['function']['output'])
				
		self.terminalnodes.append(innode)
		self.nodes.append(innode)
		
	def cleanup_terminalnodes(self,terminalnode_indices):
		for item in sorted(terminalnode_indices,reverse=True):
			self.terminalnodes.pop(item)
		
	
	def return_subgraph(self, _terminalnode):
		global graph_label
		global C
		global init_world
		#global node_label
		temp_g = Graph(graph_label)
		temp_g.terminalnodes = [_terminalnode]
		#nodes_probability={}
		#nodes_probability[str(_terminalnode)] = _terminalnode.probability
		new_init_world = copy.deepcopy(init_world)
		
		def graph_return_nodes(self,temp_g,terminalnode):

			linknodes = ()
		# Recursively fetch all parent nodes
			for i,sourcenode in enumerate(terminalnode.links):
				#print (sourcenode)
				if type(sourcenode).__name__=='world': ### terminalnode initialnode
					temp_g.initialnodes.append(terminalnode)
					
				elif len(sourcenode.links) == 0 and sourcenode.no_of_arguments >0: ######### sourcenode initialnode
					temp_g.initialnodes.append(sourcenode)
					graph_return_nodes(self,temp_g,sourcenode)
				else:
					graph_return_nodes(self,temp_g,sourcenode)

			#print(linknodes)
			#print(terminalnode)
			temp_g.nodes.append(terminalnode)
			#nodes_probability[str(terminalnode)] = terminalnode.probability
			return temp_g
			#nodes_probability_list.append((terminalnode,terminalnode.probability))
			#print(linknodes)
			#return terminalnode
		
		temp_g = graph_return_nodes(self,temp_g,_terminalnode)
		temp_g.initialnodes = list(set(temp_g.initialnodes))

		temp_g.nodes = list(set(temp_g.nodes))
		temp_node_label=[]
		if len(temp_g.initialnodes) >1:
			for tempnode in temp_g.initialnodes:
				temp_node_label.append(tempnode.label)
			sorted_node_label_idx = sorted(range(len(temp_node_label)),key=temp_node_label.__getitem__)
			temp_g.initialnodes =[temp_g.initialnodes[j] for j in sorted_node_label_idx]
		temp_g = copy.deepcopy(temp_g)
		
		#### set a copy of init world for initial nodes
		for initnode in temp_g.initialnodes:
			initnode_link_list = list(initnode.links)
			for i,sourcenode in enumerate(initnode.links):
				if type(sourcenode).__name__=='world': 
					initnode_link_list[i]=new_init_world
			initnode.links = tuple(initnode_link_list)
					
		for i in temp_g.nodes:
			i.world = None
			i.data = None
			i.version = None
		#self.atype['function']['output'] = 
		temp_g.atype['function']['output'][0] = _terminalnode.atype
		
		return temp_g
	
	
	# def return_subgraph(self,terminalnode):
	# # Create subgraph from a terminal node
		# global graph_label
		# global tempinitnodes
		# global tempinputtype
		# # check innode type
		# if not isinstance(terminalnode,node):
				# raise Exception('invalid input node type')
		# # check terminal node in graph
		# if not terminalnode in self.nodes:
					# raise Exception ('node not in graph')
		
		# g = Graph(graph_label)
		
		# tempinitnodes = []
		# tempinputtype = []
		# def return_nodes(self,terminalnode,tempnodes):
		# # Recursively fetch all parent nodes
			# global tempinitnodes
			# global tempinputtype
			# #print (terminalnode)
			# if len(terminalnode.links) == 0 and terminalnode.no_of_arguments>0:
				# if not terminalnode in tempinitnodes:
					# tempinitnodes.append(terminalnode)
					# tempinputtype  += terminalnode.atype['function']['input']
			# tempnodes.append(terminalnode)
			# for i,sourcenode in enumerate(terminalnode.links):
				# if isinstance(sourcenode,node):
				# ############ set input output type of link node having some types
					# if sourcenode.atype['function']['output'][0] == 'some' and not terminalnode.atype['function']['input'][i] in ['some','any']:
						# sourcenode.atype['function']['output'][0] = terminalnode.atype['function']['input'][i]
						# temp_index = [i for i,val in enumerate(sourcenode.atype['function']['input']) if val == 'some']
						# for j in temp_index:
							# sourcenode.atype['function']['input'][j] = terminalnode.atype['function']['input'][i]
					# return_nodes(self,sourcenode,tempnodes)
			# return tempnodes
		# node_list = return_nodes(self,terminalnode,[])
		
		# node_list = list(set(node_list))
		# g.nodes = copy.deepcopy(node_list)
		# temp_node_label = []
		# for tempnode in tempinitnodes:
			# if tempnode in node_list:
				# temp_node_label.append(tempnode.label)
				# g.initialnodes.append(g.nodes[node_list.index(tempnode)])
				
		# sorted_node_label_idx = sorted(range(len(temp_node_label)),key=temp_node_label.__getitem__)
		# g.initialnodes =[g.initialnodes[j] for j in sorted_node_label_idx]
		# #tempinputtype = [tempinputtype]
		
		# g.terminalnodes.append(g.nodes[node_list.index(terminalnode)])
		# g.atype['function']['input'] = tempinputtype
		# g.atype['function']['output'] = terminalnode.atype['function']['output']
		# graph_label += 1
		# return g

	def eval_graph(self):
	# evaluate a graph function
		if len(self.terminalnodes) == 1:
			return self.terminalnodes[0].funct()
		else:
			raise Exception('Unable to evaluate graph')
			

