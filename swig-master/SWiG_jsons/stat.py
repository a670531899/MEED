import json

datas = json.load(open('train.json','r',encoding='utf-8'))
datas.update(json.load(open('test.json','r',encoding='utf-8')))
datas.update(json.load(open('dev.json','r',encoding='utf-8')))
print(len(datas))
#
# tot_args = 0
# for verb in datas:
#     data = datas[verb]
#     args = set()
#     for reg in data['frames']:
#         for arg in reg:
#             noun = reg[arg]
#             args.add(noun)
#     tot_args+=len(args)
# print(tot_args)