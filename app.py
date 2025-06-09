from flask import Flask, render_template, request
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import os
import io
import base64

app = Flask(__name__)

def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)

def extract_colors(image_path, k=5):
    image = Image.open(image_path)
    image = image.resize((150, 150))
    pixels = np.array(image).reshape(-1, 3)

    kmeans = KMeans(n_clusters=k)
    kmeans.fit(pixels)

    colors = kmeans.cluster_centers_.astype(int)
    hex_colors = [rgb_to_hex(c) for c in colors]

    fig, ax = plt.subplots(1, k, figsize=(8, 2))
    for i in range(k):
        ax[i].imshow([[colors[i]]])
        ax[i].axis("off")

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    return hex_colors, img_base64

@app.route('/', methods=['GET', 'POST'])
def index():
    hex_colors = []
    img_base64 = None

    if request.method == 'POST':
        file = request.files['image']
        if file:
            filepath = os.path.join("uploads", file.filename)
            file.save(filepath)
            hex_colors, img_base64 = extract_colors(filepath)
            os.remove(filepath)

    return render_template('index.html', hex_colors=hex_colors, image_data=img_base64)

if __name__ == '__main__':
    if not os.path.exists("uploads"):
        os.mkdir("uploads")
    app.run(host='0.0.0.0', port=10000)
