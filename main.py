# exec(open('C:/skp/phd/UIPS/program_expression.py').read())
# exec(open('C:/skp/phd/UIPS/function_class.py').read())
# exec(open('C:/skp/phd/UIPS/graph_class.py').read())
# exec(open('C:/skp/phd/UIPS/environment.py').read())
# exec(open('C:/skp/phd/UIPS/graph_draw.py').read())
#exec(open('C:/skp/phd/UIPS/metasearcher_new.py').read())
# exec(open('C:/skp/phd/UIPS/incremental_learning.py').read())
# import copy

# A=copy.copy(locals())
# #diffA = copy.copy(A)
# input0 = sensor(node_label,'number',init_world)
# front1 = constant(node_label,1)
# action1 = actuator(node_label,'number')
# input1 = sensor(node_label,'number')
# maze_graph = Graph(graph_label)

# maze_graph.add_node(input0)
# maze_graph.add_node(front1,input0)
# maze_graph.add_node(action1,front1)

# del input0
# del front1
# del action1
# del input1
# #B=copy.copy(locals())
import cProfile
import sys
sys.path.append("C:/skp/phd/UIPS")
#import copy
#from operator import itemgetter
#from functools import reduce
#from test_uips import *
#from function_class import *
from metasearcher_new import *
from graph_draw import *
k=Graph(1)
s1=sensor(1,'number',initWorld(0))
#s3=sensor(11,'number')
c1=constant(2,1)
ac1=actuator(3,'number')
gc1=goalchecker(4)
l1=lambdagraph(5)
#l2=lambdagraph(10)
c2=constant(6,2)
ac2=actuator(7,'number')
s2=sensor(8,'number')
r1=recurse(9)
#gc1.program_expression = {'data': symbols('iW().S().GC()'), 'world': 'iW().S().GC()'}
gc1.program_expression = {'data': symbols('iW().S().1.A().GC()'), 'world': 'iW().S().1.A().GC()'}

k.add_node(s1)
k.add_node(c1,s1)
k.add_node(ac1,c1)
#k.add_node(s3,ac1)
#k.add_node(l2,s3)
k.add_node(gc1,ac1)
k.add_node(l1,gc1)
k.add_node(c2,s1)
k.add_node(ac2,c2)
k.add_node(s2,ac2)
k.add_node(r1,l1,l1,s2)

for i in k.nodes:
	i.executed=1


exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,500000)
init_prob1=exec_node.program_probability
print("prog prob")
fin_prob1=calculate_total_program_probability(exec_node.factored_program_probability)

environment.goal_state = [3,1,[1,0]]
environment.init_world = environment.world('number',environment.maze,environment.init_state,environment.goal_state)
exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,500000)
init_prob2=exec_node.program_probability
#node1= exec_node


#init_prob2=exec_node.program_probability
#for i in range(8):
#	exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,500000)

fin_prob2=calculate_total_program_probability(exec_node.factored_program_probability)
node2= exec_node

environment.goal_state = [4,1,[1,0]]
environment.init_world = environment.world('number',environment.maze,environment.init_state,environment.goal_state)
exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,500000)
init_prob3=exec_node.program_probability
fin_prob3=calculate_total_program_probability(exec_node.factored_program_probability)

node3=exec_node

environment.goal_state = [5,1,[1,0]]
environment.init_world = environment.world('number',environment.maze,environment.init_state,environment.goal_state)
exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,500000)
init_prob4=exec_node.program_probability

environment.goal_state = [6,1,[1,0]]
environment.init_world = environment.world('number',environment.maze,environment.init_state,environment.goal_state)
exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,500000)
init_prob5=exec_node.program_probability

print(init_prob1,init_prob2,init_prob3,init_prob4,init_prob5)
# for i in range(6):
	# exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,500000)
# fin_prob4=calculate_total_program_probability(exec_node.factored_program_probability)

# node4=exec_node

# environment.goal_state = [10,10,[1,0]]
# environment.init_world = environment.world('number',environment.maze,environment.init_state,environment.goal_state)	
# exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,5000000)
# init_prob5=exec_node.program_probability
# fin_prob5=calculate_total_program_probability(exec_node.factored_program_probability)

# temp=exec_node

# environment.goal_state = [20,20,[1,0]]
# environment.init_world = environment.world('number',environment.maze,environment.init_state,environment.goal_state)
# exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,5000000)
# init_prob6=exec_node.program_probability
# fin_prob6=calculate_total_program_probability(exec_node.factored_program_probability)

# print("initial_prob")
# print(init_prob1,init_prob2,init_prob3,init_prob4,init_prob5,init_prob6)
# print("final prob")
# print(fin_prob1,fin_prob2,fin_prob3,fin_prob4,fin_prob5,fin_prob6)
#exec_node,search_graph = metasearcher(search_graph,corpus_index,corpus_of_objects,init_type_compatible_node_links,5000000)


#k=search_graph.return_subgraph(exec_node)
#draw_graph(k)
# addNode(search_graph.label,eval(corpus_of_objects['constant1'][0]),search_graph.terminalnodes[0].label)
# addNode(search_graph.label,eval(corpus_of_objects['actuator_number'][0]),search_graph.terminalnodes[0].label)
# k=getSubgraph(search_graph.label,search_graph.terminalnodes[0].label)
# evalGraph(k)
# search_graph.terminalnodes[0].program_expression = k.terminalnodes[0].program_expression

# addNode(search_graph.label,eval(corpus_of_objects['lambdagraph'][0]),search_graph.terminalnodes[0].label)
# addNode(search_graph.label,eval(corpus_of_objects['goalchecker'][0]),search_graph.nodes[0].label)
# k=getSubgraph(search_graph.label,search_graph.terminalnodes[1].label)
# evalGraph(k)
# search_graph.terminalnodes[1].program_expression = k.terminalnodes[0].program_expression
# addNode(search_graph.label,eval(corpus_of_objects['lambdagraph'][0]),search_graph.terminalnodes[1].label)
# addNode(search_graph.label,eval(corpus_of_objects['recurse'][0]),search_graph.terminalnodes[0].label,search_graph.terminalnodes[1].label,search_graph.nodes[0].label)

# k=getSubgraph(search_graph.label,search_graph.terminalnodes[0].label)
# s = sensor(node_label,'number',init_world)
# k1 = constant(node_label,1,s)
# act = actuator(node_label,'number',k1)
# s1 = sensor(node_label,'number',act)
# g = goalchecker(node_label,act)
# l1 = lambdagraph(node_label,g)
# eq = equal(node_label,k1,s)
# l2 = lambdagraph(node_label,eq)
# r = recurse(node_label,l1,l1,s)

# C = {k:v for k,v in globals().items() if k not in A and k != 'A' and k != 'C'}