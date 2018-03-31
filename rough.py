import sys
sys.path.insert(0, 'C:/skp/phd/UIPS/')



#from function_class import node_add, node_identity, node_constant -- giving type error while executing add1 = node_add(3,k1,k2) add1.funct()
import copy
exec(open('C:/skp/phd/UIPS/main.py').read())

exec(open('C:/skp/phd/UIPS/type_class.py').read())

exec(open('C:/skp/phd/UIPS/environment.py').read())