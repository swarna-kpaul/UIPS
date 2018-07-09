import sys
sys.path.insert(0, 'C:/skp/phd/UIPS/')



#from function_class import node_add, node_identity, node_constant -- giving type error while executing add1 = node_add(3,k1,k2) add1.funct()
import copy
exec(open('C:/skp/phd/UIPS/main.py').read())


exec(open('C:/skp/phd/UIPS/main.py').read())

exec(open('C:/skp/phd/UIPS/function_class.py').read())

exec(open('C:/skp/phd/UIPS/type_class.py').read())_

exec(open('C:/skp/phd/UIPS/environment.py').read())

goal_state = [1,15]
init_world = world('number',maze,init_state,goal_state)

exec_node,search_graph = metasearcher(search_graph,corpus_index,init_world,corpus_of_objects,init_type_compatible_node_links,1500000)

A=locals()
diffA = A
B=locals()
all(map( diffA.pop, B))

import sys
sys.path.append("C:/skp/phd/UIPS")
import copy
from operator import itemgetter
from functools import reduce
from graph_class import *
from function_class import *

from graph_class import Graph, initGraph,addNode,Node,getSubgraph, evalGraph
from function_class import null, time_exception, node, add, identity, constant, subtract, multiply, divide, gaurd, equal, greater, conjunct, disjunct, negate, is_number, is_char, apply, recurse, sensor, actuator, goalchecker, lambdagraph