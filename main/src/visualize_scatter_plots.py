#!/usr/bin/env python3
import sys, json
import matplotlib.pyplot as plt

timeout_seconds = float(sys.argv[1])
json_filepath1 = sys.argv[2]
json_filepath2 = sys.argv[3]

plot_kwargs = {
    "baseline_ground": {"marker":".", "s":1 },
    "aries_ground": {"marker":".", "s":1 },
}
tag_labels = {
    "baseline_ground": "Baseline",
    "aries_ground": "Aries",
}

data = {}

for json_filepath in [json_filepath1, json_filepath2]:
    with open(json_filepath, 'r') as f:
        data.update(json.load(f))

points = {}

tags = list(data.keys())
assert len(tags) == 2

for tag in tags:
    points[tag] = {}

    for instance_id, instance_data in data[tag]["instances"].items():

        if instance_data["success"] == 0:
            points[tag][instance_id] = timeout_seconds
        else:
            points[tag][instance_id] = instance_data["total_time"] / 1000

for tag in tags:
    print(f"# instances less than 1 second for {tag}:",
        sum(1 for instance_id, _ in data[tag]["instances"].items() if points[tag][instance_id] <= 1),
    )

print(f"# instances faster for {tags[1]} than for {tags[0]}:",
    len([instance_id for instance_id, _ in points[tags[1]].items()
         if points[tags[1]][instance_id] <= points[tags[0]][instance_id]]
    ),
)
plt.figure(figsize=(5,5))
plt.scatter(list(points[tags[0]].values()), list(points[tags[1]].values()), marker=".", s=1) # type: ignore

plt.plot([0.001, timeout_seconds], [0.001, timeout_seconds], linestyle='-', color='black')

plt.plot([0.001, 1.0], [1.0, 1.0], linestyle='--', color='gray')
plt.plot([1.0, 1.0], [1.0, 0.001], linestyle='--', color='gray')

plt.xscale('log')
plt.yscale('log')

plt.xlabel(f"{tag_labels.get(tags[0], tags[0])} time (log s)")
plt.ylabel(f"{tag_labels.get(tags[1], tags[1])} time (log s)")

#plt.legend()

plt.show()
