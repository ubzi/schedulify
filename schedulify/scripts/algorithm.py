import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "schedulify.settings")

import django
django.setup()

import networkx as nx
import matplotlib.pyplot as plt

from schedulify.models import Project, Task, Dependency, Employee, Exclusion

def get_optimum_exclusion(graph, exclusion):
    temp1_graph = graph.copy()
    temp2_graph = graph.copy()
    temp1_graph.add_edge(exclusion.task1.name, exclusion.task2.name, weight = exclusion.task2.duration)
    temp2_graph.add_edge(exclusion.task2.name, exclusion.task1.name, weight = exclusion.task1.duration)

    if(nx.is_directed_acyclic_graph(temp1_graph) and nx.is_directed_acyclic_graph(temp2_graph)):
        return min(temp1_graph, temp2_graph, key = nx.dag_longest_path_length)
    
    elif(nx.is_directed_acyclic_graph(temp1_graph)):
        return temp1_graph
    
    else:
        return temp2_graph

def create_graph(project):
    dependencies = Dependency.objects.filter(project = project)
    graph = nx.DiGraph()
    # get all tasks that do not depend on any other tasks
    start_tasks = Task.objects.filter(project = project, dependent_task__isnull = True)
    # get all tasks that have no other tasks depending on them
    end_tasks = Task.objects.filter(project = project, precedent_task__isnull = True)
    # add a source node and connect it to all start tasks
    for task in start_tasks:
        graph.add_edge("Source",task.name, weight = task.duration)
    # add all the dependencies to the graph as edges between tasks
    for dependency in dependencies:
        graph.add_edge(dependency.precedent_task.name,dependency.dependent_task.name, weight = dependency.dependent_task.duration)
    # add a sink node and have all end tasks connect to it
    for task in end_tasks:
        graph.add_edge(task.name,"Sink", weight = 0)

    if (not nx.is_directed_acyclic_graph(graph)):
        return None
    
    exclusions = Exclusion.objects.filter(project = project)
    for exclusion in exclusions:
        graph = get_optimum_exclusion(graph, exclusion)

    return graph

def show_graph(graph):
    for layer, nodes in enumerate(nx.topological_generations(graph)):
        for node in nodes:
            graph.nodes[node]["layer"] = layer
    pos = nx.multipartite_layout(graph, subset_key = "layer")
    fig, ax = plt.subplots()
    nx.draw_networkx(graph, pos, with_labels=True, ax = ax, node_size = 1000)
    labels = nx.get_edge_attributes(graph,'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels = labels, ax = ax)
    fig.tight_layout()
    plt.show()

def run():
    project = Project.objects.get(name = "Test project")
    graph = create_graph(project)
    if graph:
        print(nx.dag_longest_path(graph))
        print(nx.dag_longest_path_length(graph))
        show_graph(graph)
        
