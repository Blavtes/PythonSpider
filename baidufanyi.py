import execjs,requests,re
from fake_useragent import UserAgent
# with open('sign_baidu.js','r',encoding='utf-8') as f:
#     js_data = f.read()
# exex_object = execjs.compile(js_data)
# sign = exex_object.eval('mycode("大象")')
# print(sign)
# # 'https://fanyi.baidu.com/v2transapi?from=zh&to=en'
# token= '621972bc558ed98aa4cc37bda6e652d3'
#
# 加密破解
class BaiduFanyiSpider():
    def __init__(self):
        self.token_url = 'https://fanyi.baidu.com/?aldtype=16047'
        self.post_url = 'https://fanyi.baidu.com/v2transapi'
        ua = UserAgent()
        self.token_headers = {
            'User-Agent':ua.random,
            # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            # "Accept-Encoding": "gzip, deflate, br",
            # "Accept-Language": "zh-CN,zh;q=0.9",
            # "Cache-Control": "max-age=0",
            # "Connection": "keep-alive",
            "Cookie": "PSTM=1667010964; BAIDUID=D37BD4B07476DD1C1E46D6AE7717EC37:FG=1; BIDUPSID=EBAD30B7E1845312C86CEAC7D2A635E8; MCITY=-%3A; H_WISE_SIDS=219946_231979_219623_236811_234020_239116_238412_240447_216841_213349_229967_214797_235966_219943_213043_234780_230186_204903_230288_239491_241962_242024_242037_242082_242222_242157_242312_242489_242753_242545_238267_110085_243450_227870_236307_243828_243842_243704_243880_244036_243763_244284_244311_244008_244554_232628_244729_240595_244957_245003_242382_239851_243207_245082_241737_245272_245262_244445_244966_245411_245474_245489_245511_245502_245509_245658_224267_245763_245772_245870_246046_245700_245817_246315_246436_246477_242682_243821_246176_234296_234208_246584_245895_246613_243424_107314_246661_246865_246876_247081_247130_246585_246288; H_WISE_SIDS_BFESS=219946_231979_219623_236811_234020_239116_238412_240447_216841_213349_229967_214797_235966_219943_213043_234780_230186_204903_230288_239491_241962_242024_242037_242082_242222_242157_242312_242489_242753_242545_238267_110085_243450_227870_236307_243828_243842_243704_243880_244036_243763_244284_244311_244008_244554_232628_244729_240595_244957_245003_242382_239851_243207_245082_241737_245272_245262_244445_244966_245411_245474_245489_245511_245502_245509_245658_224267_245763_245772_245870_246046_245700_245817_246315_246436_246477_242682_243821_246176_234296_234208_246584_245895_246613_243424_107314_246661_246865_246876_247081_247130_246585_246288; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=36552_38470_38368_38404_38468_38289_36802_37926_38382_26350_38419_37881; BAIDUID_BFESS=D37BD4B07476DD1C1E46D6AE7717EC37:FG=1; PSINO=7; delPer=0; BA_HECTOR=2h2g2l8la5000l24a1218g8m1i2aa991n; ZFY=AuSv419:Bi191pC1LHQyXg1dUAKzixuf974DoEx1EE3U:C; APPGUIDE_10_0_2=1; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1680156974; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1680165476; ab_sr=1.0.1_NTQ1YjRjNGNhNTJlYTU5MWMyNWRjZGQ2NWQyMDE1NTgzNjcyYTllODU4NDQwNzRiYjlkOTlhYjVjYTI0ZTBmZTM0MmNkZDlhNzllODk2MmViOGQyNDY5ODc3ZDU0NmJjYWI1MTYyNDlmOWZkNDRmOTFhOTM1NGM0OWVjM2FkNjVlM2Y0NWY1ZTA2NThjOGI2YmY1MTEzYTc2OTA4NjM2Mw==",
            # "Host": "fanyi.baidu.com",
            # "sec-ch-ua": "\"Google Chrome\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
            # "sec-ch-ua-mobile": "?0",
            # "sec-ch-ua-platform": "\"macOS\"",
            # "Sec-Fetch-Dest": "document",
            # "Sec-Fetch-Mode": "navigate",
            # "Sec-Fetch-Site": "same-origin",
            # "Sec-Fetch-User": "?1",
            # "Upgrade-Insecure-Requests": "1",
        }
        self.fanyi_headers = {
            # "Accept": "*/*",
            # "Accept-Encoding": "gzip, deflate, br",
            # "Accept-Language": "zh-CN,zh;q=0.9",
            # "Acs-Token": "1680166684097_1680166828374_XGRmsNMvKhnvU3VEb2OGcXxt5qKabMbmJQ/wqbdxOqbb1UORTNgiHGroXfe8vs2aq5ZmzZZN9Lz6fjBqujICb2XNUie2oOcrU1fwhwYjaDqDYRwxZTK5AiIfyn88Z83PwBljfr0USnEZp+oGSOvS2WMBRBk8lW8tl2qjPd7R0OAK729bcZysb+EzDA0Ts00wkvN7FNQmG1cm3Aiawc3Ylxr9WGTOhS0umTjQTAUP4tKDAn9E26JoRLXk9NlYKnE1ndsFtrOhkIuvrwnIaPkOwokiQ1dXuUcSKlXNWMXm2VZYfPMiKklloU5ZsG1GbkBRFjS6biqg6SMYCUXuAEtTUaWR7YeE/osuR4uE55Lzp04sGyhBeh6YrlaeBMpAG4ntto0HPFKOwa+avd4hpGLo0k03E2iVZYKODZRBgi0NW2z/zrGwZbr0GmXYYiWaJoqd/m7cIQWb2F8jDLfF7rkV/+l6tq6ew8dlcC3uu+CrdyH6I1CUfv/XnEGdeuMOrx3w",
            # "Connection": "keep-alive",
            # "Content-Length": "140",
            # "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "PSTM=1667010964; BAIDUID=D37BD4B07476DD1C1E46D6AE7717EC37:FG=1; BIDUPSID=EBAD30B7E1845312C86CEAC7D2A635E8; MCITY=-%3A; H_WISE_SIDS=219946_231979_219623_236811_234020_239116_238412_240447_216841_213349_229967_214797_235966_219943_213043_234780_230186_204903_230288_239491_241962_242024_242037_242082_242222_242157_242312_242489_242753_242545_238267_110085_243450_227870_236307_243828_243842_243704_243880_244036_243763_244284_244311_244008_244554_232628_244729_240595_244957_245003_242382_239851_243207_245082_241737_245272_245262_244445_244966_245411_245474_245489_245511_245502_245509_245658_224267_245763_245772_245870_246046_245700_245817_246315_246436_246477_242682_243821_246176_234296_234208_246584_245895_246613_243424_107314_246661_246865_246876_247081_247130_246585_246288; H_WISE_SIDS_BFESS=219946_231979_219623_236811_234020_239116_238412_240447_216841_213349_229967_214797_235966_219943_213043_234780_230186_204903_230288_239491_241962_242024_242037_242082_242222_242157_242312_242489_242753_242545_238267_110085_243450_227870_236307_243828_243842_243704_243880_244036_243763_244284_244311_244008_244554_232628_244729_240595_244957_245003_242382_239851_243207_245082_241737_245272_245262_244445_244966_245411_245474_245489_245511_245502_245509_245658_224267_245763_245772_245870_246046_245700_245817_246315_246436_246477_242682_243821_246176_234296_234208_246584_245895_246613_243424_107314_246661_246865_246876_247081_247130_246585_246288; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=36552_38470_38368_38404_38468_38289_36802_37926_38382_26350_38419_37881; BAIDUID_BFESS=D37BD4B07476DD1C1E46D6AE7717EC37:FG=1; PSINO=7; delPer=0; BA_HECTOR=2h2g2l8la5000l24a1218g8m1i2aa991n; ZFY=AuSv419:Bi191pC1LHQyXg1dUAKzixuf974DoEx1EE3U:C; APPGUIDE_10_0_2=1; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1680156974; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1680166083; ab_sr=1.0.1_ODkwN2U1YTFlMDczOTIxYjFjYmU0MzUwOWI0MTQ2MjZiNGI0MDI0ZjNmYTM0MTEzODI1NTNmNmQ2ZWVjZTQ1MGRjM2NhNWUzYjdlMDI4ZGM1N2ZmMDkyZTdhMjQzOTlkODg3YTRkZjdhYjE2YTQxOWE4MWMwYTA2YWE1YzQxOTU2OTAyZjM0ODhmNzJhMDFhMGU0YzQ5MWFmNDA2Y2Q1ZQ==",
            # "Host": "fanyi.baidu.com",
            # "Origin": "https://fanyi.baidu.com",
            # "Referer": "https://fanyi.baidu.com/?aldtype=16047",
            # "sec-ch-ua": "\"Google Chrome\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
            #  "sec-ch-ua-mobile": "?0",
            # "sec-ch-ua-platform": "\"macOS\"",
            # "Sec-Fetch-Dest": "empty",
            # "Sec-Fetch-Mode": "cors",
            # "Sec-Fetch-Site": "same-origin",
            'User-Agent': ua.random,
            # "X-Requested-With": "XMLHttpRequest",
        }

    def get_token(self):

        r = requests.get(url=self.token_url,headers=self.token_headers)
        r.encoding = 'utf-8'
        token = re.findall(r"token: '(.*?)'",r.text)
        # token = '621972bc558ed98aa4cc37bda6e652d3'
        gtk = re.findall(r'window.gtk = "(.*?)";',r.text)
        print(token,gtk)
        if token:
            return token[0],gtk[0]
    # get sign
    def get_sign(self,word,gtk):
        with open('sign_baidu.js','r',encoding='utf-8') as f:
            js_data = f.read()
        exec_data = execjs.compile(js_data)
        sign = exec_data.eval('mycode("{}","{}")'.format(word,gtk))
        return sign
    def run(self,word,fro,to):
        token,gtk = self.get_token()
        sign = self.get_sign(word,gtk)
        print(sign,token)
        # 拼接from
        form_data = {
            "from": fro,
            "to": to,
            "query": word,
            "transtype": "enter",
            "simple_means_flag": "3",
            "sign": sign,
            "token": token,
            "domain": "common",
        }
        r = requests.post(url=self.post_url,data=form_data,headers=self.fanyi_headers).json()
        print(r['trans_result']['data'][0]['dst'])

if __name__ == "__main__":
    baidu = BaiduFanyiSpider()
    baidu.run('人才','zh','en')
