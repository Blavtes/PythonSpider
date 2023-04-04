html="""
<li class="clear LOGVIEWDATA LOGCLICKDATA" data-lj_view_evtid="21625" data-lj_evtid="21624" data-lj_view_event="ItemExpo" data-lj_click_event="SearchClick" data-lj_action_source_type="链家_PC_二手列表页卡片" data-lj_action_click_position="0" data-lj_action_fb_expo_id='690253305246560256' data-lj_action_fb_query_id='690253305158479872' data-lj_action_resblock_id="2411062835809" data-lj_action_housedel_id="105112990747">
                    <a class="noresultRecommend img LOGCLICKDATA" href="https://sz.lianjia.com/ershoufang/105112990747.html" target="_blank" data-log_index="1" data-el="ershoufang" data-housecode="105112990747" data-is_focus="" data-sl="">
                        <!-- 热推标签、埋点 -->
                        <img src="https://s1.ljcdn.com/feroot/pc/asset/img/vr/vrlogo.png?_v=20230302112103216" class="vr_item">
                        <img class="lj-lazy" src="https://s1.ljcdn.com/feroot/pc/asset/img/blank.gif?_v=20230302112103216" data-original="https://image1.ljcdn.com/110000-inspection/7bc2a1fe-1f86-45a6-bb1b-89dcc2f68cc9_1000.jpg.296x216.jpg" alt="深圳龙岗区坂田">
                    </a>
                    <div class="info clear">
                        <div class="title">
                            <a class="" href="https://sz.lianjia.com/ershoufang/105112990747.html" target="_blank" data-log_index="1" data-el="ershoufang" data-housecode="105112990747" data-is_focus="" data-sl="">佳兆业三期朝南三房 房子满五年 唯一 安静看花园 诚售</a>
                            <!-- 拆分标签 只留一个优先级最高的标签-->
                            <span class="goodhouse_tag tagBlock">必看好房</span>
                        </div>
                        <div class="flood">
                            <div class="positionInfo">
                                <span class="positionIcon"></span>
                                <a href="https://sz.lianjia.com/xiaoqu/2411062835809/" target="_blank" data-log_index="1" data-el="region">佳兆业中央广场三期 </a>
                                   -  
                                <a href="https://sz.lianjia.com/ershoufang/bantian/" target="_blank">坂田</a>
                            </div>
                        </div>
                        <div class="address">
                            <div class="houseInfo">
                                <span class="houseIcon"></span>
                                3室1厅 | 89.22平米 | 东南 南 | 精装 | 高楼层(共46层) | 2016年建 | 塔楼
                            </div>
                        </div>
                        <div class="followInfo">
                            <span class="starIcon"></span>
                            2人关注 / 7天以前发布
                        </div>
                        <div class="tag">
                            <span class="subway">近地铁</span>
                            <span class="vr">VR房源</span>
                            <span class="taxfree">房本满五年</span>
                            <span class="haskey">随时看房</span>
                        </div>
                        <div class="priceInfo">
                            <div class="totalPrice totalPrice2">
                                <i>参考价: </i>
                                <span class="">527</span>
                                <i>万</i>
                            </div>
                            <div class="unitPrice" data-hid="105112990747" data-rid="2411062835809" data-price="0">
                                <span>59,000元/平</span>
                            </div>
                        </div>
                    </div>
                    <div class="listButtonContainer">
                        <div class="btn-follow followBtn" data-hid="105112990747">
                            <span class="follow-text">关注</span>
                        </div>
                        <div class="compareBtn LOGCLICK" data-hid="105112990747" log-mod="105112990747" data-log_evtid="10230">加入对比</div>
                    </div>
                </li>"""

from lxml import etree
parse_html = etree.HTML(html)
#1、查找所有li
xpath_dbs = '//li//div[@class="title"]/a/text()'
name_list = parse_html.xpath(xpath_dbs)
print(name_list)
# 小区名
xpath_dbs = '//li//div[@class="positionInfo"]/a/text()'
name_list = parse_html.xpath(xpath_dbs)
print(name_list)
# 房屋信息
# houseInfo
xpath_dbs = '//li//div[@class="houseInfo"]/text()'
name_list = parse_html.xpath(xpath_dbs)
print(name_list)

#总价 priceInfo
xpath_dbs = '//li//div[@class="totalPrice totalPrice2"]/span/text()'
name_list = parse_html.xpath(xpath_dbs)
print(name_list)
# 单价
xpath_dbs = '//li//div[@class="unitPrice"]/span/text()'
name_list = parse_html.xpath(xpath_dbs)
print(name_list)