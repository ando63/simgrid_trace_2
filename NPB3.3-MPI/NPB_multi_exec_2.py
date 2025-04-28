

import os
import glob
import argparse
import subprocess
import matplotlib.pyplot as plt
import json

def smpirun_single(basename, app, app_size):
    workdir = "./simgrid_topo/"
    txt_filepath = os.path.join(workdir, basename + ".txt")
    print(txt_filepath)
    print(os.path.exists(txt_filepath))

    xml_filepath = os.path.join(workdir, basename + ".xml")
    print(xml_filepath)
    print(os.path.exists(xml_filepath))

    num_hosts = int(subprocess.check_output(['wc', '-l', txt_filepath]).decode().split(' ')[0])
    # print(num_hosts)

    app_name = ".".join([app.lower(), app_size.upper(), str(num_hosts)])
    app_filepath = os.path.join("./bin/", app_name)
    print(app_filepath)
    print(os.path.exists(app_filepath))

    # exec_str = "smpirun --cfg=smpi/privatize_global_variables:yes -platform {0} -hostfile {1} -np 2 ./bin/lu.D.64 --log=chaix.threshold:verbose --log=chaix.fmt:%m%n --log=chaix.app:splitfile:1000000000:{3}/{4}_{5}_trace_%.csv".format(xml_filepath, txt_filepath, app_filepath, workdir, basename, app_name)
    # exec_str = "smpirun --cfg=smpi/privatize_global_variables:yes -platform {0} -hostfile {1} ./bin/lu.B.64 : ./bin/mg.B.64 --log=chaix.threshold:verbose --log=chaix.fmt:%m%n --log=chaix.app:splitfile:1000000000:{3}/{4}_{5}_trace_%.csv".format(xml_filepath, txt_filepath, app_filepath, workdir, basename, app_name)
    
    # exec_str = "smpirun --cfg=smpi/privatize_global_variables:yes -platform {0} -hostfile {1} -trace {2} --log=chaix.threshold:verbose --log=chaix.fmt:%m%n --log=chaix.app:splitfile:1000000000:{3}/{4}_{5}_trace_%.csv".format(xml_filepath, txt_filepath, app_filepath, workdir, basename, app_name)
    exec_str = "smpirun --cfg=smpi/privatize_global_variables:yes -platform {0} -hostfile {1} {2} --log=chaix.threshold:verbose --log=chaix.fmt:%m%n --log=chaix.app:splitfile:1000000000:{3}/{4}_{5}_trace_%.csv".format(xml_filepath, txt_filepath, app_filepath, workdir, basename, app_name)
    print(exec_str)
    print(exec_str.split())
    # subprocess.run(["ls"])
    
    with open("{2}/{0}_{1}.log".format(basename, app_name, workdir), "w") as outf:
        subprocess.call(exec_str.split(), stdout=outf)

def extract_metrics_from_log(filepath):
    time_in_seconds = None
    mops_total = None

    with open(filepath, 'r') as file:
        for line in file:
            if "Time in seconds" in line:
                time_in_seconds = float(line.split('=')[1].strip())
            elif "Mop/s total" in line:
                mops_total = float(line.split('=')[1].strip())

    return time_in_seconds, mops_total

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("basename")
    parser.add_argument("app")
    parser.add_argument("app_size")

    args = parser.parse_args()
    # print(args)

    benchmarks = [
    "CG",
    "EP",
    "MG",
    "FT",
    "IS",
    "LU"
    ]

    basename = "tree_2_2"
    app = "cg"
    app_size = "A"
    time_cg_tree_2_2_10 = 0
    mops_cg_tree_2_2_10 = 0
    time_cg_poweredtree_2_2_10 = 0
    mops_cg_poweredtree_2_2_10 = 0
    time_cg_fullmesh_2_2_10 = 0
    mops_cg_fullmesh_2_2_10 = 0
    time_cg_partlymesh_2_2_10 = 0
    mops_cg_partlymesh_2_2_10 = 0
    time_cg_supertree_2_2_10 = 0
    mops_cg_supertree_2_2_10 = 0

    for i in range(10):
      smpirun_single(basename, app, app_size)
      log_file = 'simgrid_topo/tree_2_2_cg.A.8.log'  # ログファイルのパスを指定
      time, mops = extract_metrics_from_log(log_file)
      time_cg_tree_2_2_10 += float(time) /10
      mops_cg_tree_2_2_10 += float(mops) /10

    basename = "poweredtree_2_2"

    for i in range(10):
      smpirun_single(basename, app, app_size)
      log_file = 'simgrid_topo/poweredtree_2_2_cg.A.8.log'  # ログファイルのパスを指定
      time, mops = extract_metrics_from_log(log_file)
      time_cg_poweredtree_2_2_10 += float(time) /10
      mops_cg_poweredtree_2_2_10 += float(mops) /10

    basename = "fullmesh_2_2"
    
    for i in range(10):
      smpirun_single(basename, app, app_size)
      log_file = 'simgrid_topo/fullmesh_2_2_cg.A.8.log'  # ログファイルのパスを指定
      time, mops = extract_metrics_from_log(log_file)
      time_cg_fullmesh_2_2_10 += float(time) /10
      mops_cg_fullmesh_2_2_10 += float(mops) /10

    basename = "partlymesh_2_2"

    for i in range(10):
      smpirun_single(basename, app, app_size)
      log_file = 'simgrid_topo/partlymesh_2_2_cg.A.8.log'  # ログファイルのパスを指定
      time, mops = extract_metrics_from_log(log_file)
      time_cg_partlymesh_2_2_10 += float(time) /10
      mops_cg_partlymesh_2_2_10 += float(mops) /10

    basename = "supertree_2_2"

    for i in range(10):
      smpirun_single(basename, app, app_size)
      log_file = 'simgrid_topo/supertree_2_2_cg.A.8.log'  # ログファイルのパスを指定
      time, mops = extract_metrics_from_log(log_file)
      time_cg_supertree_2_2_10 += float(time) /10
      mops_cg_supertree_2_2_10 += float(mops) /10

    basename = "tree_2_2"
    app = "ep"
    time_ep_tree_2_2_10 = 0
    mops_ep_tree_2_2_10 = 0
    time_ep_poweredtree_2_2_10 = 0
    mops_ep_poweredtree_2_2_10 = 0
    time_ep_fullmesh_2_2_10 = 0
    mops_ep_fullmesh_2_2_10 = 0
    time_ep_partlymesh_2_2_10 = 0
    mops_ep_partlymesh_2_2_10 = 0
    time_ep_supertree_2_2_10 = 0
    mops_ep_supertree_2_2_10 = 0

    for i in range(10):
      smpirun_single(basename, app, app_size)
      log_file = 'simgrid_topo/tree_2_2_ep.A.8.log'  # ログファイルのパスを指定
      time, mops = extract_metrics_from_log(log_file)
      time_ep_tree_2_2_10 += float(time) /10
      mops_ep_tree_2_2_10 += float(mops) /10

    basename = "poweredtree_2_2"
    for i in range(10):
      smpirun_single(basename, app, app_size)
      log_file = 'simgrid_topo/poweredtree_2_2_ep.A.8.log'  # ログファイルのパスを指定
      time, mops = extract_metrics_from_log(log_file)
      time_ep_poweredtree_2_2_10 += float(time) /10
      mops_ep_poweredtree_2_2_10 += float(mops) /10

    basename = "fullmesh_2_2"
    for i in range(10):
      smpirun_single(basename, app, app_size)
      log_file = 'simgrid_topo/fullmesh_2_2_ep.A.8.log'  # ログファイルのパスを指定
      time, mops = extract_metrics_from_log(log_file)
      time_ep_fullmesh_2_2_10 += float(time) /10
      mops_ep_fullmesh_2_2_10 += float(mops) /10

    basename = "partlymesh_2_2"
    for i in range(10):
      smpirun_single(basename, app, app_size)
      log_file = 'simgrid_topo/partlymesh_2_2_ep.A.8.log'  # ログファイルのパスを指定
      time, mops = extract_metrics_from_log(log_file)
      time_ep_partlymesh_2_2_10 += float(time) /10
      mops_ep_partlymesh_2_2_10 += float(mops) /10

    basename = "supertree_2_2"
    for i in range(10):
      smpirun_single(basename, app, app_size)
      log_file = 'simgrid_topo/supertree_2_2_ep.A.8.log'  # ログファイルのパスを指定
      time, mops = extract_metrics_from_log(log_file)
      time_ep_supertree_2_2_10 += float(time) /10
      mops_ep_supertree_2_2_10 += float(mops) /10

    basename = "tree_2_2"
    app = "mg"
    time_mg_tree_2_2_10 = 0
    mops_mg_tree_2_2_10 = 0
    time_mg_poweredtree_2_2_10 = 0
    mops_mg_poweredtree_2_2_10 = 0
    time_mg_fullmesh_2_2_10 = 0
    mops_mg_fullmesh_2_2_10 = 0
    time_mg_partlymesh_2_2_10 = 0
    mops_mg_partlymesh_2_2_10 = 0
    time_mg_supertree_2_2_10 = 0
    mops_mg_supertree_2_2_10 = 0

    for i in range(10):
      smpirun_single(basename, app, app_size)
      log_file = 'simgrid_topo/tree_2_2_mg.A.8.log'  # ログファイルのパスを指定
      time, mops = extract_metrics_from_log(log_file)
      time_mg_tree_2_2_10 += float(time) /10
      mops_mg_tree_2_2_10 += float(mops) /10

    basename = "poweredtree_2_2"
    for i in range(10):
      smpirun_single(basename, app, app_size)
      log_file = 'simgrid_topo/poweredtree_2_2_mg.A.8.log'  # ログファイルのパスを指定
      time, mops = extract_metrics_from_log(log_file)
      time_mg_poweredtree_2_2_10 += float(time) /10
      mops_mg_poweredtree_2_2_10 += float(mops) /10

    basename = "fullmesh_2_2"
    for i in range(10):
      smpirun_single(basename, app, app_size)
      log_file = 'simgrid_topo/fullmesh_2_2_mg.A.8.log'  # ログファイルのパスを指定
      time, mops = extract_metrics_from_log(log_file)
      time_mg_fullmesh_2_2_10 += float(time) /10
      mops_mg_fullmesh_2_2_10 += float(mops) /10

    basename = "partlymesh_2_2"
    for i in range(10):
      smpirun_single(basename, app, app_size)
      log_file = 'simgrid_topo/partlymesh_2_2_mg.A.8.log'  # ログファイルのパスを指定
      time, mops = extract_metrics_from_log(log_file)
      time_mg_partlymesh_2_2_10 += float(time) /10
      mops_mg_partlymesh_2_2_10 += float(mops) /10

    basename = "supertree_2_2"
    for i in range(10):
      smpirun_single(basename, app, app_size)
      log_file = 'simgrid_topo/supertree_2_2_mg.A.8.log'  # ログファイルのパスを指定
      time, mops = extract_metrics_from_log(log_file)
      time_mg_supertree_2_2_10 += float(time) /10
      mops_mg_supertree_2_2_10 += float(mops) /10

    basename = "tree_2_2"
    app = "ft"
    time_ft_tree_2_2_10 = 0
    mops_ft_tree_2_2_10 = 0
    time_ft_poweredtree_2_2_10 = 0
    mops_ft_poweredtree_2_2_10 = 0
    time_ft_fullmesh_2_2_10 = 0
    mops_ft_fullmesh_2_2_10 = 0
    time_ft_partlymesh_2_2_10 = 0
    mops_ft_partlymesh_2_2_10 = 0
    time_ft_supertree_2_2_10 = 0
    mops_ft_supertree_2_2_10 = 0

    for i in range(10):
      smpirun_single(basename, app, app_size)
      log_file = 'simgrid_topo/tree_2_2_ft.A.8.log'  # ログファイルのパスを指定
      time, mops = extract_metrics_from_log(log_file)
      time_ft_tree_2_2_10 += float(time) /10
      mops_ft_tree_2_2_10 += float(mops) /10

    basename = "poweredtree_2_2"
    for i in range(10):
      smpirun_single(basename, app, app_size)
      log_file = 'simgrid_topo/poweredtree_2_2_ft.A.8.log'  # ログファイルのパスを指定
      time, mops = extract_metrics_from_log(log_file)
      time_ft_poweredtree_2_2_10 += float(time) /10
      mops_ft_poweredtree_2_2_10 += float(mops) /10

    basename = "fullmesh_2_2"
    for i in range(10):
      smpirun_single(basename, app, app_size)
      log_file = 'simgrid_topo/fullmesh_2_2_ft.A.8.log'  # ログファイルのパスを指定
      time, mops = extract_metrics_from_log(log_file)
      time_ft_fullmesh_2_2_10 += float(time) /10
      mops_ft_fullmesh_2_2_10 += float(mops) /10

    basename = "partlymesh_2_2"
    for i in range(10):
      smpirun_single(basename, app, app_size)
      log_file = 'simgrid_topo/partlymesh_2_2_ft.A.8.log'  # ログファイルのパスを指定
      time, mops = extract_metrics_from_log(log_file)
      time_ft_partlymesh_2_2_10 += float(time) /10
      mops_ft_partlymesh_2_2_10 += float(mops) /10

    basename = "supertree_2_2"
    for i in range(10):
      smpirun_single(basename, app, app_size)
      log_file = 'simgrid_topo/supertree_2_2_ft.A.8.log'  # ログファイルのパスを指定
      time, mops = extract_metrics_from_log(log_file)
      time_ft_supertree_2_2_10 += float(time) /10
      mops_ft_supertree_2_2_10 += float(mops) /10

    basename = "tree_2_2"
    app = "is"
    time_is_tree_2_2_10 = 0
    mops_is_tree_2_2_10 = 0
    time_is_poweredtree_2_2_10 = 0
    mops_is_poweredtree_2_2_10 = 0
    time_is_fullmesh_2_2_10 = 0
    mops_is_fullmesh_2_2_10 = 0
    time_is_partlymesh_2_2_10 = 0
    mops_is_partlymesh_2_2_10 = 0
    time_is_supertree_2_2_10 = 0
    mops_is_supertree_2_2_10 = 0

    for i in range(10):
      smpirun_single(basename, app, app_size)
      log_file = 'simgrid_topo/tree_2_2_is.A.8.log'  # ログファイルのパスを指定
      time, mops = extract_metrics_from_log(log_file)
      time_is_tree_2_2_10 += float(time) /10
      mops_is_tree_2_2_10 += float(mops) /10

    basename = "poweredtree_2_2"
    for i in range(10):
      smpirun_single(basename, app, app_size)
      log_file = 'simgrid_topo/poweredtree_2_2_is.A.8.log'  # ログファイルのパスを指定
      time, mops = extract_metrics_from_log(log_file)
      time_is_poweredtree_2_2_10 += float(time) /10
      mops_is_poweredtree_2_2_10 += float(mops) /10

    basename = "fullmesh_2_2"
    for i in range(10):
      smpirun_single(basename, app, app_size)
      log_file = 'simgrid_topo/fullmesh_2_2_is.A.8.log'  # ログファイルのパスを指定
      time, mops = extract_metrics_from_log(log_file)
      time_is_fullmesh_2_2_10 += float(time) /10
      mops_is_fullmesh_2_2_10 += float(mops) /10

    basename = "partlymesh_2_2"
    for i in range(10):
      smpirun_single(basename, app, app_size)
      log_file = 'simgrid_topo/partlymesh_2_2_is.A.8.log'  # ログファイルのパスを指定
      time, mops = extract_metrics_from_log(log_file)
      time_is_partlymesh_2_2_10 += float(time) /10
      mops_is_partlymesh_2_2_10 += float(mops) /10

    basename = "supertree_2_2"
    for i in range(10):
      smpirun_single(basename, app, app_size)
      log_file = 'simgrid_topo/supertree_2_2_is.A.8.log'  # ログファイルのパスを指定
      time, mops = extract_metrics_from_log(log_file)
      time_is_supertree_2_2_10 += float(time) /10
      mops_is_supertree_2_2_10 += float(mops) /10

    basename = "tree_2_2"
    app = "lu"
    time_lu_tree_2_2_10 = 0
    mops_lu_tree_2_2_10 = 0
    time_lu_poweredtree_2_2_10 = 0
    mops_lu_poweredtree_2_2_10 = 0
    time_lu_fullmesh_2_2_10 = 0
    mops_lu_fullmesh_2_2_10 = 0
    time_lu_partlymesh_2_2_10 = 0
    mops_lu_partlymesh_2_2_10 = 0
    time_lu_supertree_2_2_10 = 0
    mops_lu_supertree_2_2_10 = 0

    for i in range(10):
      smpirun_single(basename, app, app_size)
      log_file = 'simgrid_topo/tree_2_2_lu.A.8.log'  # ログファイルのパスを指定
      time, mops = extract_metrics_from_log(log_file)
      time_lu_tree_2_2_10 += float(time) /10
      mops_lu_tree_2_2_10 += float(mops) /10

    basename = "poweredtree_2_2"
    for i in range(10):
      smpirun_single(basename, app, app_size)
      log_file = 'simgrid_topo/poweredtree_2_2_lu.A.8.log'  # ログファイルのパスを指定
      time, mops = extract_metrics_from_log(log_file)
      time_lu_poweredtree_2_2_10 += float(time) /10
      mops_lu_poweredtree_2_2_10 += float(mops) /10

    basename = "fullmesh_2_2"
    for i in range(10):
      smpirun_single(basename, app, app_size)
      log_file = 'simgrid_topo/fullmesh_2_2_lu.A.8.log'  # ログファイルのパスを指定
      time, mops = extract_metrics_from_log(log_file)
      time_lu_fullmesh_2_2_10 += float(time) /10
      mops_lu_fullmesh_2_2_10 += float(mops) /10

    basename = "partlymesh_2_2"
    for i in range(10):
      smpirun_single(basename, app, app_size)
      log_file = 'simgrid_topo/partlymesh_2_2_lu.A.8.log'  # ログファイルのパスを指定
      time, mops = extract_metrics_from_log(log_file)
      time_lu_partlymesh_2_2_10 += float(time) /10
      mops_lu_partlymesh_2_2_10 += float(mops) /10

    basename = "supertree_2_2"
    for i in range(10):
      smpirun_single(basename, app, app_size)
      log_file = 'simgrid_topo/supertree_2_2_lu.A.8.log'  # ログファイルのパスを指定
      time, mops = extract_metrics_from_log(log_file)
      time_lu_supertree_2_2_10 += float(time) /10
      mops_lu_supertree_2_2_10 += float(mops) /10

    #tree_times = [time_cg_tree_2_2_10, time_ep_tree_2_2_10,time_mg_tree_2_2_10,time_ft_tree_2_2_10,time_is_tree_2_2_10,time_lu_tree_2_2_10]
    poweredtree_times = [time_cg_poweredtree_2_2_10 / time_cg_poweredtree_2_2_10, time_ep_poweredtree_2_2_10 / time_ep_poweredtree_2_2_10,time_mg_poweredtree_2_2_10 / time_mg_poweredtree_2_2_10,time_ft_poweredtree_2_2_10 / time_ft_poweredtree_2_2_10,time_is_poweredtree_2_2_10 / time_is_poweredtree_2_2_10,time_lu_poweredtree_2_2_10 / time_lu_poweredtree_2_2_10]
    #fullmesh_times = [0.156, 0.829,1,1,1,1]
    partlymesh_times = [time_cg_partlymesh_2_2_10 / time_cg_poweredtree_2_2_10, time_ep_partlymesh_2_2_10 / time_ep_poweredtree_2_2_10,time_mg_partlymesh_2_2_10 / time_mg_poweredtree_2_2_10,time_ft_partlymesh_2_2_10 / time_ft_poweredtree_2_2_10,time_is_partlymesh_2_2_10 / time_is_poweredtree_2_2_10,time_lu_partlymesh_2_2_10 /time_lu_poweredtree_2_2_10]
    supertree_times = [time_cg_supertree_2_2_10 / time_cg_poweredtree_2_2_10, time_ep_supertree_2_2_10 / time_ep_poweredtree_2_2_10,time_mg_supertree_2_2_10 / time_mg_poweredtree_2_2_10,time_ft_supertree_2_2_10 / time_ft_poweredtree_2_2_10,time_is_supertree_2_2_10 / time_is_poweredtree_2_2_10,time_lu_supertree_2_2_10 / time_lu_poweredtree_2_2_10]

    poweredtree_mops = [mops_cg_poweredtree_2_2_10 / mops_cg_poweredtree_2_2_10, mops_ep_poweredtree_2_2_10 / mops_ep_poweredtree_2_2_10,mops_mg_poweredtree_2_2_10 / mops_mg_poweredtree_2_2_10,mops_ft_poweredtree_2_2_10 / mops_ft_poweredtree_2_2_10,mops_is_poweredtree_2_2_10 / mops_is_poweredtree_2_2_10,mops_lu_poweredtree_2_2_10 / mops_lu_poweredtree_2_2_10]
    partlymesh_mops = [mops_cg_partlymesh_2_2_10 / mops_cg_poweredtree_2_2_10, mops_ep_partlymesh_2_2_10 / mops_ep_poweredtree_2_2_10,mops_mg_partlymesh_2_2_10 / mops_mg_poweredtree_2_2_10,mops_ft_partlymesh_2_2_10 / mops_ft_poweredtree_2_2_10,mops_is_partlymesh_2_2_10 / mops_is_poweredtree_2_2_10,mops_lu_partlymesh_2_2_10 /mops_lu_poweredtree_2_2_10]
    supertree_mops = [mops_cg_supertree_2_2_10 / mops_cg_poweredtree_2_2_10, mops_ep_supertree_2_2_10 / mops_ep_poweredtree_2_2_10,mops_mg_supertree_2_2_10 / mops_mg_poweredtree_2_2_10,mops_ft_supertree_2_2_10 / mops_ft_poweredtree_2_2_10,mops_is_supertree_2_2_10 / mops_is_poweredtree_2_2_10,mops_lu_supertree_2_2_10 / mops_lu_poweredtree_2_2_10]

    data = {
        "poweredtree": {
            "times": poweredtree_times,
            "mops": poweredtree_mops
        },
        "partlymesh": {
            "times": partlymesh_times,
            "mops": partlymesh_mops
        },
        "supertree": {
            "times": supertree_times,
            "mops": supertree_mops
        }
    }
    with open("results.json", "w") as f:
        json.dump(data, f, indent=2)

    x = range(len(benchmarks))
    bar_width = 0.25
    colors = ["lightgray", "dimgray", "black"]
    plt.figure(figsize=(10, 6))
    plt.bar([i - bar_width for i in x], poweredtree_times, width=bar_width, label="tree", color=colors[0])
    plt.bar([i for i in x], partlymesh_times, width=bar_width, label="partlymesh", color=colors[1])
    plt.bar([i + bar_width for i in x], supertree_times, width=bar_width, label="flattentree", color=colors[2])
    plt.xticks(x, benchmarks, rotation=15)
    plt.xlabel("Benchmarks")
    plt.ylabel("Execution Time (s)")
    plt.title("Execution Time per Topology")
    plt.legend()
    plt.tight_layout()
    
    plt.savefig("topology_cg_ep_execution_time_comparison.png")
    plt.close()

    print("complete!")

    print("CG")
    print(time_cg_tree_2_2_10)
    print(mops_cg_tree_2_2_10)
    print(time_cg_poweredtree_2_2_10)
    print(mops_cg_poweredtree_2_2_10)
    print(time_cg_fullmesh_2_2_10)
    print(mops_cg_fullmesh_2_2_10)
    print(time_cg_partlymesh_2_2_10)
    print(mops_cg_partlymesh_2_2_10)
    print(time_cg_supertree_2_2_10)
    print(mops_cg_supertree_2_2_10)

    print("EP")
    print(time_ep_tree_2_2_10)
    print(mops_ep_tree_2_2_10)
    print(time_ep_poweredtree_2_2_10)
    print(mops_ep_poweredtree_2_2_10)
    print(time_ep_fullmesh_2_2_10)
    print(mops_ep_fullmesh_2_2_10)
    print(time_ep_partlymesh_2_2_10)
    print(mops_ep_partlymesh_2_2_10)
    print(time_ep_supertree_2_2_10)
    print(mops_ep_supertree_2_2_10)

    print("MG")
    print(time_mg_tree_2_2_10)
    print(mops_mg_tree_2_2_10)
    print(time_mg_poweredtree_2_2_10)
    print(mops_mg_poweredtree_2_2_10)
    print(time_mg_fullmesh_2_2_10)
    print(mops_mg_fullmesh_2_2_10)
    print(time_mg_partlymesh_2_2_10)
    print(mops_mg_partlymesh_2_2_10)
    print(time_mg_supertree_2_2_10)
    print(mops_mg_supertree_2_2_10)

    print("FT")
    print(time_ft_tree_2_2_10)
    print(mops_ft_tree_2_2_10)
    print(time_ft_poweredtree_2_2_10)
    print(mops_ft_poweredtree_2_2_10)
    print(time_ft_fullmesh_2_2_10)
    print(mops_ft_fullmesh_2_2_10)
    print(time_ft_partlymesh_2_2_10)
    print(mops_ft_partlymesh_2_2_10)
    print(time_ft_supertree_2_2_10)
    print(mops_ft_supertree_2_2_10)

    print("IS")
    print(time_is_tree_2_2_10)
    print(mops_is_tree_2_2_10)
    print(time_is_poweredtree_2_2_10)
    print(mops_is_poweredtree_2_2_10)
    print(time_is_fullmesh_2_2_10)
    print(mops_is_fullmesh_2_2_10)
    print(time_is_partlymesh_2_2_10)
    print(mops_is_partlymesh_2_2_10)
    print(time_is_supertree_2_2_10)
    print(mops_is_supertree_2_2_10)

    print("LU")
    print(time_lu_tree_2_2_10)
    print(mops_lu_tree_2_2_10)
    print(time_lu_poweredtree_2_2_10)
    print(mops_lu_poweredtree_2_2_10)
    print(time_lu_fullmesh_2_2_10)
    print(mops_lu_fullmesh_2_2_10)
    print(time_lu_partlymesh_2_2_10)
    print(mops_lu_partlymesh_2_2_10)
    print(time_lu_supertree_2_2_10)
    print(mops_lu_supertree_2_2_10)
