import json

datas  = {}

datas.update(json.load(open('swig-master/SWiG_jsons/train.json','r')))
datas.update(json.load(open('swig-master/SWiG_jsons/dev.json','r')))
datas.update(json.load(open('swig-master/SWiG_jsons/test.json','r')))

img_names = [k for k in datas]

json.dump(img_names,open('swig-master/SWiG_jsons/img_names.json','w'))


