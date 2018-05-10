from sympy import symbols,simplify

def get_algebra_expression(terminalnode,node_output,node_name):
	parent_expression1 = terminalnode.links[0].program_expression
	parent_expression2 = terminalnode.links[1].program_expression
	if  len(parent_expression1['world']) > len(parent_expression2['world']):
		best_world = parent_expression1['world']
	else:
		best_world = parent_expression2['world']
	parent_expression1 = parent_expression1['data']
	parent_expression2 = parent_expression2['data']
	if is_number(parent_expression1) and is_number(parent_expression2):
		current_expression = node_output
	elif node_name == 'add':
		current_expression = simplify(parent_expression1+parent_expression2)
	elif node_name == 'subtract':
		current_expression = simplify(parent_expression1-parent_expression2)
	elif node_name == 'multiply':
		current_expression = simplify(parent_expression1*parent_expression2)
	elif node_name == 'divide':
		current_expression = simplify(parent_expression1*parent_expression2)
		
	return {'data':current_expression,'world':best_world}
	
def get_logical_expression(terminalnode,node_output,node_name):
	parent_expression1 = terminalnode.links[0].program_expression
	parent_expression2 = terminalnode.links[1].program_expression
	if  len(parent_expression1['world']) > len(parent_expression2['world']):
		best_world = parent_expression1['world']
	else:
		best_world = parent_expression2['world']
	parent_expression1 = parent_expression1['data']
	parent_expression2 = parent_expression2['data']
	if (('sympy.core' in str(type(parent_expression1)) or 'sympy.core' in str(type(parent_expression2))) and (parent_expression1 not in (True,False) or parent_expression2 not in (True,False))	and (parent_expression1 != parent_expression2)) and node_name == 'equal':
		current_expression = symbols(str(parent_expression1)+'=='+str(parent_expression2))
	elif parent_expression1 == parent_expression2 and node_name == 'equal':
		current_expression = node_output
	elif ('sympy.core' not in str(type(parent_expression1)) and 'sympy.core' not in str(type(parent_expression2))) or (parent_expression1  in (True,False) and parent_expression2 in (True,False)):
		current_expression = node_output
	elif node_name == 'greater':
		current_expression = symbols(str(parent_expression1)+'>'+str(parent_expression2))
	elif node_name == 'conjunct':
		current_expression = simplify(parent_expression1 & parent_expression2)
	elif node_name == 'disjunct':
		current_expression = simplify(parent_expression1 | parent_expression2)
		
	return {'data':current_expression,'world':best_world}
		
		
		
def get_program_expression(node_name,terminalnode,node_output):
	current_expression = None
	if 'constant' in node_name :
		parent_expression = terminalnode.links[0].program_expression
		if 'function' in terminalnode.atype['function']['output'][0]: ## constant returns function
			current_expression = {'data':symbols(type(terminalnode.K).__name__), 'world':parent_expression['world']}
		else: #### constant returns data
			current_expression = {'data':terminalnode.K, 'world':parent_expression['world']}
		#print(current_expression)
	elif  'sensor' in node_name:
		if isinstance(terminalnode.links[0],world): ## initial sensornode
			#current_expression = {'data':symbols('world3'),'world':['iW','.:','iS:']}
			current_expression = {'data':symbols('iW().iS()'),'world':'iW().iS()'}
		else:  ## other sensor nodes
			parent_expression = terminalnode.links[0].program_expression
			new_world = parent_expression['world'] + '.S()'
			#current_expression = {'data':symbols('world'+str(len(new_world))), 'world': new_world}
			#current_expression = {'data':symbols(''.join([str(i) for i in new_world])), 'world': new_world}
			current_expression = {'data':symbols(new_world), 'world': new_world}
	elif  'goalchecker' in node_name:
			parent_expression = terminalnode.links[0].program_expression
			new_world = parent_expression['world'] + '.GC()'
			current_expression = {'data':symbols(new_world), 'world': new_world}
	elif 'actuator' in node_name:
		parent_expression = terminalnode.links[0].program_expression
		new_world = '{{'+parent_expression['world'] + '}X{'+str(parent_expression['data'])+'}}.A()'
		current_expression = {'data':None, 'world': new_world}
	elif node_name == 'identity':
		parent_expression = terminalnode.links[0].program_expression
		current_expression = parent_expression
	elif node_name in ('add','subtract','multiply','divide'):
		current_expression = get_algebra_expression(terminalnode,node_output,node_name)
	elif node_name in ('equal','greater','conjunct','disjunct'):
		current_expression = get_logical_expression(terminalnode,node_output,node_name)
	elif node_name == 'negate':
		parent_expression = terminalnode.links[0].program_expression
		if parent_expression['data'] in (True,False):
			current_expression = {'data':node_output,'world':best_world}
		else:
			current_expression = {'data':simplify(~parent_expression['data']),'world':best_world}
	elif node_name == 'gaurd':
		parent_expression1 = terminalnode.links[0].program_expression
		parent_expression2 = terminalnode.links[1].program_expression
		parent_expression3 = terminalnode.links[2].program_expression		 
			
		if parent_expression1['data'] == True:
			if  len(parent_expression1['world']) > len(parent_expression2['world']):
				best_world = parent_expression1['world']
			else:
				best_world = parent_expression2['world']
			current_expression = {'data':parent_expression2['data'],'world':best_world}
		elif parent_expression1['data'] == False:
			if  len(parent_expression1['world']) > len(parent_expression3['world']):
				best_world = parent_expression1['world']
			else:
				best_world = parent_expression3['world']
			current_expression = {'data':parent_expression3['data'],'world':best_world}
		else:
			best_world = '{'+parent_expression1['world']+'}.sum.{'+ parent_expression2['world']+'}.sum.{'+ parent_expression3['world']+'}'
			current_expression = {'data':symbols('{{'+str(parent_expression2['data'])+'}X{'+str(parent_expression3['data'])+'}}.{'+ str(parent_expression1['data'])+'}?'),'world':best_world}
			
	elif node_name == 'lambdagraph':
		parent_expression = str(terminalnode.links[0].program_expression['data'])
		if parent_expression[0:9] == 'iW().iS()':
			parent_expression = parent_expression[9:]
			parent_expression = 'iW().'+parent_expression
		#parent_expression = 'l().'+parent_expression
		current_expression = {'data':symbols(parent_expression),'world': 'iW()'}
		
	elif node_name == 'recurse':
		parent_expression1 = terminalnode.links[0].program_expression
		parent_expression2 = terminalnode.links[1].program_expression
		parent_expression3 = terminalnode.links[2].program_expression
		if  len(parent_expression1['world']) > max(len(parent_expression2['world']),len(parent_expression3['world'])) :
			best_world = parent_expression1['world']
		elif len(parent_expression2['world']) > max(len(parent_expression1['world']),len(parent_expression3['world'])):
			best_world = parent_expression2['world']
		else:
			best_world = parent_expression3['world']
			
		if 'iW()' not in str(parent_expression1['data']) and 'iW()' not in str(parent_expression2['data']) and 'iW()' not in str(parent_expression3['data']): # all three inputs doesn't have any side effects
			current_expression = {'data':node_output,'world':best_world}
		else: # some inputs have effects
			current_data = symbols('{{'+str(parent_expression1['data'])+'}X{'+str(parent_expression2['data'])+'}X{'+str(parent_expression3['data'])+'}}.recurse()')
			best_world +='.'+(str(current_data))
			current_expression = {'data':current_data,'world':best_world}
	elif node_name == 'apply':
		parent_expression1 = terminalnode.links[0].program_expression
		parent_expression2 = terminalnode.links[1].program_expression
		parent_expression3 = terminalnode.links[2].program_expression
		if  len(parent_expression1['world']) > max(len(parent_expression2['world']),len(parent_expression3['world'])) :
			best_world = parent_expression1['world']
		elif len(parent_expression2['world']) > max(len(parent_expression1['world']),len(parent_expression3['world'])):
			best_world = parent_expression2['world']
		else:
			best_world = parent_expression3['world']
		current_data = symbols('{{'+str(parent_expression2['data'])+'}X{'+str(parent_expression3['data'])+'}}.{'+str(parent_expression1['data']))+'}'
		current_expression = {'data':current_data,'world':best_world}
	
	elif node_name == 'head':
		parent_expression1 = terminalnode.links[0].program_expression
		if isinstance(parent_expression1['data'],list):
			current_expression = {'data':node_output,'world':parent_expression1['world']}
		else:
			current_expression = {'data':symbols('{'+str(parent_expression1['data'])+'}.head()'),'world':parent_expression1['world']}
	elif node_name == 'tail':
		parent_expression1 = terminalnode.links[0].program_expression
		if isinstance(parent_expression1['data'],list):
			current_expression = {'data':node_output,'world':parent_expression1['world']}
		else:
			current_expression = {'data':symbols('{'+str(parent_expression1['data'])+'}.tail()'),'world':parent_expression1['world']}
	elif node_name == 'cons':
		parent_expression1 = terminalnode.links[0].program_expression
		parent_expression2 = terminalnode.links[1].program_expression
		if  len(parent_expression1['world']) > len(parent_expression2['world']) :
			best_world = parent_expression1['world']
		else:
			best_world = parent_expression2['world']
		if ('sympy.core' not in str(type(parent_expression1['data'])) and 'sympy.core' not in str(type(parent_expression2['data']))):
			current_expression = {'data':node_output,'world':best_world}
		else:
			current_expression = {'data':symbols('{{'+str(parent_expression1['data'])+'}X{'+str(parent_expression2['data'])+'}}.cons()'),'world':best_world}
		
	elif node_name == 'nil':
		current_expression = {'data':[],'world':terminalnode.links[0].program_expression['world']}
	
	return current_expression
	