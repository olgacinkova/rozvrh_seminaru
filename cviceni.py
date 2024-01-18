import networkx as nx

# Create a sample graph (you can replace this with your existing graph)
G = nx.MultiGraph()
G.add_edge('node1', 'node2', weight=1)
G.add_edge('node1', 'node2', weight=100)
G.add_edge('node2', 'node3', weight=1)

# Create a new graph with aggregated edge weights
new_graph = nx.MultiGraph()

for u, v, data in G.edges(data=True):
    u, v = min(u, v), max(u, v)  # Sort nodes to avoid duplicate edges
    if new_graph.has_edge(u, v):
        # If an edge already exists, update the 'weight' attribute
        new_graph[u][v]['weight'] += data['weight']
    else:
        # If the edge doesn't exist, create a new one with the 'weight' attribute
        new_graph.add_edge(u, v, weight=)

# Print the edges of the new graph with aggregated weights
for u, v, data in new_graph.edges(data=True):
    weight = data['weight']
    print(f"Edge: ({u}, {v}), Weight: {weight}")
