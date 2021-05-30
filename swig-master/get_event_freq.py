import json
import matplotlib.pyplot as plt
datas = json.load(open('asg_test.json','r',encoding='utf-8'))

id2img = json.load(open('id2img.json','r',encoding='utf-8'))
e2freq = {}

for data in datas:
    id = data['image_id']
    img = id2img[id]
    verb = img.split('_')[0]
    if verb not in e2freq:
        e2freq[verb] = 1
    else:
        e2freq[verb] += 1


verb2event = json.load(open('../../../datas/m2e2/verb2event.json','r',encoding='utf-8'))

event2feq = {}

for data in datas:
    verb = id2img[data['image_id']].split('_')[0]
    event = verb2event[verb]
    if event not in event2feq:
        event2feq[event]=1
    else:
        event2feq[event]+=1

e2f = sorted(event2feq.items(),key = lambda x:x[1],reverse=True)


events = [i for i in range(66)]
freq = [e[1] for e in e2f]
plt.xlabel("event types", fontsize=12)
plt.ylabel("frequency", fontsize=12)
plt.plot(events,freq,linewidth=4)
plt.show()


