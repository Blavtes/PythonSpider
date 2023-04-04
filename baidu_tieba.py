import requests,random,time,os
from lxml import etree
from urllib import parse
from fake_useragent import UserAgent

# https://tieba.baidu.com/f?ie=utf-8&kw=古力娜扎&fr=search
class BaiduImageSpider():
    def __init__(self):
        self.url = 'https://tieba.baidu.com/f?ie=utf-8&kw={}&pn={}'
        self.name = ''
    def get_html(self, url):
        us = UserAgent()
        html = requests.get(
            url=url,
            headers={'User-Agent':'Mozilla/4.0 (Windows; MSIE 9.0; Windows NT 5.2);',
                    'Cookie': 'z=1&dm=baidu.com&si=66534baf-1acc-4326-adac-2a02048f2c15&ss=lfhnkbtd&sl=h&tt=hf4&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=917u&nu=mav8d0kk&cl=8z5o&ul=953h"; ab_sr=1.0.1_ZTNkYzI0MGE0YjFhMmZmNjM3MzUyYzgwN2JmNmQwYWExZWZkMzRiNGVmNjA3Yzg1Y2UxMjRmNmRlOGJiYWRkZTVmODIxNTkzNTczZDUxMzBmYTg0YWNhMzFiYmM1ZDQyYzY4N2EzZjQ3ODRlNmY4MzdmMzg4MmNhNjVlYmI0OTgzMzBmZDBmZDJkMzRmMGI2MTEyYzg1NDFjY2VlZGQ0NTNkMTYzNDUwMDI5NGQ2ZmM3ZTk4MmVlZjE1ZDJlNWZl; st_data=66ac705bf4e076fd3c0fe8447efdbc04be65400379a2c44328ff02a74d95096f5943c84194034af886c3557d64aed148bb9eba77c4852620b75b3fa37efd5dfd0c5052336daad624fc99820a4c864c828f1a8907379457e62fa53cf07d74990b; st_key_id=17; st_sign=39ae9847; USER_JUMP=-1; 146596710_FRSVideoUploadTip=1; video_bubble146596710=1; XFCS=BFAB6C73AB9747930A0F01CE98C8CA13582722C8CEC50AE566F4168D6F27C0DD; XFT=OKSShYZUAa+tiod8wdRwnbwmZcpur8CP6DdFFwBUAFg=; __bid_n=18701ce36554608dd7b8fd; XFI=23a48d60-c793-11ed-8039-83793190d5bc; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1679367028; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1679366687; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; H_PS_PSSID=38185_36554_38406_38105_38352_38308_37861_38170_38290_36802_38263_37925_38312_38383_38285_38041_26350_37958_38423_38281_37881; PSINO=6; delPer=0; arialoadData=false; BCLID=9962995294356334428; BCLID_BFESS=9962995294356334428; BDSFRCVID=OsLOJeCT5G09-d6fyj-4MeIqSmKKRwjTTPjcTR5qJ04BtyCVcmiREG0PtOG4mB8M_EGSogKK3gOTH4PF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; BDSFRCVID_BFESS=OsLOJeCT5G09-d6fyj-4MeIqSmKKRwjTTPjcTR5qJ04BtyCVcmiREG0PtOG4mB8M_EGSogKK3gOTH4PF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; FPTOKEN=QXe/40doPeIKOQkP+flN0d+d97FdoBsL7NcLqVWzjoANjidWglj2IW8crVLDJiSJneEXxn5ugfKbIAd/a7/zLmO2EC9PS0gXUdnGdVovYfa7jzjKIa1c9M9z9hDpp4UGo9W98QzbO/HvdvLCq/RsgWiSelaA7K2myOWdeOTpiCPG2Y6iorA6LgGG0Fv8NqOC/jAcxwhtzc26BW3jGosvufr9yG6S62W6kfejnnoBfbNCg5bltGlv44alZP1M40Fs9We+tWxrw3KUSH2vgwcCCUwoVXk0GUnFkHBQZRIdarfFOw04d916KOxuay/+CQ8jAYLJNBS91aCbu85Xfg3UPrldBKJk1kZXlaozdk1lBPVAOxulaKLHb5Inae73K6LItkHb77biPB9XMlSRK5Xv0Q==|ylWlaaib6kSi6cW3rPuXoSWqNPMvs0XmsRmyqVDKpNU=|10|69eddc0afb4e53b60a42eaad65ae35ed; H_BDCLCKID_SF=JnCOoI_5fCP3H48k-4QEbbQH-UnLqMvR3gOZ04n-ah02EfcOjPjdbj8XXfoAb6oMW20j0h7m3UTKsq76Wh35K5tTQP6rLtJOa2Q4KKJxbpbCh4bEQMFV2j0qhUJiB5JMBan7_UJIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbC-le50KjTcbeU5eetjK2CntsJOOaCv1hCJOy4oWK441D-QzW5bhBIIebq6HW4DaepvoD-Jc3M04K4o9-hvT-54e2p3FBUQjJb7_Qft20b0v0G5JWx3uH6KJBJ7jWhk5ep72y5OmQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8IjHCJJ6kjtJk8VIvt-5rDHJTg5DTjhPrMhtnRWMT-MTryKKJpyqAbelRN3PoYbfFLDfJiB5OMBanRh4oNB-3iV-OxDUvnyxAZ-p7yBfQxtNRJKU_-bp6U8j6wj-6obUPUDUJ9LUkJLgcdot5yBbc8eIna5hjkbfJBQttjQn3hfIkj2CKLJIDWhK_6ejA3-RJH-xQ0KnLXKKOLVMcH0h7ketn4hUt2LqIgjUjrKxjHBCTAQCjjWhk2ep72QhrKQf4WWb3ebTJr32Qr-JOyahcpsIJM5MOCDR0IQ-FLh63BaKviaKOjBMb1MMJDBT5h2M4qMxtOLR3pWDTm_q5TtUJMeCnTDMFhe6J0jaKtt5KDf5vfL5rtKRTffjrnhPF3XntTXP6-3h0t3b48sR-K5tT8KDbEbfra0PuUyn5faq3nLIQ2-U_a-lF2Mhom2fb4-Put04oxJpOJB2kJWl_yBx7psUOvbURvDP-g3-AJQU5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIE3-oJqCL5hIoP; H_BDCLCKID_SF_BFESS=JnCOoI_5fCP3H48k-4QEbbQH-UnLqMvR3gOZ04n-ah02EfcOjPjdbj8XXfoAb6oMW20j0h7m3UTKsq76Wh35K5tTQP6rLtJOa2Q4KKJxbpbCh4bEQMFV2j0qhUJiB5JMBan7_UJIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbC-le50KjTcbeU5eetjK2CntsJOOaCv1hCJOy4oWK441D-QzW5bhBIIebq6HW4DaepvoD-Jc3M04K4o9-hvT-54e2p3FBUQjJb7_Qft20b0v0G5JWx3uH6KJBJ7jWhk5ep72y5OmQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8IjHCJJ6kjtJk8VIvt-5rDHJTg5DTjhPrMhtnRWMT-MTryKKJpyqAbelRN3PoYbfFLDfJiB5OMBanRh4oNB-3iV-OxDUvnyxAZ-p7yBfQxtNRJKU_-bp6U8j6wj-6obUPUDUJ9LUkJLgcdot5yBbc8eIna5hjkbfJBQttjQn3hfIkj2CKLJIDWhK_6ejA3-RJH-xQ0KnLXKKOLVMcH0h7ketn4hUt2LqIgjUjrKxjHBCTAQCjjWhk2ep72QhrKQf4WWb3ebTJr32Qr-JOyahcpsIJM5MOCDR0IQ-FLh63BaKviaKOjBMb1MMJDBT5h2M4qMxtOLR3pWDTm_q5TtUJMeCnTDMFhe6J0jaKtt5KDf5vfL5rtKRTffjrnhPF3XntTXP6-3h0t3b48sR-K5tT8KDbEbfra0PuUyn5faq3nLIQ2-U_a-lF2Mhom2fb4-Put04oxJpOJB2kJWl_yBx7psUOvbURvDP-g3-AJQU5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIE3-oJqCL5hIoP; BAIDU_WISE_UID=wapp_1679366687103_136; STOKEN=cbc464fd36cca7c27df441c31504236b10832d226fd688d0820a4a0303f79e41; ZFY=vQtApaQ5ARV9R3Phm1CV0Lz3teYOChI4UV0enZKdOks:C; BA_HECTOR=81002ga52h840gal8k0h2lb31i1i1ei1n; MCITY=-75%3A340%3A; BDUSS=W9hNFJyejJGdnRZMG1HMEFmeWdmUElEZUQzMmloZi11MEQ5Y0VWT1RIYzZoaFprSVFBQUFBJCQAAAAAAAAAAAEAAABm47wIYmx1ZXNlYV8yMzUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADr57mM6-e5jT; H_WISE_SIDS=219946_231979_237836_236811_234020_230583_232247_219563_240397_240447_239491_240035_216844_213362_229967_214789_219943_213041_204913_241245_238073_230288_241961_242024_242083_242464_242489_242754_242542_238267_242336_243317_110085_227870_236307_243841_243706_243883_244036_244318_244009_243659_243957_234436_244712_243425_244769_244831_240590_179349_244955_245003_242379_242373_243208_245090_245183_245082_241737_245271_245262_245307_244444_244966_245403_245411_245233_245480_245520_245512_245502_245509_224436_245759_245715_245810_246045_246096_245494_245817_243827_246266_246316_246439_246491; BIDUPSID=DF68EEA95E40103239FDBBC96DA7FC78; BAIDUID=DF68EEA95E40103239FDBBC96DA7FC78:FG=1; PSTM=1661841094'
            }
        ).content.decode('utf-8','ignore')
        return html
    def parse_html(self, one_url):
        html = self.get_html(one_url)
        # 一级xpath
        xpath_dbs = '//ul/li/div[@class="t_con cleafix"]/div[2]/div/div/a/@href'
        r_list = self.xpath_func(html,xpath_dbs)
        print(r_list)
        for r in r_list:
            #拼接url
            t_url = 'https://tieba.baidu.com' + r
            #get image
            self.get_image(t_url)
            time.sleep(random.randint(1,3))
    def xpath_func(self,html,xpath_dbs):
        parse_html = etree.HTML(html)
        r_list = parse_html.xpath(xpath_dbs)
        return r_list
    def get_image(self, two_url):
        html = self.get_html(two_url)
        # 视频或图片
        xpath_dbs = '//cc/div[2]/img[@class="BDE_Image"]/@src | //div[@class="video_src_wrapper"]/embed/@data-video'
        image_list = self.xpath_func(html,xpath_dbs)
        print('image',image_list)
        us = UserAgent()
        for img in image_list:
            html_bytes = requests.get(url=img,headers={'User-Agent':us.random}).content
            self.save_image(html_bytes,img)
    def save_image(self,html_bytes,url):
        dir = self.name+'/'
        if not os.path.exists(dir):
            os.makedirs(dir)
        filename = self.name+'/'+url.split('/')[-1].split('?')[0]

        with open(filename,'wb') as f:
            f.write(html_bytes)
            print('%s下载成功'%filename)
    def run(self):
        name = input('input 输入贴吧名：')
        begin = int(input('起始页：'))
        end = int(input('结束页：'))
        self.name = name
        kw = parse.quote(name)
        for page in range(begin,end+1):
            pn = (page-1)*50
            url = self.url.format(kw,pn)
            self.parse_html(url)
if __name__ == '__main__':
    spider = BaiduImageSpider()
    spider.run()

