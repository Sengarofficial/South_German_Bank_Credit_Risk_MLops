import yaml
import os
import shutil
from src.logs import log 
import json


# set a logger file
logger = log(path="Log_File/", file="config_utils.logs")



def read_params(config_path: str) -> dict:
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    logger.info(f"read parameters")
    return config
