import networkx as nx
import community
import itertools

if __name__ == "__main__":
    G=nx.Graph()

    string=open('testsmallerlasttime.csv').read()
    count=0
    for line in string.splitlines():
        count=count+1
        print(count)
        ingredients=line.split(',')[:5]
        combos=list(itertools.combinations(ingredients, 2))
        for combo in combos:
            if combo in G.edges():
                data=G.get_edge_data(combo[0],combo[1])
                G.add_edge(combo[0],combo[1],weight=data['weight']/10)
            else:
                G.add_edge(combo[0],combo[1],weight=100)

    for edge in G.edges():
        if G.get_edge_data(edge[0],edge[1])['weight']==100:
            G.remove_edge(edge[0],edge[1])

    partition = community.best_partition(G)
    with open('communitiesnew.txt','w') as f:
        for com in set(partition.values()):
            f.write(str(com)+'\n')
            list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
            f.write(str(list_nodes))
