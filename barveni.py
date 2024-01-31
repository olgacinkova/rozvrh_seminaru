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
    pouzite_barvy = set(node_colors)
    chrom = len(pouzite_barvy) # chromaticke cislo = kolik barev pouzito
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

    return G, chrom

def obarvi_graf_lip(G, B): # G = graf, B = pozadovane chrom. c.
    # obarvím graf
    # jaké je chromatické číslo (barevnost grafu)?
    # pokud je menší nebo stejné jako B: vratim obarveny graf a jeho chrom cislo
    # pokud je větší než B:
    # odeberu z grafu hranu s nejmenší hodnotou a opakuju predchozi kroky
    # pokud odebraná hrana má hodnotu profesora, vratim graf a jeho chrom cislo
    
    # vytvorim seznam hran podle velikosti - zacina hranou s nejmensi hodnotou
    serazene_hrany = sorted(G.edges(data=True), key=lambda x: x[2]['weight'])
    print(serazene_hrany)

    # obarvím graf hladovým barvicím algoritmem
    chrom = 0
    graph_coloring = nx.greedy_color(G)
    unique_colors = set(graph_coloring.values())
    graph_color_to_mpl_color = dict(zip(unique_colors, mpl.TABLEAU_COLORS))
    node_colors = [graph_color_to_mpl_color[graph_coloring[n]] for n in G.nodes()]
    pouzite_barvy = set(node_colors)
    chrom = len(pouzite_barvy) # chromaticke cislo = kolik barev pouzito
    labels = {e: G.edges[e]['weight'] for e in G.edges}
    while chrom > B:
        nejmensi = serazene_hrany.pop(0) # hrana s nejmensi hodnotou
        print(nejmensi)
        G.remove_edge(nejmensi[0], nejmensi[1])
        graph_coloring = nx.greedy_color(G)
        unique_colors = set(graph_coloring.values())
        graph_color_to_mpl_color = dict(zip(unique_colors, mpl.TABLEAU_COLORS))
        node_colors = [graph_color_to_mpl_color[graph_coloring[n]] for n in G.nodes()]
        pouzite_barvy = set(node_colors)
        chrom= len(pouzite_barvy)
        labels = {e: G.edges[e]['weight'] for e in G.edges}
    pos = nx.spring_layout(G)
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
    print(G)
    return G, chrom


def seskup_seminare_do_bloku(G):
    # Get the weighted adjacency list representation
    weighted_adjacency_list = nx.to_dict_of_dicts(G)
    
# Convert to a dictionary of lists
    adjacency_list_of_lists = {node: [(neighbor, data['weight']) for neighbor, data in neighbors.items()] for node, neighbors in weighted_adjacency_list.items()}

# Display the adjacency list as text
    print("Weighted graph as text (dictionary of lists):")
    for node, neighbors in adjacency_list_of_lists.items():
        print(f"{node}: {neighbors}")
    """for node, neighbors in graf_jako_slovnik.items():
        neighbor_list = [f"{neighbor} (weight: {data['weight']})" for neighbor, data in neighbors.items()]
        print(f"{node}: {neighbor_list}")
        print("Weighted graph as text (dictionary of lists):")"""
    return 

