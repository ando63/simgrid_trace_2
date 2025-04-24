
import os
import glob
import argparse
import subprocess

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

    basename = "tree_8_8"
    app = "cg"
    app_size = "A"
    time_cg_10 = 0
    mops_cg_10 = 0

    for i in range(10):
      smpirun_single(basename, app, app_size)
      log_file = 'simgrid_topo/tree_8_cg.A.8.log'  # ログファイルのパスを指定
      time, mops = extract_metrics_from_log(log_file)
      time_cg_10 += float(time) /10
      mops_cg_10 += float(mops) /10

    print(time_cg_10)
    print(mops_cg_10)


