header = """<?xml version='1.0'?>
<!DOCTYPE platform SYSTEM "http://simgrid.gforge.inria.fr/simgrid/simgrid.dtd">
<platform version="4">
 
 <config>
  <prop id='maxmin/precision' value='1e-4'/>
  <prop id='network/model' value='SMPI'/>
  <!--  Negative values enable auto-select... -->
  <prop id='contexts/nthreads' value='1'/>
  <!--  Power of the executing computer in Flop per seconds. Used for extrapolating tasks execution time by SMPI [default is 20000]-->
  <prop id='smpi/running_power' value='50000000000.0'/>
  <!--  Display simulated timing at the end of simulation -->
  <prop id='smpi/display_timing' value='1'/>
  <prop id='cpu/optim' value='Lazy'/>
  <prop id='network/optim' value='Lazy'/>
  <prop id='smpi/coll_selector' value='mvapich2'/>
  <prop id='smpi/cpu_threshold' value='0.00000001'/>
 </config>
 <AS id='AS0' routing='Floyd'>
"""

node = """  <host id='n{0}' speed='200000000000.0' core='1'/>
"""

link_node_router = """  <link id='linkn{0}s{1}' bandwidth='500000000000.0' latency='0.5e-07'/>
"""

#link_node_router_cs = """  <link id='linkn{0}cs{0}' bandwidth='5000000000000.0' latency='0.5e-08'/>
#"""

link_router_ls = """  <link id='cs{0}-{1}' bandwidth='200000000000.0' latency='0.5e-08'/>
"""

router = """  <router id='s{0}'/>
"""

#router_cs = """  <router id='cs{0}'/>
#"""

link_router_router = """  <link id='links{0}s{1}' bandwidth='50000000000.0' latency='0.5e-06'/>
"""

route_node_router = """  <route src='n{0}' dst='s{1}'>
   <link_ctn id='linkn{0}s{1}'/>
  </route>
"""

route_node_router_cs = """  <route src='n{0}' dst='cs{0}'>
   <link_ctn id='linkn{0}cs{0}'/>
  </route>
"""

route_router_router = """  <route src='s{0}' dst='s{1}'>
   <link_ctn id='links{0}s{1}'/>
  </route>
"""

route_router_router_cs = """  <route src='s{0}' dst='s{1}' symmetrical='NO'>
   <link_ctn id='cs{0}-{1}'/>
  </route>
"""

footer = """ </AS>
</platform>
"""

import sys
import os
import networkx as nx
import math
import argparse

def create_dragonfly_topology(groups, routers_per_group, intra_group_links, inter_group_links):
    G = nx.Graph()
    
    # Add nodes (routers) and intra-group edges (links within a group)
    for g in range(groups):
        for r in range(routers_per_group):
            G.add_node((g, r), group=g, router=r)
            for i in range(1, intra_group_links + 1):
                if r + i < routers_per_group:
                    G.add_edge((g, r), (g, r + i))
    
    # Add inter-group edges (links between groups)
    for g1 in range(groups):
        for g2 in range(g1 + 1, groups):
            for r in range(inter_group_links):
                G.add_edge((g1, r), (g2, r))
    
    return G

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process an integer.")
    #parser.add_argument("integer", metavar="npr", type=int, help="# of processes per router")
    #args = parser.parse_args()
    #npr = args.integer
    
    parser.add_argument("cs_file", type=str, help="cs edgefile")
    #parser.add_argument("link_yaml", type=str, help="link config yaml")
    #parser.add_argument("cs_dir", type=str, help="directory for load cs/yaml")
    #parser.add_argument("xml_dir", type=str, help="directory for save xml")
    #parser.add_argument('--dim', required=True, type=int, nargs="+", help='size of each dimension in mesh')
    
    args = parser.parse_args()
    
    cs_file = args.cs_file
    link_yaml = "link_config.yaml"
    cs_dir = "cs_edges"
    xml_dir = "xmlfiles"
    out_dir = "simgrid_topo"
    edge = "crossbar"
    
    # print(header)
    # print(link_node_router.format(0, 1, 2))

    #G = nx.Graph()
    #G.add_nodes_from([1])
    #G = nx.read_edgelist(edge)

    # パラメータ設定
    groups = 8  # グループの数
    routers_per_group = 8  # 各グループ内のルーター数
    intra_group_links = 8  # グループ内の接続数
    inter_group_links = 8  # グループ間の接続数
    
    # ドラゴンフライトポロジーの作成
    G = create_dragonfly_topology(groups, routers_per_group, intra_group_links, inter_group_links)

    nodes = sorted(list(G.nodes))
    mapping = {e:i for i,e in enumerate(nodes)}
    G = nx.relabel_nodes(G, mapping)
    #G = nx.grid_graph(dim=[4,4,4,4], periodic=True)
    
    G_cs = nx.read_edgelist(os.path.join(cs_dir, cs_file), nodetype=int, data=False, create_using=nx.DiGraph())
    n_nodes = 64
    
    #G = nx.convert_node_labels_to_integers(G, first_label=1)
    n_routers = len(G.nodes())
    n_nodes = n_routers #* npr
    print(n_nodes)
    edgelist = list(G.edges())
    edgelist_cs = list(G_cs.edges())
    routerlist = list(G.nodes())
    nodelist = list(range(1, n_nodes+1))
    
    print("edgelist:", G.edges())
    print("nodelist:", G.nodes())
    print("# of routers:", n_routers)

    # print(edgelist)
    # print(routerlist)
    # print(nodelist)
    
    # exit(1)

    out_xml = "_".join((edge, str(n_nodes))) + ".xml"
    out_txt = "_".join((edge, str(n_nodes))) + ".txt"
    
    print("output node-router list:", os.path.join(out_dir, out_txt))
    print("output xmlfile:", os.path.join(out_dir, out_xml))

    with open(os.path.join(out_dir, out_txt), "w") as f:
        for n in nodelist:
            f.write("n{0}:1\n".format(n))

    with open(os.path.join(out_dir, out_xml), "w") as f:
        f.write(header)
        
        for n in nodelist:
            #r = math.ceil(n / npr)
            n_node_num_1 = 2*n - 1
            n_node_num_2 = 2*n + 1 - 1
            f.write(node.format(n_node_num_1))
            f.write(node.format(n_node_num_2))
            f.write(link_node_router.format(n_node_num_1, n))
            f.write(link_node_router.format(n_node_num_2, n))
            #f.write(link_node_router_cs.format(n))

        for i,j in edgelist_cs:
            f.write(link_router_ls.format(i,j))

        for r in nodelist:
            f.write(router.format(r))
            #f.write(router_cs.format(r))

        for r1, r2 in edgelist:
            f.write(link_router_router.format(r1+1, r2+1))

        for n in nodelist:
            #r = math.ceil(n / npr)
            n_node_num_1 = 2*n - 1
            n_node_num_2 = 2*n + 1 - 1
            f.write(route_node_router.format(n_node_num_1, n))
            f.write(route_node_router.format(n_node_num_2, n))
            #f.write(route_node_router_cs.format(n))
            
        for i,j in edgelist:
            f.write(route_router_router.format(i+1,j+1))

        for r1, r2 in edgelist_cs:
            if (r1-1, r2-1) not in edgelist:
             if (r2-1, r1-1) not in edgelist:
              f.write(route_router_router_cs.format(r1,r2))
            
        f.write(footer)
