#!/usr/bin/env python

# Dependency resolution example in Python
# By Mario Vilas (mvilas at gmail dot com)

# The graph nodes
import copy
from collections import defaultdict


class Tasks(object):
    def __init__(self):
        self.tasks = defaultdict(list)

    def register(self, name, *depends):
        if not name in self.tasks:
            self.tasks[name] = [set(depends)]
        else:
            self.tasks[name].append(set(depends))


# "Batches" are sets of tasks that can be run together
def get_task_batches(tasks):
    # Build a map of node names to node instances
    name_to_instance = copy.deepcopy(tasks.tasks)

    # Build a map of node names to dependency names
    name_to_deps = copy.deepcopy(tasks.tasks)

    # This is where we'll store the batches
    batches = []

    # While there are dependencies to solve...
    while name_to_deps:

        # Get all nodes with no dependencies
        ready = {name for name, deps in name_to_deps.items() if not any(deps)}

        # If there aren't any, we have a loop in the graph
        if not ready:
            msg = "Unresolvable dependencies found!\n"
            msg += format_dependencies(name_to_deps)
            print((msg))

            return batches


        for name in ready:
            del name_to_deps[name]

        fullfilled = []
        for name, deps in name_to_deps.items():
            for ds in deps:
                ds.difference_update(ready)
                if len( ds) == 0:
                    fullfilled.append(name)
        for ready_by_option in fullfilled:
             name_to_deps[ready_by_option] = [set()]

        # Add the batch to the list
        batches.append(ready)

    # Return the list of batches
    return batches


# Format a dependency graph for printing
def format_dependencies(name_to_deps):
    msg = []
    for name, deps in name_to_deps.items():
        for parent in deps:
            msg.append("%s -> %s" % (name, parent))
    return "\n".join(msg)


# Create and format a dependency graph for printing
def format_nodes(tasks):
    return format_dependencies(tasks.tasks)


# The test code
if __name__ == "__main__":
    optional_resolution_tasks = Tasks()
    optional_resolution_tasks.register("a")
    optional_resolution_tasks.register("b")

    optional_resolution_tasks.register("c", "c1", "c2")

    optional_resolution_tasks.register("c1", "b")
    optional_resolution_tasks.register("c2", "a")
    optional_resolution_tasks.register("c2", "a?")

    optional_resolution_tasks.register("d", "d1", "d2", "d?")

    optional_resolution_tasks.register("d1", "b")
    optional_resolution_tasks.register("d2", "a")

    # Show it on screen
    print("A working optional dependency graph example:")
    print(format_nodes(optional_resolution_tasks))
    print()
    print("Batches:")
    for bundle in get_task_batches(optional_resolution_tasks):
        print(", ".join(node for node in bundle))
    print()

    # An example, working dependency graph
    tasks = Tasks()
    a = tasks.register("a")
    b = tasks.register("b")
    c = tasks.register("c", "a")
    d = tasks.register("d", "b")
    e = tasks.register("e", "c", "d")
    f = tasks.register("f", "a", "b")
    g = tasks.register("g", "e", "f")
    h = tasks.register("h", "g")
    i = tasks.register("i", "a")
    j = tasks.register("j", "b")
    k = tasks.register("k")

    # Show it on screen
    print("A working dependency graph example:")
    print(format_nodes(tasks))
    print()
    # Show the batches on screen
    print("Batches:")
    for bundle in get_task_batches(tasks):
        print(", ".join(node for node in bundle))
    print()

    # An example, *broken* dependency graph
    a = tasks.register("a", "i")

    # Show it on screen
    print("A broken dependency graph example, adding:")
    print(format_nodes(tasks))
    print()

    # This should raise an exception and show the current state of the graph
    print("Trying to resolve the dependencies will raise an exception:")
    print()
    get_task_batches(tasks)
