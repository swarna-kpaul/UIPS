## Classes of primitive functions
#global time_limit 
#global node_label
time_limit = 1
node_label = 1
#all_node_dict = {}
class null:
	def __init__(self):
		self.name=None
		
null=null()

class time_exception(Exception):
	pass

class node:
	def __init__(self,label,no_of_arguments,atype, inlinks):
		global node_label
		if not is_number(label):
			raise Exception('Invalid node label')
		self.label = label
		self.no_of_arguments = no_of_arguments
		self.atype = atype
		self.links = inlinks
		node_label = node_label + 1
		self.world = None
		self.world_version = None
		self.data = None
		self.executed = 0
		self.semantic_failed = 0
		self.world_failed = 0
		self.time_failed = 0
		self.child_node_init_probability = None
		self.program_probability = None
		self.factored_program_probability = dict()
		self.program_expression =None
		self.update_exp = 1
		self.equivalent_prog =0
		self.reward = 0
	
	
	
	@property
	def links(self):
		return self.__links
	
	@links.setter	
	def links(self,inlinks):
		#if len(links) <= self.no_of_arguments:
		#print('test link')
		########## Type checking
		# def generic_type_check(self):
			# input_atype=self.atype
			# #print (inlinks)
			# #print(input_atype)
			# try:
				# for i in range(min(self.no_of_arguments,len(inlinks))):
					# node_input_type = input_atype['function']['input'][i]
					# link_out_atype = inlinks[i].atype['function']['output'][0]
					# #print(i)
					# #print (link_out_atype)
					# #print (node_input_type)
					# if isinstance(node_input_type,dict) :
		# # function or list type
						# if isinstance(link_out_atype,dict):
							# if 'function' in node_input_type and 'function' in link_out_atype:
								# valid = 'ok'
							# elif 'list' in node_input_type and 'list' in link_out_atype:
								# if node_input_type['list'] == link_out_atype['list'] or link_out_atype['list'] == 'none' or node_input_type['list'] == 'some':
									# valid = 'ok'
								# else:
									# raise Exception('Type Mismatch')
							# else:
								# raise Exception('Type Mismatch')
						# elif link_out_atype == 'some':
							# valid = 'ok'
							# ## Update some link
							# #print('ok')
							# # inlinks[i].atype['function']['output'][0] = input_atype['function']['input'][i]
							# # for j in range(len(inlinks[i].atype['function']['input'])):
								# # if inlinks[i].atype['function']['input'][j] == 'some':
									# # inlinks[i].atype['function']['input'][j] = input_atype['function']['input'][i]
						# else:
							# raise Exception('Type Mismatch')
					# elif node_input_type == 'any':
						# valid = 'ok'
					# elif node_input_type == 'some':
						# valid = 'ok'
					# elif link_out_atype == 'some':
						# valid = 'ok'
						# # inlinks[i].atype['function']['output'][0] = input_atype['function']['input'][i]
						# # for j in range(len(inlinks[i].atype['function']['input'])):
							# # if inlinks[i].atype['function']['input'][j] == 'some':
								# # inlinks[i].atype['function']['input'][j] = input_atype['function']['input'][i]
					# elif not isinstance(link_out_atype,dict) and (link_out_atype == node_input_type ) :
						# valid = 'ok'
					# else:
						# raise Exception('Type Mismatch')
						
				# node_input_type = input_atype['function']['input']
				# temp_set = []
				# print(self)
				# print(inlinks)
				# for i,val in enumerate(node_input_type):
					# print(i)
					# if i > len(inlinks)-1:
						# break
					# if val=='some':
						# temp_set.append(inlinks[i].atype['function']['output'][0])
				# ########## check for some type in list type
					# if isinstance(val,dict) and 'list' in val:
						# if val['list'] == 'some':
							# temp_set.append(inlinks[i].atype['function']['output'][0]['list'])
				# ############### check for some type in function type
					# if isinstance(val,dict) and 'function' in val:
						# if val['function'] == 'some':
							# temp_set.append(inlinks[i].atype['function']['output'][0]['function'])
						# elif 'input' in val['function']:
							# if val['function']['input'][0] == 'some':
								# temp_set.append(inlinks[i].atype['function']['output'][0]['function']['input'][0])
							# if val['function']['output'][0] == 'some':
								# temp_set.append(inlinks[i].atype['function']['output'][0]['function']['output'][0])
				# #print(set(temp_set))
				# try: 
					# temp_set.remove('some')
					# temp_set.remove('any')
				# except:
					# valid = 'ok'
				# print(temp_set)
				# if len(temp_set) <= 1:
					# valid = 'ok'
				# else:
					# for j in temp_set:
						# if j != temp_set[0]:
							# raise Exception('Type Mismatch')
						# else:
							# return valid
			# except:
				# print('Type Mismatch')
				# raise
		def update_type(self):
			if type(self).__name__=='head':
				self.atype['function']['input'] = self.links[0].atype['function']['output']
				self.atype['function']['output'][0] = self.links[0].atype['function']['output'][0]['list']
			elif type(self).__name__=='tail':
				self.atype['function']['input'] = self.links[0].atype['function']['output']
				self.atype['function']['output'] = self.links[0].atype['function']['output']
			elif type(self).__name__=='cons':
				self.atype['function']['input'] = [self.links[0].atype['function']['output'][0],self.links[1].atype['function']['output'][0]]
				self.atype['function']['output'][0] = {'list':self.links[1].atype['function']['output'][0]}
			elif type(self).__name__=='identity':
				self.atype['function']['input'] = self.links[0].atype['function']['output']
				self.atype['function']['output'] = self.links[0].atype['function']['output']
		#generic_type_check(self)
		self.__links = inlinks
		if self.no_of_arguments <= len(inlinks):
			update_type(self)
		
		
	def funct(self):
		global time_limit
		time_limit = time_limit - 1
		if time_limit < 1:
			raise time_exception ('time over')
			
	def update_program_expression(self,node_name,node_output):
		if self.update_exp == 1:
			current_expression = get_program_expression(node_name,self,node_output)
			if str(current_expression['data']) == 'True' :
				current_expression['data'] = True
			elif str(current_expression['data']) == 'False':
				current_expression['data'] = False
			self.program_expression = current_expression
			#print(current_expression)

		
class add(node):
# Node object for addition function
	def __init__(self,label, *links):
		node.__init__(self,label,2,{'function':{'input':['number','number'],'output':['number']}},links)
		
	def funct(self):
		super().funct()
		if self.data == None:
			link1_in = self.links[0].funct()
			link2_in = self.links[1].funct()
			self.data =  link1_in['data'] + link2_in['data']
			self.world = link1_in['world']
			self.world_version = self.world.version
		super().update_program_expression('add',self.data)
		return  {'data':self.data,'world':self.world}
		
class identity(node):
# Node object for addition function
	def __init__(self,label, *links):
		node.__init__(self,label,1,{'function':{'input':['some'],'output':['some']}},links)
		
	def funct(self):
		super().funct()
		if self.data == None:
			link1_in = self.links[0].funct()
			self.data =  link1_in['data']
			self.world = link1_in['world']
			self.world_version = self.world.version
			super().update_program_expression('identity',self.data)
		return {'data':copy.deepcopy(self.data),'world':self.world}
		
class constant(node):
# Node for constant
	def __init__(self,label,K,*links):
		node.__init__(self,label,1,{'function':{'input':['any'],'output':['any']}},links)
		self.K = K
		if isinstance(K,node) or isinstance(K,Graph):
		########## for function type
			# if isinstance(K,true) or isinstance(K,false):
				# self.atype['function']['output'][0] = 'boolean'
			# else:
			self.atype['function']['output'][0] = K.atype
		if isinstance(K,list):
		########### For list type
			if len(K) == 0:
				self.atype['function']['output'][0] = {'list':'any'}
			elif is_number(K[0]):
				self.atype['function']['output'][0] = {'list':'number'}
			elif is_instance(is_number(K[0]),true) or is_instance(is_number(K[0]),false):
				self.atype['function']['output'][0] = {'list':'boolean'}
			elif is_instance(is_number(K[0]),node):
				self.atype['function']['output'][0] = {'list':K[0].atype}
			elif is_char(K[0]):
				self.atype['function']['output'][0] = {'list':'character'}
		elif is_number(K):
		########### For number type
			self.atype['function']['output'][0] = 'number'
		elif K == null:
			self.atype['function']['output'][0] = 'none'
		elif is_char(K):
		########### For character type
			self.atype['function']['output'][0] = 'character'

		
	
	def funct(self):
		super().funct()
		if self.data == None:
			link1_in = self.links[0].funct()
			self.data = self.K
			self.world = link1_in['world']
			self.world_version = self.world.version
			super().update_program_expression('constant',self.data)
		return {'data':copy.deepcopy(self.data),'world':self.world}

class subtract(node):
# Node class for subtract function
	def __init__(self,label, *links):
		node.__init__(self,label,2,{'function':{'input':['number','number'],'output':['number']}},links)
		
	def funct(self):
		super().funct()
		if self.data == None:
			link1_in = self.links[0].funct()
			link2_in = self.links[1].funct()
			self.data =  link1_in['data'] - link2_in['data']
			self.world = link1_in['world']
			self.world_version = self.world.version
			super().update_program_expression('subtract',self.data)
		return  {'data':self.data,'world':self.world}

class multiply(node):
# Node class for multiply function
	def __init__(self,label, *links):
		node.__init__(self,label,2,{'function':{'input':['number','number'],'output':['number']}},links)
		
	def funct(self):
		super().funct()
		if self.data == None:
			link1_in = self.links[0].funct()
			link2_in = self.links[1].funct()
			self.data =  link1_in['data'] * link2_in['data']
			self.world = link1_in['world']
			self.world_version = self.world.version
			super().update_program_expression('multiply',self.data)
		return  {'data':self.data,'world':self.world}
		
class divide(node):

# Node class for divide function
	def __init__(self,label, *links):
		node.__init__(self,label,2,{'function':{'input':['number','number'],'output':['number']}},links)
		
	def funct(self):
		super().funct()
		if self.data == None:
			link1_in = self.links[0].funct()
			link2_in = self.links[1].funct()
			self.data =  link1_in['data'] / link2_in['data']
			self.world = link1_in['world']
			self.world_version = self.world.version
			super().update_program_expression('divide',self.data)
		return  {'data':self.data,'world':self.world}

class gaurd(node):
	def __init__(self,label, *links):
		node.__init__(self,label,3,{'function':{'input':['boolean','some','some'],'output':['some']}},links)
		
	def funct(self):
		super().funct()
		#print(self.links[0])
		if self.data == None:
			link1_in = self.links[0].funct()
			if str(link1_in['data']) not in ('True','False'):
				raise Exception('Invalid input type for gaurd')
			if link1_in['data'] == True:
				link2_in = self.links[1].funct()
				self.data =  link2_in['data']
				self.world = link2_in['world']
				self.world_version = self.world.version
			elif link1_in['data'] == False:
				link3_in = self.links[2].funct()
				self.data =  link3_in['data']
				self.world = link3_in['world']
				self.world_version = self.world.version
			super().update_program_expression('gaurd',self.data)
		return  {'data':copy.deepcopy(self.data),'world':self.world}


class equal(node):
# Node class for divide function
	def __init__(self,label, *links):
		node.__init__(self,label,2,{'function':{'input':['some','some'],'output':['boolean']}},links)
		
	def funct(self):
		global node_label
		super().funct()
		if self.data == None:
			link1_in = self.links[0].funct()
			link2_in = self.links[1].funct()
			if link1_in['data'] == link2_in['data']:
				self.data =  True
				self.world = link1_in['world']
				self.world_version = self.world.version
			else:
				self.data =  False
				self.world = link1_in['world']
				self.world_version = self.world.version
			super().update_program_expression('equal',self.data)
		return  {'data':copy.deepcopy(self.data),'world':self.world}


class greater(node):
# Node class for divide function
	def __init__(self,label, *links):
		node.__init__(self,label,2,{'function':{'input':['number','number'],'output':['boolean']}},links)
		
	def funct(self):
		global node_label
		super().funct()
		if self.data == None:
			link1_in = self.links[0].funct()
			link2_in = self.links[1].funct()
			if link1_in['data'] > link2_in['data']:
				self.data =  True
				self.world = link1_in['world']
				self.world_version = self.world.version
			else:
				self.data =  False
				self.world = link1_in['world']
				self.world_version = self.world.version
			super().update_program_expression('greater',self.data)
		return  {'data':copy.deepcopy(self.data),'world':self.world}
			
class lesser(node):

# Node class for divide function
	def __init__(self,label, *links):
		node.__init__(self,label,2,{'function':{'input':['number','number'],'output':['boolean']}},links)
		
	def funct(self):
		global node_label
		super().funct()
		if self.data == None:
			link1_in = self.links[0].funct()
			link2_in = self.links[1].funct()
			if link1_in['data'] < link2_in['data']:
				self.data =  True
				self.world = link1_in['world']
				self.world_version = self.world.version
			else:
				self.data =  False
				self.world = link1_in['world']
				self.world_version = self.world.version
		return  {'data':copy.deepcopy(self.data),'world':self.world}

class conjunct(node):

# Node class for divide function
	def __init__(self,label, *links):
		node.__init__(self,label,2,{'function':{'input':['boolean','boolean'],'output':['boolean']}},links)
		
	def funct(self):
		global node_label
		super().funct()
		if self.data == None:
			link1_in = self.links[0].funct()
			link2_in = self.links[1].funct()
			if link1_in['data'] and link2_in['data']:
				self.data =  True
				self.world = link1_in['world']
				self.world_version = self.world.version
			else:
				self.data =  False
				self.world = link1_in['world']
				self.world_version = self.world.version
			super().update_program_expression('conjunct',self.data)
		return  {'data':copy.deepcopy(self.data),'world':self.world}
			
class disjunct(node):

# Node class for divide function
	def __init__(self,label, *links):
		node.__init__(self,label,2,{'function':{'input':['boolean','boolean'],'output':['boolean']}},links)
		
	def funct(self):
		global node_label
		super().funct()
		if self.data == None:
			link1_in = self.links[0].funct()
			link2_in = self.links[1].funct()
			if link1_in['data'] or link2_in['data']:
				self.data =  True
				self.world = link1_in['world']
				self.world_version = self.world.version
			else:
				self.data =  False
				self.world = link1_in['world']
				self.world_version = self.world.version
			super().update_program_expression('disjunct',self.data)
		return  {'data':copy.deepcopy(self.data),'world':self.world}
			
class negate(node):

# Node class for divide function
	def __init__(self,label, *links):
		node.__init__(self,label,1,{'function':{'input':['boolean'],'output':['boolean']}},links)
		
	def funct(self):
		global node_label
		super().funct()
		if self.data == None:
			link1_in = self.links[0].funct()
			self.data =  not link1_in['data']
			self.world = link1_in['world']
			self.world_version = self.world.version
			super().update_program_expression('negate',self.data)
		return  {'data':copy.deepcopy(self.data),'world':self.world}
			
class head(node):

# Node class for head function
	def __init__(self,label, *links):
		node.__init__(self,label,1,{'function':{'input':[{'list':'some'}],'output':['some']}},links)
		
	def funct(self):
		super().funct()
		temp_list = self.links[0].funct()
		if self.data == None:
			link1_in = self.links[0].funct()
			if not isinstance(link1_in['data'],list):
				raise Exception ('Invalid Input Type for head')
			try:
				self.data = link1_in['data'][0]
			except IndexError: 
				self.data = null
			self.world = link1_in['world']
			self.world_version = self.world.version
			super().update_program_expression('head',self.data)
		return  {'data':copy.deepcopy(self.data),'world':self.world}
		

class tail(node):
	def __init__(self,label, *links):
		node.__init__(self,label,1,{'function':{'input':[{'list':'some'}],'output':[{'list':'some'}]}},links)
		
	def funct(self):
		super().funct()
		list_var = self.links[0].funct()
		if self.data == None:
			link1_in = self.links[0].funct()
			temp_list = link1_in['data']
			if not isinstance(temp_list,list):
				raise Exception ('Invalid Input Type tail')
			self.data = temp_list[1:len(temp_list)]
			self.world = link1_in['world']
			self.world_version = self.world.version
			super().update_program_expression('tail',self.data)
		return  {'data':copy.deepcopy(self.data),'world':self.world}

		
class cons(node):
# Node class for head function
	def __init__(self,label, *links):
		node.__init__(self,label,2,{'function':{'input':[{'list':'some'},'some'],'output':[{'list':'some'}]}},links)
		
	def funct(self):
		super().funct()
		if self.data == None:
			link1_in = self.links[0].funct()
			if not isinstance(link1_in['data'],list):
				raise Exception ('Invalid Input Type for cons')
			link2_in = self.links[1].funct()
			self.data = link1_in['data'].append(link2_in['data'])
			self.world = link1_in['world']
			self.world_version = self.world.version
			super().update_program_expression('cons',self.data)
		return  {'data':copy.deepcopy(self.data),'world':self.world}

		
class nil(node):
	def __init__(self,label,*links):
		node.__init__(self,label,1,{'function':{'input':['any'],'output':[{'list':'null'}]}},links)
	def funct(self):
		super().funct()
		if self.data == None:
			link1_in = self.links[0].funct()
			self.data = []
			self.world = link1_in['world']
			self.world_version = self.world.version
			super().update_program_expression('nil',self.data)
		return  {'data':copy.deepcopy(self.data),'world':self.world}

		
def is_number(n):
    try:
        float(n)   # Type-casting the string to `float`.
                   # If string is not a valid `float`, 
                   # it'll raise `ValueError` exception
    except:
        return False
    return True

def is_char(n):
    try:
        n.isalpha()   # Type-casting the string to `float`.
                   # If string is not a valid `float`, 
                   # it'll raise `ValueError` exception
    except:
        return False
    return True
	
###################### Higher order functions
class apply(node):

# Node class for apply function
	def __init__(self,label, *links):
		node.__init__(self,label,3,{'function':{'input':[{'function':{'input':['any'],'output':['any']}},'any','any'],'output':['some']}},links)
		
	def funct(self):
		global node_label
		super().funct()
		
		if self.data == None:
			link1_in = self.links[0].funct()
			input_funct = link1_in['data']
			
			if isinstance(input_funct,Graph):
				if len(input_funct.atype['function']['input']) <= len(input_funct.glinks)+2 :
			# number of input arguments satisfied
					input_funct.glinks += self.links[1:3]
					index = 0
					for initnode in input_funct.initialnodes:
					#print (initnode)
						initnode.links = input_funct.glinks[index:(index+initnode.no_of_arguments)]
						index += initnode.no_of_arguments
				##### set output type of apply node
					self.atype['function']['output'] = input_funct.atype['function']['output']
				#print (input_funct.terminalnodes[0].funct())
					if self.links[0].program_expression != None:
						for i_node in input_funct.nodes:
							i_node.update_exp = 1
					output = input_funct.terminalnodes[0].funct()
					self.data = output['data']
					self.world = output['world']
					self.world_version = self.world.version
					self.program_expression = input_funct.terminalnodes[0].program_expression
				else:
					input_funct.glinks += self.links[1:3]
					temp_atpye = input_funct.atype
					temp_atpye['function']['input'] = temp_atpye['function']['input'][2:len(temp_atpye['function']['input'])]
					self.atype['function']['output'][0] = temp_atpye
					self.data =  input_funct
					if self.links[0].program_expression != None:
						super().update_program_expression('apply',self.data)
			elif isinstance(input_funct,node):
				if input_funct.no_of_arguments <= len(input_funct.links)+2:
					input_funct.links += self.links[1:3]
					self.atype['function']['output'] = input_funct.atype['function']['output']
					output =  input_funct.funct()
					self.data = output['data']
					self.world = output['world']
					self.world_version = self.world.version
					self.program_expression = input_funct.program_expression
				else:
		#### Return Partial function
					input_funct.links += self.links[1:3]
					temp_atpye = input_funct.atype
					temp_atpye['function']['input'] = temp_atpye['function']['input'][2:len(temp_atpye['function']['input'])]
					self.atype['function']['output'][0] = temp_atpye
					self.data = input_funct
					super().update_program_expression('apply',self.data)
			else:
				raise Exception('invalid input type')
		
		return  {'data':copy.deepcopy(self.data),'world':self.world}

class recurse(node):

	def __init__(self,label, *links):
		#print(links[2].atype)
		# try:
			# if len(links) >= 2:
				# if links[1].atype['function']['output'][0]['function']['output'][0] == 'boolean':
					# valid = 'ok'
				# else:
					# raise Exception('Type Mismatch')
		# except:
			# raise Exception('Type Mismatch')
		node.__init__(self,label,3,{'function':{'input':[{'function':{'input':['some'],'output':['some']}},{'function':{'input':['some'],'output':['boolean']}},'some'],'output':['some']}},links)
		
		
	def funct(self):
		global node_label
		#print(str(self.links[1].program_expression['data']))
		super().funct()
		node_list_dict ={}
		if self.data == None:
			self.g = Graph(graph_label)
			node_list_dict[7] = identity(node_label) #7
			node_list_dict[6] = identity(node_label) #6
			node_list_dict[5] = identity(node_label)	#5
			node_list_dict[4] = apply(node_label)	#4
			node_list_dict[3] = apply(node_label)	#3
			node_list_dict[2] = gaurd(node_label)	#2
			node_list_dict[1] = recurse(node_label)	#1
			for node_i in node_list_dict.values():
				node_i.update_exp = 0
			self.g.add_node(node_list_dict[7])
			self.g.add_node(node_list_dict[6])
			self.g.add_node(node_list_dict[5])
			self.g.add_node(node_list_dict[4],node_list_dict[6],node_list_dict[5],node_list_dict[5])
			self.g.add_node(node_list_dict[3],node_list_dict[7],node_list_dict[5],node_list_dict[5])
			self.g.add_node(node_list_dict[1],node_list_dict[7],node_list_dict[6],node_list_dict[3])
			self.g.add_node(node_list_dict[2],node_list_dict[4],node_list_dict[5],node_list_dict[1])
			self.g.glinks = self.links
		#print(self.links)
			for i in range(len(self.links)): 
				self.g.initialnodes[i].links = (self.links[i],)
			#print(self.g.terminalnodes[0].update_exp)
			output = self.g.terminalnodes[0].funct()
			self.data = output['data']
			self.world = output['world']
			#print('ok')
			super().update_program_expression('recurse',self.data)
			# cleanup memory
			del(node_list_dict)
			del(output)
			self.world_version = self.world.version
		return  {'data':copy.deepcopy(self.data),'world':self.world}
			
			
class sensor(node):
	def __init__(self,label,out_type, *links):
		node.__init__(self,label,1,{'function':{'input':['world'],'output':[out_type]}},links)
		
	def funct(self):
		super().funct()
		if self.data == None:
			temp_world = self.links[0].funct()['world']
			self.data = temp_world.get_data()
			try:
				prev_version = self.links[0].world_version
			except:
				prev_version = self.links[0].version
			temp_world.upgrade()
			if temp_world.version != prev_version + 1:
				raise Exception("Invalid sequence of sensor")
			self.world = temp_world
			self.world_version = self.world.version
			super().update_program_expression('sensor',self.data)
		return {'data':copy.copy(self.data),'world':self.world}
		
class actuator(node):
	def __init__(self,label,in_type, *links):
		node.__init__(self,label,1,{'function':{'input':[in_type],'output':['world']}},links)
		
	def funct(self):
		super().funct()
		if self.data == None:
			link1_in=self.links[0].funct()
			temp_world = link1_in['world']
			temp_world.put_action(link1_in['data'])
			prev_version = self.links[0].world_version
			temp_world.upgrade()
			if temp_world.version != prev_version + 1:
				raise Exception("Invalid sequence of actuator")
			self.data = null
			self.world = temp_world
			# Cleanup memory
			self.world_version = self.world.version
			super().update_program_expression('actuator',self.data)
		return {'world':self.world}
		
class goalchecker(node):
	def __init__(self,label, *links):
		node.__init__(self,label,1,{'function':{'input':['world'],'output':['boolean']}},links)
		
	def funct(self):
		super().funct()
		if self.data == None:
			link1_in=self.links[0].funct()
			temp_world = link1_in['world']
			prev_version = self.links[0].world_version
			temp_world.upgrade()
			if temp_world.version != prev_version + 1:
				raise Exception("Invalid sequence of goalchecker")
			self.data = temp_world.check_goal_state()
			self.world = temp_world
			self.world_version = self.world.version
			super().update_program_expression('goalchecker',self.data)
		return {'data':self.data, 'world':self.world}
		

class lambdagraph(node):
	def __init__(self,label, *links):
		node.__init__(self,label,1,{'function':{'input':['any'],'output':[{'function':{'input':['any'],'output':['any']}}]}},links)
		
	def funct(self):
		super().funct()
		if self.data == None:
			_terminalnode=self.links[0]
			global graph_label
			global node_label
			global call_cnt
			tempinitnodes = identity(node_label)
			tempinitnodes.update_exp = 0
			temp_g = Graph(graph_label)
			temp_g.terminalnodes = [_terminalnode]
			init_world = None
			call_cnt =0
			def graph_return_nodes(self,temp_g,terminalnode):
				global call_cnt
				linknodes = ()
				super().funct()
			# Recursively fetch all parent nodes
				for i,sourcenode in enumerate(terminalnode.links):
					#print (sourcenode)
					if isinstance(sourcenode,world): ### terminalnode initialnode
						temp_g.initialnodes.append(terminalnode)
					elif len(sourcenode.links) == 0 and sourcenode.no_of_arguments >0: ######### sourcenode initialnode
						temp_g.initialnodes.append(sourcenode)
						graph_return_nodes(self,temp_g,sourcenode)
						call_cnt +=1
					else:
						graph_return_nodes(self,temp_g,sourcenode)
						call_cnt += 1

			##print(linknodes)
			#print(terminalnode)
				temp_g.nodes.append(terminalnode)
			#print(linknodes)
			#return terminalnode
		
			graph_return_nodes(self,temp_g,_terminalnode)
			if call_cnt >100:
				print(_terminalnode,call_cnt)
			temp_g.initialnodes = list(set(temp_g.initialnodes))
			temp_g.nodes = list(set(temp_g.nodes))
			temp_node_label=[]
			for tempnode in temp_g.initialnodes:
				temp_node_label.append(tempnode.label)
			sorted_node_label_idx = sorted(range(len(temp_node_label)),key=temp_node_label.__getitem__)
			temp_g.initialnodes =[temp_g.initialnodes[j] for j in sorted_node_label_idx]
			temp_g = copy.deepcopy(temp_g)
			for i in temp_g.nodes:
				i.world = None
				i.data = None
				i.version = None
				i.update_exp = 0
		#self.atype['function']['output'] = 
			temp_g.atype['function']['output'][0] = _terminalnode.atype
		
		##### Find all initial sensor nodes
			temp_nodes = temp_g.nodes
			for i_nodes in temp_g.nodes:
				if isinstance(i_nodes,sensor):
					if isinstance(i_nodes.links[0],world):
						init_world = i_nodes.links[0]
						temp_nodes.remove(i_nodes)
					######## Change child nodes pointer to initial identity node
						for j_nodes in temp_g.nodes:
							new_links =()
							for k_link in j_nodes.links:
								if k_link == i_nodes:
									new_links += (tempinitnodes,)
								else:
									new_links += (k_link,)
							j_nodes.links = new_links
					############ delete init sensor node from initialnodes and terminal nodes
						try:
							temp_g.initialnodes.remove(i_nodes)
						except:
							None
						try:
							temp_g.terminalnodes.remove(i_nodes)
							temp_g.terminalnodes.append(tempinitnodes)
						except:
							None
		############# Remove all initial sensor nodes from nodes list
			temp_g.nodes = temp_nodes
			temp_g.nodes.append(tempinitnodes)
			temp_g.initialnodes.append(tempinitnodes)
			self.world = init_world
			self.world_version = self.world.version
			#self.world =None
			super().update_program_expression('lambdagraph','null')
			self.data = temp_g
		return {'data':copy.deepcopy(self.data),'world':self.world}
		
		
		
		
		