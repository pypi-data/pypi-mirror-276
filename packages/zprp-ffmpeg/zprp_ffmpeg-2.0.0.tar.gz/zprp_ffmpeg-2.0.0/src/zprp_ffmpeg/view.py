import networkx as nx
from matplotlib import pyplot as plt

from .FilterGraph import Filter
from .FilterGraph import SinkFilter
from .FilterGraph import SourceFilter
from .FilterGraph import Stream


def view(graph: Stream, filename=None) -> None:
    "Creates graph of filters"

    colors = {"input": "#99cc00", "output": "#99ccff", "filter": "#ffcc00"}

    G = nx.DiGraph()

    graph_connection = []

    for node in graph._nodes:
        if isinstance(node, SourceFilter):
            graph_connection.append((node.in_path.split("/")[-1], colors["input"]))
        elif isinstance(node, SinkFilter):
            graph_connection.append((node.out_path.split("/")[-1], colors["output"]))
        elif isinstance(node, Filter):
            graph_connection.append((node.command, colors["filter"]))

    # Adding nodes
    for node, color in graph_connection:
        G.add_node(node, color=color)

    # Adding edges
    for i in range(len(graph_connection) - 1):
        G.add_edge(graph_connection[i][0], graph_connection[i + 1][0])

    # Set nodes to be horizontal
    pos = {}
    for i, node in enumerate(graph_connection):
        pos[node[0]] = (i, 0)

    nx.draw(
        G, pos, with_labels=True, node_shape="s", node_size=3000, node_color=[color for _, color in graph_connection], font_weight="bold"
    )

    if filename:
        plt.savefig(filename)
    else:
        plt.show()
