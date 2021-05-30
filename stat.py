import json

space = json.load(open('swig-master/SWiG_jsons/imsitu_space.json','r',encoding='utf-8'))

verbs = space['verbs']
num = 0

all_args = set()
for verb in verbs:
    args = verbs[verb]['order']
    for arg in args:
        all_args.add(arg)

print(len(all_args))