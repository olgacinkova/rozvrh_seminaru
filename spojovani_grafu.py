import copy


def merge_weighted_graphs(pridavek_graf: dict, pridavek_colors: dict, zaklad_graf: dict, zaklad_colors: dict):
    """
    Spojí dva obarvené grafy. Duplicitní vrcholy nahradí vrcholy z grafu 2 (včetně barev).

    Parametry: 
        pridavek_graf (dict): Pridavny graf vyjádřený jako dictionary pomocí nx.to_dict_of_dicts().
        pridavek_colors (dict): Dictionary, kde je pro každý vrchol pridavneho grafu jeho barva.
        zaklad_graf (dict): Zakladni graf vyjádřený jako dictionary pomocí nx.to_dict_of_dicts().
        zaklad_colors (dict): Dictionary, kde je pro každý vrchol zakladniho grafu jeho barva.

    Vrací:
        dict: Spojený graf ze dvou grafů - z pridavneho a zakladniho. 
        dict: Dictionary, kde je pro každý vrchol spojeného grafu jeho barva.

    """

    # graph 1 = graf ktery pridavam do spojeneho - jeste neobarveny
    # graph 2 = spojeny graf
    merged_graph = copy.deepcopy(zaklad_graf)
    merged_colors = zaklad_colors.copy()

    for node in pridavek_graf.keys():
        # pokud je vrchol zaroven v pridavnem i zakladnim grafu
        if node not in merged_graph.keys():
            merged_graph[node] = pridavek_graf[node]
            #merged_colors[node] = 0

    print(f"kolik jsem pridala vrcholu: {len(merged_graph.keys())-len(zaklad_graf.keys())}")
    return merged_graph, merged_colors


    """
    # Make a deep copy of the base graph and its colors
    merged_graph = copy.deepcopy(zaklad_graf)
    merged_colors = zaklad_colors.copy()

    # Merge nodes and their colors from the additional graph
    for node, color in pridavek_colors.items():
        # If the node is already in the merged graph, update its color if it's not zero
        if node in merged_graph:
            if color != 0:
                merged_colors[node] = color
        # If the node is not in the merged graph, add it along with its color
        else:
            merged_graph[node] = pridavek_graf.get(node, {})
            merged_colors[node] = color

    # Merge edges and their weights from the additional graph
    for node, neighbors in pridavek_graf.items():
        for neighbor, attributes in neighbors.items():
            # If the edge doesn't exist in the merged graph, add it
            if neighbor not in merged_graph[node]:
                merged_graph[node][neighbor] = attributes
            # If the edge exists, update its weight
            else:
                merged_graph[node][neighbor]['weight'] = attributes['weight']
    """
    return merged_graph, merged_colors