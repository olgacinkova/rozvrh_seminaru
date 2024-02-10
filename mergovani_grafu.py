import copy

def merge_weighted_graphs(graph1, colors1, graph2, colors2):
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