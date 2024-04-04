import networkx as nx


TEST_GRAPH_FILES = [
    "practicum_2\homework\\basic\graph_1_wo_cycles.edgelist",
    "practicum_2\homework\\basic\graph_2_w_cycles.edgelist",
]


def has_cycles(g: nx.Graph):
    visited = {n: False for n in G}
    for n in g:
    if (used[v]) {
        cout << "Graph has a cycle, namely:" << endl;
        return v;
    }
    used[v] = true;
    for (int u : g[v]) {
        if (u != p) {
            int k = dfs(u, v);
            if (k != -1) {
                cout << v << endl;
                if (k == v)
                    exit(0);
                return k;
            }
        }
    }
    return -1;
}


if __name__ == "__main__":
    for filename in TEST_GRAPH_FILES:
        # Load the graph
        G = nx.read_edgelist(filename, create_using=nx.Graph)
        # Output whether it has cycles
        print(f"Graph {filename} has cycles: {has_cycles(G)}")
