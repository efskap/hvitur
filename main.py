from StringIO import StringIO
import io
import urllib
from threading import Thread
from PIL import Image
from flask import Flask, request, render_template

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
CUTOFF = 2 ** 20

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def process_data_sequential(pixdata, xmin, xmax, ymin, ymax, threshold):
    for x_pos in xrange(xmin, xmax):
        for y_pos in xrange(ymin, ymax):
            alpha = 255 - sum(pixdata[x_pos, y_pos][:3])/3
            alpha = alpha if alpha > threshold else 0
            pixdata[x_pos, y_pos] = tuple(pixdata[x_pos, y_pos][:3]) + (alpha,)

def process_data(pixdata, xmin, xmax, ymin, ymax, threshold):
    xsize = xmax-xmin
    ysize = ymax-ymin

    if xsize*ysize < CUTOFF:
        process_data_sequential(pixdata, xmin, xmax, ymin, ymax, threshold)
        return

    if xsize > ysize:
        processing_thread = Thread(target=process_data,
                                   args=(pixdata,
                                        0, xmax//2,
                                        ymin, ymax,
                                        threshold))
        processing_thread.start()
        process_data(pixdata, xmax//2, xmax, ymin, ymax, threshold)
        processing_thread.join()

    else:
        processing_thread = Thread(target=process_data,
                                            args=(pixdata,
                                                  xmin, xmax,
                                                  0, ymax//2,
                                                  threshold))
        processing_thread.start()
        process_data(pixdata, xmin, xmax, ymax//2, ymax, threshold)
        processing_thread.join()

@app.route('/do', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        photo = request.files['file']
        if photo and allowed_file(photo.filename):
            in_memory_file = io.BytesIO()
            photo.save(in_memory_file)
            img = Image.open(StringIO(in_memory_file.getvalue())).convert('RGBA')

            pixdata = img.load()
            xsize, ysize = img.size

            process_data(pixdata, 0, xsize, 0, ysize, 0)

            outbuf = io.BytesIO()
            img.save(outbuf, format='PNG')
            b64 = outbuf.getvalue().encode('base64')
            return 'data:image/png;base64,{}'.format(urllib.quote(b64.rstrip('\n')))


@app.route('/')
def mainpage():
    return render_template('main.html')

if __name__ == '__main__':
    app.run()
