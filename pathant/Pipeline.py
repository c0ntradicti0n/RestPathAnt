import itertools


class Pipeline:
    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.dummy_generator = itertools.cycle([("dummy", {"meta":None})])
        self.extra_paths = []

    def __call__(self, *args, **kwargs):
        """ connects the calls of the nodes in the pipeline with intermediate results and a start argument"""
        intermediate_result = args
        for functional_object in self.pipeline:
            print(intermediate_result)
            if functional_object in self.extra_paths:
                others = self.extra_paths[functional_object]
                others = [other(self.dummy_generator) for other in others ]
                intermediate_result = functional_object(intermediate_result, *others)
            elif intermediate_result:
                intermediate_result = functional_object(*args, **kwargs)
            else:
                intermediate_result = functional_object()
        return intermediate_result
