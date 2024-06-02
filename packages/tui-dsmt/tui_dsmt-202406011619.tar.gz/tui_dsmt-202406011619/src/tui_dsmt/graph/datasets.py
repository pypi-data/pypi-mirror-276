import bz2
import json
import os
import pickle
import random

import networkx as nx

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


# graph partitioning
def multiprocessing_small():
    graph_path = os.path.join(__location__, 'resources', 'multiprocessing_small.csv')
    graph = nx.read_edgelist(graph_path, create_using=nx.DiGraph(), delimiter=',', nodetype=int)

    pos_path = os.path.join(__location__, 'resources', 'multiprocessing_small_pos.json')
    with open(pos_path, 'r') as f:
        pos = json.load(f)
        pos = {int(k): v for k, v in pos.items()}

    return graph, pos


def multiprocessing_small_undirected():
    graph_path = os.path.join(__location__, 'resources', 'multiprocessing_small.csv')
    graph = nx.read_edgelist(graph_path, create_using=nx.Graph(), delimiter=',', nodetype=int)

    pos_path = os.path.join(__location__, 'resources', 'multiprocessing_small_pos.json')
    with open(pos_path, 'r') as f:
        pos = json.load(f)
        pos = {int(k): v for k, v in pos.items()}

    return graph, pos


def multiprocessing_small_weighted():
    graph_path = os.path.join(__location__, 'resources', 'multiprocessing_small.csv')
    graph = nx.read_edgelist(graph_path, create_using=nx.Graph(), delimiter=',', nodetype=int)

    random.seed(12)
    for u, v in graph.edges:
        if (u, v) in ((3, 4), (4, 3)):
            graph[u][v]['weight'] = 100
        else:
            graph[u][v]['weight'] = random.randint(1, 7)

    pos_path = os.path.join(__location__, 'resources', 'multiprocessing_small_pos.json')
    with open(pos_path, 'r') as f:
        pos = json.load(f)
        pos = {int(k): v for k, v in pos.items()}

    return graph, pos

