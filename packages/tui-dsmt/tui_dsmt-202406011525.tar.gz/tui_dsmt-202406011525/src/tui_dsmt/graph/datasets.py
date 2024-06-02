import bz2
import os
import pickle

import networkx as nx

# location of this file is required to load resource urls
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


# helper functions
def _get_path(filename: str) -> str:
    return os.path.join(__location__, 'datasets', filename)


def _load_graph(name: str, **kwargs) -> nx.Graph:
    return nx.read_edgelist(_get_path(f'{name}.csv'), delimiter=',', **kwargs)


# cliques examples
def small_cliques() -> nx.Graph:
    return _load_graph('small_cliques', nodetype=int)


# some Wikipedia articles
def dewiki_sample():
    graph_path = _get_path('dewiki_sample.pickle.bz2')
    with bz2.open(graph_path, 'rb') as file:
        return pickle.load(file)
