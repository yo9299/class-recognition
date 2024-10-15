import clingo
import clingo.ast
import networkx as nx 
from time import time
import argparse

def generateClingoGraph(G):
    """
    G: networkx graph 
    output: text file with G represented in lp syntaxis for ASP 
    """
    s = ""
    for (u,v) in G.edges():
        s += "pedge(" + str(u) + ", " + str(v) + "). \n"
    s += "edge(U,V) :- pedge(U,V), vertex(U), vertex(V), U < V.\n"
    s += "edge(V,U) :- pedge(U,V), vertex(U), vertex(V), U > V.\n"
    s += "vertex(0..N) :- nbVertices(N).\n"
    s += "nbVertices(" + str(len(G.nodes())-1) + ").\n"
    #print(s)
    return s

def storeModel(model,output):
    l = model.symbols(atoms=True)
    output.append(str(l))
    """for atom in l:
        if atom.name == "theedge":
            assert(len(atom.arguments) == 2)
            eu = atom.arguments[0]
            ev = atom.arguments[1]
            output.append((str(eu),str(ev)))"""



def collectDefaultConstraints(file):
    """file: path to the model written in lp syntaxis. It should describe the characterization of desired class. For example, interval.lp, chordal.lp
    """ 
    with open(file,'r') as f:
        storedConstraints = f.read()
    total = storedConstraints
    return total

def belongsToClass(graph, class_file):
    """ 
    graph: string restulting from generateClingoGraph
    """
    t0 = time()

    ctl = clingo.Control()
    with clingo.ast.ProgramBuilder(ctl) as bld:
        clingo.ast.parse_string(graph, bld.add)
        clingo.ast.parse_string(collectDefaultConstraints(class_file), bld.add) # parse from string

    ctl.ground([('base', [])])
    #output = defaultdict(lambda: defaultdict(list))
    output = []
    #print(ctl.solve(on_model=print))
    result = ctl.solve(on_model=lambda m: storeModel(m, output))
    print(time()-t0)
    if result.satisfiable:
        #print(output)
        return True #output
#        print(output)
#        pass
    elif result.satisfiable is False:
#        print(False)
        return False
    else:
        print("???")
        assert False


#create a function that given a list of forbidden patters expressed as list of list of tupples,
#returns a .lp file with the asp model 

def writeConstraintFile(list_constraints):
    """ 
    list_constraints : list of dictionaries. Every dictionary has two keys, edges and non edges, and their values are the present edges in the forbidden patter and the non present edges, respectively. Edges should be tuples between vertices numbered from 0 to n.
    """
    s= ":- order(X,Y), order(Y,Z), not order(X,Z).\n"
    s += ":- order(X,Y), order(Y,X).\n "
    s += " 1 { order(X,Y); order(Y,X) } 1 :- vertex(X), vertex(Y), X != Y.\n "
    for c in list_constraints:
        s += ":-"
        edges = c["edges"]
        nedges = c["nonedges"]
        nbv = max(max(max(edges)), max(max(nedges)))
        for i in range(nbv-1):
            s += "order(X" + str(i) + ", X" + str(i+1) + "),"
        for e in edges : 
            s += "edge(X" + str(e[0]) + ", X" + str(e[1]) + ")," 
        for n in nedges: 
            s += "not edge(X" + str(n[0]) + ", X" + str(n[1]) + "),"
        s = s[:-1]
        s += ".\n edge(X,Y) :- edge(Y,X)."

    with open("constraints.lp", "w") as file:
        file.write(s)
    #return s 

G=nx.erdos_renyi_graph(10, 0.2)
G1 = nx.Graph()
G1.add_edges_from([(0,1), (1,2), (2,3), (3,0)])

def inClass(cgraph, constraints=None, predefined_class=None):
    """
    graph: networkx graph
    constraints: list of dictionaries
    """
    #cgraph= generateClingoGraph(graph)
    if not constraints and not predefined_class:
        raise ValueError("one of constraints or file must be passed as argument") 
    if constraints : 
        writeConstraintFile(constraints)
        sol = belongsToClass(cgraph, "constraints.lp")
    else :
        sol = belongsToClass(cgraph, predefined_class)
    return sol 


"""def main():
    n = 5 
    for i in range(n):
        graph= nx.erdos_renyi_graph(30, 0.2)
        start = time()
        print(nx.is_chordal(graph))
        print(time()-start)
        g = generateClingoGraph(graph)
        print(inClass(g, predefined_class="chordal.lp"))
"""

def read_graph_from_file(graph_file):
    """
    Reads a graph from a file and returns a NetworkX graph object.
    
    Parameters:
    graph_file (str): Path to the file containing the graph edges (format: one edge per line, space-separated).

    Returns:
    NetworkX graph: The graph represented in the file.
    """
    G = nx.Graph()
    with open(graph_file, 'r') as f:
        for line in f:
            u, v = map(int, line.split())
            G.add_edge(u, v)
    print(G.edges)
    return G

def main():
    # Command-line argument parsing
    parser = argparse.ArgumentParser(description="Check if a graph belongs to a given class or satisfies certain constraints.")
    
    parser.add_argument('graph_file', type=str, help='Path to the file containing the graph edges.')
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--constraints', type=str, help='Path to the JSON file containing constraints.')
    group.add_argument('--predefined_class', type=str, help='Path to the .lp file describing a predefined class (e.g., interval.lp).')
    
    args = parser.parse_args()
    
    # Read the graph from the file
    g = read_graph_from_file(args.graph_file)
    graph = generateClingoGraph(g)
    # Load constraints or predefined class
    if args.constraints:
        # If constraints are provided, read them from the JSON file
        import json
        with open(args.constraints, 'r') as f:
            constraints = json.load(f)
        result = inClass(graph, constraints=constraints)
    elif args.predefined_class:
        # If a predefined class file is provided
        result = inClass(graph, predefined_class=args.predefined_class)
    
    # Output the result
    if result:
        print("The graph belongs to the specified class.")
    else:
        print("The graph does not belong to the specified class.")


if __name__=="__main__":
    main()