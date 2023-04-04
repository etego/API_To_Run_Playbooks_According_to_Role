import os
import subprocess

def run_playbook(playbook_name):
    # Set the path to your playbooks directory
    playbook_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'playbooks')

    # Replace this with the command to run your specific playbook
    command = f"ansible-playbook {os.path.join(playbook_dir, playbook_name)}.yml"

    # Run the command and capture the output
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        raise Exception(f"Playbook execution failed: {stderr.decode('utf-8')}")

    return stdout.decode('utf-8')

def run_shell_script(script_name):
    # Here you can define the path to your shell scripts
    script_path = os.path.join('path', 'to', 'your', 'scripts', script_name)

    # Run the shell script and capture the output
    result = subprocess.run([script_path], capture_output=True, text=True, shell=True)
    return result.stdout