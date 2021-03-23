import pandas as pd
import main as mn
import json
import urllib
import time
import sys

from aip import AipNlp

""" 你的 APPID AK SK """
APP_ID = '你的 App ID'
API_KEY = '3AxdYY1nBtKlafUAku5QG0O8'
SECRET_KEY = 'KxG0SSgzX2LeCnuUmId9eBhDMrPzk2U5'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

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
            result_str1 = f.read()
            break
        except URLError as err:
            print(err)
            time.sleep(0.1)
            continue
    if (IS_PY3):
        result_str1 = result_str1.decode()


    result = json.loads(result_str1)

    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not 'brain_all_scope' in result['scope'].split(' '):
            print ('please ensure has check the  ability')
            exit()
        return result['access_token']
    else:
        print ('please overwrite the correct API_KEY and SECRET_KEY')
        exit()



"""
    该项封装的函数调用百度AI接口 url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify'
"""


def get_classify(list2):
    #(1)情绪判断以及置信区间
    fs_sublist1 = []
    fs_sublist2 = []
    for content in list2:
        if content:
            token = get_token()
            url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify'
            params = dict()
            params['text'] = content
            params = json.dumps(params).encode('utf-8')
            access_token = token
            url = url + "?access_token=" + access_token
            while 1:
                try:
                    request = urllib.request.Request(url=url, data=params)
                    request.add_header('Content-Type', 'application/json')
                    response = urllib.request.urlopen(request, timeout=10)
                    content1 = response.read()
                    content1 = content1.decode('gb18030')
                    try:
                        data = json.loads(content1)
                        data = data['items'][0]
                        sentiment = data['sentiment']
                        if sentiment == 0:
                            sentiment = '消极'
                        elif sentiment == 1:
                            sentiment = '中性'
                        else:
                            sentiment = '积极'
                            print(data['confidence'])
                            confid = data['confidence']
                        fs_sublist1.append(sentiment)
                        fs_sublist2.append(confid)
                        break
                    except Exception as e:
                        print("该项内容为空，我们想列表中插入+++")
                        fs_sublist1.append("+++")
                        fs_sublist2.append("+++")
                        break
                except urllib.error.URLError as e1:
                    print('Time Out', e1)
                    # 停用1s 再次尝试连接
                    time.sleep(0.5)
                    continue
        else:
            print("该项内容为空 我们这里直接把给列表插入***代表该项为空")
            fs_sublist1.append("***")
            fs_sublist2.append("***")
    fs_sublist = [fs_sublist1,fs_sublist2]
    return fs_sublist