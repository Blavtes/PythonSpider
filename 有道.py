# -*- coding: utf-8 -*-
import string
import unicodedata

import requests, time, random
from hashlib import md5
from Crypto.Cipher import AES
from Crypto.Hash import MD5
import base64,json
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import json
from typing import ByteString

import chardet

class YDSpider():
    def __init__(self):
        self.post_url = 'https://dict.youdao.com/webtranslate'
        self.headers={
            "Accept": "application/json, text/plain, */*",
            # "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Length": "261",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": "OUTFOX_SEARCH_USER_ID_NCOO=1607124104.045135; OUTFOX_SEARCH_USER_ID=-1850731602@116.25.40.13",
            "Host": "dict.youdao.com",
            "Origin": "https//fanyi.youdao.com",
            "Referer": "https://fanyi.youdao.com/",
            "sec-ch-ua": "Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            # "Sec-Fetch-Dest": "empty",
            # "Sec-Fetch-Mode": "cors",
            # "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        }



    def get_ts_salt_sign_bv(self,world):
        ts = str(int(time.time()*1000))
        salt = ts+str(random.randint(0,9))
        # "client=fanyideskweb&mysticTime=1679620705343&product=webfanyi&key=fsdsogkndfokasodnaso"
        string = 'client=fanyideskweb&mysticTime={}&product=webfanyi&key=fsdsogkndfokasodnaso'.format(ts)
        # string = "fsdsogkndfokasodnaso" + world + salt + "Ygy_4c=r#e#4EX^NUGUc5"
        s = md5()
        s.update(string.encode())
        sign = s.hexdigest()
        #bv
        s.update('5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'.encode())
        bv = s.hexdigest()
        return ts,salt,sign,bv
    def attack_yd(self,world):
        #1.参数
        ts, salt, sign, bv = self.get_ts_salt_sign_bv(world)
        data = {
            "i": world,
            "from": "auto",
            "to": "",
            "domain": "0",
            "dictResult": "true",
            "keyid": "webfanyi",
            "sign": sign,
            "client": "fanyideskweb",
            "product": "webfanyi",
            "appVersion": "1.0.0",
            "vendor": "web",
            "pointParam": "client,mysticTime,product",
            "mysticTime": ts,
            "keyfrom": "fanyi.web",
        }
        #2 拼接数据
        res = requests.post(
            url = self.post_url,
            data = data,
            headers = self.headers
        )
        html = res.text
        return html
    def parse_result(self,src):
        keys = b'ydsecret://query/key/B*RGygVywfNBwpmBaZg*WT7SIOUP2T0C9WHMZN39j^DAdaZhAnxvGcCY6VYFwnHl'
        # s = md5()
        # s.update(keys)
        # key1 = s.digest()[0:16]
        # 这里使用的16个1作为iv,亦可动态生成可变iv
        key = MD5.new(keys).digest()[:16]
        ivs = b'ydsecret://query/iv/C@lZe2YzHtZ2CYgaXKSVfsb7Y4QWHjITPPZ0nQp87fBeJ!Iv6v^6fvi2WN@bYpJ4'
        # s = md5()
        # s.update(ivs)
        # iv1 = s.digest()[0:16]
        iv = MD5.new(ivs).digest()[:16]
        # a = ByteString([8,20,157,167,60,89,206,98,85,91,1,233,47,52,232,56])
        # b = ByteString([210,187,27,253,232,59,56,195,68,54,99,87, 183,156,174,28])
        # print('==' ,key1, iv1)
        print("key=>",key, iv)
        print(list(key),MD5.new(ivs).digest())
        print(type(list(key)), type(list(iv)))
        print(src)
        decrypter = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)

        plaintext=decrypter.decrypt(base64.urlsafe_b64decode(src)).decode('utf-8')
        print(plaintext)
        print(type(plaintext))
        plaintext_by =json.loads(plaintext[: plaintext.rindex("}") + 1])
        print(plaintext_by)
        print(type(plaintext_by))
        # plaintext = r'\xde9\x8d\x8e\x03j\xeec\x95\xbc\xba\xc8\xe2\x81UY\x96\xc1\xd9\x1c;'
        print(plaintext_by['translateResult'][0][0]['tgt'])


    def run(self):
        word = input("单词")
        if word != "" :
           self.parse_result(self.attack_yd(word))
if __name__ == "__main__":
    spider = YDSpider()
    spider.run()


