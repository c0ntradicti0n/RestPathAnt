import itertools
import logging
import unittest
from collections import defaultdict

import numpy
from Package2Rest.package2rest import Import2Rest
from WireApe.wire_ape import WireApe
from generalape.SitInGraphApe import SitInGraphApe
from helpers.cache_tools import file_persistent_cached_generator
from helpers.dependency_solver import get_task_batches, Tasks
from pathant.Converter import converter
from pathant.PathSpec import PathSpec

api_hash_counter = itertools.count(0, 1)

DEFAULT_ARGUMENTS = {
    "shape": (20,20),
    "list": [1,2,3],
    "string": "enemenemopel",
    "number": 42,
    "float": 3.14,
    "boolean": True,
    "tupel": (1,2,3),
    "array": numpy.eye(20,20)
}

@converter("graph", "path")
class RandomPath(PathSpec):
    api_hash = "no"

    def __init__(self, *args, **kwargs):
        """
        It will look in default arguments to give some starting points, when resolving
        "dependencies" of calls, and later we yield possible input stuff from the responses.
        """
        super().__init__(*args, **kwargs)

    @file_persistent_cached_generator(api_hash + ".api_cache")
    def __iter__(self, *_args, **_kwargs):
        for args, kwargs in zip(_args, _kwargs):
            yield from self(*args, **kwargs)
        else:
            logging.info(f"{self.api.name} finished")
            logging.info(f"{self.succes} made some sense")

    def heuristic(self, item):
        return item.pipeline[0].params.len + [-1 if it.is_optional else 1 for it in item.pipeline[0].params]

    def __call__(self, iter, default_arguments = None, **kwargs):
        self.default_arguments = default_arguments

        tasks = Tasks()
        dependecy_data = defaultdict(lambda : defaultdict(list))
        for pathAnt, meta in iter:

            for target, source, data in pathAnt.get_edges():
                tasks.register(target, target + " -- " + data['match'][1].arg_name)

                source_description = pathAnt.G.nodes[source]
                source_dependencies = []
                tasks.register(target + " -- " + data['match'][1].arg_name, source)

                for param in source_description['description']['params']:
                    """for key in self.default_arguments:
                        if key in param.description:
                            tasks.register(source + " -- " + param.arg_name, key)
                            tasks.register(key)"""

                    if not param.is_optional and not param.default and not "default" in param.description:
                        tasks.register(source, source + " -- " + param.arg_name)
                tasks.register(source, *source_dependencies)

                dependecy_data[target][data['match'][1].arg_name] += [source]

            dependency_stages = get_task_batches(tasks)



            yield from [(node, dependecy_data) for batch in dependency_stages for node in batch]


class TEST(unittest.TestCase):

    def test_import(self):
        print(list(RandomPath(SitInGraphApe(WireApe(Import2Rest(numpy))), default_arguments=DEFAULT_ARGUMENTS)))


if __name__ == '__main__':
    pass
