import urllib
import json
import main as mn
import time
import sys



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
            result_str3 = f.read()
            break
        except URLError as err:
            print(err)
            time.sleep(0.1)
            continue
    if (IS_PY3):
        result_str3 = result_str3.decode()


    result = json.loads(result_str3)

    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not 'brain_all_scope' in result['scope'].split(' '):
            print ('please ensure has check the  ability')
            exit()
        return result['access_token']
    else:
        print ('please overwrite the correct API_KEY and SECRET_KEY')
        exit()


"""
    该项封装的函数调用百度AI接口 url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/keyword'
"""

def tag(list1,list2):
    tt_list = [list1, list2]

    tt_sublist1 = []
    tt_sublist2 = []
    for i in range(0, len(list1)):
        # print(tt_list[1][i])
        # time.sleep(1)
        token = get_token()
        urlb = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/keyword'
        params1 = dict()
        params1['title'] = tt_list[0][i][:40]
        params1['content'] = tt_list[1][i]
        params1 = json.dumps(params1).encode('utf-8')
        access_token = token
        urlb = urlb + "?access_token=" + access_token
        for k in range(0,10):
            try:
                request = urllib.request.Request(url=urlb, data=params1)
                request.add_header('Content-Type', 'application/json')
                response = urllib.request.urlopen(request, timeout=10)
                content3 = response.read()
                content3 = content3.decode('gb18030')
                tag = json.loads(content3)
                print(tag)
                try:
                    tag['items']
                    item = tag['items']
                    a = []
                    b = []
                    # 我们这里需要将标签和权重进行拆分
                    for k in item:
                        a.append(k['tag'])
                        b.append(k['score'])
                    str1 = "".join(str(a))
                    str2 = "".join(str(b))
                    tt_sublist1.append(str1)
                    tt_sublist2.append(str2)
                    break
                except Exception as e:
                    print("该项内容为空，我们想列表中插入+++")
                    tt_sublist1.append("+++")
                    tt_sublist2.append("+++")
                    break
            except urllib.error.URLError as e1:
                print('Time Out', e1)
                time.sleep(0.5)
                continue
    tt_sublist = [tt_sublist1,tt_sublist2]
    print(tt_sublist)
    return tt_sublist



