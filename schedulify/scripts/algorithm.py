import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "schedulify.settings")

import django
django.setup()

import networkx as nx
import matplotlib.pyplot as plt

from schedulify.models import Project, Task, Dependency, Employee, Exclusion

def initialise(graph):
    dist = dict()
    predecessor = dict()

    for i in range(len(graph)):
        node = graph[i]
        dist[node] = -1
        predecessor[node] = -1

    dist[graph[0]] = 0

    return dist, predecessor

def calculate_longest_path(graph):
    topo_graph = list(nx.topological_sort(graph))
    dist, predecessor = initialise(topo_graph)

    for u in topo_graph:
        for v in graph.neighbors(u):
            if dist[v] < dist[u] + graph.get_edge_data(u, v)["weight"]:
                dist[v] = dist[u] + graph.get_edge_data(u, v)["weight"]
                predecessor[v] = u
    
    end_node = max(dist, key = dist.get)
    path = []

    while predecessor.get(end_node) != -1:
        path.append(end_node)
        end_node = predecessor.get(end_node)

    path.append(end_node)
    path.reverse()
    
    return path, max(dist.values())

def get_longest_path(graph):
    return calculate_longest_path(graph)[0]

def get_longest_path_length(graph):
    return calculate_longest_path(graph)[1]

def get_optimum_exclusion(graph, estimate, exclusion):
    temp1_graph = graph.copy()
    temp2_graph = graph.copy()
    temp1_graph.add_edge(exclusion.task1.name, exclusion.task2.name, weight = get_task_duration(exclusion.task2, estimate))
    temp2_graph.add_edge(exclusion.task2.name, exclusion.task1.name, weight = get_task_duration(exclusion.task1, estimate))

    if(nx.is_directed_acyclic_graph(temp1_graph) and nx.is_directed_acyclic_graph(temp2_graph)):
        return min(temp1_graph, temp2_graph, key = get_longest_path_length)
    
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
    # add a source node and connect it to all start tasks
    for task in start_tasks:
        graph.add_edge("Source",task.name, weight = get_task_duration(task, estimate))
    # add all the dependencies to the graph as edges between tasks
    for dependency in dependencies:
        graph.add_edge(dependency.precedent_task.name,dependency.dependent_task.name, weight = get_task_duration(dependency.dependent_task, estimate))

    if (not nx.is_directed_acyclic_graph(graph)):
        return None
    
    exclusions = Exclusion.objects.filter(project = project)
    for exclusion in exclusions:
        graph = get_optimum_exclusion(graph, estimate, exclusion)

    return graph

def highlight_longest_path(graph, pos, longest_path):
    edge_list = []
    for i in range(0, len(longest_path) - 1):
        edge_list.append((longest_path[i], longest_path[i + 1]))

    nx.draw_networkx_edges(graph, pos, edgelist = edge_list, edge_color = 'r', arrows = True, width = 5)

def create_graph_image(graph, path):
    for layer, nodes in enumerate(nx.topological_generations(graph)):
        for node in nodes:
            graph.nodes[node]["layer"] = layer
    pos = nx.multipartite_layout(graph, subset_key = "layer")
    fig, ax = plt.subplots()
    nx.draw_networkx(graph, pos, with_labels=True, ax = ax, node_size = 1000)
    labels = nx.get_edge_attributes(graph,'weight')
    highlight_longest_path(graph, pos, path)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels = labels, ax = ax)
    fig.tight_layout()


def create_uniform_graph(graph):
    
    topo_graph = list(nx.topological_sort(graph))
    for node in topo_graph[1:]:
        in_edges = graph.in_edges(node)
        duration = graph.get_edge_data(*list(in_edges)[0])["weight"]
        start_node = node
        if duration != 1:
            neighbours = list(graph.neighbors(node))
            out_edges = list(graph.edges(node, "weight"))
            graph.remove_edges_from(out_edges)
            for edge in in_edges:
                graph.add_edge(*edge, weight = 1)
            start_node = node

            for i in range(2, duration+1):
                new_node = str(node) +"(" + str(i) + ")"
                graph.add_node(new_node)
                graph.add_edge(start_node, new_node, weight = 1)
                start_node = new_node
            
            for _,dest,weight in out_edges:
                graph.add_edge(start_node, dest, weight=weight)

    return graph

def get_longest_path_length_from_source(graph, node):
    subgraph = nx.subgraph(graph, nx.all_neighbors(graph, node))
    return get_longest_path_length(subgraph)

def calculate_length_of_resource_graph(n, graph):
    resource_dependent_graph = create_resource_dependent_graph(n, graph)
    _, length = calculate_longest_path(resource_dependent_graph)
    return length

def find_optimum_number_of_employees(graph):
    graph = graph.copy()
    generations = [generation for generation in nx.topological_generations(graph)]
    #calculates the length of the longest list within the topological generation
    #i.e. highest number of tasks that can be completed concurrently
    number_of_employees = max(map(len, generations))
    length = calculate_length_of_resource_graph(number_of_employees, graph)
    while length == calculate_length_of_resource_graph(number_of_employees -1, graph):
        number_of_employees -= 1
    return number_of_employees


def create_employees_dependent_graph(project, graph):
    graph = graph.copy()
    number_of_employees = Employee.objects.filter(project = project).count()
    graph = create_resource_dependent_graph(number_of_employees, graph)
    return graph

def create_resource_dependent_graph(number_of_employees, graph):
    graph = graph.copy()
    generations = [generation for generation in nx.topological_generations(graph)]
    #calculates the length of the longest list within the topological generation
    #i.e. highest number of tasks that can be completed concurrently
    max_concurrent_tasks = max(map(len, generations))
    while max_concurrent_tasks > number_of_employees:
        for i in range (0, len(generations)):
            if len(generations[i]) > number_of_employees:
                shortest_path_node = min(generations[i], key = lambda node: get_longest_path_length_from_source(graph, node))
                other_nodes = [node for node in generations[i] if node != shortest_path_node]
                shortest_path_node_2 = min(other_nodes, key = lambda node: get_longest_path_length_from_source(graph, node))
                graph.add_edge(shortest_path_node, shortest_path_node_2, weight = 1)
                generations = [generation for generation in nx.topological_generations(graph)]
                max_concurrent_tasks = max(map(len, generations))

    return graph

def output_schedule(graph):
    day = 1
    generations = iter(nx.topological_generations(graph))
    next(generations)
    for generation in generations:
        print("Day "+str(day)+": "+str(generation))
        day += 1

def output_schedules(min_graph, max_graph):
    print("--- Schedule for best case ---")
    output_schedule(min_graph)
    print("--- Schedule for worst case ---")
    output_schedule(max_graph)


def run():
    project = Project.objects.get(name = "Test project")
    min_graph = create_graph(project, "min")
    max_graph = create_graph(project, "max")

    path, min_length = calculate_longest_path(min_graph)
    create_graph_image(min_graph, path)

    path, max_length = calculate_longest_path(max_graph)
    create_graph_image(max_graph, path)

    print("optimimum time is estimated to be between: "+str(min_length)+"-"+str(max_length)+" days")

    uniform_min_graph = create_uniform_graph(min_graph)
    uniform_max_graph = create_uniform_graph(max_graph)

    optimum_max_number_of_employees = find_optimum_number_of_employees(uniform_max_graph)
    optimum_min_number_of_employees = find_optimum_number_of_employees(uniform_min_graph)
    print("optimimum number of employees is between: "+str(optimum_min_number_of_employees)+"-"+str(optimum_max_number_of_employees))

    min_resource_graph = create_employees_dependent_graph(project, uniform_min_graph)
    path, min_length = calculate_longest_path(min_resource_graph)
    create_graph_image(min_resource_graph, path)

    max_resource_graph = create_employees_dependent_graph(project, uniform_max_graph)
    path, max_length = calculate_longest_path(max_resource_graph)
    create_graph_image(max_resource_graph, path)
    print("optimimum time under resource constraints is estimated to be between: "+str(min_length)+"-"+str(max_length)+" days")

    output_schedules(min_resource_graph, max_resource_graph)

    plt.show()



        
