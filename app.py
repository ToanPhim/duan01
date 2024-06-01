
from flask import Flask, render_template, request, send_file,  redirect, url_for, render_template_string
from PIL import Image, ImageDraw, ImageFont
import cv2
import requests

app = Flask(__name__)

global img_out_path
img_out_path = 'static/output_image.png'

def DoiKichThuocAnh(img_path, img_out):
    new_width = 640
    new_height = 950
    img = cv2.imread(img_path)
    img_resized = cv2.resize(src=img, dsize=(new_width, new_height))
    cv2.imwrite(img_out, img_resized)
    return img_resized

def VeChu(img_out_path, text):
    font = ImageFont.truetype("./iCiel-Brush-Up.otf", 47)
    textColor = 'white'
    shadowColor = 'black'
    outlineAmount = 4
    img = Image.open(img_out_path)
    draw = ImageDraw.Draw(img)
    imgWidth, imgHeight = img.size
    txtWidth = draw.textlength(text, font=font) 
    txtHeight,_ = draw.textlength(text), font.getmetrics()[0]
    x = (imgWidth - txtWidth) / 2
    y = (imgHeight - txtHeight) / 4

    for adj in range(outlineAmount):
        

        draw.text((x - adj, y), text, font=font, fill=shadowColor)
        draw.text((x + adj, y), text, font=font, fill=shadowColor)
        draw.text((x, y + adj), text, font=font, fill=shadowColor)
        draw.text((x, y - adj), text, font=font, fill=shadowColor)
        draw.text((x - adj, y + adj), text, font=font, fill=shadowColor)
        draw.text((x + adj, y + adj), text, font=font, fill=shadowColor)
        draw.text((x - adj, y - adj), text, font=font, fill=shadowColor)
        draw.text((x + adj, y - adj), text, font=font, fill=shadowColor)

    draw.text((x, y), text, font=font, fill=textColor)
    img.save(img_out_path)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        text = request.form.get('text', 'Thuyết Minh Tại bit.ly/tvphim')
        imgFile = request.files['image']
        img_url = request.form.get('img_url')

        if imgFile:
            img_path = 'downloads/temp_image.jpg'
            imgFile.save(img_path)
        elif img_url:
            response = requests.get(img_url)
            img_path = 'downloads/temp_image.jpg'
            with open(img_path, 'wb') as f:
                f.write(response.content)
        else:
            return "Link rỗng rồi"
        img_resized = DoiKichThuocAnh(img_path, img_out_path)
        VeChu(img_out_path, text)
        return redirect(url_for('downloadfinal', img_out_path=img_out_path))

    return render_template('index.html')

@app.route('/<img_path>')
def download(img_path):
    return send_file(img_path, as_attachment=True)

@app.route('/changelink')
def changelink():
    return render_template('changeLink.html')

@app.route('/downloadfinal')
def downloadfinal():
    return render_template('downloadfinal.html', img_path=img_out_path)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
