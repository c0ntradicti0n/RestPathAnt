import itertools
import json
import logging
import unittest

import numpy
import requests

from Package2Rest.package2rest import Import2Rest
from WireApe.wire_ape import WireApe
from generalape.TryCallApe import TryCallApe
from generalape.ape import Ape
from generalape.api import Api
from helpers.cache_tools import file_persistent_cached_generator
from pathant.Converter import converter
from pathant.PathAnt import PathAnt
from pathant.PathSpec import PathSpec
from pathant.converters import converter_nodes


api_hash_counter = itertools.count(0, 1)

@converter("ape", "graph")
class SitInGraphApe(PathSpec):
    api_hash = "no"
    def __init__(self, *args,  api=None, **kwargs):
        super().__init__(*args, **kwargs)



    @file_persistent_cached_generator(api_hash + ".api_cache")
    def __iter__(self, *_args, **_kwargs):
        for args, kwargs in zip(_args, _kwargs):
            yield from self(*args, **kwargs)
        else:
            logging.info(f"{self.api.name} finished")
            logging.info(f"{self.succes} made some sense")


    def __call__(self, api_descriptions, **kwargs):
        api_descriptions = list(api_descriptions)
        pathAnt = PathAnt(use_converters=False)
        for api1, api_description_matches in api_descriptions:
            for api2 in api_description_matches:
                url1, api_description1, target_plug = api1
                url2, api_description2, source_plug = api2

                pathAnt.add_node(url1, functional_object=Api(url=url1, funs=[]), description = api_description1)
                pathAnt.add_node(url2, functional_object=Api(url=url2, funs=[]), description = api_description2)
                pathAnt.add_edge(url1, url2, functional_object=TryCallApe, match=(source_plug, target_plug))

        pathAnt.info(path="api_paths_connected_on_parameters")


class TEST(unittest.TestCase):

    def test_import(self):
        list(SitInGraphApe(WireApe(Import2Rest(numpy))))


if __name__ == '__main__':
    pass
