#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to my web servers
"""
from datetime import datetime
from fabric.api import *
import os


env.hosts = ['3.231.212.152', '35.153.144.82']
env.user = "ubuntu"


def deploy():
    """
        Creates and distributes an archive to my web servers
    """
    try:
        archive_path = do_pack()
    except:
        return False

    return do_deploy(archive_path)


def do_pack():
    """
        Generates an archive for web_static folder
    """
    try:
        if not os.path.exists("versions"):
            local('mkdir versions')
        t = datetime.now()
        f = "%Y%m%d%H%M%S"
        archive_path = 'versions/web_static_{}.tgz'.format(t.strftime(f))
        local('tar -cvzf {} web_static'.format(archive_path))
        return archive_path
    except Exception:
        return None


def do_deploy(archive_path):
    """
        Distributes an archive to my web servers
    """
    if not os.path.exists(archive_path):
        return False
    try:
        filename = archive_path.split("/")
        filename = filename[1]

        fname = filename.split('.')
        fname = fname[0]

        newpath = '/data/web_static/releases/{}/'.format(fname)

        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(newpath))
        run("tar -xzf /tmp/{} -C {}".format(filename, newpath))
        run("rm /tmp/{}".format(filename))
        run("mv {}web_static/* {}".format(newpath, newpath))
        run("rm -rf {}web_static".format(newpath))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(newpath))
        return True
    except Exception:
        return False
