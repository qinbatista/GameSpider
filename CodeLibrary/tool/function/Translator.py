# -*- coding: utf-8 -*- 
import urllib.request
import random, execjs, requests
import json, hashlib, time
import xml.dom.minidom
# import unicodedata
import os

pyjs = """// a:你要翻译的内容
// uq:tkk的值
function vq(a,uq='422388.3876711001') {
    if (null !== uq)
        var b = uq;
    else {
        b = sq('T');
        var c = sq('K');
        b = [b(), c()];
        b = (uq = window[b.join(c())] || "") || "";
    }
    var d = sq('t');
    c = sq('k');
    d = [d(), c()];
    c = "&" + d.join("") + "=";
    d = b.split(".");
    b = Number(d[0]) || 0;
    for (var e = [], f = 0, g = 0; g < a.length; g++) {
        var l = a.charCodeAt(g);
        128 > l ? e[f++] = l : (2048 > l ? e[f++] = l >> 6 | 192 : (55296 == (l & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (l = 65536 + ((l & 1023) << 10) + (a.charCodeAt(++g) & 1023),
        e[f++] = l >> 18 | 240,
        e[f++] = l >> 12 & 63 | 128) : e[f++] = l >> 12 | 224,
        e[f++] = l >> 6 & 63 | 128),
        e[f++] = l & 63 | 128)
    }
    a = b;
    for (f = 0; f < e.length; f++)
        a += e[f],
        a = tq(a, "+-a^+6");
    a = tq(a, "+-3^+b+-f");
    a ^= Number(d[1]) || 0;
    0 > a && (a = (a & 2147483647) + 2147483648);
    a %= 1000000;
    return c + (a.toString() + "." + (a ^ b))
};

/*--------------------------------------------------------------------------------
参数：a 为你要翻译的原文
其他外部函数：
--------------------------------------------------------------------------------*/
function sq(a) {
    return function() {
        return a
    }
}
function tq(a, b) {
    for (var c = 0; c < b.length - 2; c += 3) {
        var d = b.charAt(c + 2);
        d = "a" <= d ? d.charCodeAt(0) - 87 : Number(d);
        d = "+" == b.charAt(c + 1) ? a >>> d : a << d;
        a = "+" == b.charAt(c) ? a + d & 4294967295 : a ^ d
    }
    return a
}"""
GoogleTkk = ''
Googleexejs = ''
Language_dict = {
    '中文': {'Google': 'zh-CN', 'Bing': 'zh-CHS', 'Youdao': 'zh-CHS'},
    '英语': {'Google': 'en', 'Bing': 'en', 'Youdao': 'en'},
    '俄语': {'Google': 'ru', 'Bing': 'ru', 'Youdao': 'ru'},
    '日语': {'Google': 'ja', 'Bing': 'ja', 'Youdao': 'ja'},
    '德语': {'Google': 'de', 'Bing': 'de', 'Youdao': 'de'},
    '法语': {'Google': 'fr', 'Bing': 'fr', 'Youdao': 'fr'},
    '韩语': {'Google': 'ko', 'Bing': 'ko', 'Youdao': 'ko'},
    '泰语': {'Google': 'th', 'Bing': 'th', 'Youdao': 'None'},
    '意大利语': {'Google': 'it', 'Bing': 'it', 'Youdao': 'None'},
}

UA_List_PC = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "User-Agent:Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
]
UA_List_Mobile = [
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "JUC (Linux; U; 2.3.7; zh-cn; MB200; 320*480) UCWEB7.9.3.103/139/999",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0a1) Gecko/20110623 Firefox/7.0a1 Fennec/7.0a1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/1A542a Safari/419.3",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A403 Safari/8536.25",
    "Mozilla/5.0 (iPad; CPU OS 5_0_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A405 Safari/7534.48.3",
]


def ListFolder(path):
    List = []
    for i in os.listdir(path):
        List.append(i)
    return List


def urlrequest():
    wd = {"q": "覃于澎"}
    print("http://www.bing.com/search?" + urllib.parse.urlencode(wd))
    html = ReadPage("http://www.bing.com/search?" + urllib.parse.urlencode(wd))
    WritePage(html, "abc")


def ReadPage(url):
    UseAgent = random.choice(UA_List_PC)
    my_headers = {"User-Agent": UseAgent}
    request = urllib.request.Request(url, headers=my_headers)
    print("正在读取网页")
    html = urllib.request.urlopen(request).read()
    print("读取网页完毕")
    # print(html.decode('utf-8'))
    return html


def WritePage(html, filename):
    print("正在下载网页")
    with open(filename, "wb+") as f:
        f.write(html)
    print("下载网页完毕")


def YoudaoTranslate(key):
    url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
    TranslateWord = key
    FormateData = {
        "i": TranslateWord,
        "from": "zh-CHS",
        "to": "to=en",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": "1525787891750",
        "sign": "2d8c81cf37929314d1bd5cd13a87c79c",
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_CLICKBUTTION",
        "typoResult": "false"
    }
    my_datas = urllib.parse.urlencode(FormateData).encode(encoding='UTF8')
    my_headers = {
        "Accept-Language": "zh-Hans-CN,zh-Hans;q=0.7,ja;q=0.3",
        "User-Agent": random.choice(UA_List_PC),
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Length": len(my_datas),
        "Host": "fanyi.youdao.com",
        "Connection": "Keep-Alive",
        "Pragma": "no-cache",
    }
    request = urllib.request.Request(url, data=my_datas, headers=my_headers)
    text = urllib.request.urlopen(request).read()
    target = json.loads(text.decode("UTF-8"))
    results = target['translateResult'][0][0]['tgt']
    return results


def BingTranslate(key):
    FormateData = {
        "q": key,
        "qs": "n",
        "form": "Z9LH5",
        "sp": "-1",
        "pq": key,
        "sc": "8-1",
        "sk": "",
        "cvid": "0FB337345A9443FABC342D4F520C1138"
    }
    my_datas = urllib.parse.urlencode(FormateData)

    url = "https://cn.bing.com/dict/search" + "?" + my_datas
    my_datas = urllib.parse.urlencode(FormateData).encode(encoding='UTF8')
    # my_datas = urllib.parse.urlencode(FormateData).encode(encoding='UTF8')
    my_headers = {
        "User-Agent": random.choice(UA_List_PC),
    }
    request = urllib.request.Request(url, headers=my_headers)
    text = urllib.request.urlopen(request).read()
    findText = text.decode("UTF-8")
    # print(text.decode("UTF-8"))
    findText = findText[findText.find("必应词典为您提供" + key + "的释义，") + len("必应词典为您提供" + key + "的释义，"):]
    findText = findText[:findText.find(" /><meta") - 1]
    # print(text.decode("UTF-8"))
    return findText


def is_english_char(ch):
    if ord(ch) not in (97, 122) and ord(ch) not in (65, 90):
        return False
    return True


def is_chinese(text):
    hz_yes = False
    for ch in text:
        if isinstance(ch, str):
            if unicodedata.east_asian_width(ch) != 'Na':
                hz_yes = True
                break
        else:
            continue
    return hz_yes


def BingTranslateContext(key, Myfrom="zh-CHS", Myto="en"):
    url = "https://cn.bing.com/ttranslationlookup?&IG=3EF2174489CC4319A90ECF75C534ABCB&IID=translator.5035.6"
    FormateData = {
        "text": key,
        "from": Myfrom,
        "to": Myto
    }
    my_datas = urllib.parse.urlencode(FormateData).encode(encoding='UTF8')
    my_headers = {
        "Accept": "*/*",
        "Origin": "https://cn.bing.com",
        "Referer": "https://cn.bing.com/",
        "Accept-Language": "zh-Hans-CN,zh-Hans;q=0.7,ja;q=0.3",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
        "Content-type": "application/x-www-form-urlencoded",
        "Host": "cn.bing.com",
        "Connection": "Keep-Alive",
        "Cache-Control": "no-cache"
    }
    request = urllib.request.Request(url, data=my_datas, headers=my_headers)
    n = False
    while not n:
        try:
            urllib.request.urlopen(request, timeout=20).read()
            n = True
        except:
            print('Bing超时，重新访问！', n)
    url = "https://cn.bing.com/ttranslate?&category=&IG=3EF2174489CC4319A90ECF75C534ABCB&IID=translator.5035.8"
    my_datas = urllib.parse.urlencode(FormateData).encode(encoding='UTF8')
    my_headers = {
        "Accept": "*/*",
        "Origin": "https://cn.bing.com",
        "Referer": "https://cn.bing.com/",
        "Accept-Language": "zh-Hans-CN,zh-Hans;q=0.7,ja;q=0.3",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
        "Content-type": "application/x-www-form-urlencoded",
        "Host": "cn.bing.com",
        "Connection": "Keep-Alive",
        "Cache-Control": "no-cache"
    }
    request = urllib.request.Request(url, data=my_datas, headers=my_headers)
    text = None
    n = False
    while not n:
        try:
            text = urllib.request.urlopen(request, timeout=20).read()
            n = True
        except:
            print('Bing超时，重新访问！', n)
    target = json.loads(text.decode("UTF-8"))
    results = target['translationResponse']
    print(key + "->" + results)
    return results


def GoogleTranslateContext(key, Myfrom='zh-CN', Myto='en'):  # google翻译
    global Googleexejs
    global GoogleTkk
    session = requests.Session()
    if GoogleTkk == '':
        Googleexejs = execjs.compile(pyjs)
        url = 'https://translate.google.cn/'
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
            'upgrade-insecure-requests': '1',
        }
        response = session.get(url=url, headers=header, timeout=30)
        n = False
        while not n:
            try:
                response = session.get(url=url, headers=header, timeout=30)
                n = True
            except:
                print('Google超时，重新访问！', n)
        rs = str(response.text)[response.text.find('tkk:'):response.text.find('tkk:') + 40]
        GoogleTkk = rs[rs.find("'") + 1:rs.rfind("'")]
    header2 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Host': 'translate.google.cn',
    }
    tk = Googleexejs.call('vq', key, GoogleTkk)
    url2 = 'https://translate.google.cn/translate_a/single?client=webapp&sl=auto&hl=' + Myfrom + '&tl=' + Myto + '&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&dt=gt&otf=1&ssel=0&tsel=3&kc=1&q=' + key + tk
    response = None
    n = False
    while not n:
        try:
            response = session.post(url=url2, headers=header2, timeout=20)
            n = True
        except:
            print('Google超时，重新访问！', n)
    results = json.loads(response.text)
    results = results[0][0][0]
    print(key + "->" + results)
    return results


def YoudaoTranslateContext(key, Myfrom='zh-CNS', Myto='zh-CNS'):  # 有道翻译
    session = requests.Session()
    UA = "5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"
    url1 = "http://fanyi.youdao.com/"
    header1 = {
        'Host': 'fanyi.youdao.com',
        'User-Agent': UA,
    }
    session.get(url=url1, headers=header1)
    url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
    salt = str(int(time.time() * 10000))
    header = {
        'Host': 'fanyi.youdao.com',
        'Origin': 'http://fanyi.youdao.com',
        'Referer': 'http://fanyi.youdao.com/',
        'User-Agent': UA,
    }
    bv = hashlib.md5(UA.encode('utf-8')).hexdigest()
    md = hashlib.md5()
    md.update(("fanyideskweb" + key + salt + "p09@Bn{h02_BIEe]$P^nG").encode('utf-8'))
    sign = md.hexdigest()
    data = {
        'i': key,
        'from': Myfrom,  # 'from':'AUTO',
        'to': Myto,
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': salt,
        'sign': sign,
        'ts': salt[:len(salt) - 1],
        'bv': bv,
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTIME',
        'typoResult': 'true',
    }
    response = ''
    n = False
    while not n:
        try:
            response = session.post(url, headers=header, data=data, timeout=20)
            n = True
        except:
            print('Youdao超时，重新访问！', response.text)
    result = json.loads(response.text)
    result = result["translateResult"][0][0]["tgt"]
    print(key + "->" + result)
    return result


def PythonLocation():
    return os.path.dirname(os.path.realpath(__file__))


# XML特征
# <?xml version="1.0" encoding="UTF-8"?>
# <data>
#     <ref link="ability_damage_enemyfront_desc">
#         <string lang="en">Deals #value1# damage to the closest enemy</string>
#         <string lang="fr">Inflige #value1# de dégâts à l'ennemi le plus proche</string>
#         <string lang="it">Infligge #value1# di danno al nemico più vicino</string>
#         <string lang="de">Fügt dem Feind, der sich am wenigsten weit entfernt befindet, #value1# Schaden zu.</string>
#         <string lang="es">Provoca #value1# puntos de daños al enemigo más cercano.</string>
#         <string lang="pt">Causa #value1# de dano ao inimigo mais perto</string>
#     </ref>
# </data>
def TranslateXML(_ResourceLocation, _DesLocation, Language):
    if _ResourceLocation.find(".xml") != -1:
        print("Translate xml Started:" + _ResourceLocation)
        file_object = open(_ResourceLocation, encoding="utf8")
        Context = []
        try:
            all_the_text = file_object.readlines()
            for i in all_the_text:
                if i.find("lang=\"en\"") != -1:  # 找到需要翻译的特征符合lang="en"
                    text = i[i.find(">") + 1:i.rfind("</")]
                    TranslatedText = BingTranslateContext(text, Language)
                    TranslatedContext = i.replace(text, TranslatedText)
                    Context.append(TranslatedContext.replace("lang=\"en\"", "lang=\"zh-cn\""))  # 添加中文特征符合
                    Context.append(i)
                else:
                    Context.append(i)
        finally:
            file_object.close()
        file_object_read = open(_DesLocation, 'w', encoding="utf8")
        try:
            file_object_read.writelines(Context)
        finally:
            file_object_read.close()
    else:
        pass


def TranslateDoc(_ResourceLocation, _DesLocation, FromLanguage, ToLanguage):
    pass


def TranslateJson(_ResourceLocation, _DesLocation, FromLanguage, ToLanguage):
    if _ResourceLocation.find(".json") != -1:
        file_object = json.load(open(_ResourceLocation, 'r', encoding="utf-8"))  # 加载json
        file_object_end = file_object
        n = 2  # 改模式0，1，2
        for key in file_object.keys():
            # n = random.randint(0,9)
            n = n + 1
            if n % 3 == 0:
                file_object_end[key] = GoogleTranslateContext(file_object[key], Language_dict[FromLanguage]['Google'],
                                                              Language_dict[ToLanguage]['Google'])
            elif n % 3 == 1:
                file_object_end[key] = BingTranslateContext(file_object[key], Language_dict[FromLanguage]['Bing'],
                                                            Language_dict[ToLanguage]['Bing'])
            else:
                if Language_dict[FromLanguage]['Youdao'] != "zh-CHS" and Language_dict[ToLanguage][
                    'Youdao'] != "zh-CHS" or Language_dict[FromLanguage]['Youdao'] != "None" or \
                        Language_dict[ToLanguage]['Youdao'] != "None":
                    file_object_end[key] = GoogleTranslateContext(file_object[key],
                                                                  Language_dict[FromLanguage]['Google'],
                                                                  Language_dict[ToLanguage]['Google'])
                else:
                    file_object_end[key] = YoudaoTranslateContext(file_object[key],
                                                                  Myfrom=Language_dict[FromLanguage]['Youdao'],
                                                                  Myto=Language_dict[ToLanguage]['Youdao'])
        with open(_DesLocation, 'w', encoding='utf-8') as out:
            json.dump(file_object_end, out, ensure_ascii=False, indent=4, separators=(',', ':'))


def TranslateAllFolder(FromPath, ToPath):
    LanguageList = []
    print('可翻译语言为：', end='')
    for Language in Language_dict.keys():
        LanguageList.append(Language)
        print(' ', Language, end='')
    print()
    FromLanguage = input('请输入翻译的原语种：')
    ToLanguage = input('请输入翻译的目标语种：')
    while FromLanguage not in LanguageList:
        FromLanguage = input('原语种有错，请输入翻译的原语种：')
    while ToLanguage not in LanguageList:
        ToLanguage = input('目标语种有错，请输入翻译的目标语种：')
    myList = ListFolder(PythonLocation())
    for i in myList:
        if i.find(".") != -1:
            TranslateXML(FromPath + "/" + i, ToPath + "/" + Language_dict[ToLanguage]['Google'] + i, 'en')  # 翻译xml格式
            TranslateDoc(FromPath + "/" + i, ToPath + "/" + Language_dict[ToLanguage]['Google'] + i, FromLanguage,
                         ToLanguage)  # 翻译doc格式
            TranslateJson(FromPath + "/" + i, ToPath + "/" + Language_dict[ToLanguage]['Google'] + i, FromLanguage,
                          ToLanguage)  # 翻译json格式


def main():
    if os.path.exists(PythonLocation() + "/TranslatedFileFolder") == False:
        os.mkdir(PythonLocation() + "/TranslatedFileFolder")
    TranslateAllFolder(PythonLocation(), PythonLocation() + "/TranslatedFileFolder")


############################################################
############################################################
############################################################


from fake_useragent import UserAgent
import re

UA = UserAgent()


class Google:
    def __init__(self, timeout=30):
        self.js = """
            // a:你要翻译的内容
            // uq:tkk值
            function vq(a,uq='422388.3876711001') {
                if (null !== uq)
                    var b = uq;
                else {
                    b = sq('T');
                    var c = sq('K');
                    b = [b(), c()];
                    b = (uq = window[b.join(c())] || "") || "";
                }
                var d = sq('t');
                c = sq('k');
                d = [d(), c()];
                c = "&" + d.join("") + "=";
                d = b.split(".");
                b = Number(d[0]) || 0;
                for (var e = [], f = 0, g = 0; g < a.length; g++) {
                    var l = a.charCodeAt(g);
                    128 > l ? e[f++] = l : (2048 > l ? e[f++] = l >> 6 | 192 : (55296 == (l & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (l = 65536 + ((l & 1023) << 10) + (a.charCodeAt(++g) & 1023),
                    e[f++] = l >> 18 | 240,
                    e[f++] = l >> 12 & 63 | 128) : e[f++] = l >> 12 | 224,
                    e[f++] = l >> 6 & 63 | 128),
                    e[f++] = l & 63 | 128)
                }
                a = b;
                for (f = 0; f < e.length; f++)
                    a += e[f],
                    a = tq(a, "+-a^+6");
                a = tq(a, "+-3^+b+-f");
                a ^= Number(d[1]) || 0;
                0 > a && (a = (a & 2147483647) + 2147483648);
                a %= 1000000;
                return c + (a.toString() + "." + (a ^ b))
            };
        
            /*--------------------------------------------------------------------------------
            参数：a 为你要翻译的原文
            其他外部函数：
            --------------------------------------------------------------------------------*/
            function sq(a) {
                return function() {
                    return a
                }
            }
            function tq(a, b) {
                for (var c = 0; c < b.length - 2; c += 3) {
                    var d = b.charAt(c + 2);
                    d = "a" <= d ? d.charCodeAt(0) - 87 : Number(d);
                    d = "+" == b.charAt(c + 1) ? a >>> d : a << d;
                    a = "+" == b.charAt(c) ? a + d & 4294967295 : a ^ d
                }
                return a
            }"""
        self.exec = execjs.compile(self.js)
        self.tkk = None
        self.url = 'https://translate.google.cn/'
        self.timeout = timeout
        self.headers = {
            'User-Agent': UA.random,
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Host': 'translate.google.cn'
        }
        self.session = requests.Session()

    def register(self):
        res = self.session.get(url=self.url, headers=self.headers, timeout=self.timeout)
        content = res.content.decode(encoding='utf-8')
        self.tkk = re.search("tkk:'(.*?)'", content).groups()[0]

    def build(self, hl, tl, key):
        self.tkk or self.register()
        tk = self.exec.call('vq', key, self.tkk)
        url = f'https://translate.google.cn/translate_a/single?' \
              f'client=webapp&sl=auto&hl={hl}&tl={tl}&dt=at&dt=bd&dt=ex&' \
              f'dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&dt=gt&otf=1&' \
              f'ssel=0&tsel=3&kc=1&q={key}{tk}'
        self.headers['User-Agent'] = UA.random
        return url

    def translate(self, key, hl='zh-CN', tl='en'):
        """hl -> tl"""
        url = self.build(hl, tl, key)
        res = self.session.post(url=url, headers=self.headers, timeout=self.timeout)
        results = json.loads(res.content.decode(encoding='utf-8'))
        return results[0][0][0]


if __name__ == '__main__':
    # main()
    print(Google().translate(input('请输入需要翻译的内容：') or '你没有输入内容'))
