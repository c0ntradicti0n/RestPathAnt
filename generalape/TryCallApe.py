import itertools
import json
import logging
import unittest
from collections import defaultdict

import numpy
import requests

from Package2Rest.package2rest import Import2Rest
from WireApe.wire_ape import WireApe
from generalape.RandomPath import RandomPath, DEFAULT_ARGUMENTS
from generalape.SitInGraphApe import SitInGraphApe
from helpers.cache_tools import file_persistent_cached_generator
from pathant.Converter import converter
from pathant.PathSpec import PathSpec


api_hash_counter = itertools.count(0, 1)

@converter('graph', 'try_call')
class TryCallApe(PathSpec):
    api_hash = "no"
    def __init__(self, *args,  api=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.succes = {}

    @file_persistent_cached_generator(api_hash + ".api_cache")
    def __iter__(self, *_args, **_kwargs):
        for args, kwargs in zip(_args, _kwargs):
            yield from self(*args, **kwargs)
        else:
            logging.info(f"{self.api.name} finished")
            logging.info(f"{self.succes} made some sense")

    def forbidden_arg (self, param):
        return "*" in param and "," in param

    def param_permutations(self, dependencies, results):
       possible_sources = list(dependencies.values())
       possible_params = list(dependencies.keys())

       if not possible_sources:
           yield {}
       else:
           for sources in itertools.product(*possible_sources):
               data = { param :results[source] for param, source in zip(possible_params, sources) if not self.forbidden_arg(param)}
               yield  data



    def __call__(self, paths, calling_api_fun=None, **kwargs):
        results = {}
        for uri, api in paths:
            dependencies = api[uri]

            for data in self.param_permutations(dependencies, results):
                try:
                    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                    res = requests.post("http://" +uri, headers=headers, data=data)
                except Exception as e:
                    logging.error(e)
                    logging.info(f"{self.api.url} can't eat  and {kwargs}")
                else:
                    # this creates an edge in the pathants graph
                    logging.warning("succes!")

                    if res.status_code < 400:
                        results[uri] = res.text

                    print(res)
                    print(res.text)
                    yield res



class TEST(unittest.TestCase):

    def test_import(self):
        list(TryCallApe(RandomPath(SitInGraphApe(WireApe(Import2Rest(numpy))), default_arguments=DEFAULT_ARGUMENTS)))


if __name__ == '__main__':
    pass
