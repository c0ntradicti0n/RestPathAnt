import itertools
import logging
import os
from typing import List, Tuple

import networkx as nx
import pylab
from more_itertools import pairwise

from helpers.os_tools import make_dirs_recursive
from pathant.Pipeline import Pipeline
from pathant.converters import converters, converter_nodes


class PathAnt:
    def __init__(self):
        self.G = nx.DiGraph()

        for _from, _to, functional_object in converters:
            self.add_edge(_from, _to, functional_object)

        for _node, functional_object in converter_nodes:
            self.add_node(_node, functional_object)


    def realize_node(self, node):
        os.system(f"mkdir {node.dir}")

    def make_path(self, G, source, target):
        try:
            return nx.shortest_path(G, source, target)
        except:
            self.info()
            raise

    def __call__(self, source, target, *args, over=None, **kwargs):
        if over:
            if isinstance(over, str):
                return self.__call__(source, over, *args) + self.__call__(over, target, **kwargs)

        converters_path = self.make_path(self.G, source, target)
        converters_implications = {uv: [_a for _a in a if _a not in converters_path ]
                                   for uv, a in nx.get_edge_attributes(self.G, 'implicite').items()
                                   if uv[1] in converters_path
                                      and [_a for _a in a if _a not in converters_path ] }
        extra_paths = {self.lookup(edge[0],edge[1]):
                           [self.estimate_targeting_paths(intermediate_target)  for intermediate_target in intermediate_targets]
               for edge, intermediate_targets in converters_implications.items()
                      }

        logging.debug(f"found path: {converters_path}")
        pipeline = [self.lookup(*_from_to) for _from_to in pairwise(converters_path)]
        return Pipeline(pipeline, source, target, extra_paths)

    def info(self, path="pathant.png", pipelines_to_highlight=None):
        import pylab as plt
        pylab.rcParams['figure.figsize'] = 10,10

        dG = self.G.copy()

        nx.set_edge_attributes(dG, 0, 'color')
        nx.set_edge_attributes(dG, " ", 'label')


        if pipelines_to_highlight:
            for  color, pipeline in enumerate(pipelines_to_highlight):
                pipe_path = self.make_path(dG, pipeline.source, pipeline.target)
                edges = pairwise(pipe_path)
                for u, v in edges:
                    dG[u][v]['color'] = color + 1
                for n in pipe_path:
                    dG.nodes[n]['label'] =  str(pipeline)

        edge_colors = nx.get_edge_attributes(dG, 'color').values()

        for (u, v, d) in dG.edges(data=True):
            d["functional_object"] = d['functional_object'].__class__.__name__

        pos = nx.nx_agraph.graphviz_layout(dG)

        edge_labels = {(u,v):
                           f"{a['functional_object']} " +
                           ("(needs also " + (", ".join(a['implicite'])) +')' if 'implicite' in a else "")
                       for u, v, a in dG.edges(data=True)}


        nx.draw_networkx_edge_labels(dG, pos, edge_labels=edge_labels, rotate=False)
        nx.draw(dG, pos, node_color="blue",
                font_weight='bold',
                edge_color = edge_colors,
                edge_labels=False,
                arrowsize=20, label='Path Ant',
                node_size=150, edge_cmap=plt.cm.plasma)

        pos_attrs = {}
        for node, coords in pos.items():
            pos_attrs[node] = coords[0] + 0.08, coords[1]

        labels = {n: str(f"{data['functional_object'].api.url} ") for n, data in self.G.nodes(data=True)}
        nx.draw_networkx_labels(dG, pos_attrs, labels=labels)
        pylab.savefig(path)
        plt.legend(scatterpoints = 1)
        plt.show()

    def add_node(self, node, functional_object, **kwargs):
        self.G.add_node(node, functional_object=functional_object, **kwargs)

    def add_edge(self, froms, tos, functional_object, **kwargs):
        if isinstance(froms, (List)):
            for _from in froms:
                self.add_edge(_from, tos, functional_object, **kwargs)
        elif isinstance(froms, Tuple):
            for _from in froms:
                others = list(froms)
                others.remove(_from)
                self.add_edge(_from, tos, functional_object,
                              **{"implicite":
                                   others})

        elif isinstance(tos, (List, Tuple)):
            for _to in tos:
                self.add_edge(froms,_to, functional_object, **kwargs)
        else:
            functional_object.path_spec._from = "." + froms
            functional_object.path_spec._to = "." + tos

            self.G.add_edge(froms,tos, functional_object=functional_object, **kwargs)

    def lookup(self, _from, _to, attr='functional_object'):
        return self.G[_from][_to][attr]

    def estimate_targeting_paths(self, intermediate_target):
        for possible_path in nx.single_target_shortest_path(self.G, intermediate_target).values():
            if len(possible_path) == 2:
                return self.lookup(*possible_path)

    def get_all_possible_edges(self):
        for (_in, _in_data), (_out, _out_data) in itertools.permutations(self.G.nodes(data=True), 2):
            yield Pipeline([_in_data['functional_object'], _out_data['functional_object']])



