from graphviz import Digraph, Source

def plot_graph(trazas):
    """Función para visualizar el grafo de trazas"""
    dot = Digraph(comment="Grafo")

    for traza in trazas:
        dot.node(traza["id"], label=f"{traza['type']}\n{traza['id'][-10:]}")
        for child in traza["childrens"]:
            dot.edge(traza["id"], child)

    return Source(dot.source)