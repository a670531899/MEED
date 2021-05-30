import json
import numpy as np
import os

all_datas = {}
with open('swig-master/SWiG_jsons/train.json', 'r',encoding='utf-8') as f:
    all_datas.update(json.load(f))
    # print(json.load(f))
with open('swig-master/SWiG_jsons/dev.json', 'r',encoding='utf-8') as f:
    all_datas.update(json.load(f))
with open('swig-master/SWiG_jsons/test.json', 'r',encoding='utf-8') as f:
    all_datas.update(json.load(f))
with open('../m2e2/all_event_verbs.json', 'r',encoding='utf-8') as f:
    all_event_verbs = json.load(f)
space = json.load(open('swig-master/SWiG_jsons/imsitu_space.json','r',encoding='utf-8'))

verb2rels = json.load(open('verb2rels.json','r',encoding='utf-8'))
int2word = np.load('int2word.npy')
word2int = json.load(open('word2int.json','r',encoding='utf-8'))

id2noun = {}
for noun in space['nouns']:
    id2noun[noun]=space['nouns'][noun]['gloss']
all_verbs = []
for event in all_event_verbs:
    all_verbs.extend(all_event_verbs[event])
verb2datas = {}
for verb in all_verbs:
    num = 1
    verb2datas[verb]=[]
    for data in all_datas:
        if verb in data:
            verb2datas[verb].append(all_datas[data])
            num+=1
            if num==4:
                break

argus = set()
res = set()
arg2verb = {}
for k in all_datas:
    frames = all_datas[k]['frames']
    verb = k.split('_')[0]
    if verb not in all_verbs:
        continue
    res.add(k)
    for frame in frames:
        aa = ""
        for a in frame:
            aa += "_" + a
        argus.add(aa)
        if aa not in arg2verb:
            arg2verb[aa]=set()
            arg2verb[aa].add(verb)
        else:
            arg2verb[aa].add(verb)
            # print(k, all_datas[k]['frames'])

#ramming
# ------get relations------
# for arg in argus:
#     args = arg.split('_')[1:]
#     arg_verbs = arg2verb[arg]
#     verb2rels = all_verbs_now
#     print(args)
#     for verb in arg_verbs:
#
#         if verb in all_verbs_now:
#             continue
#         print(verb)
#         num = 1
#         for data in verb2datas[verb]:
#             for frame in data['frames']:
#                 num +=1
#                 if num==5:
#                     break
#                 new_arg = {}
#                 for k in frame:
#                     if frame[k]!='':
#                         new_arg[k]=id2noun[frame[k]]
#                     else:
#                         new_arg[k]=frame[k]
#                 print(new_arg)
#             if num == 5:
#                 break
#         for data in verb2datas[verb]:
#             ff = 0
#             for frame in data['frames']:
#                 f = 0
#                 for k in frame:
#                     if frame[k]=='':
#                         f=1
#                         break
#                 if f==0:
#                     ff=1
#                     new_arg = {}
#                     for k in frame:
#                         if frame[k] != '':
#                             new_arg[k] = id2noun[frame[k]]
#                         else:
#                             new_arg[k] = frame[k]
#                     print(new_arg)
#                     break
#             if ff==1:
#                 break
#         while(True):
#             inp = input()
#             if inp=='0':
#                 break
#             coms = inp.split()
#             rel = coms[1]
#             if coms[1]=='verb':
#                 rel=verb
#             else:
#                 for word in coms[2:-1]:
#                     rel+=' '+word
#             if verb not in verb2rels:
#                 verb2rels[verb] = [[coms[0],rel,coms[-1]]]
#             else:
#                 verb2rels[verb].append([coms[0],rel,coms[-1]])
#         json.dump(verb2rels,open('verb2rels.json','w',encoding='utf-8'),indent=4)
#         all_verbs_now = verb2rels

with open('swig-master/SWiG_jsons/imsitu_space.json', 'r') as f:
    space = json.load(f)
id2n = space['nouns']
res = list(res)
id2img = {}
img2id = {}
id2object = {}
object2id = {}
object2id["<BOS>"]="0"
object2id["<EOS>"]="1"
object2id["<UKN>"]="2"

id2object["0"]="<BOS>"
id2object["1"]="<EOS>"
id2object["2"]="<UNK>"
id = 0
reg_id = 0
o_id = 0
object_id = 3
w_file = []
rel_id = 0
ob2num = {}
all_ob = set()

#判断一下argument是否为空
inf_names = np.load('swig-master/inf_names.npy')
image_id = 0
for image in inf_names:
    # print(image)
    img2id[image] = image_id
    id2img[image_id] = image
    image_id+=1
ob2id = {}
ob2name = {}
for r in res:
    w_file.append({"image_id": str(img2id[r]), 'regions': [], 'relationships': []})
    width = all_datas[r]['width']
    height = all_datas[r]['height']
    verb = r.split('_')[0]
    boxes = all_datas[r]['bb']
    reg = {}
    for frame in all_datas[r]['frames']:
        reg[reg_id]={}
        reg[reg_id]['objects'] = []
        reg[reg_id]['relationships']=[]
        reg[reg_id]['phrase'] = ''

        for k in frame:
            if frame[k] == '':
                continue
            minx = 999999
            min_n = ""
            for n in id2n[frame[k]]['gloss']:
                if n not in ob2num:
                    ob2num[n]=0
                if ob2num[n] < minx:
                    minx = ob2num[n]
                    min_n = n

            if min_n == "":
                min_n = id2n[frame[k]]['gloss'][0]
            if min_n not in ob2num:
                ob2num[min_n] = 1
            else:
                ob2num[min_n] += 1

            ob2name[frame[k]] = min_n
            if boxes[k][0]==-1:
                reg[reg_id]['objects'].append(
                    {'object_id': o_id, 'name': min_n, 'attributes': [], 'x': 0, 'y': 0, 'w': width, 'h': height})
            else:
                reg[reg_id]['objects'].append(
                    {'object_id': o_id, 'name': min_n, 'attributes': [], 'x': boxes[k][0], 'y': boxes[k][1],
                     'w': boxes[k][3] - boxes[k][1], 'h': boxes[k][2] - boxes[k][0]})
            ob2id[frame[k]] = o_id
            if ob2name[frame[k]] not in all_ob:
                object2id[frame[k]] = object_id
                id2object[object_id] = frame[k]
                all_ob.add(frame[k])
                object_id+=1
            o_id += 1
        for rel in verb2rels[verb]:
            # print(frame)
            if rel[0] not in frame or rel[-1] not in frame:
                continue
            if frame[rel[0]] not in ob2id or frame[rel[-1]] not in ob2id:
                continue
            reg[reg_id]['relationships'].append({'relationship_id':rel_id,'subject_id':ob2id[frame[rel[0]]],'object_id':ob2id[frame[rel[-1]]],'name':rel[1]})
            rel_id+=1
        # if 'agent' in ob2id and 'victim' in ob2id:
        #     w_file[-1]['relationships'].append(
        #         {'relationship_id': rel_id, 'subject_id': ob2id['agent'], 'object_id': ob2id['victim'], 'name': verb})
        # if 'agent' in ob2id and 'place' in ob2id:
        #     w_file[-1]['relationships'].append(
        #         {'relationship_id': rel_id + 1, 'subject_id': ob2id['agent'], 'object_id': ob2id['place'],
        #          'name': "in"})
        w_file[-1]['regions'].append({str(reg_id):reg[reg_id]})
        w_file[-1]['relationships']=reg[reg_id]['relationships']
        reg_id += 1
    f = open('swig-master/regionfiles_swig/'+r.split('.')[0]+".json",'w')
    f.write(json.dumps(reg))
    f.close()
    id += 1




with open('swig-master/asg_test.json', 'w') as f:
    json.dump(w_file, f, indent=4)

# with open('swig-master/img2id.json','w') as f:
#     f.write(json.dumps(img2id))
# with open('swig-master/id2img.json','w') as f:
#     f.write(json.dumps(id2img))
# with open('swig-master/object2id.json', 'w') as f:
#     f.write(json.dumps(object2id))
# with open('swig-master/id2object.json', 'w') as f:
#     f.write(json.dumps(id2object))