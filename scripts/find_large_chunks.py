

import json

with open(
    "data/generated/chunks.json",
    "r",
    encoding="utf-8"
) as f:
    chunks = json.load(f)

chunks.sort(
    key=lambda x: len(x["content"]),
    reverse=True
)

for chunk in chunks[:10]:

    print("\n" + "="*80)

    print("SIZE:", len(chunk["content"]))

    print("TYPE:", chunk["chunk_type"])

    print("NAME:", chunk["name"])

    print("FILE:", chunk["file"])