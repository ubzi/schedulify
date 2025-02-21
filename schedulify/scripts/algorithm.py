import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "schedulify.settings")

import django
django.setup()

import networkx as nx
import matplotlib.pyplot as plt

from schedulify.models import Project, Task, Dependency, Employee, Exclusion

def get_optimum_exclusion(graph, estimate, exclusion):
    temp1_graph = graph.copy()
    temp2_graph = graph.copy()
    temp1_graph.add_edge(exclusion.task1.name, exclusion.task2.name, weight = get_task_duration(exclusion.task2, estimate))
    temp2_graph.add_edge(exclusion.task2.name, exclusion.task1.name, weight = get_task_duration(exclusion.task1, estimate))

    if(nx.is_directed_acyclic_graph(temp1_graph) and nx.is_directed_acyclic_graph(temp2_graph)):
        return min(temp1_graph, temp2_graph, key = nx.dag_longest_path_length)
    
    elif(nx.is_directed_acyclic_graph(temp1_graph)):
        return temp1_graph
    
    else:
        return temp2_graph


def get_task_duration(task, estimate):
    if estimate == "min":
        return task.min_estimated_duration
    elif estimate == "max":
        return task.max_estimated_duration

def create_graph(project, estimate):
    dependencies = Dependency.objects.filter(project = project)
    graph = nx.DiGraph()
    # get all tasks that do not depend on any other tasks
    start_tasks = Task.objects.filter(project = project, dependent_task__isnull = True)
    # get all tasks that have no other tasks depending on them
    end_tasks = Task.objects.filter(project = project, precedent_task__isnull = True)
    # add a source node and connect it to all start tasks
    for task in start_tasks:
        graph.add_edge("Source",task.name, weight = get_task_duration(task, estimate))
    # add all the dependencies to the graph as edges between tasks
    for dependency in dependencies:
        graph.add_edge(dependency.precedent_task.name,dependency.dependent_task.name, weight = get_task_duration(dependency.dependent_task, estimate))
    # add a sink node and have all end tasks connect to it
    for task in end_tasks:
        graph.add_edge(task.name,"Sink", weight = 0)

    if (not nx.is_directed_acyclic_graph(graph)):
        return None
    
    exclusions = Exclusion.objects.filter(project = project)
    for exclusion in exclusions:
        graph = get_optimum_exclusion(graph, estimate, exclusion)

    return graph

def highlight_longest_path(graph, pos):
    edge_list = []
    longest_path = nx.dag_longest_path(graph)
    for i in range(0, len(longest_path) - 1):
        edge_list.append((longest_path[i], longest_path[i + 1]))

    nx.draw_networkx_edges(graph, pos, edgelist = edge_list, edge_color = 'r', arrows = True, width = 5)

def create_graph_image(graph):
    for layer, nodes in enumerate(nx.topological_generations(graph)):
        for node in nodes:
            graph.nodes[node]["layer"] = layer
    pos = nx.multipartite_layout(graph, subset_key = "layer")
    fig, ax = plt.subplots()
    nx.draw_networkx(graph, pos, with_labels=True, ax = ax, node_size = 1000)
    labels = nx.get_edge_attributes(graph,'weight')
    highlight_longest_path(graph, pos)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels = labels, ax = ax)
    fig.tight_layout()

def show_graphs(min_graph, max_graph):
    create_graph_image(min_graph)
    create_graph_image(max_graph)
    plt.show()

def run():
    project = Project.objects.get(name = "Test project")
    min_graph = create_graph(project, "min")
    max_graph = create_graph(project, "max")

    print(nx.dag_longest_path(min_graph))
    print(nx.dag_longest_path_length(min_graph))

    print(nx.dag_longest_path(max_graph))
    print(nx.dag_longest_path_length(max_graph))

    print([generation for generation in nx.topological_generations(min_graph)])

    show_graphs(min_graph, max_graph)

        
