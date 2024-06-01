import os
import subprocess

def launch_notebook():
    notebook_dir = os.path.join(os.path.dirname(__file__), '..', 'notebooks')
    subprocess.run(['jupyter', 'notebook', notebook_dir])

if __name__ == '__main__':
    launch_notebook()