# -*- coding: utf-8 -*-
#    Copyright (C) 2014 by
#    Christian Olsson <chro@itu.dk>
#    Jan Aagaard Meier <jmei@itu.dk>
#    Henrik Haugbølle <hhau@itu.dk>
#    Arya McCarthy <admccarthy@smu.edu>
#    All rights reserved.
#    BSD license.
"""
Greedy graph coloring using various strategies.
"""
from collections import defaultdict, deque
import itertools
import networkx as nx
from networkx.utils import arbitrary_element
from networkx.utils import py_random_state

__all__ = ['greedy_color', 'strategy_connected_sequential',
           'strategy_connected_sequential_bfs',
           'strategy_connected_sequential_dfs', 'strategy_independent_set',
           'strategy_largest_first', 'strategy_random_sequential',
           'strategy_saturation_largest_first', 'strategy_smallest_last']


def strategy_largest_first(G, colors):
    """Returns a list of the nodes of ``G`` in decreasing order by
    degree.

    ``G`` is a NetworkX graph. ``colors`` is ignored.

    """
    return sorted(G, key=G.degree, reverse=True)


@py_random_state(2)
def strategy_random_sequential(G, colors, seed=None):
    """Returns a random permutation of the nodes of ``G`` as a list.

    ``G`` is a NetworkX graph. ``colors`` is ignored.

    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.
    """
    nodes = list(G)
    seed.shuffle(nodes)
    return nodes


def strategy_smallest_last(G, colors):
    """Returns a deque of the nodes of ``G``, "smallest" last.

    Specifically, the degrees of each node are tracked in a bucket queue.
    From this, the node of minimum degree is repeatedly popped from the
    graph, updating its neighbors' degrees.

    ``G`` is a NetworkX graph. ``colors`` is ignored.

    This implementation of the strategy runs in $O(n + m)$ time
    (ignoring polylogarithmic factors), where $n$ is the number of nodes
    and $m$ is the number of edges.

    This strategy is related to :func:`strategy_independent_set`: if we
    interpret each node removed as an independent set of size one, then
    this strategy chooses an independent set of size one instead of a
    maximal independent set.

    """
    H = G.copy()
    result = deque()

    # Build initial degree list (i.e. the bucket queue data structure)
    degrees = defaultdict(set)  # set(), for fast random-access removals
    lbound = float('inf')
    for node, d in H.degree():
        degrees[d].add(node)
        lbound = min(lbound, d)  # Lower bound on min-degree.

    def find_min_degree():
        # Save time by starting the iterator at `lbound`, not 0.
        # The value that we find will be our new `lbound`, which we set later.
        return next(d for d in itertools.count(lbound) if d in degrees)

    for _ in G:
        # Pop a min-degree node and add it to the list.
        min_degree = find_min_degree()
        u = degrees[min_degree].pop()
        if not degrees[min_degree]:  # Clean up the degree list.
            del degrees[min_degree]
        result.appendleft(u)

        # Update degrees of removed node's neighbors.
        for v in H[u]:
            degree = H.degree(v)
            degrees[degree].remove(v)
            if not degrees[degree]:  # Clean up the degree list.
                del degrees[degree]
            degrees[degree - 1].add(v)

        # Finally, remove the node.
        H.remove_node(u)
        lbound = min_degree - 1  # Subtract 1 in case of tied neighbors.

    return result


def _maximal_independent_set(G):
    """Returns a maximal independent set of nodes in ``G`` by repeatedly
    choosing an independent node of minimum degree (with respect to the
    subgraph of unchosen nodes).

    """
    result = set()
    remaining = set(G)
    while remaining:
        G = G.subgraph(remaining)
        v = min(remaining, key=G.degree)
        result.add(v)
        remaining -= set(G[v]) | {v}
    return result


def strategy_independent_set(G, colors):
    """Uses a greedy independent set removal strategy to determine the
    colors.

    This function updates ``colors`` **in-place** and return ``None``,
    unlike the other strategy functions in this module.

    This algorithm repeatedly finds and removes a maximal independent
    set, assigning each node in the set an unused color.

    ``G`` is a NetworkX graph.

    This strategy is related to :func:`strategy_smallest_last`: in that
    strategy, an independent set of size one is chosen at each step
    instead of a maximal independent set.

    """
    remaining_nodes = set(G)
    while len(remaining_nodes) > 0:
        nodes = _maximal_independent_set(G.subgraph(remaining_nodes))
        remaining_nodes -= nodes
        for v in nodes:
            yield v


def strategy_connected_sequential_bfs(G, colors):
    """Returns an iterable over nodes in ``G`` in the order given by a
    breadth-first traversal.

    The generated sequence has the property that for each node except
    the first, at least one neighbor appeared earlier in the sequence.

    ``G`` is a NetworkX graph. ``colors`` is ignored.

    """
    return strategy_connected_sequential(G, colors, 'bfs')


def strategy_connected_sequential_dfs(G, colors):
    """Returns an iterable over nodes in ``G`` in the order given by a
    depth-first traversal.

    The generated sequence has the property that for each node except
    the first, at least one neighbor appeared earlier in the sequence.

    ``G`` is a NetworkX graph. ``colors`` is ignored.

    """
    return strategy_connected_sequential(G, colors, 'dfs')


def strategy_connected_sequential(G, colors, traversal='bfs'):
    """Returns an iterable over nodes in ``G`` in the order given by a
    breadth-first or depth-first traversal.

    ``traversal`` must be one of the strings ``'dfs'`` or ``'bfs'``,
    representing depth-first traversal or breadth-first traversal,
    respectively.

    The generated sequence has the property that for each node except
    the first, at least one neighbor appeared earlier in the sequence.

    ``G`` is a NetworkX graph. ``colors`` is ignored.

    """
    if traversal == 'bfs':
        traverse = nx.bfs_edges
    elif traversal == 'dfs':
        traverse = nx.dfs_edges
    else:
        raise nx.NetworkXError("Please specify one of the strings 'bfs' or"
                               " 'dfs' for connected sequential ordering")
    for component in nx.connected_component_subgraphs(G):
        source = arbitrary_element(component)
        # Yield the source node, then all the nodes in the specified
        # traversal order.
        yield source
        for (_, end) in traverse(component, source):
            yield end


def strategy_saturation_largest_first(G, colors):
    """Iterates over all the nodes of ``G`` in "saturation order" (also
    known as "DSATUR").

    ``G`` is a NetworkX graph. ``colors`` is a dictionary mapping nodes of
    ``G`` to colors, for those nodes that have already been colored.

    """
    distinct_colors = {v: set() for v in G}
    for i in range(len(G)):
        # On the first time through, simply choose the node of highest degree.
        if i == 0:
            node = max(G, key=G.degree)
            yield node
            # Add the color 0 to the distinct colors set for each
            # neighbors of that node.
            for v in G[node]:
                distinct_colors[v].add(0)
        else:
            # Compute the maximum saturation and the set of nodes that
            # achieve that saturation.
            saturation = {v: len(c) for v, c in distinct_colors.items()
                          if v not in colors}
            # Yield the node with the highest saturation, and break ties by
            # degree.
            node = max(saturation, key=lambda v: (saturation[v], G.degree(v)))
            yield node
            # Update the distinct color sets for the neighbors.
            color = colors[node]
            for v in G[node]:
                distinct_colors[v].add(color)


#: Dictionary mapping name of a strategy as a string to the strategy function.
STRATEGIES = {
    'largest_first': strategy_largest_first,
    'random_sequential': strategy_random_sequential,
    'smallest_last': strategy_smallest_last,
    'independent_set': strategy_independent_set,
    'connected_sequential_bfs': strategy_connected_sequential_bfs,
    'connected_sequential_dfs': strategy_connected_sequential_dfs,
    'connected_sequential': strategy_connected_sequential,
    'saturation_largest_first': strategy_saturation_largest_first,
    'DSATUR': strategy_saturation_largest_first,
}


def prioritizovane_barveni(G, povolene_bloky_seminaru, strategy='largest_first', colors={},
                           poradi=[1, 3, 5, 4, 2, 6, 7, 8, 9, 10, 11, 12]):
    """
    Parametry:
        G (networkx graph): Graf, který chci barvit.
        povolene_bloky_seminaru (dict): Dictionary, kde je pro každý seminář, ve kterých blocích může být.
        strategy (str): Strategie barvení. Doporučuju, nechat tam defaultní "largest_first".
        colors (dict): Dictionary, kde je pro každý vrchol grafu jeho barva.
        poradi (list): Pořadí, ve kterém se při barvení přiřazují barvy.

    Vrací:
        dict: Dictionary, kde je pro každý vrchol grafu jeho nová barva.
    """

    if len(G) == 0:
        return {}
    # Determine the strategy provided by the caller.
    strategy = STRATEGIES.get(strategy, strategy)
    if not callable(strategy):
        raise nx.NetworkXError('strategy must be callable or a valid string. '
                               '{0} not valid.'.format(strategy))
    # Perform some validation on the arguments before executing any
    # strategy functions.

    nodes = strategy(G, colors)
    for u in nodes:
        print("aktualni vrchol " + str(u))
        if u not in colors:
            if u not in povolene_bloky_seminaru.keys():
                # pokud neni v tabulce pozadavku ucitelu, dam k nemu, ze muze byt ve vsech blocich
                povolene_bloky_seminaru[u] = set()
                povolene_bloky_seminaru[u].update(
                    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
            # Set to keep track of colors of neighbours

            neighbour_colors = {colors[v] for v in G[u] if v in colors}
            # dictionaty na barvy sousedu aktualniho vrcholu U (vzdy par vrchol:jeho_barva
            #neighbour_colors_dict = {node: color for node, color in zip(G[u], neighbour_colors) if node in colors}
            neighbour_colors_dict = {v: colors[v] for v in G[u] if v in colors}
            # print("barvy sousedu (vzdy par vrchol:jeho_barva) " + str(neighbour_colors_dict))
            # print("povolene barvy " + str(povolene_bloky_seminaru[u]))
            v_povolenych_ne_v_sousedech = povolene_bloky_seminaru[u] - neighbour_colors
            # vahy sousednich hran: dict, kde je vzdy hrana z vrcholu U do jeho souseda a jeji vaha
            vahy_sousednich_hran = dict()

            for v in neighbour_colors_dict.keys():  # pro vrchol v sousedech
                hrana = (u, v)
                # data o barve i ohodnoceni hrany mezi u a v
                data_hrany = G.get_edge_data(u, v)
                hodnota = data_hrany['weight']
                vahy_sousednich_hran[(u, v)] = hodnota
            # seradim sousedni hrany od nejmensi po nejvetsi
            # abych pak odebirala ty s mensimi hodnotami
            serazene_vahy_sousednich_hran = dict(
                sorted(vahy_sousednich_hran.items(), key=lambda item: item[1]))

            if (len(v_povolenych_ne_v_sousedech)) == 0:
                # pokud vsechny povolene barvy nevyplacali sousedi
                # najdi v sousedech vrchol V ktery ma nejakou z povolenych barev U
                # pokud je takovy vrchol V jen jeden, smazu mezi V a U hranu
                # pokud je vrcholu V vic, musim najit ten s nejlehci hranou.
                hrana_k_odstraneni = None
                hodnota_hrany = None
                for hrana in serazene_vahy_sousednich_hran.keys():
                    v = hrana[1]  # sousedni vrchol
                    # pokud je barva sousedniho vrcholu stejna jako nejaka z povolenych barev u
                    if neighbour_colors_dict[v] in povolene_bloky_seminaru[u]:
                        hrana_k_odstraneni = (u, v)
                        hodnota_hrany = serazene_vahy_sousednich_hran[(u, v)]
                        break
                # odstranim hranu mezi u a v
                G.remove_edge(hrana_k_odstraneni[0], hrana_k_odstraneni[1])
                print(
                    f"ODSTRANENA HRANA {hrana_k_odstraneni[0]} a {hrana_k_odstraneni[1]} s hodnotou {hodnota_hrany}")
                # neighbour_colors.remove(neighbour_colors_dict[hrana_k_odstraneni[1]])
                del neighbour_colors_dict[hrana_k_odstraneni[1]]

            # Find the first unused color.
            # for color in itertools.count(1)
            for color in itertools.cycle(poradi):
                if (color not in neighbour_colors_dict.values()) and (color in povolene_bloky_seminaru[u]):
                    break
            # Assign the new color to the current node.
            colors[u] = color
            print("vrchol = " + str(u) + " barva = " + str(color))
    print("obarveno")
    return colors
