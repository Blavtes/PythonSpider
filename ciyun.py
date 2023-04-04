import jieba, wordcloud, imageio

with open('kkx.txt', encoding='utf-8') as f:
    kkx = f.read()
    kkx = jieba.cut(kkx)
    kkx = ' '.join(kkx)

im = imageio.imread('kk.jpg')

# 图形生成器
image_color = wordcloud.ImageColorGenerator(im)

wc = wordcloud.WordCloud(
    width = 600,
    height = 800,
    background_color = 'white',
    font_path = 'OPPOSans H.ttf',
    mask = im,
    contour_width=1,
    contour_color = 'black'
)
wc.generate(kkx)
rwc = wc.recolor(color_func=image_color)
rwc.to_file('qmm.png')
