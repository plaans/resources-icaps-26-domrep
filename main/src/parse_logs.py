#!/usr/bin/env python3
import os, sys, json, re

logs_folder = sys.argv[1] # e.g. "benchmark_runs/lifted/033/logs"
tag = sys.argv[2]         # e.g. "aries_ground"

data = {tag: {"instances": {}, "summary": {}}}

for file in os.listdir(logs_folder):
    if not os.path.isfile(os.path.join(logs_folder, file)):
        continue
    if not file.endswith(".log"):
        continue

    data[tag]["summary"]["num_instances"] = data[tag]["summary"].get("num_instances", 0) + 1 

    with open(os.path.join(logs_folder, file), 'r') as f:
        num_skipped_effects = 0
        num_known_effects = 0
        num_total_effects = 0
        num_variables = 0
        num_constraints = 0

        lines = f.readlines()
        for line in lines:
            line = line.strip()

            if line.startswith("- Plan:"):
                #with open(line.split("Plan:")[1].strip(), 'r') as f:
                #    plan_length = sum(1 for line in f if line.startswith("("))
                plan_name = os.path.splitext(os.path.basename(line.split("Plan:")[1]))[0]

            if line.startswith("- Domain:"):
                domain_name = os.path.basename(os.path.dirname(line.split("Domain:")[1]))
        
            #if "--- skipped" in line:
            #    num_skipped_effects += 1
            #if line.startswith("# NUM EFFECTS (known only):"):
            #    num_known_effects = int(line.split("# NUM EFFECTS (known only):")[1])
            #if line.startswith("# NUM EFFECTS (known + potential):"):
            #    num_total_effects = int(line.split("# NUM EFFECTS (known + potential):")[1])
            #if line.startswith("# NUM VARIABLES:"):
            #    num_variables = int(line.split("# NUM VARIABLES:")[1])
            #if line.startswith("# NUM CONSTRAINTS:"):
            #    num_constraints = int(line.split("# NUM CONSTRAINTS:")[1])

        instance_id = domain_name+"__"+plan_name # type: ignore
        data[tag]["instances"].setdefault(instance_id, {})
        #data[tag]["instances"].setdefault(instance_id, {}).update({ "plan_length": plan_length }) # type: ignore
        
        if (len(lines) > 0
            and ("VALID" in lines[-1].strip() or "SMCS" in lines[-1].strip()
        )):
            data[tag]["summary"]["successes"] = data[tag]["summary"].get("successes", 0) + 1

            smcs_match = re.search(r"Smallest\s+SMCS\((\d+)\)|Smallest\s+SMCS\s+valid", lines[-1].strip())
            runtime_enctime_match = re.search(r"(\d+)\s+\(runtime ms\)\s+(\d+)\s+\(enctime ms\)", lines[-1].strip())

            data[tag]["instances"][instance_id].update({                                      # type: ignore
                "success": 1,
                "repair_size": int(smcs_match.group(1)) if smcs_match and smcs_match.group(1) else 0,        # type: ignore
                "total_time": float(runtime_enctime_match.group(1)),                                           # type: ignore
                "encoding_time": float(runtime_enctime_match.group(2)),                                      # type: ignore
                #"num_known_effects": num_known_effects,
                #"num_total_effects": num_total_effects,
                #"num_skipped_effects": num_skipped_effects,
                #"num_variables": num_variables,
                #"num_constraints": num_constraints,
            })

        else:
            data[tag]["instances"][instance_id].update({ "success": 0 }) # type: ignore

print(json.dumps(data, indent=4))