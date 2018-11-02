class world_exception(Exception):
	pass


class world:
	
	def __init__(self,out_data_type,init_world,init_state,goal_state):
		self.data_type = out_data_type
		self.version = 0
		self.world_funct = init_world
		self.state = init_state
		self.goal_state = goal_state
		self.world_failed = 0
	
	def get_data(self):
		
		return self.world_funct(self.state)
		
	def upgrade(self):
		self.version +=1
	
	def put_action(self,action):
		try: 
			self.state = self.world_funct(self.state,action)
		except:
			self.world_failed = 1
			raise world_exception('invalid action')
	
	def funct(self):
		return {'world':self}
		
	def check_goal_state(self):
		if self.goal_state == self.state:
			return True
		else:
			return False
			
	def get_reward(self):
		if self.goal_state == self.state:
			return 1
		elif self.world_failed == 1:
			return 0
		else:
			return 0
		
		
init_state = [1,1,[1,0]]
goal_state = [20,20,[1,0]]



def maze(*args):
	#w, h = 22, 22;
	#maze_def = [[0 for x in range(w)] for y in range(h)] 
	maze_def = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
				[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
				[1,0,0,1,0,1,1,1,1,1,0,0,1,0,0,0,0,0,0,1,0,1],
				[1,0,0,0,1,1,0,0,0,0,0,0,1,0,1,1,1,1,0,1,0,1],
				[1,0,1,0,0,1,0,1,0,1,1,1,1,0,1,0,0,0,0,1,0,1],
				[1,0,0,1,0,0,0,1,0,0,1,0,0,1,1,0,0,0,1,1,0,1],
				[1,0,0,1,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
				[1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,1,1,1],
				[1,0,1,0,1,0,1,0,0,1,1,0,0,0,0,0,0,0,0,1,0,1],
				[1,0,1,0,0,0,0,0,0,0,1,0,0,1,1,0,1,0,0,1,0,1],
				[1,0,1,0,1,1,1,1,0,0,0,0,0,0,1,0,1,1,1,1,0,1],
				[1,0,1,0,0,0,0,1,1,1,0,0,1,1,0,0,0,0,0,1,0,1],
				[1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
				[1,0,1,0,0,1,1,1,0,1,0,1,0,0,1,0,0,0,0,0,0,1],
				[1,0,1,1,0,0,0,1,0,1,0,0,0,0,0,1,1,1,0,1,0,1],
				[1,0,0,0,0,0,0,0,0,1,1,1,0,1,0,0,0,0,0,1,0,1],
				[1,0,0,1,1,1,1,1,0,1,0,0,0,0,1,0,0,1,1,1,0,1],
				[1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
				[1,0,1,1,1,1,1,0,0,0,0,1,1,1,1,1,0,0,0,1,0,1],
				[1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,1],
				[1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,1],
				[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
	# maze_def = [[1,1,1,1,1,1,1],
				# [1,0,0,0,0,0,1],
				# [1,0,0,1,0,1,1],
				# [1,0,0,0,1,1,0],
				# [1,0,1,0,0,1,0],
				# [1,0,0,1,0,0,0],
				# [1,1,1,1,1,1,1]]
	direction_list = [[1,0],[0,1],[-1,0],[0,-1]]
	if len(args) ==1:
		current_state = args[0]
		current_direction = current_state[2]
		## Direction [1,0] - down face [0,1] - right face , [-1,0] - up face, [0,-1] left face
		########## return next state
		
		x = current_state[0] + current_direction[0]
		y = current_state[1] + current_direction[1]
		return bool(maze_def[x][y])

	elif len(args) ==2:
		current_state = args[0]
		current_direction = current_state[2]
		action = args[1]
		########### Take action
		if action == 1: ######### Front
			current_state[0] = current_state[0] + current_direction[0]
			current_state[1] = current_state[1] + current_direction[1]
			
		elif action == 2: ####### Right
			current_direction = direction_list[(direction_list.index(current_direction)+1)%4]
		elif action == 3: ####### Left
			next_index = (direction_list.index(current_direction)-1)
			if next_index < 0:
				next_index = 3
			current_direction = direction_list[next_index]
		elif action == 4: ####### Back
			current_state[0] = current_state[0] - current_direction[0]
			current_state[1] = current_state[1] - current_direction[1]
		else:
			raise world_exception('invalid action')
		
		if maze_def[current_state[0]][current_state[1]] == 1:
			raise world_exception('invalid action')
		else :
			return [current_state[0],current_state[1],current_direction]
		
	else:
		raise world_exception("invalid number of arguments for maze function")
	
	
init_world = world('number',maze,init_state,goal_state)