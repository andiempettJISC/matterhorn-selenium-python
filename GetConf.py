import os
import yaml

__author__ = 'andrew wilson'

conf_file = (os.path.abspath(os.path.join(os.path.dirname(__file__), 'conf.yaml')))

def getconf():
    return yaml.load(open(conf_file))


def get_url():
    return getconf()["matterhorn-server"]["url"]


def get_ca():
    return getconf()["matterhorn-server"]["capture-agent"]


def get_engageurl():
    return getconf()["matterhorn-server"]["engage"]


def get_users():
    return getconf()["users"]


def get_video():
    return getconf()["video-file"]