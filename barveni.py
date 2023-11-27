import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mpl
import networkx as nx
def obarvi_graf(G):
    # obarvím graf hladovým barvicím algoritmem
    graph_coloring = nx.greedy_color(G)
    unique_colors = set(graph_coloring.values())
    graph_color_to_mpl_color = dict(zip(unique_colors, mpl.TABLEAU_COLORS))
    node_colors = [graph_color_to_mpl_color[graph_coloring[n]] for n in G.nodes()]
    labels = {e: G.edges[e]['weight'] for e in G.edges}
    pos = nx.spring_layout(G, seed=14)
    nx.draw(
        G,
        pos, 
        with_labels=True,
        node_size=500,
        node_color=node_colors,
        edge_color="grey",
        font_size=12,
        font_color="#333333",
        width=2
    )
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show() # zobrazí graf
    return G