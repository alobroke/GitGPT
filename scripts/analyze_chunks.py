import json

with open(
    "data/generated/chunks.json",
    "r",
    encoding="utf-8"
) as f:
    chunks = json.load(f)

lengths = [
    len(chunk["content"])
    for chunk in chunks
]

print("Total Chunks:", len(lengths))

print("Min:", min(lengths))

print("Max:", max(lengths))

print("Average:", sum(lengths) / len(lengths))