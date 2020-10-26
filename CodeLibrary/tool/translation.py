# -*- coding: utf-8 -*-
import re
import json
import execjs
import requests
from fake_useragent import UserAgent

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
