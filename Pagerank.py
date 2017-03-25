from pymongo import MongoClient
import operator
import os
import json


def pagerank(graph, damping=0.85, epsilon=1.0e-8):
    inlink_map = {}
    outlink_counts = {}

    def new_node(node):
        if node not in inlink_map: inlink_map[node] = set()
        if node not in outlink_counts: outlink_counts[node] = 0

    for tail_node, head_node in graph:
        new_node(tail_node)
        new_node(head_node)
        if tail_node == head_node: continue

        if tail_node not in inlink_map[head_node]:
            inlink_map[head_node].add(tail_node)
            outlink_counts[tail_node] += 1

    all_nodes = set(inlink_map.keys())
    for node, outlink_count in outlink_counts.items():
        if outlink_count == 0:
            outlink_counts[node] = len(all_nodes)
            for l_node in all_nodes: inlink_map[l_node].add(node)

    initial_value = 1 / len(all_nodes)
    ranks = {}
    for node in inlink_map.keys(): ranks[node] = initial_value

    new_ranks = {}
    delta = 1.0
    n_iterations = 0
    while delta > epsilon:
        new_ranks = {}
        for node, inlinks in inlink_map.items():
            new_ranks[node] = ((1 - damping) / len(all_nodes)) + (
            damping * sum(ranks[inlink] / outlink_counts[inlink] for inlink in inlinks))
        delta = sum(abs(new_ranks[node] - ranks[node]) for node in new_ranks.keys())
        ranks, new_ranks = new_ranks, ranks
        n_iterations += 1

    sorted_dict = sorted(ranks.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_dict, n_iterations


def findEdge(db):
    query = {}
    edgesDict = db.edges.find(query)
    edges = []
    for e in edgesDict:
        edges.append([str(e["loose"]), str(e["win"])])
    return edges


def handler(event, context):
    current_folder = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_folder, 'app', 'mlab.json')) as data_file:
        mlab = json.load(data_file)

    uri = "mongodb://{0}:{1}@ds143050-a0.mlab.com:43050,ds143050-a1.mlab.com:43050/fliqpick?replicaSet=rs-ds143050".format(
        mlab["username"], mlab["password"])
    client = MongoClient(uri,
                         connectTimeoutMS=30000,
                         socketTimeoutMS=None,
                         socketKeepAlive=True)
    db = client.get_default_database()
    ranks = pagerank(findEdge(db))
    print ranks

    for rank in ranks[0]:
        db.Globalranking.insert({"movieID": rank[0], "rank": rank[1]})


#handler(None, None)

#graph = [['1','2'], ['2','3'], ['5','1']]

#for i in range(0,50000):
#    graph.append([str(random.randint(1,75)), str(random.randint(1,75))])

#print pagerank(graph)[0]

