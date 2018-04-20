exec(open('C:/skp/phd/UIPS/program_expression.py').read())
exec(open('C:/skp/phd/UIPS/function_class.py').read())
exec(open('C:/skp/phd/UIPS/graph_class.py').read())
exec(open('C:/skp/phd/UIPS/environment.py').read())
exec(open('C:/skp/phd/UIPS/graph_draw.py').read())
exec(open('C:/skp/phd/UIPS/metasearcher.py').read())
time_limit = 10000
node_label = 1
node_list_dict={}



# id1=identity(node_label)
# add1=add(node_label,id1,id1)
# g2=Graph(graph_label)
# g2.add_node(id1)
# g2.add_node(add1,id1,id1)
# g2 = g2.return_subgraph(add1)

# g3=Graph(graph_label)
# g3.add_node(identity(node_label))
# g3.add_node(constant(node_label,5),g3.terminalnodes[0])
# g3.add_node(greater(node_label),g3.initialnodes[0],g3.terminalnodes[0])
# g3 = g3.return_subgraph(g3.terminalnodes[0])

# k4=constant(node_label,g2,init_world)
# k5=constant(node_label,g3,init_world)
# r1=recurse(node_label,k4,k5,constant(node_label,1,init_world))

# ap=apply(node_label,k5,constant(node_label,1,init_world))

# ap=apply(node_label,k4,constant(node_label,3,init_world),constant(node_label,1,init_world))
# #ap.funct()


###### Maze program

input0 = sensor(node_label,'number',init_world)

#function_graph = Graph(graph_label)
front1 = constant(node_label,1) ## Front
front2 = constant(node_label,1) ## Front
right = constant(node_label,2)
left = constant(node_label,3) 
action1 = actuator(node_label,'number')
input1 = sensor(node_label,'number')
action2 = actuator(node_label,'number')
input2 = sensor(node_label,'number')
action3 = actuator(node_label,'number')
input3 = sensor(node_label,'number')
action4 = actuator(node_label,'number')
input4 = sensor(node_label,'number')
#condition_graph = Graph(graph_label)
id1 = identity(node_label)
eq1 = equal(node_label)
k1= constant(node_label,1)
l1 = lambdagraph(node_label)
l2 = lambdagraph(node_label)
r3=recurse(node_label)
gs=goalchecker(node_label)

maze_graph = Graph(graph_label)
maze_graph.add_node(input0)
maze_graph.add_node(front1,input0)
maze_graph.add_node(action1,front1)
maze_graph.add_node(input1,action1)
maze_graph.add_node(right,input1)
maze_graph.add_node(action2,right)
maze_graph.add_node(input2,action2)
maze_graph.add_node(front2,input2)
maze_graph.add_node(action3,front2)
maze_graph.add_node(input3,action3)
maze_graph.add_node(left,input3)
maze_graph.add_node(action4,left)
maze_graph.add_node(input4,action4)
maze_graph.add_node(l1,input4)

maze_graph.add_node(k1,input0)
maze_graph.add_node(eq1,input0,k1)
maze_graph.add_node(l2,eq1)
maze_graph.add_node(r3,l1,l2,input0)
maze_graph.add_node(gs,r3)

# function_graph.add_node(front1)
# function_graph.add_node(action1,front1)
# function_graph.add_node(input1,action1)
# function_graph.add_node(right,input1)
# function_graph.add_node(action2,right)
# function_graph.add_node(input2,action2)
# function_graph.add_node(front2,input2)
# function_graph.add_node(action3,front2)
# function_graph.add_node(input3,action3)
# function_graph.add_node(left,input3)
# function_graph.add_node(action4,left)
# function_graph.add_node(input4,action4)



# condition_graph.add_node(id1)
# condition_graph.add_node(k1,id1)
# condition_graph.add_node(eq1,id1,k1)

# k6=constant(node_label,function_graph,init_world)
# k7=constant(node_label,condition_graph,init_world)
# r2=recurse(node_label,k6,k7,input0)
# solver=goalchecker(node_label,r2)

# #ap1=apply(node_label,k7,input0)

# # #ap2=apply(node_label,k6,input0)
# l3=lambdagraph(node_label)
# g = Graph(graph_label)
# g.add_node(input0)
# # #g.add_node(front1,input0)
# # #g.add_node(id1,input0)
# g.add_node(k1,input0)
# g.add_node(eq1,k1,input0)
# g.add_node(l3,eq1)
# # gx=g.return_subgraph(g.terminalnodes[0])