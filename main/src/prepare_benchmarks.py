#!/usr/bin/env python3
import os, sys

all_domains_folder   =     sys.argv[1]  # e.g. "../benchmarks/domrep"
max_plan_length      = int(sys.argv[2]) # e.g. 15
plans_subfolder_name =     sys.argv[3]  # e.g. "lifted_plans/033"
plans_extension      =     sys.argv[4]  # e.g. ".plan-lifted"

# loop over domain folders
for domain_folder in os.listdir(all_domains_folder):

    domain_folder_fullpath = os.path.join(all_domains_folder, domain_folder)
    if not os.path.isdir(domain_folder_fullpath):
        continue

    # loop over files in domain folders
    for file in os.listdir(domain_folder_fullpath):

        if not os.path.isfile(os.path.join(domain_folder_fullpath, file)):
            continue
        if not file.startswith("domain-"):
            continue

        domain_file = file
        domain_file_fullpath = os.path.join(domain_folder_fullpath, domain_file)

        problem_file = file.removeprefix("domain-")
        problem_file_fullpath = os.path.join(domain_folder_fullpath, problem_file)

        plan_file = problem_file.removesuffix(".pddl") + plans_extension
        plan_file_fullpath = os.path.join(domain_folder_fullpath, plans_subfolder_name, plan_file)

        # check if plan length does not exceed given bound
        with open(plan_file_fullpath, 'r') as f:
            plan_length = sum(1 for line in f if line.startswith("("))
        if plan_length > max_plan_length:
            continue
        
        print(f"{domain_file_fullpath} {problem_file_fullpath} {plan_file_fullpath}", end=None)