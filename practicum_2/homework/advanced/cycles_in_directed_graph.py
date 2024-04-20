import networkx as nx


TEST_GRAPH_FILES = [
    "graph_1_wo_cycles.edgelist",
    "graph_2_wo_cycles.edgelist",
    "graph_3_w_cycles_edgelist",
]
def dfs(node,visit,stack,g:nx.DiGraph):
    visit.add(node)
    stack.add(node)
    for neighbor in g.neighbors(node):
        if neighbor not in visit:
            if dfs(neighbor,visit,stack,g):
                return True
        elif neighbor in stack:
            return True
    stack.remove(node)
    return False
def has_cycles(g: nx.DiGraph):
    visit = set()
    stack = set()
    for node in g.nodes:
        if node not in visit:
            if dfs(node,visit,stack,g):
                return True
    return False



if __name__ == "__main__":
    for filename in TEST_GRAPH_FILES:
        # Load the graph
        G = nx.read_edgelist(filename, create_using=nx.DiGraph)
        # Output whether it has cycles
        print(f"Graph {filename} has cycles: {has_cycles(G)}")