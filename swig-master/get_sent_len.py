import json
import matplotlib.pyplot as plt
import scipy.signal
datas = json.load(open('pred.json','r',encoding='utf-8'))

sents = datas.values()
lens = [len(sent[0]) for sent in sents]

lens.sort(reverse=True)


tmp = scipy.signal.savgol_filter(lens, 25, 3)

ss = [i for i in range(len(sents))]
plt.xlabel("sentence", fontsize=12)
plt.ylabel("length", fontsize=12)
plt.plot(ss,tmp,linewidth=4)
plt.show()

