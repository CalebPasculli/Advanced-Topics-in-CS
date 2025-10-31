import math
import networkx as nx
import pulp

def _edge_len(G, u, v, weight_attr=None):
    return 1.0 if weight_attr is None else G[u][v].get(weight_attr, 1.0)

def _path_len(G, path, weight_attr=None):
    if len(path) <= 1: 
        return 0.0
    return sum(_edge_len(G, u, v, weight_attr) for u, v in zip(path, path[1:]))

def enumerate_k_paths(G, sources, t, k, weight_attr=None):
    out = {}
    for s in sources:
        try:
            if not nx.has_path(G, s, t):
                out[s] = []
                continue
        except nx.NetworkXError:
            out[s] = []
            continue

        try:
            gen = nx.shortest_simple_paths(G, s, t, weight=weight_attr)
        except nx.NetworkXNoPath:
            out[s] = []
            continue

        paths = []
        try:
            for p in gen:
                paths.append(p)
                if len(paths) >= k:
                    break
        except nx.NetworkXNoPath:
            pass

        out[s] = paths
    return out

def greedy_ksp_nodes(G, k=10, weight_attr=None):
    starting_nodes = list(G.graph["starting_nodes"])
    DA = G.graph["DA"]
    budget = int(G.graph["budget"])

    H = G.copy()
    blocked = []

    while budget > 0:
        hit = {n: 0.0 for n in H.nodes()}
        for s in starting_nodes:
            paths = enumerate_k_paths(H, [s], DA, k, weight_attr).get(s, [])
            if not paths:
                continue
            w = 1.0 / len(paths)
            for p in paths:
                for n in p:
                    hit[n] += w / max(1, len(starting_nodes))

        ranked = sorted(hit.items(), key=lambda kv: kv[1], reverse=True)
        picked = None
        for n, _score in ranked:
            if n == DA or n in starting_nodes:
                continue
            if H.nodes[n].get("blockable", True) is not False:
                picked = n
                break
        if picked is None:
            break
        blocked.append(picked)
        H.remove_node(picked)
        budget -= 1

    return blocked

