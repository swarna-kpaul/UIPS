exec(open('C:/skp/phd/UIPS/program_expression.py').read())
exec(open('C:/skp/phd/UIPS/function_class.py').read())
exec(open('C:/skp/phd/UIPS/graph_class.py').read())
exec(open('C:/skp/phd/UIPS/environment.py').read())
exec(open('C:/skp/phd/UIPS/graph_draw.py').read())
exec(open('C:/skp/phd/UIPS/metasearcher_new.py').read())
import copy
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


s = sensor(node_label,'number',init_world)
k1 = constant(node_label,1,s)
act = actuator(node_label,'number',k1)
s1 = sensor(node_label,'number',act)
g = goalchecker(node_label,act)
l1 = lambdagraph(node_label,g)
eq = equal(node_label,k1,s)
l2 = lambdagraph(node_label,eq)
r = recurse(node_label,l1,l1,s)

# C = {k:v for k,v in globals().items() if k not in A and k != 'A' and k != 'C'}