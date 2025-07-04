import subprocess

for i in range(1, 65):
    print(f"Running python3 xmlgen_crossbar.py {i}")
    subprocess.run(["python3", "xmlgen_crossbar.py", str(i)])
