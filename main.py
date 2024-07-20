# import pandas as pd 
# import numpy as np
# from scipy import misc
# from PIL import Image
# from matplotlib import pyplot as plt
# from numpy.random import random

# grey_vals = np.array([0.2126, 0.7152, 0.0722])
# file_name="yummy_macarons.jpg"
# my_img=Image.open(file_name)
# # sRGB_array=my_img/225
# my_img_gray = my_img @ grey_vals
# plt.imshow(np.flip(my_img_gray), cmap='gray')
# # plt.imshow(np.rot90(my_img_gray))
# plt.show()

# app.py
import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import cv2
import numpy as np
from sklearn.cluster import KMeans

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

def extract_colors(image_path, num_colors=10):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.reshape((image.shape[0] * image.shape[1], 3))

    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(image)

    colors = kmeans.cluster_centers_
    return colors.astype(int)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            colors = extract_colors(file_path)
            hex_colors = ['#%02x%02x%02x' % tuple(color) for color in colors]
            return render_template('result.html', colors=hex_colors)

    return render_template('upload.html')

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
