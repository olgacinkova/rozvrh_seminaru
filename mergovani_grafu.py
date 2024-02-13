import copy

def merge_weighted_graphs(graph1: dict, colors1: dict, graph2: dict, colors2: dict):
    """
    Spojí dva obarvené grafy. Duplicitní vrcholy nahradí vrcholy z grafu 2 (včetně barev).

    Parametry: 
        graph1 (dict): První graf vyjádřený jako dictionary pomocí nx.to_dict_of_dicts().
        colors1 (dict): Dictionary, kde je pro každý vrchol prvního grafu jeho barva.
        graph2 (dict): Druhý graf vyjádřený jako dictionary pomocí nx.to_dict_of_dicts().
        colors2 (dict): Dictionary, kde je pro každý vrchol druhého grafu jeho barva.

    Vrací:
        dict: Spojený graf ze dvou grafů. 
        dict: Dictionary, kde je pro každý vrchol spojeného grafu jeho barva.
    
    """
    merged_graph = copy.deepcopy(graph1)  # Create a copy of the first graph representation
    merged_colors = colors1.copy()  # Create a copy of the first colors dictionary

    for node, neighbors in graph2.items():
        if node in merged_graph:
            # Check if the node in graph1 has color 8, if so, replace it with the node from graph2
            if merged_colors[node] == 8 and node in colors2 and colors2[node] in range(1, 8):
                merged_graph[node] = graph2[node]
                merged_colors[node] = colors2[node]
        else:
            # Add the node from graph2 to graph1 if it doesn't exist in graph1
            if node in colors2 and colors2[node] in range(1, 8):
                merged_graph[node] = graph2[node]
                merged_colors[node] = colors2[node]

    # Merge the edges of graph2 into graph1
    for node, neighbors in graph2.items():
        if node not in merged_graph:
            continue
        for neighbor, attributes in neighbors.items():
            if neighbor not in merged_graph[node]:
                merged_graph[node][neighbor] = attributes
            else:
                # If the edge already exists, update the weight to the new weight
                merged_graph[node][neighbor]['weight'] = attributes['weight']

    return merged_graph, merged_colors