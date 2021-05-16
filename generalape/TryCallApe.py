import itertools
import json
import logging
import unittest

import numpy
import requests

from Package2Rest.package2rest import Import2Rest
from WireApe.wire_ape import WireApe
from generalape.ape import Ape
from generalape.api import Api
from helpers.cache_tools import file_persistent_cached_generator
from pathant.Converter import converter
from pathant.PathSpec import PathSpec
from pathant.converters import converter_nodes


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


    def __call__(self, *args, calling_api_fun=None, **kwargs):
        for fun in self.api:
            for method in [requests.post, requests.get]:

                try:
                    if method == requests.post:
                        res = method(fun, data=json.dumps(args))
                    if method == requests.get:
                        res =  method(fun.format(*args))

                except Exception as e:
                    logging.error(e)
                    logging.info(f"{self.api.url} can't eat {args} and {kwargs}")
                else:
                    # this creates an edge in the pathants graph
                    _converter = converter(calling_api_fun, fun, method=method) (Ape(fun, method))
                    logging.warning("succes!")
                    yield res



class TEST(unittest.TestCase):

    def test_import(self):
        list(GeneralApe(WireApe(Import2Rest(numpy))))


if __name__ == '__main__':
    pass
