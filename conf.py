__author__ = 'andrew'

matterhornenv = {"cluster": {"url": "http://testadmin.usask.ca:8080", "engage": "http://testengage.usask.ca:8080/engage/ui/index.html",
                             "ca": "testca.usask.ca"}, "allinone": {"url": "http://testallinone.usask.ca:8080",
                                                                    "ca": "demo_capture_agent", "engage": "/engage/ui/index.html"}}


def get_url(server):
    return matterhornenv[server]["url"]

def get_ca(server):
    return matterhornenv[server]["ca"]

def get_engageurl(server):
    return matterhornenv[server]["engage"]
