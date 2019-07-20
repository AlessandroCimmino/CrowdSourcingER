import json
import os
sys.path.append("/home/nvidia/workspace/dbgroup/benchmark/CrowdSourcingER")
import config

def parse_entites(spark):
    path_entities = config.PATHS["entities_gt"]
    df = spark.read.json(path_entities, multiLine=True)
    return df

def parse_json_files(spark):
    path_entities = config.PATHS["json_files"]
    df = spark.read.json(path_entities, multiLine=True)
    return df
