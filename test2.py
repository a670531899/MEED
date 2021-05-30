import os
import json
import numpy as np

datas = json.load(open('swig-master/asg_test.json','r',encoding='utf-8'))

int2word = list(np.load('int2word.npy'))
word2int = json.load(open('word2int.json','r',encoding='utf-8'))
id = len(int2word)

for data in datas:
    for reg in data['regions']:
        for k in reg:
            region = reg[k]
            objects = region['objects']
            relations = region['relationships']
            for object in objects:
                name = object['name']
                if name not in int2word:
                    id +=1
                    int2word.append(name)
                    word2int[name]=id+1
            for object in relations:
                name = object['name']
                if name not in int2word:
                    id += 1
                    int2word.append(name)
                    word2int[name] = id + 1


np.save('swig-master/int2word.npy',int2word)
json.dump(word2int,open('swig-master/word2int.json','w',encoding='utf-8'))


