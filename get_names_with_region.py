import json
import numpy as np
all_datas = json.load(open('swig-master/asg_test.json','r',encoding='utf-8'))
all_regs = []
img2id = {}
id2img = {}
inf_names = np.load('swig-master/inf_names.npy')
image_id = 0
for image in inf_names:
    # print(image)
    img2id[image] = image_id
    id2img[image_id] = image
    image_id+=1
for data in all_datas:
    for reg in data['regions']:
        for k in reg:
            all_regs.append([id2img[int(data['image_id'])].split('.')[0],k])
print(all_regs)
np.save('swig-master/inf_names_reg.npy',all_regs)

