#!/usr/bin/python3
""" Function that deploys """
from fabric.api import *


env.hosts = ['3.231.212.152', '35.153.144.82']
env.user = "ubuntu"


def do_clean(number=0):
    """
        Deletes out-of-date archives
    """

    number = int(number)
    if number == 1 or number == 0:
        local("cd versions; ls | head -n -1 | xargs rm -rf")
        run("cd /data/web_static/releases; ls | head -n -1 | xargs rm -rf")
    else:
        local("cd versions; ls | head -n -{} | xargs rm -rf".format(number))
        run("cd /data/web_static/releases; ls | head -n -{} | xargs rm -rf"
            .format(number))
