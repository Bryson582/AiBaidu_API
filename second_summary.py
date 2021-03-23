import urllib
import json
import sys
import pandas as pd
import time


# make it work in both python2 both python3
IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.parse import quote_plus
else:
    import urllib2
    from urllib import quote_plus
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode


# skip https auth
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
API_KEY = '3AxdYY1nBtKlafUAku5QG0O8'

SECRET_KEY = 'KxG0SSgzX2LeCnuUmId9eBhDMrPzk2U5'

"""  TOKEN start """
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'

"""
    get token
"""
def get_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    while 1:
        try:
            f = urlopen(req, timeout=5)
            result_str2 = f.read()
            break
        except URLError as err:
            print(err)
            time.sleep(0.1)
            continue

    if (IS_PY3):
        result_str2 = result_str2.decode()


    result = json.loads(result_str2)

    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not 'brain_all_scope' in result['scope'].split(' '):
            print ('please ensure has check the  ability')
            exit()
        return result['access_token']
    else:
        print ('please overwrite the correct API_KEY and SECRET_KEY')
        exit()



"""
    该项封装的函数调用百度AI接口 url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/news_summary'
"""

def summary(list1,list2,max_summary_len):
    ss_list = [list1,list2]
    ss_sublist1 = []
    for i in range(0,len(list1)):
        if pd.isna(ss_list[0][i]) or pd.isna(ss_list[1][i]):
            print("该项内容由于参数不足 无法调用我们的接口 所以我们给摘要插入***")
            # with open("./result.csv", "a+") as csvfile:
            #     writer = csv.writer(csvfile)
            #     writer.writerow([theme,title,content,sentiment,data['confidence'],content])
                # 该情况下摘要直接保留内容项，我们可以得到倾向 但标签和权重都为空值
            ss_sublist1.append("***")
        else:
            token = get_token()
            urla = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/news_summary'
            params = dict()
            params['title'] = ss_list[0][i]
            params['content'] = ss_list[1][i]
            params['max_summary_len'] = max_summary_len
            params = json.dumps(params).encode('utf-8')
            access_token = token
            urla = urla + "?access_token=" + access_token
            while 1:
                try:
                    request = urllib.request.Request(url=urla, data=params)
                    request.add_header('Content-Type', 'application/json')
                    response = urllib.request.urlopen(request, timeout=10)
                    content2 = response.read()
                    content2 = content2.decode('gb18030')
                    try:
                        data = json.loads(content2)
                        summary = data['summary']
                        print('Summary：', summary)
                        ss_sublist1.append(summary)
                        break
                    except Exception as e:
                        print("该项内容接口无法识别，我们想列表中插入+++")
                        ss_sublist1.append("+++")
                        break
                except urllib.error.URLError as e1:
                    print('Time Out', e1)
                    time.sleep(0.5)
                    continue
    return ss_sublist1