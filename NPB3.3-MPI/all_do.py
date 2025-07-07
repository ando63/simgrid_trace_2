import os
import subprocess

benchmarks = ["cg", "lu", "mg", "ep", "ft"]
class_name = "A"

for bench in benchmarks:
    for np in range(1, 65):
        file_path = f"bin/{bench}.{class_name}.{np}"
        if os.path.isfile(file_path):
            platform_file = f"./simgrid_topo/crossbar_{np}.xml"
            host_file = f"./simgrid_topo/crossbar_{np}.txt"
            benchmark_file = f"./bin/{bench}.A.{np}"
            file_name = f"--log=chaix.app:splitfile:1000000000:./traf_mat/sample_{np}_{bench}.A.{np}_trace_%.csv"
            log_file = f"./traf_log/sample_{bench}_A_{np}.log"
            cmd = [
                "smpirun",
                "--cfg=smpi/privatize_global_variables:yes",
                "-platform", platform_file,
                "-hostfile", host_file,
                benchmark_file,
                "--log=chaix.threshold:verbose",
                "--log=chaix.fmt:%m%n",
                file_name
            ]
            with open(log_file, "w") as outf:
                subprocess.run(cmd, stdout=outf)
        else:
            print(f"{file_path} is not existed")
