import subprocess


class CommonUtil:

    @classmethod
    def run_subprocess_command(cls, command):
        subprocess.check_output(command,  shell=True, stderr=subprocess.PIPE)