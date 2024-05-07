import subprocess
import os

main_local_path = "main.py"
current_dir = os.getcwd()
main_full_path = os.path.join(current_dir, main_local_path)

subprocess.Popen(["start", "cmd", "/k", "python", main_full_path], shell=True)
