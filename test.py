import json

meed = json.load(open("meed.json"))
for data in meed:
  print(data)