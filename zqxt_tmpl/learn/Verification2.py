from PIL import Image,ImageDraw,ImageFilter,ImageFont
import random
import math,string
from django import template


save_path = '/home/CORPUSERS/xp023799/PycharmProjects/zqxt_tmpl/learn/static/Verfily-code'
font_path = '/usr/share/fonts/truetype/somc/SST-Heavy.otf'

number      = 4
size        = (100,30)
bgcolor     = (0,0,0)
draw_line   = True
line_number = (1,5)


def gen_text():
    source = list(string.ascii_letters)
    for index in range(0,10):
        source.append(str(index))
    return ''.join(random.sample(source,number))
# create the random math
def randomcolor():
    return (random.randint(64,255),random.randint(64,255),random.randint(64,255))
def gene_line(draw,width,height):
    begin = (random.randint(0,width),random.randint(0,height))
    end   = (random.randint(0,width),random.randint(0,height))
    draw.line([begin,end],fill = randomcolor())


def gene_code(save_path):
    width,height = size
    image        = Image.new('RGBA',(width,height),bgcolor)
    font         = ImageFont.truetype(font_path,25)
    draw         = ImageDraw.Draw(image)
    text         = gen_text()
    print(text)
    font_width, font_height = font.getsize(text)
    draw.text(((width - font_width) / number, (height - font_height) / number), text,font= font,fill=randomcolor())
    if draw_line:
        gene_line(draw, width, height)
        gene_line(draw, width, height)
        gene_line(draw, width, height)
        gene_line(draw, width, height)
    image = image.transform((width + 20, height + 10), Image.AFFINE, (1, -0.3, 0, -0.1, 1, 0), Image.BILINEAR)
    #翻转图片
    image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    #滤镜
    image.save('%s/%s.png' % (save_path, text))
    print("savepath:", save_path)
    return text

gene_code(save_path)