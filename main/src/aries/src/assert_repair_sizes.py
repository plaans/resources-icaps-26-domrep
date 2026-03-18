#!/usr/bin/env python3
import sys, json

json_filepath1 = sys.argv[1]
json_filepath2 = sys.argv[2]

data = {}

for json_filepath in [json_filepath1, json_filepath2]:
    with open(json_filepath, 'r') as f:
        data.update(json.load(f))

repair_sizes = {}

tags = list(data.keys())

for tag in tags:
    for instance_id, instance_data in data[tag]["instances"].items():
        if "repair_size" in instance_data:
            if instance_id not in repair_sizes:
                repair_sizes[instance_id] = instance_data["repair_size"]
            elif repair_sizes[instance_id] != instance_data["repair_size"]:
                print(tag, instance_id, repair_sizes[instance_id], instance_data["repair_size"])

