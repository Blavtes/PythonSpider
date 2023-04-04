from lxml import etree

html = """
        <ul class="Carlist">
            <li class="bjd" id="cat_001" href="http://www.bjd.com/">
                <p class="name">布加迪</p>
                <p class="model">bjd</p>
                <p class="price">2500w</p>
            </li>
            <li class="byd" id="cat_002" href="http://www.byd.com/">
                <p class="name">BYD</p>
                <p class="model">秦</p>
                <p class="price">15w</p>
            </li>
        </ul>
        """
parse_html = etree.HTML(html)
xpath_dbs = '//li'
r_list = parse_html.xpath(xpath_dbs)
print(r_list)
for r in r_list: # ./p[@class]/text()'
    name = r.xpath('./p[@class="price"]/text()')
    print(name)

#取汽车的name
xpath_dbs='//li/p[@class="name"]/text()'
r_list = parse_html.xpath(xpath_dbs)
print(r_list)

#取比亚迪的型号
xpath_dbs = '//ul/li[2]/p[@class="model"]/text()'
r_list = parse_html.xpath(xpath_dbs)
print(r_list)

#取链接
xpath_dbs = '//li/@href'
r_list = parse_html.xpath(xpath_dbs)
print(r_list)