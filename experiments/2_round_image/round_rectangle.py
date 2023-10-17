from PIL import Image
from PIL import ImageDraw

# 角丸四角を描画する
img1 = Image.new("RGB", (100,100), "#ffffff")
draw = ImageDraw.Draw(img1)
rx = 10
ry = 10
fillcolor = "#bbddff"
draw.rectangle((0,ry)+(img1.size[0]-1,img1.size[1]-1-ry), fill=fillcolor)
draw.rectangle((rx,0)+(img1.size[0]-1-rx,img1.size[1]-1), fill=fillcolor)
draw.pieslice((0,0)+(rx*2,ry*2), 180, 270, fill=fillcolor)
draw.pieslice((0,img1.size[1]-1-ry*2)+(rx*2,img1.size[1]-1), 90, 180, fill=fillcolor)
draw.pieslice((img1.size[0]-1-rx*2,img1.size[1]-1-ry*2)+
(img1.size[0]-1,img1.size[1]-1), 0, 180, fill=fillcolor)
draw.pieslice((img1.size[0]-1-rx*2,0)+
(img1.size[0]-1,ry*2), 270, 360, fill=fillcolor)
del draw

img1.save("img/roundrectangle.png")