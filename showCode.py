from PIL import Image, ImageDraw, ImageFont
import string
import random

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
navyblue = (0, 0, 128)
goldenyellow = (255, 255, 29)

# 生成数字和字符 4位
# string 模块ascii_letters和digits方法

strings = string.digits + string.ascii_letters
code = random.choice(strings) + random.choice(strings) + random.choice(strings) + random.choice(strings)
print('生成的验证码：', code)

width, height = 400, 100
font_size = 98
image = Image.new('RGB', (width, height), color=white)
draw = ImageDraw.Draw(image)
font = ImageFont.truetype(font='Chalkduster.ttf', size=font_size)

for index, value in enumerate(code):
    color = random.choice([goldenyellow, blue, red])
    draw.text((index * font_size, 1), value, font=font, fill=color)
# 增加噪声

for i in range(100):
    fill = random.choice([cyan, black])
    xy = (random.randrange(0, width),random.randrange(0,height))
    draw.point((xy), fill=fill)
image.save('code.png')

