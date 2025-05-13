import subprocess
from PyQt5.QtWidgets import QMessageBox

def check_docker_engine():
    try:
        cmd = 'wsl --distribution ubuntu --user root -- bash -lic "docker info"'
        subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False

def start_docker_engine():
    if not check_docker_engine():
        QMessageBox.warning(None, "Docker Engine Not Running",
                            "Docker Engine is not running in WSL. Please ensure Docker is installed and running in your Ubuntu WSL distribution.")

def dkill():
    cmds = [
        'docker stop $(docker ps -aq)',
        'docker rm $(docker ps -aq)',
        'docker rmi $(docker images -q)',
        'docker system prune -a --volumes --force',
        'docker network prune --force'
    ]
    for cmd in cmds:
        try:
            wsl_cmd = f'wsl --distribution ubuntu --user root -- bash -lic "{cmd}"'
            subprocess.call(wsl_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass
