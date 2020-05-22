import itertools
import logging

from generalape.api import Api
from helpers.cache_tools import file_persistent_cached_generator
from pathant.Converter import converter
from pathant.PathSpec import PathSpec




class GeneralApe(PathSpec):
    api_hash = itertools.count(0, 1)
    def __init__(self, *args,  api=None, **kwargs):
        super().__init__(*args, **kwargs)
        if not isinstance(api, Api):
            raise ValueError("Api must be an api and set")
        self.api = api
        self.succes = {}


    def __iter__(self, *_args, **_kwargs):
        for args, kwargs in zip(_args, _kwargs):
            yield from self(*args, **kwargs)
        else:
            logging.info(f"{self.api.name} finished")
            logging.info(f"{self.succes} made some sense")


    @file_persistent_cached_generator(str(next(api_hash)) + ".api_cache")
    def __call__(self, *args, calling_api_fun=None, **kwargs):
        for fun in self.api:
            api_fun = (self.api_hash, fun)

            try:
                res = fun(*args, calling_api_fun=api_fun, **kwargs)
            except Exception as e:
                logging.error(e)
                logging.info(f"{self.api.name} can't eat {args} and {kwargs}")
            else:
                _converter = converter(calling_api_fun, api_fun) ()
                yield res