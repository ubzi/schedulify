import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "schedulify.settings")

import django
django.setup()

import networkx as nx
import matplotlib.pyplot as plt

from schedulify.models import Project, Task, Dependency, Employee, Exclusion

def run():
    dependencies = Dependency.objects.all()
    graph = nx.DiGraph()
    # get all tasks that do not depend on any other tasks
    start_tasks = Task.objects.filter(dependent_task__isnull=True)
    # get all tasks that have no other tasks depending on them
    end_tasks = Task.objects.filter(precedent_task__isnull=True)
    # add a source node and connect it to all start tasks
    for task in start_tasks:
        graph.add_edge("Source",task.name, weight = task.duration)
    # add all the dependencies to the graph as edges between tasks
    for dependency in dependencies:
        graph.add_edge(dependency.precedent_task.name,dependency.dependent_task.name, weight = dependency.dependent_task.duration)
    # add a sink node and have all end tasks connect to it
    for task in end_tasks:
        graph.add_edge(task.name,"Sink", weight = 0)
    if(nx.is_directed_acyclic_graph(graph)):
        for layer, nodes in enumerate(nx.topological_generations(graph)):
            for node in nodes:
                graph.nodes[node]["layer"] = layer
        pos = nx.multipartite_layout(graph, subset_key = "layer")
        fig, ax = plt.subplots()
        nx.draw_networkx(graph, pos, with_labels=True, ax = ax, node_size = 1000)
        labels = nx.get_edge_attributes(graph,'weight')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels = labels, ax = ax)
        print(nx.dag_longest_path_length(graph))
        fig.tight_layout()
        plt.show()
