import urllib
import json
import main as mn
import difflib
from simtext import similarity

"""
    该项封装的函数调用百度AI接口 url = "https://aip.baidubce.com/rpc/2.0/nlp/v2/simnet"
"""

def textsim(para):
    # 我们现在已经得到了根据关键词分组过的list 现在我们需要根据分割这个list
    simk = []
    simk1 = []
    tem = 0
    for j in range(0,len(para)):
        # print(j)
        point = tem
        for i in para[j][1]['内容']:
            # print(i)
            max = 0.0
            tem = tem - len(para[j][1]['内容'])
            while tem < (len(para[j][1]['内容']) + point):
                # token = mn.get_token()
                # url = "https://aip.baidubce.com/rpc/2.0/nlp/v2/simnet"
                # params = dict()
                try:
                    # params['text_2'] = i[:256]
                    # params['text_1'] = para[j][1]['内容'][tem][:256]
                    # params['model'] = "CNN"
                    # params = json.dumps(params).encode('utf-8')
                    # access_token = token
                    # url = url + "?access_token=" + access_token
                    # request = urllib.request.Request(url=url, data=params)
                    # request.add_header('Content-Type', 'application/json')
                    # response = urllib.request.urlopen(request, timeout=100)
                    # content = response.read()
                    # content = content.decode('gb18030')
                    # data = json.loads(content)
                    sim = similarity()
                    # data = sim.compute(i,para[j][1]['内容'][tem][:256])
                    data = difflib.SequenceMatcher(None,i,para[j][1]['内容'][tem][:256]).quick_ratio()
                    # print(data)
                    if data > max and data != 1.0:
                        max = data
                        flag = tem
                    tem = tem + 1
                except Exception as e:
                    tem = tem + 1
                    continue
            simk.append(max)
            simk1.append(para[j][1]['内容'][flag])
    print(len(simk))
    print(len(simk1))
    similar = [simk,simk1]
    return similar