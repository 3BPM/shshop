import subprocess


def gitupdate():
    subprocess.call(['git','fetch --all'], shell=False)
    subprocess.call(['git','reset --hard origin/master'], shell=False)
    subprocess.call(['git','pull'], shell=False)



if __name__ == '__main__':
    gitupdate()