#!/usr/bin/env python3
import sys, json
import matplotlib.pyplot as plt

json_filepaths = sys.argv[1:]

plot_kwargs = {
    "baseline_ground": { "linestyle":'-', "markersize":3, "color":'blue', "label":"Baseline (0.00)" },
    "aries_ground": { "linestyle":'-', "markersize":3, "color":'red', "label":"Aries (0.00)" },
    "baseline_lifted_033_exhaust": { "linestyle":'-', "markersize":3, "color":'blue', "label":"Exhaust (0.33)" },
    "baseline_lifted_066_exhaust": { "linestyle":'--', "markersize":3, "color":'blue', "label":"Exhaust (0.66)" },
    "baseline_lifted_100_exhaust": { "linestyle":':', "markersize":3, "color":'blue', "label":"Exhaust (1.00)" },
    "baseline_lifted_033_relaxpre": { "linestyle":'-', "markersize":3, "color":'green', "label":"RelaxPre (0.33)" },
    "baseline_lifted_066_relaxpre": { "linestyle":'--', "markersize":3, "color":'green', "label":"RelaxPre (0.66)" },
    "baseline_lifted_100_relaxpre": { "linestyle":':', "markersize":3, "color":'green', "label":"RelaxPre (1.00)" },
    "aries_lifted_standard_033": { "linestyle":'-', "markersize":3, "color":'red', "label":"Aries (0.33)" },
    "aries_lifted_standard_066": { "linestyle":'--', "markersize":3, "color":'red', "label":"Aries (0.66)" },
    "aries_lifted_standard_100": { "linestyle":':', "markersize":3, "color":'red', "label":"Aries (1.00)" },
    "aries_lifted_independent_033": { "linestyle":'-', "markersize":3, "color":'red', "label":"Aries (0.33)" },
    "aries_lifted_independent_066": { "linestyle":'--', "markersize":3, "color":'red', "label":"Aries (0.66)" },
    "aries_lifted_independent_100": { "linestyle":':', "markersize":3, "color":'red', "label":"Aries (1.00)" },
}

data = {}

for json_filepath in json_filepaths:
    with open(json_filepath, 'r') as f:
        data.update(json.load(f))

points = {}

tags = list(data.keys())

for tag in tags:
    points[tag] = []

    for instance_id, instance_data in data[tag]["instances"].items():

        if instance_data.get("success", 0) == 0:
            continue
        points[tag].append((instance_id, instance_data["total_time"] / 1000))

max_time = 0

for tag in tags:
    max_time = max(max_time, max([pt[1] for pt in points[tag]]))
    points[tag] = sorted([pt[1] for pt in points[tag]])
for tag in tags:
    points[tag].append(max_time)

for tag in tags:
    plt.plot(points[tag], range(1, len(points[tag])+1, 1), **plot_kwargs.get(tag, {}))

plt.vlines(1, ymin=1, ymax=max(len(points[tag]) for tag in tags), linestyle=':', color='gray')
plt.vlines(60, ymin=1, ymax=max(len(points[tag]) for tag in tags), linestyle=':', color='gray')

plt.xscale('log')

plt.xlabel("Time (log s)")
plt.ylabel("Instances")

plt.legend(loc="upper left")

plt.show()