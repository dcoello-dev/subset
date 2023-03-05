import subprocess


def _ex_subprocess(cmd: str, shell=True) -> tuple:
    p = subprocess.Popen(
        cmd, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = p.communicate()
    return (p.returncode, output, error)
