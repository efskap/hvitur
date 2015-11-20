from StringIO import StringIO
import io
import urllib
from PIL import Image
from flask import Flask, redirect, request, url_for, render_template, send_file
app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/do', methods=[ 'POST'])
def upload_file():
    if request.method == 'POST':
        photo = request.files['file']
        if photo and allowed_file(photo.filename):
            in_memory_file = io.BytesIO()
            photo.save(in_memory_file)
            img =Image.open(StringIO(in_memory_file.getvalue())).convert('RGBA')

            pixdata= img.load()
            for y in xrange(img.size[1]):
                for x in xrange(img.size[0]):
                    pixdata[x, y] = pixdata[x,y][:3] + \
                                    (255-((pixdata[x, y][0] + pixdata[x, y][1] + pixdata[x, y][2])/3),)
            outbuf = io.BytesIO()
            img.save(outbuf, format='PNG')
            b64 = outbuf.getvalue().encode('base64')
            return 'data:image/png;base64,{}'.format(urllib.quote(b64.rstrip('\n')))


@app.route('/')
def mainpage():
    return render_template('main.html')

if __name__ == '__main__':
    app.run()
