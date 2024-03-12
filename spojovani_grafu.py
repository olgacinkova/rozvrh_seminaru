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
    merged_graph = copy.deepcopy(graph1)
    merged_colors = colors1.copy()

    for node, neighbors in graph2.items():
        if node in merged_graph:
            if merged_colors[node] == 8 and node in colors2 and colors2[node] in range(1, 8):
                merged_graph[node] = graph2[node]
                merged_colors[node] = colors2[node]
        else:

            if node in colors2 and colors2[node] in range(1, 8):
                merged_graph[node] = graph2[node]
                merged_colors[node] = colors2[node]

    for node, neighbors in graph2.items():
        if node not in merged_graph:
            continue
        for neighbor, attributes in neighbors.items():
            if neighbor not in merged_graph[node]:
                merged_graph[node][neighbor] = attributes
            else:

                merged_graph[node][neighbor]['weight'] = attributes['weight']

    return merged_graph, merged_colors
