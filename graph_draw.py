import csv;
import subprocess

def draw_graph(g_obj):
	#terminalnode = g_obj.terminalnodes[0]
	
	edge_list =[]
	def return_edge_list(g_obj,terminalnode, edge_list):
		for i,sourcenode in enumerate(terminalnode.links):
			if isinstance(sourcenode,world):
				s_node = 'initworld'
				t_node = type(terminalnode).__name__ + str(terminalnode.label)
				#edge_list.append([s_node,t_node])
			elif len(sourcenode.links) == 0 and sourcenode.no_of_arguments >0: ######### sourcenode initialnode
				s_node = type(sourcenode).__name__ + str(sourcenode.label)
				t_node = type(terminalnode).__name__ + str(terminalnode.label)
				#edge_list.append([s_node,t_node])
				#graph_return_nodes(self,temp_g,sourcenode)
			else:
				s_node = type(sourcenode).__name__ + str(sourcenode.label)
				t_node = type(terminalnode).__name__ + str(terminalnode.label)
				edge_list = return_edge_list(g_obj,sourcenode,edge_list)
			
			if (type(sourcenode).__name__ == 'constant'):
				s_node = str(sourcenode.K) + '.' + s_node
			if (type(terminalnode).__name__ == 'constant'):
				t_node = str(terminalnode.K) + '.' + t_node
			edge_list.append([s_node,t_node,i+1])	
		return edge_list
		
	for terminalnode in g_obj.terminalnodes:
		edge_list = return_edge_list(g_obj,terminalnode, edge_list)
	
	node_list=[['initworld','']]
	for node_i in g_obj.nodes:
		n_node = type(node_i).__name__ + str(node_i.label)
		if (type(node_i).__name__ == 'constant'):
			n_node = str(node_i.K) + '.' + n_node
		
		node_list.append([n_node,node_i.program_expression])
	
	with open('C:/skp/phd/UIPS/edge_list.csv', 'w', newline='') as csvfile:
		spamwriter = csv.writer(csvfile)
		spamwriter.writerow(['from','to','label'])
		for edge in edge_list:
			spamwriter.writerow(edge)
	
	with open('C:/skp/phd/UIPS/node_list.csv', 'w', newline='') as csvfile:
		spamwriter = csv.writer(csvfile)
		spamwriter.writerow(['id','title'])
		for node in node_list:
			spamwriter.writerow(node)
	#try:
	#	subprocess.check_call (["C:/Program Files/R/R-3.3.2/bin/Rscript","C:/skp/phd/UIPS/graph_view.r"], shell =True)
	#except CalledProcessError as e:
	#	print(e.message)
	#subprocess.call ("C:/skp/phd/UIPS/graph_view.html", shell =True)
	#return edge_list

	
	
	
