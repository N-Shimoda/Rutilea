from PIL import Image, ImageDraw
import numpy as np

def generate_gradient_image(color1, color2, color3, width, height):
    # 画像を生成し、描画オブジェクトを作成
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)

    # 各色をRGBタプルに変換
    color1 = tuple(int(color1[i:i+2], 16) for i in (0, 2, 4))
    color2 = tuple(int(color2[i:i+2], 16) for i in (0, 2, 4))
    color3 = tuple(int(color3[i:i+2], 16) for i in (0, 2, 4))

    # グラデーションを描画
    for x in range(width):
        r = int(np.interp(x, [0, width - 1], [color1[0], color2[0]]))
        g = int(np.interp(x, [0, width - 1], [color1[1], color2[1]]))
        b = int(np.interp(x, [0, width - 1], [color1[2], color2[2]]))
        
        for y in range(height):
            r = int(np.interp(y, [0, height - 1], [r, color3[0]]))
            g = int(np.interp(y, [0, height - 1], [g, color3[1]]))
            b = int(np.interp(y, [0, height - 1], [b, color3[2]]))
            
            draw.point((x, y), fill=(r, g, b))

    return image

def remove_hashtag(color_code):
    # 文字列の先頭が「#」である場合、それを取り除く
    if color_code.startswith("#"):
        color_code = color_code[1:]
    return color_code

if __name__ == '__main__':

    color1 = input("1番目の色コードを入力してください（例: #FF0000）: ")
    color2 = input("2番目の色コードを入力してください（例: #00FF00）: ")
    color3 = input("3番目の色コードを入力してください（例: #0000FF）: ")

    color1 = remove_hashtag(color1)
    color2 = remove_hashtag(color2)
    color3 = remove_hashtag(color3)

    width = int(input("画像の幅を入力してください: "))
    height = int(input("画像の高さを入力してください: "))

    image = generate_gradient_image(color1, color2, color3, width, height)
    image.save("gradient_image.png")
    print("グラデーションの画像を保存しました: gradient_image.png")

