import os
import json
import re

import yaml

# find & replace tokens for repo envs (sparql creds)
SPARQL_ENDPOINT = os.environ.get("SPARQL_ENDPOINT", "")
SPARQL_USERNAME = os.environ.get("SPARQL_USERNAME", "")
SPARQL_PASSWORD = os.environ.get("SPARQL_PASSWORD", "")

with open("config.yaml", "r") as f:
    c = f.read()
c = c.replace("#{SPARQL_ENDPOINT}#", SPARQL_ENDPOINT)
c = c.replace("#{SPARQL_USERNAME}#", SPARQL_USERNAME)
c = c.replace("#{SPARQL_PASSWORD}#", SPARQL_PASSWORD)

# read config.yaml
config = yaml.load(c, Loader=yaml.Loader)

# find & replace remaining tokens depending on deployment method (& pipeline method?)
deploy_file = ""
deploy_str = ""
if config["deploymentMethod"] == "kubernetes":
    deploy_file = "kube-manifest.yaml"
elif config["deploymentMethod"] == "ecs":
    deploy_file = "ecs-task-def.json"
elif config["deploymentMethod"] == "docker":
    deploy_file = "docker-compose.yml"
else:
    raise ValueError(
        "Deployment method must be one of: 'kubernetes', 'ecs' or 'docker'"
    )


def config_name(name: str) -> str:
    """Transforms the camelCase config var name to UPPER_FORMAT"""
    name_list = [word.upper() for word in re.split("(?=[A-Z])", name)]
    return "_".join(name_list)


def config_val(key: str) -> str:
    """Returns the appropriate format of the config variable for each deploy file type"""
    k = config[key]
    deploy_type = config["deploymentMethod"]
    if k is None:
        return ""
    elif isinstance(k, bool):
        if deploy_type in ["kubernetes", "docker"]:
            return '"' + str(k) + '"'
        else:  # ecs
            return str(k)
    elif isinstance(k, int):
        return str(k)
    elif isinstance(k, list) or isinstance(k, dict):
        if deploy_type in ["kubernetes", "docker"]:
            return "'" + json.dumps(k) + "'"
        else:  # ecs
            return str(k)
    else:  # str
        return k


with open(f"deploy/{deploy_file}", "r") as f:
    deploy_str = f.read()

# need validation for each config var
for key in config.keys():
    deploy_str = deploy_str.replace(f"#{{{config_name(key)}}}#", config_val(key))

# remove http:// for kubernetes ingress host
if config["deploymentMethod"] == "kubernetes":
    old_host = re.findall("- host: (.*)", deploy_str)[0]
    new_host = old_host.split("//")[1]
    deploy_str = deploy_str.replace(f"- host: {old_host}", f"- host: {new_host}")

with open(f"deploy/new_{deploy_file}", "w") as f:
    f.write(deploy_str)
