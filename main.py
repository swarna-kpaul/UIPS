
exec(open('C:/skp/phd/UIPS/function_class.py').read())
exec(open('C:/skp/phd/UIPS/graph_class.py').read())
time_limit = 10000
node_label = 1
node_list_dict={}

k1 = constant(node_label,1)
k2 = constant(node_label,2)
add1 = add(node_label,k1,k2)
add2 = add(node_label,add1,add1)
gt1 = greater(node_label,k2,k1)
gt2 = greater(node_label,k2,k1)
eq1 = equal(node_label,k1,k2)
and1=conjunct(node_label,gt1,gt2)
and2=conjunct(node_label,gt1,eq1)

g=Graph(graph_label)
g.add_node(k1)
g.add_node(k2)
a1 = add(node_label)
g.add_node(a1,k1,k2)
g.add_node(gt1,k1,k2)

g1=Graph(graph_label)
add1=add(node_label)
add2=add(node_label)
id1=identity(node_label)
g1.add_node(add1)
g1.add_node(id1)
g1.add_node(add2,add1,id1)
g2=g1.return_subgraph(add2)
k3=constant(node_label,g2)
ap=apply(node_label,k3,k1,k2)
ap1=apply(node_label,ap,k1,k2)