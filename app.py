from flask import Flask, render_template, request
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import os
import io
import base64

# HTML dosyası aynı klasörde olduğu için template_folder='.' olarak belirleniyor
app = Flask(__name__, template_folder='.')

def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)

def extract_colors(image_path, k=5):
    image = Image.open(image_path).convert("RGB")  # Her ihtimale karşı RGB'ye dönüştür
    image = image.resize((150, 150))
    pixels = np.array(image).reshape(-1, 3)

    kmeans = KMeans(n_clusters=k)
    kmeans.fit(pixels)

    colors = kmeans.cluster_centers_.astype(int)
    hex_colors = [rgb_to_hex(c) for c in colors]

    # Renk paletini matplotlib ile oluştur
    fig, ax = plt.subplots(1, k, figsize=(8, 2))
    for i in range(k):
        ax[i].imshow([[colors[i]]])
        ax[i].axis("off")

    # Şekli base64 olarak kaydet
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    return hex_colors, img_base64

@app.route('/', methods=['GET', 'POST'])
def index():
    hex_colors = []
    img_base64 = None

    if request.method == 'POST':
        file = request.files.get('image')
        if file and file.filename:
            upload_folder = "uploads"
            if not os.path.exists(upload_folder):
                os.mkdir(upload_folder)
            filepath = os.path.join(upload_folder, file.filename)
            file.save(filepath)

            hex_colors, img_base64 = extract_colors(filepath)
            os.remove(filepath)  # İşlem tamamlandıktan sonra dosya silinir

    return render_template('index.html', hex_colors=hex_colors, image_data=img_base64)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
