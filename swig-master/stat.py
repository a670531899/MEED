import json

datas = json.load(open('asg_test.json','r',encoding='utf-8'))

tot_args = 0
for data in datas:
    all_objs = set()
    regs= data['regions']
    for reg in regs:
        for k in reg:
            objs = reg[k]['objects']
            for ob in objs:
                id = ob['object_id']
                all_objs.add(id)
    print(all_objs)
    tot_args+=len(all_objs)
print(tot_args)