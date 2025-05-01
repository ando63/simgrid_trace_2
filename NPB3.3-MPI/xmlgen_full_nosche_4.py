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

node = """  <host id='n{0}' speed='100000000000.0' core= '1'/>
"""

link_node_router = """  <link id='linkn{1}s{0}' bandwidth='10000000000.0' latency='8.799999999999999e-07'/>
"""

link_router_ls = """  <link id='ls{0}' bandwidth='1.0e+16' latency='1.0e-07'/>
"""

router = """  <router id='s{0}'/>
"""


link_router_router = """  <link id='links{0}s{1}' bandwidth='10000000000.0' latency='2.0852e-06'/>
"""

link_router_router_upper = """  <link id='links{0}s{1}' bandwidth='{2}.0' latency='2.0852e-06'/>
"""

route_node_router = """  <route src='n{1}' dst='s{0}' symmetrical='NO'>
   <link_ctn id='linkn{1}s{0}'/>
  </route>
"""

route_router_node = """  <route src='s{0}' dst='n{1}' symmetrical='NO'>
   <link_ctn id='linkn{1}s{0}'/>
  </route>
"""

route_router_router = """  <route src='s{0}' dst='s{1}' symmetrical='NO'>
   <link_ctn id='links{2}s{3}'/>
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
import random

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process an integer.")
    parser.add_argument("integer", metavar="npr", type=int, help="# of processes per router")
    args = parser.parse_args()
    npr = args.integer
    
    out_dir = "simgrid_topo"
    edge = "full_nosche_4"
    
    # print(header)
    # print(link_node_router.format(0, 1, 2))

    random_numbers = random.sample(range(64),4)

    group_counts = {f"Group{i+1}": 0 for i in range(8)}

    for num in random_numbers:
      group_index = num // 8  # 0-7 -> 0, 8-15 -> 1, ..., 56-63 -> 7
      group_name = f"Group{group_index + 1}"
      group_counts[group_name] += 1

    non_zero_groups =0

    for name, num in group_counts.items():
      if (num == 0):
        continue
      else:
        non_zero_groups += 1
      
    

    G = nx.Graph()
    G.add_nodes_from(range(0,5 + non_zero_groups))
    #G = nx.read_edgelist(edge)
    #G = nx.grid_2d_graph(4,4)
    #G = nx.grid_graph(dim=[4,4,4,4], periodic=True)
 
    # G = nx.complete_graph(range(0, 8))

    n = 0
    j = 4

    for name, num in group_counts.items():
      if num != 0:
        for i in range(4,4+num):
          G.add_edge(j,n)
          n += 1
        G.add_edge(j,4 + non_zero_groups)
        j += 1
      else:
        continue
  
    #for i in range(4,4+non_zero_groups):
    # G.add_edge(i,i + 4)
    #for i in range(4,8):
    # G.add_edge(i,8)
 
    #G = nx.convert_node_labels_to_integers(G, first_label=1)
    n_routers = len(G.nodes())
    n_nodes = 4 # * npr
    edgelist = list(G.edges())
    routerlist = list(G.nodes())
    nodelist = list(range(0, n_nodes))
    
    print("edgelist:", G.edges())
    print("nodelist:", G.nodes())
    print("# of routers:", n_routers)

    # print(edgelist)
    # print(routerlist)
    # print(nodelist)
    
    # exit(1)

    out_xml = "_".join((edge, str(npr))) + ".xml"
    out_txt = "_".join((edge, str(npr))) + ".txt"
    
    print("output node-router list:", os.path.join(out_dir, out_txt))
    print("output xmlfile:", os.path.join(out_dir, out_xml))

    with open(os.path.join(out_dir, out_txt), "w") as f:
        for n in nodelist:
            f.write("n{0}:1\n".format(n))

    with open(os.path.join(out_dir, out_xml), "w") as f:
        f.write(header)
        
        for n in nodelist:
            # r = math.ceil(n / npr)
            r = n
            f.write(node.format(n))
            f.write(link_node_router.format(r, n))

        """

        for r in routerlist:
            f.write(link_router_ls.format(r))

        """

        for r in routerlist:
            f.write(router.format(r))

        for r1, r2 in edgelist:
          if (r1 >= 4 and r2 >= 4):
            if (r1 < (4 + non_zero_groups) and G.degree[r1] >= 3):
              f.write(link_router_router_upper.format(r1, r2, int((G.degree[r1] - 1) * 10000000000)))
            elif (r2 < (4 + non_zero_groups) and G.degree[r2] >= 3):
              f.write(link_router_router_upper.format(r1, r2, int((G.degree[r2] - 1) * 10000000000)))
            else:
              f.write(link_router_router.format(r1, r2))
          else:
            f.write(link_router_router.format(r1, r2))

        for n in nodelist:
            # r = math.ceil(n / npr)
            r = n
            f.write(route_node_router.format(n, r))
            f.write(route_router_node.format(r, n))

        for r1, r2 in edgelist:
            f.write(route_router_router.format(r1, r2, r1, r2))
            f.write(route_router_router.format(r2, r1, r1, r2))
            
        f.write(footer)
