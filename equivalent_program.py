###### function --> function:
#### expression as list
def fetch_terms(item_data):
	if item_data['name'] == 'neg:' and item_data['arguments'][0]['name'] == 'multiply':
		A=item_data['arguments'][0]['arguments']
		sign = 'neg:'
	elif item_data['name'] == 'neg:':
		A=item_data['arguments']
		sign = 'neg:'
	elif item_data['name'] == 'multiply:':
		A=item_data['arguments']
		sign = 'pos:'
	else:
		A = [item_data]
		sign = 'pos:'
	
	return (A,sign)
					
					
					
def expression_reducer(expression):
	if expression['name'] = 'add:':
		data1 = expression['arguments'][0]
		data2 = expression['arguments'][1]
		for i,item_data1 in enumerate(data1):
			for j,item_data2 in enumerate(data2):
				
				A,sign1 = fetch_terms(item_data1)
				B,sign2 = fetch_terms(item_data2)
				if len(A) == 1 and sign1 = 'neg:': # term A is single and negative -- -A
					if len(B) == 1 and sign2 = 'pos:' and B[0] == A[0]: #### term B is single and positive and A = B
						####### +ve -ve cancellation
						data1.pop(i)
						data2.pop(j)
						expression = expression_reducer({'name':'add:','arguments':[data1,data2]})
						return expression
					elif len(B) == 1 and sign2 = 'neg:' and B[0] == A[0]: #### term B is single and negative and A = B;  -A -A = -2A
						##### additive terms
						data1.pop(i)
						data2.pop(j)
						data1.append({'name':'neg:','arguments':[{'name':'multiply':'arguments':[2,B[0]]}]})
						expression = expression_reducer({'name':'add:','arguments':[data1,data2]})
						return expression
					elif len(B) == 2 and sign2 = 'neg:': ####### term B is 
				
				if (item_data1['name'] == 'neg:' and item_data1['arguments'] == item_data2) or (item_data2['name'] == 'neg:' and item_data2['arguments'] == item_data1): ### negative cancellation
					data1.pop(i)
					data2.pop(j)
					expression = expression_reducer({'name':'add:','arguments':[data1,data2]})
					return expression
				elif  item_data1['name'] == 'neg:' and item_data1[arguments][0]['name'] == 'multiply' 
				
				and 
					((item_data1['arguments'][0]['arguments'][0] == item_data2 and is_number(item_data1['arguments'][0]['arguments'][1])) or
					((item_data1['arguments'][0]['arguments'][1] == item_data2 and is_number(item_data1['arguments'][0]['arguments'][0]))))   
					###### (3xA).mul.neg + A = (2xA).mul.neg; (2xA).mul.neg + A = A.neg

def derive_program_expression(node_name,terminalnode,node_output):
	if 'constant' in node_name :
		parent_expression = terminalnode.links[0].program_expression
		if 'function' in terminalnode.atype['function']['output'][0]: ## constant returns function
			current_expression = {'data':{'name':type(terminalnode.K).__name__ + ':','arguments':None}, 'world':parent_expression['world']}
		else: #### constant returns data
			current_expression = {'data':{'name':terminalnode.K,'arguments':None}, 'world':parent_expression['world']}
	elif  'sensor' in node_name:
		if isinstance(terminalnode.links[0],world): ## initial sensornode
			current_expression = {'data':{'name':'world','arguments':'world3'},'world':['iW','.:','iS:']}
		else:  ## other sensor nodes
			parent_expression = terminalnode.links[0].program_expression
			new_world = parent_expression['world'] + ['.:', 'S:']
			current_expression = {'data':{'name':'world','arguments':'world'+str(len(new_world))}, 'world': new_world}
	elif 'actuator' in node_name:
		parent_expression = terminalnode.links[0].program_expression
		new_world = parent_expression['world'] + ['X:',parent_expression['data'],'.:','A:' ]
		current_expression = {'data':{'name':None,'arguments':None}, 'world': new_world}
		
	elif node_name == 'identity':
		parent_expression = terminalnode.links[0].program_expression
		current_expression = parent_expression
		
	elif node_name == 'add' or node_name = 'subtract':
		parent_expression1 = terminalnode.links[0].program_expression
		parent_expression2 = terminalnode.links[1].program_expression
		if  len(parent_expression1['world']) < len(parent_expression1['world']):
			best_world = parent_expression1['world']
		else:
			best_world = parent_expression2['world']
		if is_number(parent_expression1['data']) and is_number(parent_expression2['data']): #### if both the inputs are number type
			current_expression = {'data':node_output, 'world': new_world}
		else: ##### either of the input is expression
			data1 = parent_expression1['data']
			data2 = parent_expression2['data']

			if node_name == 'subtract' and data2['name'] != 'neg:':
				data2 = {'name':'neg:','arguments':[data2]}
			
			if data1 == 0:  ############## addition identity
				current_expression ={'data':data2,'world':best_world}
			elif data2 ==0:  ############## addition identity
				current_expression ={'data':data1,'world':best_world}
			elif is_number(data1) or is_number(data2): ### either of the input is a number
				current_expression = {'data':{'name':'add:','arguments':[data1,data2]},'world':best_world}
			
			elif (data2['name'] == 'neg:' and data2['arguments'][0] == data1) or (data1['name'] == 'neg:' and data1['arguments'][0] == data2)## equal subtraction
				current_expression ={'data':0,'world':best_world}
			elif data1 == data2: # both input data expressions are equal
				current_expression = {'data':{'name':'multiply:','arguments':[2,data1]},'world':best_world}
			else:	
				if data2['name'] == 'add:':
					data2 = data2['arguments']
				elif data2['name'] == 'neg:':
					if data2['arguments'][0]['name'] == 'add:':
						tempdata =[]
						for item in data2['arguments'][0]['arguments']:
							if item['name'] == 'neg:':
								tempdata.append(item)
							else:
								tempdata.append({'name':'neg:','arguments':item})
						data2 = tempdata
					else:
						data2=[data2]
				else:
					data2=[data2]
				if data1['name'] == 'add:':
					data1 = data1['arguments']
				else:
					data1=[data1]
				
				temparguments = []
				#current_expression = {'data':{'name':'add','arguments':data1+data2},'world':best_world}
				current_expression = {'name':'add:','arguments':[data1,data2]}
				current_expression = expression_reducer(current_expression)
				
				
				for item_data1 in data1:
					for item_data2 in data2:
						if item_data1['name'] == 'neg:' and item_data1['arguments'] == item_data2: ### negative cancellation
							break
						elif item_data2['name'] == 'neg:' and item_data2['arguments'] == item_data1:  ### negative cancellation
							break
						elif  item_data1['name'] == 'neg:' and item_data1[arguments][0]['name'] == 'multiply' and 
							((item_data1[arguments][0]['arguments'][0] == item_data2 and is_number(item_data1[arguments][0]['arguments'][1])) or
							((item_data1[arguments][0]['arguments'][1] == item_data2 and is_number(item_data1[arguments][0]['arguments'][0]))))
							

							
				
				
			